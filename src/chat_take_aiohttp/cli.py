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


@click.group()
def cli() -> None:
    pass


async def create_pool_redis(loop):
    return await aioredis.create_pool(settings.REDIS, loop=loop)


def make_routes(app):
    app.router.add_static('/static', settings.STATIC_DIR, name='static')
    for route in routes:
        app.router.add_route(**route)


def database_connection(app):
    database.init(**settings.DATABASE)
    app.database = database
    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database)


def jinja_env_setup(app):
    jinja_env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR),
        context_processors=[aiohttp_jinja2.request_processor],
    )
    jinja_env.globals.update(tags)


async def create_application(loop, host, port):
    redis_pool = await create_pool_redis(loop)
    middlewares = [
        session_middleware(RedisStorage(redis_pool)),
        request_user_middleware,
    ]
    app = web.Application(
        middlewares=middlewares,
    )

    jinja_env_setup(app)

    app.redis_pool = redis_pool

    database_connection(app)

    make_routes(app)

    handler = app.make_handler()
    serv_generator = loop.create_server(handler, host, port)
    return serv_generator, handler, app


@cli.command()
@click.option('--host', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=8000)
def serve(host: str, port: int) -> None:
    loop = asyncio.get_event_loop()
    serv_generator, handler, app = loop.run_until_complete(
        create_application(loop, host, port)
    )
    loop.run_until_complete(serv_generator)
    loop.run_forever()
