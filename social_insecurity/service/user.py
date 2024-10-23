from social_insecurity import login_manager, bcrypt  # noqa: I001
from social_insecurity.repository.user import (
    User,
    get_principal,
    get_user_by_username,
    create_user,
    get_posts_by_userid,
    create_post,
)
from flask import flash, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user, current_user


@login_manager.user_loader
def load_user(user_id):
    user = get_principal(user_id)
    return User(user[0], user[1], user[2]) if user is not None else None


def find_user_by_username(username: str):
    user = get_user_by_username(username)
    return User(user[0], user[1], user[2])


def _login(username: str, password: str, remember_me):
    user = get_user_by_username(username)
    if len(user) > 0 and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember_me=remember_me)
        return redirect(url_for("stream", username=user.username))
    flash("Invalid username/password!", category="warning")


def _create_user(username: str, first_name: str, lastname: str, password):
    data = {
        "username": username,
        "first_name": first_name,
        "last_name": lastname,
        "password": password,
    }
    response = create_user(data)
    if response is not None:
        flash("User successfully created!", category="success")
        return redirect(url_for("index"))
    flash("Operation unsuccessful!", category="warning")


def _create_post(username: str, data: str, image_name: str):
    user = find_user_by_username(username)
    if user is not None:
        response = create_post(user.id, data, image_name)
        if response is not None:
            flash("User successfully created!", category="success")
            return redirect(url_for("stream", username=username))
    flash("Operation unsuccessful!", category="warning")


def _create_comment():
    pass


def get_user_comments():
    pass


def _get_user_posts(username: str):
    user = find_user_by_username(username)
    if user is not None:
        posts = get_posts_by_userid(user.id)
        return posts
    flash("Operation unsuccessful!", category="warning")


def create_user_friend():
    pass


def get_user_friends():
    pass


def upload_file():
    pass
