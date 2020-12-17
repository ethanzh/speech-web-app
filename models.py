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
    language = CharField(null=True)
    salted_pw = CharField()
    created_at = DateTimeField(default=datetime.now)


class UserSample(BaseModel):
    user = ForeignKeyField(User, backref="samples")
    filename = CharField()
    audio_source = CharField(null=True)
    video_source = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
