from peewee import (
    Model,
    SqliteDatabase,
    ForeignKeyField,
    CharField,
    DateTimeField,
    UUIDField,
)
from datetime import datetime
from flask_login import UserMixin

db = SqliteDatabase("main.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    id = UUIDField(primary_key=True)
    email = CharField(unique=True)
    gender = CharField()
    age_range = CharField()
    salted_pw = CharField()
    created_at = DateTimeField(default=datetime.now)


class UserRecording(BaseModel):
    user = ForeignKeyField(User, backref="recordings")
    audio_path = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
