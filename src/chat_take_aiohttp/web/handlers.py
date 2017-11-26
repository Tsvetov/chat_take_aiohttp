import re
import hashlib
import aiohttp_jinja2
from datetime import time
from aiohttp import web
from typing import Tuple, Dict, Any

from chat_take_aiohttp.helpers.utils import redirect, add_message
from chat_take_aiohttp.helpers.decorators import (
    login_required,
    anonymous_required,
)
from chat_take_aiohttp.models.users import Users
from chat_take_aiohttp.models.rooms import Room


class Ping(web.View):
    """ ping """
    async def get(self) -> web.Response:
        return web.Response(text='OK')


class HandlersMixinAccount:
    """Миксин для работы с пользователями"""

    async def is_valid(self, username: str, password: str) -> bool:
        """Валидация парвметров"""
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

    async def login_user(self, user: Users) -> None:
        """ Сетим пользователю сессию """
        self.request.session['user'] = str(user.users_id)
        self.request.session['time'] = str(time())
        add_message(
            self.request,
            'info',
            f'Hello {user}!'
        )
        redirect(self.request, 'index')

    async def get_normalize_data(self) -> Tuple[str, str]:
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
    async def get(self) -> Dict:
        return {}

    @anonymous_required
    async def post(self) -> None:
        """Cоздаем пользователя"""
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


class Login(HandlersMixinAccount, web.View):
    """ Вход пользователя """

    template_name = 'login.html'

    @anonymous_required
    @aiohttp_jinja2.template(template_name)
    async def get(self) -> Dict:
        return {}

    @anonymous_required
    async def post(self) -> None:
        username, password = await self.get_normalize_data()
        is_valid = await self.is_valid(username, password)
        if not is_valid:
            redirect(self.request, 'login')
        try:
            user = await self.request.app.objects.get(
                Users,
                Users.username ** username,
                Users.password ** hashlib.md5(password.encode()).hexdigest()
            )
            await self.login_user(user)
        except Users.DoesNotExist:
            add_message(self.request, 'danger', f'User {username} not found')
            redirect(self.request, 'login')

    async def login_user(self, user: Users) -> None:
        self.request.session['user'] = str(user.users_id)
        self.request.session['time'] = str(time())
        add_message(self.request, 'info', f'Hello {user}!')
        redirect(self.request, 'index')


class Logout(web.View):
    """ Выход пользователя """
    @login_required
    async def get(self) -> None:
        self.request.session.pop('user')
        add_message(self.request, 'info', 'You are logged out')
        redirect(self.request, 'index')


class Index(web.View):

    """ Main page view """

    template_name = 'index.html'

    @aiohttp_jinja2.template(template_name)
    async def get(self) -> Dict[str, Any]:
        if self.request.user:
            return {
                'chat_rooms': await Room.all_rooms(self.request.app.objects)
            }
        return {}