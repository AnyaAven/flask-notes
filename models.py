from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
dbx = db.session.execute

bcrypt = Bcrypt()


class User(db.Model):
    """ Site user """

    __tablename__ = "users"

    username = db.mapped_column(
        db.String(20),
        unique=True,
        primary_key=True,
    )

    hashed_password = db.mapped_column(
        db.String(100),
        nullable=False,
    )

    email = db.mapped_column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    first_name = db.mapped_column(
        db.String(30),
        nullable=False,
    )

    last_name = db.mapped_column(
        db.String(30),
        nullable=False,
    )

    # Note: the @property function can only take 'self'
    @property
    def full_name(self):
        """returns first and last name"""
        return (f"{self.first_name} {self.last_name}")

    # start_register
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user
        and hash the password, username, email, first name, and last name
        Return user."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        # FIXME: this is where to authenticate all the info
        # raise error and catch the error in the route
        # if error, show errors in the route

        # return instance of user w/username and hashed pwd
        return cls(
            username=username,
            hashed_password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        # FIXME: db.session.get (just look in session, don't have to re-query the db - faster)
        q = (db.select(cls).filter_by(username=username))
        u = dbx(q).scalar_one_or_none()

        # can refactor "u"to user
        if u and bcrypt.check_password_hash(u.hashed_password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate

    @classmethod
    def is_valid_username(cls, username):
        """Checks if the username exists in the database already."""
        # FIXME: when fetching a primary key, use session.get
        # FIXME: use select/dbx instead of .query
        user = db.session.query(cls).filter(cls.username == username).first()

        # FIXME: can just return user (bc .first() returns record or None )
        if user:
            return False
        return True

    # FIXME: rename the fn name
    # this rule is intrinsic to the form
    # if validating email/username is part of the form, we can have this on the form
    # can put the actual logic of how the check is done can be put in the model
    @classmethod
    def is_valid_email(cls, email):
        """Checks if the email exists in the database already."""

        # FIXME: when not fetching primary key, use .where (to match SQL)
        # FIXME: use select/dbx instead of .query
        user = db.select(cls).where(cls.email == email).first()
        # user = db.session.query(cls).filter(cls.email == email).first()

        # FIXME: can just return user (bc .first() returns record or None )

        if user:
            return False
        return True
