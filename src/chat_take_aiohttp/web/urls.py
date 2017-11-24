from chat_take_aiohttp.web.handlers import Ping, Register, Login, Logout


routes_base = [
    dict(method='GET', path='/ping', handler=Ping, name='index'),
]


routes_user = [
    dict(method='*', path='/register', handler=Register, name='register'),
    dict(method='*', path='/login', handler=Login, name='login'),
    dict(method='GET', path='/logout', handler=Logout, name='logout'),
]


routes = (
    * routes_base,
    * routes_user
)
