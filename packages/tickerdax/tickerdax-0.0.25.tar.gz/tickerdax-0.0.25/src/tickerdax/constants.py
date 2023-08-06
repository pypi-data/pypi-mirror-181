
NAME = 'tickerdax'


class KeyTypes:
    REST = 'REST'
    WEBSOCKET = 'WEBSOCKET'


class Envs:
    DEV = f'{NAME.upper()}_DEV'
    OFFICIAL_DOCKER_IMAGE = f'{NAME.upper()}_OFFICIAL_DOCKER_IMAGE'
    EMAIL = f'{NAME.upper()}_EMAIL'
    REST_API_KEY = f'{NAME.upper()}_REST_API_KEY'
    WEBSOCKET_API_KEY = f'{NAME.upper()}_WEBSOCKET_API_KEY'
    CACHE_ROOT = f'{NAME.upper()}_CACHE_ROOT'
    CONFIG = f'{NAME.upper()}_CONFIG'
    REDIS_SERVER_ADDRESS = f'{NAME.upper()}_REDIS_SERVER_ADDRESS'
    REDIS_SERVER_PORT = f'{NAME.upper()}_REDIS_SERVER_PORT'
