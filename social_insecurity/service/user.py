from social_insecurity import login_manager, bcrypt  # noqa: I001
from social_insecurity.repository.user import (
    User,
    get_principal,
    get_user_by_username,
    create_user,
    get_posts_by_userid,
    create_post,
    create_comment,
    get_user_comments,
    get_post,
    get_user_friends,
    create_user_friend,
    update_user_profile,
)
from flask import flash, abort, redirect, url_for
from flask_login import login_user
from typing import Union
from datetime import datetime, date
import uuid


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


def _find_user_by_username(username: str) -> User:
    user = get_user_by_username(username)
    if user is not None:
        return User(user[1], user[2], user[5])
    return None


def _login(username: str, password: str, remember_me):
    user = _find_user_by_username(username)
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            flash("you were just logged in!", category="success")
            login_user(user, remember=remember_me)
            return redirect(url_for("stream", username=user.username))
    flash("Invalid username/password!", category="warning")
    return redirect(url_for("index"))


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
    user = _find_user_by_username(username)
    if "Error" not in user:
        payload = (user.get_id, data, image_name, time_now_utc())
        response = create_post(payload)
        if "Error" not in response:
            flash("User successfully created!", category="success")
            return redirect(url_for("stream", username=username))
    flash("Operation unsuccessful!", category="warning")
    abort(500, "Operation unsuccessful!")


def _create_comment(username: str, post_id: int, data: str):
    user = _find_user_by_username(username)
    if user is not None:
        comment_info = (post_id, user.get_id, data, time_now_utc())
        create_comment(comment_info)
    abort(500, "Operation unsuccessful!")


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
    user = _find_user_by_username(username)
    if user is not None:
        posts = get_posts_by_userid(user.id)
        return posts
    flash("Operation unsuccessful!", category="warning")
    abort(404, "Operation unsuccessful!")


def _create_user_friend(current_user: User, friend_username: str):
    new_friend_check = _find_user_by_username(friend_username)
    user_friends = _get_user_friends(current_user.get_id)
    if new_friend_check is None:
        flash("User does not exist!", category="warning")
    elif new_friend_check.get_id() == current_user.get_id():
        flash("You cannot be friends with yourself!", category="warning")
    elif new_friend_check.get_id in [friend["userid"] for friend in user_friends]:
        flash("You are already friends with this user!", category="warning")
    elif _create_friend(current_user.get_id, new_friend_check.get_id) is not None:
        flash("Friend successfully added!", category="success")
    else:
        abort(404, "Operation unsuccessful!")


def _create_friend(userid, friend_id):
    response = create_user_friend((userid, friend_id))
    if "Error" not in response:
        return response
    return None


def _get_user_friends(userid: str):
    friends = get_user_friends(userid)
    if "Error" not in friends:
        return friends
    flash("Operation unsuccessful!", category="warning")
    return None


def upload_file():
    pass


def _get_user(username: str) -> User:
    user = get_user_by_username(username)
    if "Error" in user:
        abort(500, "Operation unsuccessful!")
    elif user is None:
        abort(404, f"User with username : {username} not found!")
    return user


def _update_user_profile(
    education: str,
    employment: str,
    music: str,
    movie: str,
    nationality: str,
    birthday: str,
    current_user: User,
):
    modify = (
        education,
        employment,
        music,
        movie,
        nationality,
        datetime.strptime(birthday, "%d%m%Y").date(),
        time_now_utc(),
        current_user.get_username(),
        current_user.get_username(),
    )
    response = update_user_profile(modify)
    if "Error" not in response:
        return redirect(url_for("profile", username=current_user.get_username()))
    abort(500, "Operation unsuccessful!")
