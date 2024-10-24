from social_insecurity import login_manager, bcrypt  # noqa: I001
from social_insecurity.repository.user import (
    User,
    get_principal,
    get_user_by_username,
    create_user,
    get_posts_by_userid,
    create_post,
    time_now_utc,
    get_indent,
    create_comment,
    get_user_comments,
    get_post,
)
from flask import flash, abort, redirect, url_for
from flask_login import login_user
from typing import Union


@login_manager.user_loader
def load_user(user_id) -> Union[User, None]:
    user = get_principal(user_id)
    if user is None:
        return None
    elif "Error" not in user:
        return None
    return User(user[0], user[1], user[2])


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return "failed login"


def find_user_by_username(username: str) -> User:
    user = get_user_by_username(username)
    if "Error" not in user and user is not None:
        return User(user[1], user[2], user[5])
    return None


def _login(username: str, password: str, remember_me):
    user = find_user_by_username(username)
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            flash("you were just logged in!", category="success")
            login_user(user, remember=remember_me)
            return redirect(url_for("stream", username=user.username))
    flash("Invalid username/password!", category="warning")
    abort(404, "Invalid username/password!")


def _create_user(username: str, first_name: str, lastname: str, password):
    hashed_password = bcrypt.generate_password_hash(password)
    user_info = (
        get_indent(),
        username,
        first_name,
        lastname,
        get_indent(),
        hashed_password,
        time_now_utc(),
        time_now_utc(),
    )
    response = create_user(user_info)
    if "Error" in response:
        message = "Operation unsuccessful!!"
        if "Error - UNIQUE" in response:
            message = "User already exist!"
        flash(message, category="warning")
        return redirect(url_for("index"))
    flash("User successfully created!", category="success")
    return redirect(url_for("index"))


def _create_post(username: str, data: str, image_name: str):
    user = find_user_by_username(username)
    if "Error" not in user:
        payload = (user.get_id, data, image_name, time_now_utc())
        response = create_post(payload)
        if "Error" not in response:
            flash("User successfully created!", category="success")
            return redirect(url_for("stream", username=username))
    flash("Operation unsuccessful!", category="warning")


def _create_comment(username: str, post_id: int, data: str):
    user = find_user_by_username(username)
    if user is not None:
        comment_info = (post_id, user.get_id, data, time_now_utc())
        create_comment(comment_info)


def _get_user_comments(post_id: int):
    comments = get_user_comments(post_id)
    if "Error" not in comments:
        return comments
    flash("Operation unsuccessful!", category="warning")


def _get_user_post(post_id: int):
    post = get_post(post_id)
    if "Error" not in post:
        return post
    abort(404, f"Post with {post_id} is not found!")


def _get_user_posts(username: str):
    user = find_user_by_username(username)
    if user is not None:
        posts = get_posts_by_userid(user.id)
        return posts
    flash("Operation unsuccessful!", category="warning")
    abort(404, "Operation unsuccessful!")


def create_user_friend():
    pass


def get_user_friends():
    pass


def upload_file():
    pass
