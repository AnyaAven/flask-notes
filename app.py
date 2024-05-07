
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

    form = CSRFProtectForm()
    # TODO: put stuff in index.jinja
    return render_template("index.jinja", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission.
        - Checks if username is unique in the DB
    """

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # check if username is unique in DB
        check_valid_username = name.validate_username

        # TODO: question: how can we write this without duplicating what's in the else?
        if (check_valid_username is False):
            flash(f"Sorry, username has already been taken.")
            return render_template("register.jinja", form=form)

        # adding new user into db
        # User.register method is hashing the password
        user = User.register(name, pwd)
        db.session.add(user)
        db.session.commit()

        # putting the user_id into the session so that the we can remember who is logged in
        # browser is stateless
        session["user_id"] = user.id

        # on successful login, redirect to secret page (authenticated)
        return redirect("/secret")

    else:
        return render_template("register.jinja", form=form)
