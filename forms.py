from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


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
        ]  # FIXME: add a minimum length
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


class NoteForm(FlaskForm):
    """Form for adding a note to a user."""

    title = StringField(
        "Title",
        validators=[
            InputRequired(),
            Length(max=100, message="Limit is 100 characters"),
        ]
    )

    content = TextAreaField(
        "Content",
        validators=[
            InputRequired(),
        ]
    )



class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
