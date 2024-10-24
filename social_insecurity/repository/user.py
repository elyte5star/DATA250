from flask_login import UserMixin  # noqa: I001
from social_insecurity import sqlite, bcrypt
import sqlite3
from datetime import datetime
import uuid
from typing import Union


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
        return self.id

    def get_username(self):
        return self.username

    def __repr__(self):
        return "<User {}>".format(self.username)


def get_indent() -> str:
    return str(uuid.uuid4())


def creation_time() -> str:
    """
    Get the current time in ISO 8601 format.

    Returns
    -------
    str
        The current time in ISO 8601 format.
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def time_now_utc() -> datetime:
    return datetime.now()


def create_user(data: tuple) -> Union[str, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Users (id,username,first_name,
            last_name, userid, password,creation_time,modification_time)
              VALUES (?, ?, ?, ?, ?, ?,? ,?)""",
            data,
        )
        sqlite.connection.commit()
        return "Done - Row ID: " + str(cur.lastrowid)
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_user_by_username(username: str) -> Union[tuple, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where username = (?)", [username])
        return cur.fetchone()
    except sqlite3.Error as err:
        print("Error getting  - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def create_comment(comment_info: tuple) -> Union[str, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Comments (p_id, u_id, comment,
            creation_time) VALUES (?, ?,?,?)""",
            comment_info,
        )
        sqlite.connection.commit()
        return "Done - Row ID: " + str(cur.lastrowid)
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def create_post(post_info: tuple) -> Union[tuple, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Comments (u_id, content, image, creation_time) 
            VALUES (?, ?,?,?)""",
            post_info,
        )
        sqlite.connection.commit()
        return "Done - Row ID: " + str(cur.lastrowid)
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_post(post_id: int) -> Union[tuple, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """SELECT * FROM Posts AS p JOIN Users AS u ON p.u_id=
            u.id  WHERE p.id = (?)""",
            [post_id],
        )
        return cur.fetchone()
    except sqlite3.Error as err:
        print("Error getting  - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_user_comments(post_id: str) -> Union[list, Exception]:
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
        return cur.fetchall()
    except sqlite3.Error as err:
        print("Error getting  - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_posts_by_userid(userid: str) -> Union[list, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """
       SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id = p.id) AS cc
          FROM Posts AS p JOIN Users AS u ON u.id = p.u_id
          WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id =
        (?) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id = (?)) OR p.u_id=(?)
       ORDER BY p.creation_time DESC;
        """,
            [userid, userid],
        )
        return cur.fetchall()
    except sqlite3.Error as err:
        print("Error getting  - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_principal(user_id: str) -> Union[tuple, None, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where userid = (?)", [user_id])
        return cur.fetchone()
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        return None
    finally:
        cur.close()


def create_user_friend():
    pass


def get_user_friends():
    pass


def upload_file():
    pass
