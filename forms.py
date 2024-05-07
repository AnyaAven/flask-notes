from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from models import db, dbx, User

class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(max=20, message="Limit is 20 characters"),
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(max=100, message="Limit is 100 characters"),
        ]
    )

    email = EmailField(
        "Email",
        validators=[
            InputRequired(),
            Email(),
            Length(max=50, message="Limit is 50 characters"),
        ]
    )

    first_name = StringField(
        "First name",
        validators=[
            InputRequired(),
            Length(max=30, message="Limit is 30 characters"),
        ]
    )

    last_name = StringField(
        "Last name",
        validators=[
            InputRequired(),
            Length(max=30, message="Limit is 30 characters"),
        ]
    )

    def is_valid_username(self, username):
        """Checks if the username exists in the database already."""

        user = db.session.get(User, username)
        if user:
            return False
        return True

    def is_valid_email(self, email):
        """Checks if the username exists in the database already."""

        user = db.session.get(User, email)
        if user:
            return False
        return True


# FIXME: LoginForm was copied from hash lecture

class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired()]  # FIXME: add the correct validators
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]  # FIXME: add the correct validators
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
