import os
import sys
import shutil
import click
import logging
import pkg_resources
import tickerdax
from logging.handlers import TimedRotatingFileHandler
from tickerdax.constants import Envs

try:
    VERSION = pkg_resources.get_distribution(tickerdax.__name__).version
except:
    VERSION = '0.0.1'

config = click.option(
    '--config',
    help='Path to config file.',
    required=not os.environ.get(Envs.CONFIG)
)

email = click.option(
    '--email',
    help='The email linked to you account at https://tickerdax.com',
    required=not os.environ.get(Envs.EMAIL)
)


rest_api_key = click.option(
    '--rest-api-key',
    help='Your api created on https://tickerdax.com',
    required=not os.environ.get(Envs.REST_API_KEY)
)

websocket_api_key = click.option(
    '--websocket-api-key',
    help='Your api created on https://tickerdax.com',
    required=not os.environ.get(Envs.WEBSOCKET_API_KEY)
)

force = click.option(
    '--force',
    is_flag=True,
    help='Forces new REST requests for all missing data, even if that data has already been marked as missing',
    required=False
)


@click.group(
    name='tickerdax',
    help=f'TickerDax version {VERSION}. A CLI tool that interfaces with the tickerdax.com REST and websockets API. It '
         f'handles common data operations like batch downloading, streaming, and caching data '
         f'locally to minimize network requests.'
)
def cli():
    pass


@click.command()
def create_config(**kwargs):
    file_formats = ['json', 'yaml']
    extension = click.prompt(
        'What file format do you want to use? (json or yaml)',
        default='yaml'
    )
    if extension not in file_formats:
        raise click.UsageError(f'Your choice {extension} is not one of the valid formats {file_formats}')

    # copy the example config to the current working directory
    shutil.copyfile(
        os.path.join(os.path.dirname(__file__), 'example_configs', f'config.{extension}'),
        os.path.join(os.getcwd(), f'config.{extension}')
    )


@click.command()
def list_routes(**kwargs):
    from tickerdax.client import TickerDax
    tickerdax_client = TickerDax(connect=False)
    output = 'All Routes:\n'
    for route in tickerdax_client.get_available_routes():
        output += f'\t- "{route}"'
    print(output)


@click.command()
@config
@force
@rest_api_key
def download(**kwargs):
    from tickerdax.downloader import Downloader
    config_name = kwargs.pop('config')
    Downloader(config=config_name, client_kwargs=kwargs)


@click.command()
@config
@force
@websocket_api_key
@email
def stream(**kwargs):
    from tickerdax.streamer import Streamer
    config_name = kwargs.pop('config')
    Streamer(config=config_name, client_kwargs=kwargs)


def main():
    formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

    # create log handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # create log handler for file output
    file_handler = TimedRotatingFileHandler('tickerdax.log', when='midnight')
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )
    cli.add_command(create_config)
    cli.add_command(list_routes)
    cli.add_command(download)
    cli.add_command(stream)
    cli()


if __name__ == '__main__':
    sys.exit(main())
