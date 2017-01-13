from flask_sqlalchemy import SQLAlchemy
from . import app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./bucketlist.db"


db = SQLAlchemy(app)


# class User(db.Model):
#     pass


# class Bucketlist(db.Model):
#     pass
