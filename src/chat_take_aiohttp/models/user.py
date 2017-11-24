import peewee
from chat_take_aiohttp.models.base_model import BaseModel


class User(BaseModel):

    """ Simple model for save users in DB """

    username = peewee.CharField(unique=True, index=True, max_length=10, null=False)
    password = peewee.CharField(unique=True, index=True, max_length=10, null=False)

    def __str__(self):
        return f'@{self.username}'