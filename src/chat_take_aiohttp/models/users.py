import peewee
from chat_take_aiohttp.models.base_model import BaseModel


class Users(BaseModel):
    """Модель пользователя"""
    users_id = peewee.PrimaryKeyField(help_text='Идентификатор')
    username = peewee.CharField(max_length=10, null=False, unique=True, help_text='Имя пользователя')
    password = peewee.CharField(max_length=10, null=False, help_text='Хэш от пароля пользователя')

    def __str__(self) -> str:
        return f'@{self.username}'