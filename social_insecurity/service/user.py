from social_insecurity import login_manager, bcrypt, limiter  # noqa: I001
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
    get_user_friends_ids,
    create_user_friend,
    update_user_profile,
    get_user_friends,
)
from flask import flash, abort, redirect, url_for, request, session
from flask_login import login_user
from typing import Union
from datetime import datetime, timedelta
import uuid
from flask import current_app as app
import social_insecurity.log as logger
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
from pathlib import Path

REMEMBER_COOKIE_DURATION = timedelta(minutes=15)
PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)


log = logger.get_logger("User actions")


def allowed_file(filename: str):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def get_indent() -> str:
    return str(uuid.uuid4())


def time_now_utc() -> datetime:
    return datetime.now()


@login_manager.user_loader
def load_user(user_id) -> Union[User, None]:
    user = get_principal(user_id)
    if user is None:
        return None
    active = int(user[9]) == 1
    return User(user[1], user[2], user[5], active)


@app.errorhandler(429)
def ratelimit_handler(e):
    log.warning(f"ratelimit exceeded {e.description}")
    flash("Too Many Requests,limits exceeded!", category="danger")
    return redirect(url_for("index"))


@login_manager.unauthorized_handler
def unauthorized():
    flash("Unauthorized, Please log in!", category="warning")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    flash("Page not found!", category="warning")
    log.warning(f"Page not found! {error.description}")
    return redirect(url_for("stream"))


@app.errorhandler(500)
def internal_server_error(error):
    flash("Operation unsuccessful", category="warning")
    log.error(f"Server error {error.description}")
    return redirect(url_for("stream"))


def _find_user_by_username(username: str) -> User:
    user = get_user_by_username(username)
    if user is not None:
        active = int(user[9]) == 1
        return User(user[1], user[2], user[5], active)
    return None


def get_ipaddress():
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    return ip_address


@limiter.limit("3 per minute", key_func=lambda: get_ipaddress)
def _login(username: str, password: str, remember_me: bool):
    user = _find_user_by_username(username)
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            flash("you were just logged in!", category="success")
            login_user(user, remember=remember_me, duration=REMEMBER_COOKIE_DURATION)
            session.permanent = True
            app.permanent_session_lifetime = PERMANENT_SESSION_LIFETIME
            next_page = request.args.get("next")
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for("stream")
            return redirect(next_page)
    flash("Invalid username or password!", category="danger")
    log.warning(f"Failed login attempt by user :{username}")
    return redirect(url_for("index"))


def _create_user(username: str, first_name: str, lastname: str, password):
    find_user = _find_user_by_username(username)
    if find_user is None:
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
        log.info(response)
        flash(f"User successfully with id {user_info[4]} created!", category="success")
        return redirect(url_for("index"))
    flash("Operation unsuccessful, user already exits!!", category="warning")
    return redirect(url_for("index"))


def _create_post(current_user: User, data: str, image_name: str):
    if current_user is not None:
        payload = (current_user.get_id(), data, image_name, time_now_utc())
        response = create_post(payload)
        if "Error" not in response:
            flash("Post successfully created!", category="success")
            return redirect(url_for("stream", username=current_user.get_username()))
    flash("Operation unsuccessful!", category="warning")
    abort(500, "Operation unsuccessful!")


def _create_comment(current_user: User, post_id: int, data: str):
    if current_user is not None:
        comment_info = (post_id, current_user.get_id(), data, time_now_utc())
        _ = create_comment(comment_info)
    else:
        abort(500, "Operation unsuccessful!")


def _get_user_comments(post_id: int):
    comments = get_user_comments(post_id)
    if "Error" not in comments:
        return comments
    flash("Operation unsuccessful!", category="warning")


def _get_user_post(post_id: int):
    post = get_post(post_id)
    if post is not None:
        return post
    abort(404, f"Post with {post_id} is not found!")


def _get_user_posts(userid: str):
    posts = get_posts_by_userid(userid)
    return posts


def _create_user_friend(current_user: User, friend_username: str):
    new_friend_check = _find_user_by_username(friend_username)
    if new_friend_check is None:
        flash("User does not exist!", category="warning")
    elif new_friend_check.get_id() == current_user.get_id():
        flash("You cannot be friends with yourself!", category="warning")
    elif check_if_a_user_is_a_friend(current_user.get_id(), new_friend_check.get_id()):
        flash("You are already friends with this user!", category="warning")
    elif _create_friend(current_user.get_id(), new_friend_check.get_id()) is not None:
        flash("Friend successfully added!", category="success")
    else:
        abort(404, "Operation unsuccessful!")


def check_if_a_user_is_a_friend(userid: str, new_friend_id: str):
    friends_ids = _get_friends_ids(userid)
    if friends_ids:
        for id in friends_ids:
            if id[0] == new_friend_id:
                return True
    return False


def _create_friend(userid, friend_id):
    response = create_user_friend((userid, friend_id))
    if "Error" not in response:
        return response
    return None


def _get_friends_ids(userid: str):
    ids = get_user_friends_ids(userid)
    if "Error" in ids:
        flash("Operation unsuccessful!", category="warning")
    return ids


def upload_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = Path(app.instance_path) / app.config["UPLOADS_FOLDER_PATH"] / filename
        file.save(path)
        flash(f"Picture with name {filename} uploaded!", category="success")
    else:
        flash("Invalid file type!", category="warning")


def _get_user(username: str) -> User:
    user = get_user_by_username(username)
    if user is None:
        abort(404, f"User with username : {username} not found!")
    return user


def _get_user_friends(userid: str) -> list:
    friends = get_user_friends(userid)
    if "Error" in friends:
        abort(500, "Operation unsuccessful!")
    return friends


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
        birthday,
        time_now_utc(),
        current_user.get_username(),
        current_user.get_username(),
    )
    response = update_user_profile(modify)
    if "Error" not in response:
        return redirect(url_for("profile"))
    abort(500, "Operation unsuccessful!")
