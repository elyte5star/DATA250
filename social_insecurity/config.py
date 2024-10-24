"""Provides the configuration for the Social Insecurity application.

This file is used to set the configuration for the application.

Example:
    from flask import Flask
    from social_insecurity.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    # Use the configuration
    secret_key = app.config["SECRET_KEY"]
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "secret"
    SQLITE3_DATABASE_PATH = "sqlite3.db"
    UPLOADS_FOLDER_PATH = "uploads"
    ALLOWED_EXTENSIONS = {}
    WTF_CSRF_ENABLED = True
    PERMANENT_SESSION_LIFETIME = (
        int(os.environ.get("PERMANENT_SESSION_LIFETIME")) or 10000
    )
    REMEMBER_COOKIE_DURATION = int(os.environ.get("REMEMBER_COOKIE_DURATION")) or 30000
