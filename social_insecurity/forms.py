"""Provides all forms used in the Social Insecurity application.

This file is used to define all forms used in the application.
It is imported by the social_insecurity package.

Example:
    from flask import Flask
    from app.forms import LoginForm

    app = Flask(__name__)

    # Use the form
    form = LoginForm()
    if form.validate_on_submit() and form.login.submit.data:
        username = form.username.data
"""

from datetime import datetime
from typing import cast

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FileField,
    FormField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    validators,
)

# Defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields


class LoginForm(FlaskForm):
    """Provides the login form for the application."""

    username = StringField(
        label="Username",
        render_kw={"placeholder": "Username"},
        validators=[validators.DataRequired(message=("Please enter a valid Username"))],
    )
    password = PasswordField(
        label="Password",
        render_kw={"placeholder": "Password"},
        validators=[validators.DataRequired(message=("Please enter Password"))],
    )
    remember_me = BooleanField(label="Remember me")
    submit1 = SubmitField(label="Sign In")


class RegisterForm(FlaskForm):
    """Provides the registration form for the application."""

    first_name = StringField(
        label="First Name",
        render_kw={"placeholder": "First Name"},
        validators=[validators.DataRequired(message="Please enter your name")],
    )
    last_name = StringField(
        label="Last Name",
        render_kw={"placeholder": "Last Name"},
        validators=[
            validators.DataRequired(message="Please enter your surname"),
        ],
    )
    username = StringField(
        label="Username",
        render_kw={"placeholder": "Username"},
        validators=[
            validators.Length(min=4, max=25, message=("Username must be within 4-25")),
            validators.Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ],
    )
    password = PasswordField(
        label="Password",
        render_kw={"placeholder": "Password"},
        validators=[
            validators.Length(min=8, max=35, message=("Password must be within 8-35")),
        ],
    )
    confirm = PasswordField(
        label="Confirm Password",
        render_kw={"placeholder": "Confirm Password"},
        validators=[
            validators.Length(min=8, max=35),
            validators.EqualTo("password", message="Passwords must match!"),
        ],
    )
    submit2 = SubmitField(label="Sign Up")


class IndexForm(FlaskForm):
    login = cast(LoginForm, FormField(LoginForm))
    register = cast(RegisterForm, FormField(RegisterForm))


class PostForm(FlaskForm):
    """Provides the post form for the application."""

    content = TextAreaField(
        label="New Post",
        render_kw={"placeholder": "What are you thinking about?"},
        validators=[validators.DataRequired(), validators.Length(max=200)],
    )
    image = FileField(label="Image")
    submit = SubmitField(label="Post")


class CommentsForm(FlaskForm):
    """Provides the comment form for the application."""

    comment = TextAreaField(
        label="New Comment",
        render_kw={"placeholder": "What do you have to say?"},
        validators=[
            validators.DataRequired(message="Please enter your message"),
            validators.Length(max=200),
        ],
    )
    submit = SubmitField(label="Comment")


class FriendsForm(FlaskForm):
    """Provides the friend form for the application."""

    username = StringField(
        label="Friend's username",
        render_kw={"placeholder": "Username"},
        validators=[validators.DataRequired(message="Please enter a friends username")],
    )
    submit = SubmitField(label="Add Friend")


class ProfileForm(FlaskForm):
    """Provides the profile form for the application."""

    education = StringField(
        label="Education",
        render_kw={"placeholder": "Highest education"},
        validators=[validators.DataRequired(message="Please enter Highest education")],
    )
    employment = StringField(
        label="Employment",
        render_kw={"placeholder": "Current employment"},
        validators=[validators.DataRequired(message="Please enter Current employment")],
    )
    music = StringField(
        label="Favorite song",
        render_kw={"placeholder": "Favorite song"},
        validators=[validators.DataRequired(message="Please enter Favorite song")],
    )
    movie = StringField(
        label="Favorite movie",
        render_kw={"placeholder": "Favorite movie"},
        validators=[validators.DataRequired(message="Please enter Favorite movie")],
    )
    nationality = StringField(
        label="Nationality",
        render_kw={"placeholder": "Your nationality"},
        validators=[validators.DataRequired(message="Please enter Your nationality")],
    )
    birthday = DateField(
        label="Your Birthday",
        validators=[validators.DataRequired(message="Please enter Your Birthday")],
    )
    submit = SubmitField(label="Update Profile")
