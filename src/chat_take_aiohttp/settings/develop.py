from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

REDIS = 'redis', 6379

DATABASE = {
    'database': 'chat_take_aiohttp',
    'password': '123',
    'user': 'chat_user',
    'host': 'postgres',
    'port': 5432
}
