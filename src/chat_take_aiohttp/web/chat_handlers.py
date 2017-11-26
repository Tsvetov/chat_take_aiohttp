from typing import Dict, Any
import re
import aiohttp_jinja2

from textwrap import dedent
from aiohttp import web

from chat_take_aiohttp.models.message import Message
from chat_take_aiohttp.models.message import Room
from chat_take_aiohttp.helpers.decorators import login_required
from chat_take_aiohttp.helpers.utils import (
    redirect,
    add_message,
    get_object_or_404
)


class CreateRoom(web.View):

    """ Создать новую комнату """

    @login_required
    @aiohttp_jinja2.template('rooms.html')
    async def get(self) -> Dict[str, Any]:
        return {'chat_rooms': await Room.all_rooms(self.request.app.objects)}

    @login_required
    async def post(self) -> None:
        data = await self.request.post()
        roomname = data.get('roomname', '').lower()
        if not roomname:
            redirect(self.request, 'create_room')
        if await self.request.app.objects.count(Room.select().where(Room.name ** roomname)):
            add_message(self.request, 'danger', f'Room with {roomname} already exists.')
            redirect(self.request, 'create_room')
        room = await self.request.app.objects.create(Room, name=roomname)
        redirect(self.request, 'room', parts=dict(slug=room.name))


class ChatRoom(web.View):

    """ Заходим в комнату """

    @login_required
    @aiohttp_jinja2.template('chat.html')
    async def get(self) -> Dict[str, Any]:
        room = await get_object_or_404(self.request, Room, name=self.request.match_info['slug'].lower())
        return {
            'room': room, 'chat_rooms': await Room.all_rooms(self.request.app.objects),
            'room_messages': await room.all_messages(self.request.app.objects)
        }


class WebSocketMixin:
    """
    Вспомогательный класс для всяких нужных методов для работы с вебсокетами,
    что бы не засорять хелпер
    """

    async def command_line(self, cmd: str) -> Dict[str, str]:
        """ Некоторые управляющие команды """
        app = self.request.app
        app.logger.debug(f'Chat command {cmd}')

        if cmd == '/clear':
            await app.objects.execute(Message.delete().where(Message.room == self.room))
            app.logger.debug(f'Removed {count} messages')
            for peer in app.wslist[self.room.id].values():
                peer.send_json({'cmd': 'empty'})

        elif cmd == '/help':
            return {'text': dedent('''\
                - /help - помощь
                - /clear - очищаем комнату от сообщений
                ''')}
        else:
            return {'text': 'wrong cmd {cmd}'}

    async def broadcast(self, message: Message) -> None:
        """ Рассылка сообщениий по всей комнате """
        self.request.app.logger.debug(self.request.app.wslist[self.room.room_id].values())

        for peer in self.request.app.wslist[self.room.room_id].values():
            peer.send_json(message.as_dict())


class WebSocket(WebSocketMixin, web.View):

    """ Helper  для работы с вебсокетами"""
    async def get(self) -> web.WebSocketResponse:

        self.room = await get_object_or_404(
            self.request, Room, name=self.request.match_info['slug'].lower()
        )
        user = self.request.user
        app = self.request.app

        app.logger.debug('Prepare WS connection')

        ws = web.WebSocketResponse()

        await ws.prepare(self.request)

        if self.room.room_id not in app.wslist:
            app.wslist[self.room.room_id] = {}

        message = await app.objects.create(
            Message,
            room=self.room,
            users=None,
            text=f'@{user.username} join chat room'
        )

        app.wslist[self.room.room_id][user.username] = ws

        await self.broadcast(message)

        async for msg in ws:
            app.logger.debug(msg)
            if msg.tp == web.MsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    text = msg.data.strip()
                    if text.startswith('/'):
                        ans = await self.command_line(text)
                        if ans is not None:
                            await ws.send_json(ans)
                    else:
                        message = await app.objects.create(
                            Message, room=self.room, users=user, text=text
                        )
                        await self.broadcast(message)
            elif msg.tp == web.MsgType.error:
                app.logger.debug(
                    f'Connection closed with exception {ws.exception()}'
                )

        return ws
