from flask_login import UserMixin  # noqa: I001
from social_insecurity import sqlite, bcrypt
import sqlite3
from datetime import datetime
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

    def get_username(self):
        return self.username


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


def create_user(data: dict):
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Users (username, userid,first_name,
            last_name, password,creation_time,modification_time)
              VALUES (?, ?, ?, ?, ?, ?,?)""",
            [
                data["username"],
                data["userid"],
                data["first_name"],
                data["last_name"],
                data["password"],
                data["creation_time"],
                data["modification_time"],
            ],
        )
        row_count = cur.rowcount
        sqlite.connection.commit()
        response = "Done - Rows affected: " + str(row_count)
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        response = None
    finally:
        cur.close()
        return response


def get_user_by_username(username: str):
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where username = (?)", [username])
        result = cur.fetchone()
    except sqlite3.Error as err:
        print("Error getting  - " + err.args[0])
        result = None
    finally:
        cur.close()
        return User(result[0], result[1], result[2])


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
        print("Error - " + err.args[0])
        response = None
    finally:
        cur.close()
        return response


def create_post(userid: str, data: str, image_name: str):
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Comments (u_id, content, image, creation_time) 
            VALUES (?, ?,?,?)""",
            [userid, data, image_name, time_now_utc()],
        )
        row_count = cur.rowcount
        sqlite.connection.commit()
        response = "Done - Rows affected: " + str(row_count)
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        response = None
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
        print("Error - " + err.args[0])
        result = None
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
        print("Error - " + err.args[0])
        result = None
    finally:
        cur.close()
        return result


def get_posts_by_userid(userid: str):
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
        result = cur.fetchall()
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        result = None
    finally:
        cur.close()
        return result


def get_principal(user_id: str):
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where userid = (?)", [user_id])
        result = cur.fetchone()
    except sqlite3.Error as err:
        print("Error - " + err.args[0])
        result = None
    finally:
        cur.close()
        return result


def create_user_friend():
    pass


def get_user_friends():
    pass


def upload_file():
    pass
