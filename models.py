
from peewee import *

DATABASE = SqliteDatabase('todos.sqlite')


class Todo(Model):
    """The model for todos, only names are present at this point"""
    name = CharField()

    class Meta:
        database = DATABASE


def initialize():
    """start up the database"""
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
