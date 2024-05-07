from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
dbx = db.session.execute

bcrypt = Bcrypt()
