import peewee
from datetime import datetime

from chat_take_aiohttp.models.users import Users
from chat_take_aiohttp.models.rooms import Room
from chat_take_aiohttp.models.users import BaseModel


class Message(BaseModel):

    """  Чат модель """

    message_id = peewee.PrimaryKeyField(help_text='Идентификатор')

    users = peewee.ForeignKeyField(
        Users,
        null=True,
        related_name='messages',
        to_field='users_id',
        help_text="Ссылка на пользователя"
    )
    room = peewee.ForeignKeyField(
        Room, related_name='messages',
        to_field='room_id',
        help_text="Ссылка на комнату"
    )
    text = peewee.TextField(help_text="Текст сообщения")
    created_at = peewee.DateTimeField(
        default=datetime.now, help_text="Время создания сообщения"
    )

    def __str__(self):
        return self.text

    class Meta:
        order_by = ('created_at', )

    def as_dict(self):
        """ Return dict repr of message """
        return {
            'text': self.text, 'created_at': self.created_at.isoformat(),
            'user': self.users.username if self.users else None
        }
