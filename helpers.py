import os
import sqlite3
from models import db, User, UserRecording
from pathlib import Path
from typing import Optional
from flask import flash
from dataclasses import dataclass


@dataclass
class TextDetail:
    name: str
    formatted_name: str
    body: str
    word_count: int


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "Error in the %s field - %s" % (getattr(form, field).label.text, error),
                "error",
            )


def format_name(name):
    return name.replace("_", " ").split(".")[0]


def format_email(email):
    return email.lower().strip()


def get_text_detail(text_name: str) -> Optional[TextDetail]:
    # TODO: proper file extension handling
    if text_name.split(".")[1] != "txt":
        return None

    with open(f"text/{text_name}", "r") as f:
        text_body = f.read()
        words = text_body.split()

    return TextDetail(
        name=text_name,
        formatted_name=format_name(text_name),
        body=text_body,
        word_count=len(words),
    )


def get_all_text_details():
    text_details = []
    for t in os.listdir("text"):
        text_detail = get_text_detail(t)
        text_details.append(text_detail)

    return text_details


def init_db():
    db.connect()
    db.create_tables([User, UserRecording])


def init_dirs():
    Path("text").mkdir(parents=True, exist_ok=True)
    Path("audio").mkdir(parents=True, exist_ok=True)
