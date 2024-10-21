from social_insecurity import sqlite, login_manager
from social_insecurity.repository import User

@login_manager.user_loader
def load_user(user_id) -> User:
    return User


def create_comment():
    pass


def get_user_comments():
    pass


def get_principal(userid: str):
    
    return User


def create_user_friend():
    pass


def get_user_friends():
    pass


def upload_file():
    pass
