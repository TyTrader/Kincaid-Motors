from peewee import *
from os import path

db_connection_path = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(db_connection_path, "myDB"))


class User(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db


class Cars(Model):
    make = CharField()
    model = CharField()
    YOM = DoubleField()
    price = DoubleField()
    power = CharField()

    class Meta:
        database = db


class Requests(Model):
    content = CharField()

    class Meta:
        database = db


User.create_table(fail_silently=True)
Cars.create_table(fail_silently=True)
