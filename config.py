import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "DEVELOPMENT_KEY"
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024
