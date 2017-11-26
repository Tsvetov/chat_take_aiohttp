from chat_take_aiohttp.web.handlers import Ping, Register, Login, Logout, Index
from chat_take_aiohttp.web.chat_handlers import CreateRoom, ChatRoom, WebSocket


routes_base = [
    dict(method='GET', path='/', handler=Index, name='index'),
    dict(method='GET', path='/ping', handler=Ping, name='ping'),
]


routes_user = [
    dict(method='*', path='/register', handler=Register, name='register'),
    dict(method='*', path='/login', handler=Login, name='login'),
    dict(method='GET', path='/logout', handler=Logout, name='logout'),
]


routes_chat = (
    dict(method='*', path='/chat/rooms', handler=CreateRoom, name='create_room'),
    dict(method='GET', path='/chat/rooms/{slug}', handler=ChatRoom, name='room'),
    dict(method='GET', path='/ws/{slug}', handler=WebSocket, name='ws'),
)


routes = (
    * routes_base,
    * routes_user,
    * routes_chat,
)
