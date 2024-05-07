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


