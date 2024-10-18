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


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret"
    SQLITE3_DATABASE_PATH = "sqlite3.db"
    SQLALCHEMY_DATABASE_URI = "sqlite3.db"
    UPLOADS_FOLDER_PATH = "uploads"
    ALLOWED_EXTENSIONS = {}
    WTF_CSRF_ENABLED = True
    PERMANENT_SESSION_LIFETIME = os.environ.get("PERMANENT_SESSION_LIFETIME")
    REMEMBER_COOKIE_DURATION = os.environ.get("REMEMBER_COOKIE_DURATION")
