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
        db.Identity(),
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

    # start_register
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed)

    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        q = (db.select(cls).filter_by(username=username))
        u = dbx(q).scalar_one_or_none()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate
