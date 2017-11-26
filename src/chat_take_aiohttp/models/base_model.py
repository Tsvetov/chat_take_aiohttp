import peewee
import peewee_async


database = peewee_async.PostgresqlDatabase(None)


class BaseModel(peewee.Model):
    """ Базовая модель """
    class Meta:
        database = database