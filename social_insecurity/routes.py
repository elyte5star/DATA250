"""Provides all routes for the Social Insecurity application.

This file contains the routes for the application. It is imported by the social_insecurity package.
It also contains the SQL queries used for communicating with the database.
"""

from pathlib import Path  # noqa: I001
from werkzeug.utils import secure_filename
from flask import current_app as app
from flask import redirect, render_template, send_from_directory, url_for
from flask_login import login_required, current_user, logout_user, fresh_login_required
from social_insecurity.forms import (
    CommentsForm,
    FriendsForm,
    IndexForm,
    PostForm,
    ProfileForm,
)
from social_insecurity.service.user import (
    _login,
    _create_user,
    _get_user_posts,
    _create_post,
    _create_comment,
    _get_user_post,
    _get_user_comments,
    _create_user_friend,
    _get_user_friends,
    _update_user_profile,
    _get_user,
    upload_file,
)


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    """Provides the index page for the application.
    It reads the composite IndexForm and based on which form was submitted,
    it either logs the user in or registers a new user.
    If no form was submitted, it simply renders the index page.
    """
    if current_user.is_authenticated:
        return redirect(url_for("stream"))

    index_form = IndexForm()
    login_form = index_form.login
    register_form = index_form.register

    if login_form.submit1.data and login_form.validate_on_submit():
        return _login(
            login_form.username.data,
            login_form.password.data,
            login_form.remember_me.data,
        )
    elif register_form.submit2.data and register_form.validate_on_submit():
        return _create_user(
            register_form.username.data,
            register_form.first_name.data,
            register_form.last_name.data,
            register_form.password.data,
        )
    return render_template("index.html.j2", title="Welcome", form=index_form)


@app.route("/stream", methods=["GET", "POST"])
@login_required
def stream():
    """Provides the stream page for the application.
    If a form was submitted, it reads the form data and inserts a new post into the database.
    Otherwise, it reads the username from the URL and displays all posts from the user and their friends.
    """
    post_form = PostForm()
    if post_form.submit.data and post_form.validate_on_submit():
        if post_form.image.data:
            upload_file(post_form.image.data)
        return _create_post(
            current_user, post_form.content.data, post_form.image.data.filename
        )
    return render_template(
        "stream.html.j2",
        title="Stream",
        username=current_user.get_username(),
        form=post_form,
        posts=_get_user_posts(current_user.get_id()),
    )


@app.route("/comments/<string:username>/<int:post_id>", methods=["GET", "POST"])
@login_required
def comments(username: str, post_id: int):
    """Provides the comments page for the application.
    If a form was submitted, it reads the form data
    and inserts a new comment into the database.
    Otherwise, it reads the username
    and post id from the URL and displays all comments for the post.
    """
    # manage access control
    if current_user.get_username() != username:
        return app.login_manager.unauthorized()

    comments_form = CommentsForm()
    if comments_form.submit.data and comments_form.validate_on_submit():
        _create_comment(current_user, post_id, comments_form.comment.data)
    return render_template(
        "comments.html.j2",
        title="Comments",
        username=current_user.get_username(),
        form=comments_form,
        post=_get_user_post(post_id),
        comments=_get_user_comments(post_id),
    )


@app.route("/friends", methods=["GET", "POST"])
@login_required
@fresh_login_required
def friends():
    """Provides the friends page for the application.
    If a form was submitted, it reads the form data
    and inserts a new friend into the database.
    Otherwise, it reads the username from the URL
    and displays all friends of the user.
    """
    friends_form = FriendsForm()
    if friends_form.validate_on_submit():
        _create_user_friend(current_user, friends_form.username.data)

    friends = _get_user_friends(current_user.get_id())
    return render_template(
        "friends.html.j2",
        title="Friends",
        username=current_user.get_username(),
        friends=friends,
        form=friends_form,
    )


@app.route("/profile", methods=["GET", "POST"])
@login_required
@fresh_login_required
def profile():
    """Provides the profile page for the application.
    If a form was submitted, it reads the form data
    and updates the user's profile in the database.
    Otherwise, it reads the username from the URL
    and displays the user's profile.
    """
    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        return _update_user_profile(
            profile_form.education.data,
            profile_form.employment.data,
            profile_form.music.data,
            profile_form.movie.data,
            profile_form.nationality.data,
            profile_form.birthday.data,
            current_user,
        )
    return render_template(
        "profile.html.j2",
        title="Profile",
        username=current_user.get_username(),
        user=_get_user(current_user.get_username()),
        form=profile_form,
    )


@app.route("/uploads/<string:filename>")
@login_required
def uploads(filename):
    """Provides an endpoint for serving uploaded files."""
    return send_from_directory(
        Path(app.instance_path) / app.config["UPLOADS_FOLDER_PATH"], filename
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
