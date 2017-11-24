import re
import hashlib
import aiohttp_jinja2
from datetime import time
from aiohttp import web

from chat_take_aiohttp.helpers.utils import redirect, add_message
from chat_take_aiohttp.helpers.decorators import (
    login_required,
    anonymous_required,
)
from chat_take_aiohttp.models.users import Users


class Ping(web.View):
    """ ping """
    async def get(self):
        return web.Response(text='OK')


class HandlersMixinAccount:
    async def is_valid(self, username, password):
        if (
            re.match(r'^[a-z]\w{0,9}$', username) and
            re.match(r'^[a-z]\w{0,9}$', password)
        ):
            return True

        add_message(
            self.request,
            'warning',
            'username or password not valid'
        )
        return False

    async def login_user(self, user):
        """ Put user to session and redirect to Index """
        self.request.session['user'] = str(user.id)
        self.request.session['time'] = str(time())
        add_message(
            self.request,
            'info',
            f'Hello {user}!'
        )
        redirect(self.request, 'index')

    async def get_normalize_data(self):
        data = await self.request.post()
        self.request.post()
        username = data.get('username', '').lower()
        password = data.get('password', '').lower()
        return username, password


class Register(HandlersMixinAccount, web.View):
    """ Регистрация пользователей """

    template_name = 'register.html'

    @anonymous_required
    @aiohttp_jinja2.template(template_name)
    async def get(self):
        return {}

    @anonymous_required
    async def post(self):
        username, password = await self.get_normalize_data()

        is_valid = await self.is_valid(username, password)

        if not is_valid:
            redirect(self.request, 'register')

        if await self.request.app.objects.count(
                Users.select().where(Users.username ** username)
        ):
            add_message(
                self.request, 'danger', f'{username} already exists'
            )
            redirect(self.request, 'register')
        user = await self.request.app.objects.create(
            Users,
            username=username,
            password=hashlib.md5(password.encode()).hexdigest()
        )
        await self.login_user(user)


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
