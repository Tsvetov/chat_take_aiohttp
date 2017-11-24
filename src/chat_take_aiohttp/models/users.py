import peewee
from chat_take_aiohttp.models.base_model import BaseModel


class Users(BaseModel):
    username = peewee.CharField(max_length=10, null=False)
    password = peewee.CharField(max_length=10, null=False)

    def __str__(self):
        return f'@{self.username}'