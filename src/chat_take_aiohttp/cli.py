import click
import asyncio
import aioredis
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from simple_settings import settings
import peewee_async
import aiohttp_jinja2
import jinja2

from chat_take_aiohttp.web.urls import routes
from chat_take_aiohttp.middleware.middleware_user import request_user_middleware
from chat_take_aiohttp.models.base_model import database
from chat_take_aiohttp.helpers.template_tags import tags
from chat_take_aiohttp.settings.base import logger


@click.group()
def cli() -> None:
    pass


async def create_pool_redis(loop):
    """Поднимаем коннект к редису"""
    return await aioredis.create_pool(settings.REDIS, loop=loop)


def make_routes(app: web.Application) -> None:
    """Сетим урлы в приложение"""
    app.router.add_static('/static', settings.STATIC_DIR, name='static')
    for route in routes:
        app.router.add_route(**route)


def database_connection(app):
    """Поднимаем коннект к базе"""
    database.init(**settings.DATABASE)
    app.database = database
    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database)


def jinja_env_setup(app):
    """Настройки шаблонизатора"""
    jinja_env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR),
        context_processors=[aiohttp_jinja2.request_processor],
    )
    jinja_env.globals.update(tags)


async def create_application(loop, host: str, port: int):
    redis_pool = await create_pool_redis(loop)
    middlewares = [
        session_middleware(RedisStorage(redis_pool)),
        request_user_middleware,
    ]
    app = web.Application(
        middlewares=middlewares,
    )
    app.wslist = {}
    jinja_env_setup(app)

    app.redis_pool = redis_pool

    database_connection(app)

    make_routes(app)
    app.logger = logger
    handler = app.make_handler(access_log=logger)
    serv_generator = loop.create_server(handler, host, port)
    return serv_generator, handler, app


async def shutdown(server, app: web.Application) -> None:
    for room in app.wslist.values():
        for peer in room.values():
            peer.send_json({'text': 'Server shutdown'})
    server.close()
    await server.wait_closed()
    app.redis_pool.close()
    await app.redis_pool.wait_closed()
    await app.objects.close()
    await app.shutdown()
    await app.cleanup()


@cli.command()
@click.option('--host', type=str, default='0.0.0.0')
@click.option('--port', type=int, default=8000)
def serve(host: str, port: int) -> None:
    """Запуск сервера"""
    loop = asyncio.get_event_loop()
    serv_generator, handler, app = loop.run_until_complete(
        create_application(loop, host, port)
    )
    server = loop.run_until_complete(serv_generator)
    logger.debug(
        f'Start server {server.sockets[0].getsockname()}'
    )
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug('Keyboard Interrupt ^C')
    finally:
        logger.debug('Stop server begin')
        loop.run_until_complete(shutdown(server, app))
        loop.close()