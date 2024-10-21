from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
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


def get_user_by_username(username: str):
    pass


def create_comment(username: str, post_id: int):
    pass


def get_user_comments(username: str):
    pass


def get_principal(userid: str):
    return


def create_user_friend():
    pass


def get_user_friends():
    pass


def upload_file():
    pass
