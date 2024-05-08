
import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm

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

SESSION_KEY = "username"

@app.get("/")
def homepage():
    """Show homepage with links to site areas."""

    return redirect("/register")

################################################################################
# USER REGISTRATION

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission.
        - Checks if username is unique in the DB
        - Creates new user if all validation checks pass
    """

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # Check if username and email is valid
        errs = False
        if not User.is_valid_username(name):
            form.username.errors = ["Username taken"]
            errs = True

        if User.is_email_taken(email):
            form.email.errors = ["Email taken"]
            errs = True

        if errs:
            return render_template("register.jinja", form=form)

        # adding new user into db
        # User.register method is hashing the password
        user = User.register(
            username=name,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        db.session.add(user)
        db.session.commit()

        # putting the username into the session so that the we can remember who is logged in
        # browser is stateless
        session[SESSION_KEY] = user.username

        flash(f"Added {user.full_name}")

        # on successful login, redirect to secret page (authenticated)
        return redirect(f"/users/{name}")

    else:
        return render_template("register.jinja", form=form)

################################################################################
# USER LOGIN / LOGOUT

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # calling authenticate method on the class on the user
        # authenticate will return a user or None
        user = User.authenticate(name, pwd)

        if user:
            session[SESSION_KEY] = user.username  # keep logged in
            return redirect(f"/users/{name}")

        else:
            form.username.errors = ["Incorrect name/password"]

    return render_template("login.jinja", form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()
    # TODO: add a werkzeug things for unauthorized users

    if form.validate_on_submit():

        session.pop(SESSION_KEY, None)

    return redirect("/")

################################################################################
# USER INFO

@app.get("/users/<username>")
def display_user(username):
    """Displays user information for the logged in user (username, first name
    last name, email)

    Checks for user authorization to view user page. Else redirects to user's
    own page.
    """

    if SESSION_KEY not in session:
        flash("You must be logged in to view!")

        return redirect("/login")

    if session[SESSION_KEY] != username:

        flash(f"You don't have authorization to view {username}.")
        return redirect(f"/users/{session[SESSION_KEY]}")

    # don't need to query database before we check everything above
    user = db.get_or_404(User, username)
    return render_template("user_info.jinja", user=user)

################################################################################
# NOTES


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """ Add note to user """

    if SESSION_KEY not in session or session[SESSION_KEY] != username:
        flash("Not allowed.") # FIXME: change the flash

        return redirect("/login")

    form = NoteForm()
    user = db.get_or_404(User, username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(
            title=title,
            content=content,
            owner_username=username,
        )

        db.session.add(note)
        db.session.commit()

        flash(f"Note {title} added!")



    return render_template("note_add.jinja", form=form, username=user.username)
