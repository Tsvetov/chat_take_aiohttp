import peewee
from datetime import datetime

from chat_take_aiohttp.models.users import Users
from chat_take_aiohttp.models.users import BaseModel


class Room(BaseModel):
    """ Модель комнаты """
    room_id = peewee.PrimaryKeyField(help_text='Идентификатор')
    name = peewee.CharField(unique=True, index=True, max_length=32, null=False, help_text='Наименование комнаты')

    @classmethod
    async def all_rooms(cls, objects):
        """ ОТдать все комнаты """
        return await objects.execute(cls.select())

    async def all_messages(self, objects):
        """ Отдать все сообщения для комнаты """
        return await objects.prefetch(self.messages, Users.select())

    class Meta:
        order_by = ('name', )

    def __str__(self):
        return self.name