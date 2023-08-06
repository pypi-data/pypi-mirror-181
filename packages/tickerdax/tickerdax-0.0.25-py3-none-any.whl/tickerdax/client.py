import os
import json
import subprocess
import sys
import asyncio
import time

import requests
import tempfile
import logging
import redis
import docker
import socket
import websockets
from websockets.exceptions import InvalidStatusCode, ConnectionClosed, ConnectionClosedOK
from tickerdax.constants import Envs, KeyTypes, NAME
from docker.errors import DockerException
from datetime import datetime, timedelta, timezone
from tickerdax import formatting
from pprint import pformat, pprint


class TickerDax:
    def __init__(
            self,
            email=None,
            rest_api_key=None,
            websocket_api_key=None,
            fast_start=True,
            connect=True,
            log_connection=True,
            force=False
    ):
        websocket_api_prefix = 'ws'
        rest_api_prefix = 'api'
        if os.environ.get(Envs.DEV):
            rest_api_prefix = 'dev-api'
            websocket_api_prefix = 'dev-ws'

        # general configuration
        self.supported_timeframes = ['1h']
        self.rest_values = []
        self.cached_values = []
        self.missing_values = []
        self._batch_size = 500
        self._fast_start = fast_start
        self._log_connection = log_connection
        self._force = force

        # rest api configuration
        self._rest_api_host = f'https://{rest_api_prefix}.{NAME}.com'
        self._rest_api_version = 'v1'
        self._rest_api_key = os.environ.get(Envs.REST_API_KEY, rest_api_key)

        # websocket api configuration
        self._host = f'wss://{websocket_api_prefix}.{NAME}.com'
        self._email = os.environ.get(Envs.EMAIL, email)
        self._websocket_api_key = os.environ.get(Envs.WEBSOCKET_API_KEY, websocket_api_key)

        # redis configuration
        self._image_name = f'{NAME}:latest'
        self._container_name = NAME
        self._redis_server_address = os.environ.get(Envs.REDIS_SERVER_ADDRESS, '127.0.0.1')
        self._redis_container_port = os.environ.get(Envs.REDIS_SERVER_PORT, 6379)
        self._redis_host_port = os.environ.get(Envs.REDIS_SERVER_PORT, 6379)

        # clients
        self._docker_client = None
        self.redis_client = None

        self._cache_folder = os.environ.get(Envs.CACHE_ROOT, os.path.join(tempfile.gettempdir(), f'{NAME}_cache'))
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(level=logging.DEBUG)

        if connect:
            self._start_redis_server()

    @staticmethod
    def _get_cache_keys(route, symbols, timestamps):
        """
        Get all the cache keys.

        :param str route: The data route.
        :param list[str] symbols: A list of symbols.
        :param list[float] timestamps: The timestamps to get.
        :returns: A complete list of all the cache keys.
        :rtype list
        """
        keys = []
        for symbol in symbols:
            keys.extend([f'{NAME}/{route}/{symbol}/{timestamp}' for timestamp in timestamps])
        return keys

    @staticmethod
    def _format_route(route):
        """
        Normalizes the route format.

        :param str route: The data route.
        :returns: A normalizedd the route.
        :rtype str
        """
        return route.strip('/').strip('\\').replace('\\', '/')

    def _get_unused_port_number(self, default_port) -> int:
        """
        Gets an unused port number from the OS.

        :returns: A port number.
        :rtype: int
        """
        if not self._is_port_in_use(default_port):
            return default_port
        else:
            sock = socket.socket()
            sock.bind(('', 0))
            return sock.getsockname()[1]

    def _get_from_cache(self, keys):
        """
        Get the data from the cache that already exists, and which REST requests still need to be made.

        :param list[str] keys: A complete list of all the cache keys.
        :returns: Which REST requests still need to be made.
        :rtype dict
        """
        cache_values = self.redis_client.mget(keys)

        rest_requests = {}
        for key, cache_value in zip(keys, cache_values):
            items = key.split('/')
            symbol = items[-2]
            timestamp = float(items[-1])

            if not cache_value:
                if not rest_requests.get(symbol):
                    rest_requests[symbol] = []
                rest_requests[symbol].append(timestamp)

            # if the data is nothing more than the symbol and id, then this should be
            # marked as missing data.
            elif json.loads(cache_value) == {'id': timestamp, 'symbol': symbol}:
                # if force is true then request the already reported missing values
                if self._force:
                    if not rest_requests.get(symbol):
                        rest_requests[symbol] = []
                    rest_requests[symbol].append(timestamp)
                else:
                    self.missing_values.append(json.loads(cache_value))

            # otherwise, the data is already cached
            else:
                self.cached_values.append(json.loads(cache_value))

        # return the needed rest requests
        return rest_requests

    def _set_redis_client(self):
        """
        Sets the redis client.
        """
        # verify the connection with the redis server
        try:
            self.redis_client = redis.Redis(
                host=self._redis_server_address,
                port=self._redis_host_port,
                db=0
            )
            self.redis_client.ping()
            if self._log_connection:
                self._logger.info(f'Redis server is connected!')
            return True
        except redis.exceptions.ConnectionError:
            return False

    def _is_port_in_use(self, port: int) -> bool:
        """
        Checks if port number is in use.

        :param int port: A port number.
        :returns: Whether the port is in use.
        :rtype: bool
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
            return stream.connect_ex((self._redis_server_address, port)) == 0

    def _start_redis_server(self, attempts=0) -> None:
        """
        Starts the redis docker container.
        """
        # quickly try to connect to the running redis server
        if self._fast_start:
            if self._set_redis_client():
                return
            else:
                self._logger.warning(f'Failed to connect with fast start. Starting full reboot...')

        # if in the official docker image, try starting redis manually and
        if os.environ.get(Envs.OFFICIAL_DOCKER_IMAGE) and attempts < 1:
            try:
                subprocess.Popen(
                    f'redis-server /home/redis.conf --port {self._redis_host_port}',
                    shell=True
                )
                self._logger.info('Attempting to start redis server on local system...')
                time.sleep(5)
                if self._set_redis_client():
                    return
            except Exception as error:
                self._logger.debug(error)
                self.report_error(f'Failed to start redis server in {NAME} container')

        # get a unused host port
        self._redis_host_port = self._get_unused_port_number(6379)

        # initialize the docker client
        try:
            self._docker_client = docker.from_env()
        except DockerException:
            self.report_error('Failed to connect to docker. Make sure docker is installed and currently running.')

        # stop any running redis docker containers first
        for container in self._docker_client.containers.list(all=True):
            if self._container_name == container.name:
                if container.status == 'running':
                    self._logger.info(f'Stopping docker container "{self._container_name}"')
                    container.stop()
                    container.wait()
                self._logger.info(f'Removing docker container "{self._container_name}"')
                container.remove()

        # start the redis docker container
        self._logger.info(f'Starting docker container "{self._container_name}"')
        self._docker_client.containers.run(
            name=self._container_name,
            image=self._image_name,
            ports={
                f'{self._redis_container_port}/tcp': (self._redis_server_address, self._redis_host_port)
            },
            volumes=[f'{self._cache_folder}:/data'],
            detach=True
        )

        # connect the redis client
        if not self._set_redis_client():
            raise ConnectionError('TickerDax failed to connect to the redis server')

    def _batch_request(self, route, symbol, timestamps):
        """
        Batches requests until all timestamps are retrieved.

        :param str route: The data route.
        :param str symbol: The symbol to get.
        :param list[float] timestamps: The timestamps to get.
        :returns A list of all the responses to the request.
        :rtype list[dict]
        """
        result = []
        batch = []
        number_of_timestamp = len(timestamps)
        for index, key in enumerate(timestamps, 1):
            batch.append(key)

            if index % self._batch_size == 0:
                self._logger.info(f'batch requesting {index}/{number_of_timestamp} "{route}/{symbol}" timestamps...')
                result.extend(self._rest_request(route, symbol, batch))

                # clear the batch
                batch.clear()

        # get any remaining items in the last batch
        if batch:
            self._logger.info(
                f'batch requesting {number_of_timestamp}/{number_of_timestamp} "{route}/{symbol}" timestamps...'
            )
            result.extend(self._rest_request(route, symbol, batch))

        self._logger.debug(f'batch "{route}/{symbol}" requests complete!')
        return result

    async def _async_batch_request(self, route, symbol, timestamps):
        """
        Batches requests until all timestamps are retrieved.

        :param str route: The data route.
        :param str symbol: The symbol to get.
        :param list[float] timestamps: The timestamps to get.
        :returns A list of all the responses to the request.
        :rtype list[dict]
        """
        result = []
        batch = []
        number_of_timestamp = len(timestamps)
        for index, key in enumerate(timestamps, 1):
            batch.append(key)

            if index % self._batch_size == 0:
                self._logger.info(f'batch requesting {index}/{number_of_timestamp} "{route}/{symbol}" timestamps...')
                result.extend(self._rest_request(route, symbol, batch))

                # clear the batch
                batch.clear()

        # get any remaining items in the last batch
        if batch:
            self._logger.info(
                f'batch requesting {number_of_timestamp}/{number_of_timestamp} "{route}/{symbol}" timestamps...'
            )
            result.extend(self._rest_request(route, symbol, batch))

        self._logger.debug(f'batch "{route}/{symbol}" requests complete!')
        return result

    async def _stream_to_cache(self, route, symbols):
        """
        Connects to the given route and its symbols and updates the
        cache as it receives new data.

        :param str route: The data route.
        :param list[str] symbols: A list of symbols.
        """
        uri = f'{self._host}?route={route}&symbols={symbols}'
        try:
            async with websockets.connect(
                    uri,
                    extra_headers={'email': self._email, 'token': self._websocket_api_key}
            ) as connected_socket:
                self._logger.info(f'> Connected to {uri}')
                while True:
                    data = json.loads(await connected_socket.recv())
                    symbol = data.get('symbol')
                    timestamp = data.get('id')
                    if symbol and timestamp:
                        for key in self._get_cache_keys(self._format_route(route), [symbol], [timestamp]):
                            self.redis_client.set(key, json.dumps(data))
                            self._logger.info(f'Cached: {pformat(data)}')

        except (ConnectionClosed, ConnectionClosedOK) as error:
            if getattr(error, 'status_code', None) == 1001:
                self._logger.info('refreshing connection...')
                # re-connect if the connection was closed
                await self._stream_to_cache(route, symbols)

        except InvalidStatusCode as error:
            if error.status_code == 401:
                self.report_error(
                    'This email and API key combination are not authorized to connect to '
                    f'the {self._host} websocket API. Please check your credentials.'
                )

    # async def _rest_request(self, route, symbol, timestamps):
    def _rest_request(self, route, symbol, timestamps):
        """
        Preforms a single REST request.

        :param str route: The data route.
        :param str symbol: The symbol to get.
        :param list[float] timestamps: The timestamps to get.
        :return list[dict]: A list of dictionaries as the response to the request.
        """
        try:
            response = requests.get(
                f'{self._rest_api_host}/{self._rest_api_version}/{route}',
                headers={"x-api-key": self._rest_api_key},
                data=json.dumps({
                    'symbol': symbol,
                    'timestamps': timestamps
                })
            )
            if response.ok:
                return response.json()
            else:
                if response.json().get('message') == 'Forbidden':
                    self.report_error(
                        'This API key is not authorized to connect to the https://api.tickerdax.com REST API. '
                        'Please check your credentials.'
                    )
                elif response.json().get('message') == 'Limit Exceeded':
                    self.report_error(
                        'This API key has exceeded its usage limit. Go to https://tickerdax.com to upgrade your plan.'
                    )
                else:
                    self.report_error(response.json())
        except Exception as error:
            self.report_error(str(error))

    def _request(self, route, rest_requests):
        """
        A request to first the local cache, then to the REST API if data is missing in the
        cache.

        :param str route: The data route.
        :param dict rest_requests: A dictionary of symbols and timestamps.
        :return list[dict]: A list of dictionaries as the response to the request.
        """
        rest_values = []
        if rest_requests:
            self._logger.info(f'Requesting {route} data from REST API...')
            # gather the symbols concurrently
            for symbol, timestamps in rest_requests.items():
                rest_values.extend(self._batch_request(route, symbol, timestamps))
        return rest_values

    async def _async_request(self, route, rest_requests):
        """
        A request to first the local cache, then to the REST API if data is missing in the
        cache.

        :param str route: The data route.
        :param dict rest_requests: A dictionary of symbols and timestamps.
        :return list[dict]: A list of dictionaries as the response to the request.
        """
        rest_values = []
        if rest_requests:
            self._logger.info(f'Requesting {route} data from REST API...')
            # gather the symbols concurrently
            for result in await asyncio.gather(*[
                self._batch_request(route, symbol, timestamps) for symbol, timestamps in rest_requests.items()
            ]):
                rest_values.extend(result)
        return rest_values

    async def _stream(self, routes):
        """
        Streams all given routes and their symbols concurrently.

        :param dict routes: A dictionary of route names and their symbols.
        """
        await asyncio.gather(*[self._stream_to_cache(
                f'/{self._format_route(route)}', ','.join(symbols)) for route, symbols in routes.items()
        ])

    def _update_cache(self, route, keys, timeframe):
        """
        Saves any new data from the response to the cache.

        :param str route: The data route.
        :param list[str] keys: A complete list of all the cache keys.
        :param str timeframe: The time interval.
        :returns: The combined result of cache values, rest values, and blank values.
        :rtype list
        """
        result = []
        # remove all the cache keys that already had a cached value
        for cached_value in self.cached_values:
            symbol = cached_value.get('symbol')
            timestamp = cached_value.get('id')
            key = f'{NAME}/{route}/{symbol}/{timestamp}'
            if key in keys:
                keys.remove(key)

        result.extend(self.cached_values)

        # cache the rest values
        for rest_value in self.rest_values:
            symbol = rest_value.get('symbol')
            timestamp = rest_value.get('id')
            key = f'{NAME}/{route}/{symbol}/{timestamp}'

            self.redis_client.set(key, json.dumps(rest_value))
            # remove the key now that it is cached
            if key in keys:
                keys.remove(key)
        result.extend(self.rest_values)

        # if there are any remaining keys, then that means they were missing from the rest api
        for key in keys:
            items = key.split('/')
            symbol = items[-2]
            timestamp = float(items[-1])

            missing_value = {'id': timestamp, 'symbol': symbol}
            result.append(missing_value)

            # this will set the missing value in the cache with an expiration time that matches the given timeframe
            self.missing_values.append(missing_value)
            self.redis_client.set(
                key,
                json.dumps(missing_value),
                ex=formatting.convert_timeframe_to_seconds(timeframe)
            )
        return result

    def validate_api_key(self,  key_type):
        """
        Validate whether the key of the given type exists and show and error message.

        :param str key_type: The type of key i.e. REST or WEBSOCKET.
        """
        env_key_name = None
        if key_type == KeyTypes.REST and not self._rest_api_key:
            env_key_name = Envs.REST_API_KEY

        elif key_type == KeyTypes.WEBSOCKET and not self._websocket_api_key:
            env_key_name = Envs.WEBSOCKET_API_KEY

        if env_key_name:
            self.report_error(
                f'The environment variable "{env_key_name}" must set to your API key from https://tickerdax.com'
            )

    def get_available_routes(self):
        """
        Gets all available routes from the REST api.

        :returns: A list of all available routes from the REST api.
        :rtype: list
        """
        ignored_routes = ['info/plans']
        routes = []
        for route in requests.get(f'{self._rest_api_host}/openapi.json').json().get('paths', {}).keys():
            route = route.replace(f'/{self._rest_api_version}/', '')
            if route not in ignored_routes:
                routes.append(route)
        return routes

    def get_route(self, route, symbols, start, end, timeframe='1h', asynchronous=False):
        """
        Get data for a route and it's symbols between the start and end times and at the timeframe interval.

        :param str route: The data route.
        :param list[str] symbols: A list of symbols.
        :param datetime start: The UTC start time.
        :param datetime end: The UTC end time.
        :param str timeframe: The time interval.
        :param bool asynchronous: Whether the request is asynchronous.
        :returns: The sorted result.
        :rtype list
        """
        self.cached_values.clear()
        self.rest_values.clear()
        self.missing_values.clear()

        route = self._format_route(route)
        timestamps = formatting.get_timestamp_range(start, end, timeframe)
        keys = self._get_cache_keys(route, symbols, timestamps)

        # get the cached values and determine which rest requests are outstanding
        self._logger.debug(f'Checking "{route}" cache for {symbols}...')
        outstanding_rest_requests = self._get_from_cache(keys)

        # make the request asynchronously or synchronously
        if asynchronous:
            self.rest_values = asyncio.run(self._async_request(route, outstanding_rest_requests))
        else:
            self.rest_values = self._request(route, outstanding_rest_requests)

        result = self._update_cache(route, keys, timeframe)
        return sorted(result, key=lambda i: i['id'])

    def report_error(self, message):
        """
        Reports an error message to the user.

        :param str message: A error message.
        """
        self._logger.error(message)
        sys.exit(1)

    def stream(self, routes):
        """
        Streams all given routes and their symbols to the cache in real-time.

        :param dict routes: A dictionary of route names and their symbols.
        """
        try:
            asyncio.run(self._stream(routes))
        except Exception as error:
            self._logger.error(error)
            self._logger.info('Trying to reconnect...')
            self.stream(routes)


if __name__ == '__main__':
    client = TickerDax(force=True)

    pprint(client.get_route(
        route='predictions/ml-order-book-model-1',
        symbols=['BTC'],
        start=datetime.now(tz=timezone.utc) - timedelta(hours=6),
        end=datetime.now(tz=timezone.utc)
    ))

    # client.stream(
    #     routes={
    #         'predictions/ml-order-book-model-1': ['BTC', 'LTC'],
    #     },
    # )
