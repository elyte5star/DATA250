"""Provides a SQLite3 database extension for Flask.

This extension provides a simple interface to the SQLite3 database.

Example:
    from flask import Flask
    from social_insecurity.database import SQLite3

    app = Flask(__name__)
    db = SQLite3(app)
"""

from __future__ import annotations

import sqlite3
from os import PathLike
from pathlib import Path
from typing import Any, Optional, cast

from flask import Flask, current_app, g


class SQLite3:
    """Provides a SQLite3 database extension for Flask.

    This class provides a simple interface to the SQLite3 database.
    It also initializes the database if it does not exist yet.

    Example:
        from flask import Flask
        from social_insecurity.database import SQLite3

        app = Flask(__name__)
        db = SQLite3(app)

        # Use the database
        # db.query("SELECT * FROM Users;")
        # db.query("SELECT * FROM Users WHERE id = 1;", one=True)
        # db.query("INSERT INTO Users (name, email) VALUES ('John', 'test@test.net');")
    """

    def __init__(
        self,
        app: Optional[Flask] = None,
        *,
        path: Optional[PathLike | str] = None,
        schema: Optional[PathLike | str] = None,
    ) -> None:
        """Initializes the extension.

        params:
            app: The Flask application to initialize the extension with.
            path (optional): The path to the database file. Is relative to the instance folder.
            schema (optional): The path to the schema file. Is relative to the application root folder.

        """
        if app is not None:
            self.init_app(app, path=path, schema=schema)

    def init_app(
        self,
        app: Flask,
        *,
        path: Optional[PathLike | str] = None,
        schema: Optional[PathLike | str] = None,
    ) -> None:
        if not hasattr(app, "extensions"):
            app.extensions = {}
        if "sqlite3" not in app.extensions:
            app.extensions["sqlite3"] = self
        else:
            raise RuntimeError("Flask SQLite3 extension already initialized")

        instance_path = Path(app.instance_path)
        database_path = path or app.config.get("SQLITE3_DATABASE_PATH")

        if database_path:
            if ":memory:" in str(database_path):
                self._path = Path(database_path)
            else:
                self._path = instance_path / database_path
        else:
            raise ValueError("No database path provided to SQLite3 extension")

        if not self._path.exists():
            self._path.parent.mkdir(parents=True)

        if schema and not self._path.exists():
            with app.app_context():
                self._init_database(schema)

        app.teardown_appcontext(self._close_connection)

    @property
    def connection(self) -> sqlite3.Connection:
        """Returns the connection to the SQLite3 database."""
        conn = getattr(g, "flask_sqlite3_connection", None)
        if conn is None:
            conn = g.flask_sqlite3_connection = sqlite3.connect(self._path)
            conn.row_factory = sqlite3.Row
        return conn

    # TODO: Add more specific query methods to simplify code
    def get_all(self, param):
        cur = self.connection.cursor()
        try:
            cur.execute(param)
            result = cur.fetchall()
        except sqlite3.Error as err:
            result = "Error - " + err.args[0]
        finally:
            self.close()
            return result

    def get_one(self, param):
        cur = self.connection.cursor()
        try:
            cur.execute(query)
            result = cur.fetchone()
        except sqlite3.Error as err:
            result = "Error - " + err.args[0]
        finally:
            cur.close()
            return result

    def put(self, query):
        cur = self.connection.cursor()
        try:
            cur.execute(query)
            row_count = cur.rowcount
            self.connection.commit()
            response = "Done - Rows affected: " + str(row_count)
        except sqlite3.Error as err:
            response = "Error - " + err.args[0]
        finally:
            cur.close()
            return response

    def _init_database(self, schema: PathLike | str) -> None:
        """Initializes the database with the supplied schema if it does not exist yet."""
        with current_app.open_resource(str(schema), mode="r") as file:
            self.connection.executescript(file.read())
            self.connection.commit()

    def _close_connection(self, exception: Optional[BaseException] = None) -> None:
        """Closes the connection to the database."""
        conn = cast(sqlite3.Connection, getattr(g, "flask_sqlite3_connection", None))
        if conn is not None:
            conn.close()
