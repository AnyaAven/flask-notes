
import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

app.config["SECRET_KEY"] = "abc123"

app.app_context().push()
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """Show homepage with links to site areas."""

    # form = CSRFProtectForm() TODO: where do we need this?

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission.
        - Checks if username is unique in the DB
    """

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # check if username is unique in DB
        # check_valid_username = name.validate_username

        # # TODO: question: how can we write this without duplicating what's in the else?
        # if (check_valid_username is False):
        #     flash(f"Sorry, username has already been taken.")
        #     return render_template("register.jinja", form=form)

        # adding new user into db
        # User.register method is hashing the password
        user = User.register(
            username=name,
            pwd=password,
            email=email,
            fname=first_name,
            lname=last_name,
        )
        db.session.add(user)
        db.session.commit()

        # putting the user_id into the session so that the we can remember who is logged in
        # browser is stateless
        session["username"] = user.username

        # on successful login, redirect to secret page (authenticated)
        return redirect(f"/users/{name}")

    else:
        return render_template("register.jinja", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # calling authenticate method on the class on the user
        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect(f"/users/{name}")

        else:
            form.username.errors = ["Incorrect name/password"]
    # TODO:
    return render_template("login.jinja", form=form)


@app.get("/users/<username>")
def display_user(username):
    """Displays user information for the logged in user (username, first name
    last name, email)"""

    # TODO:
    return render_template("user_info.jinja")
