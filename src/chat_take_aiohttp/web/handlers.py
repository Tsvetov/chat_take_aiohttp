from aiohttp import web
from chat_take_aiohttp.helpers.utils import redirect, add_message
from chat_take_aiohttp.helpers.decorators import login_required


class Ping(web.View):
    """ ping """
    async def get(self):
        return web.Response(text='OK')


class Register(web.View):
    """ Регистрация пользователей """
    async def get(self):
        return web.Response(text='OK')


class Login(web.View):
    """ Вход пользователя """
    async def get(self):
        return web.Response(text='OK')


class Logout(web.View):
    """ Выход пользователя """
    @login_required
    async def get(self):
        self.request.session.pop('user')
        add_message(self.request, 'info', 'You are logged out')
        redirect(self.request, 'index')
