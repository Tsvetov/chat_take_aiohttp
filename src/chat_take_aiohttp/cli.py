import click
import asyncio
import aioredis
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from simple_settings import settings

from chat_take_aiohttp.web.urls import routes
from chat_take_aiohttp.middleware.middleware_user import request_user_middleware


@click.group()
def cli() -> None:
    pass


async def create_application(loop, host, port):
    redis_pool = await aioredis.create_pool(settings.REDIS, loop=loop)
    middlewares = [
        session_middleware(RedisStorage(redis_pool)),
        request_user_middleware,
    ]
    app = web.Application(
        middlewares=middlewares,
    )

    app.redis_pool = redis_pool

    for route in routes:
        app.router.add_route(**route)

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
