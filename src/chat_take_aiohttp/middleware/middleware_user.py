from aiohttp_session import get_session
from chat_take_aiohttp.models.users import Users


async def request_user_middleware(app, handler):
    """Миддельвара для того чтобы обогатить request пользователем"""
    async def middleware(request):
        request.session = await get_session(request)
        request.user = None
        user_id = request.session.get('user')
        if user_id is not None:
            request.user = await request.app.objects.get(Users, users_id=user_id)
        return await handler(request)
    return middleware
