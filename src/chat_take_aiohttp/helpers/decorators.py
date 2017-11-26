from chat_take_aiohttp.helpers.utils import add_message, redirect


def login_required(func):
    """ Проверка авторизации """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is None:
            add_message(self.request, 'info', 'LogIn to continue.')
            redirect(self.request, 'login')
        return await func(self, *args, **kwargs)
    return wrapped


def anonymous_required(func):
    """ Пользователь должен быть анонимным """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is not None:
            add_message(
                self.request,
                'info',
                '<a href="/logout" class="alert-link">LogOut</a> to continue.'
            )
            redirect(self.request, 'index')
        return await func(self, *args, **kwargs)
    return wrapped