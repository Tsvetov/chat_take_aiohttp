from chat_take_aiohttp.helpers.utils import add_message, redirect


def login_required(func):
    """ Allow only auth users """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is None:
            add_message(self.request, 'info', 'LogIn to continue.')
            redirect(self.request, 'login')
        return await func(self, *args, **kwargs)
    return wrapped