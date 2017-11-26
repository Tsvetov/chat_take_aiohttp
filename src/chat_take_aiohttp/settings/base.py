import logging
import os
from typing import List


APPLICATION_NAME = 'chat_take_aiohttp'
APPLICATION_DESCRIPTION = 'чат на aiohttp'
APPLICATION_PACKAGE_NAME = 'chat_take_aiohttp'

CHECK_SERVICES: List[str] = []

REDIS = '', ''

DATABASE = {
    'database': '',
    'password': '',
    'user': '',
    'host': '',
}

BASE_DIR = os.path.dirname(__file__)

TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'templates')

STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), 'static')

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger.addHandler(console)