from flask_login import UserMixin  # noqa: I001
from social_insecurity import sqlite
import sqlite3
from typing import Union
import social_insecurity.log as logger


log = logger.get_logger("Database activities")


class User(UserMixin):
    def __init__(self, userid, username, password, active):
        self.id = userid
        self.username = username
        self.password = password
        self.authenticated = False
        self.active = active

    def is_active(self) -> bool:
        return self.active

    def is_anonymous(self) -> bool:
        return False

    def is_authenticated(self):
        return self.authenticated

    def get_id(self) -> str:
        return self.id

    def get_username(self) -> str:
        return self.username

    def __repr__(self):
        return "<User {}>".format(self.username)


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
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_user_by_username(username: str) -> Union[tuple, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where username = (?)", [username])
        return cur.fetchone()
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
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
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def create_post(post_info: tuple) -> Union[str, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """INSERT INTO Posts (u_id, content, image, creation_time) 
            VALUES (?, ?,?,?)""",
            post_info,
        )
        sqlite.connection.commit()
        return "Done - Row ID: " + str(cur.lastrowid)
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_post(post_id: int) -> Union[tuple, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """SELECT * FROM Posts AS p JOIN Users AS u ON p.u_id=
            u.userid  WHERE p.id = (?)""",
            [post_id],
        )
        return cur.fetchone()
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_user_comments(post_id: str) -> Union[list, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """
        SELECT DISTINCT *
        FROM Comments AS c JOIN Users AS u ON c.u_id = u.userid
        WHERE c.p_id=(?)
        ORDER BY c.creation_time DESC
        """,
            [post_id],
        )
        return cur.fetchall()
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_posts_by_userid(userid: str) -> Union[list, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """
       SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id = p.id) AS cc
         FROM Posts AS p JOIN Users AS u ON u.userid = p.u_id
         WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id = ?) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id = ?) OR p.u_id = ?
         ORDER BY p.creation_time DESC
        """,
            [userid, userid, userid],
        )
        return cur.fetchall()
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_principal(userid: str) -> Union[tuple, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT * from Users where userid = (?)", [userid])
        return cur.fetchone()
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def create_user_friend(data: tuple) -> Union[str, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """
            INSERT INTO Friends (u_id, f_id) VALUES (?, ?)
            """,
            data,
        )
        sqlite.connection.commit()
        return "Done - Row ID: " + str(cur.lastrowid)
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_user_friends_ids(userid: str) -> Union[list, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute("SELECT f_id FROM Friends WHERE u_id = (?)", [userid])
        return cur.fetchall()
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def upload_file():
    pass


def update_user_profile(data: tuple) -> Union[str, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """
               UPDATE Users
            SET education=(?), 
            employment=(?),
                music=(?), movie=(?),
                nationality=(?), birthday=(?),
                modification_time=(?),
                modified_by=(?)
            WHERE username=(?);
                """,
            data,
        )
        sqlite.connection.commit()
        return "Done - Row Affected: " + str(cur.rowcount)
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()


def get_user_friends(userid: str) -> Union[list, Exception]:
    try:
        cur = sqlite.connection.cursor()
        cur.execute(
            """SELECT * FROM Friends AS f JOIN Users as u ON f.f_id = u.userid
        WHERE f.u_id = (?) AND f.f_id != (?)""",
            [userid, userid],
        )
        return cur.fetchall()
    except sqlite3.Error as err:
        log.error("Error - " + err.args[0])
        return "Error - " + err.args[0]
    finally:
        cur.close()
