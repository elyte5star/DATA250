from flask_login import UserMixin
from social_insecurity import sqlite, bcrypt
import sqlite3
import datetime
import uuid


class User(UserMixin):
    def __init__(self, userid, username, password):
        self.id = userid
        self.username = username
        self.password = password
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self.userid


def get_indent() -> str:
    return str(uuid.uuid4())


def time_now_utc() -> datetime:
    return datetime.now()


def create_user(data: dict):
    username = data["username"]
    hashed_password = bcrypt.generate_password_hash(data["password"], 12).decode()
    first_name = data["first_name"]
    last_name = data["last_name"]
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Users (username, userid,first_name,
            last_name, password,creation_time,modification_time)
              VALUES (?, ?, ?, ?, ?, ?,?)""",
            [
                username,
                get_indent(),
                first_name,
                last_name,
                hashed_password,
                time_now_utc(),
                time_now_utc(),
            ],
        )
        row_count = cur.rowcount
        sqlite.connection.commit()
        response = "Done - Rows affected: " + str(row_count)
    except sqlite3.Error as err:
        response = "Error - " + err.args[0]
    finally:
        cur.close()
        return response


def get_user_by_username(username: str):
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where username = (?)", [username])
        result = cur.fetchone()
    except sqlite3.Error as err:
        result = "Error - " + err.args[0]
    finally:
        cur.close()
        return result


def create_comment(post_id: int, user_id: int, data: str):
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Comments (p_id, u_id, comment,
            creation_time) VALUES (?, ?,?,?)""",
            [post_id, user_id, data, time_now_utc()],
        )
        row_count = cur.rowcount
        sqlite.connection.commit()
        response = "Done - Rows affected: " + str(row_count)
    except sqlite3.Error as err:
        response = "Error - " + err.args[0]
    finally:
        cur.close()
        return response


def get_post(post_id: int):
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """SELECT * FROM Posts AS p JOIN Users AS u ON p.u_id=
            u.id  WHERE p.id = (?)""",
            [post_id],
        )
        result = cur.fetchone()
    except sqlite3.Error as err:
        result = "Error - " + err.args[0]
    finally:
        cur.close()
        return result


def get_user_comments(post_id: str):
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """
        SELECT DISTINCT *
        FROM Comments AS c JOIN Users AS u ON c.u_id = u.id
        WHERE c.p_id=(?)
        ORDER BY c.creation_time DESC
        """,
            [post_id],
        )
        result = cur.fetchall()
    except sqlite3.Error as err:
        result = "Error - " + err.args[0]
    finally:
        cur.close()
        return result


def get_principal(user_id: str):
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where userid = (?)", [user_id])
        result = cur.fetchone()
    except sqlite3.Error as err:
        result = "Error - " + err.args[0]
    finally:
        cur.close()
        return result


def create_user_friend():
    pass


def get_user_friends():
    pass


def upload_file():
    pass
