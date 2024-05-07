
import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///hashing_login")
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

app.config["SECRET_KEY"] = "abc123"

app.app_context().push()
db.create_all()

toolbar = DebugToolbarExtension(app)

# FIXME: add validation error on username route
# EX:
#def validate_username(self, username):
#    user = User.query.filter_by(username=username.data).first()
#    if user:
#        raise ValidationError('That username is taken. Please choose
#        another.')
