from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from passlib.hash import sha256_crypt

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./bucketlist.db"


db = SQLAlchemy(app)


class Bucketlist(db.Model):

    __tablename__ = "Bucketlist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    data_created = db.Column(db.DateTime, nullable=False)
    data_modified = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(20), nullable=False)
    items = db.relationship("Items", backref="bucket", lazy="dynamic")

    def __init__(self, name, date_created, date_modified, created_by):
        self.name = name
        self.date_created = date_created
        self.date_modified = date_modified
        self.created_by = created_by

    def __repr__():
        return "<{} {} {} {} {} >".format(self.id, self.name, self.date_created, self.date_modified, self.created_by)


class Items(db.Model):

    __tablename__ = "Items"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    dated_created = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, nullable=False, unique=False, default=False)
    bucketlistid = db.Column(db.Integer, db.ForeignKey("Bucketlist.id"), nullable=False, unique=False)

    def __init__(self, name, data_created, date_modified, done):
        self.name = name
        self.date_created = date_created
        self.date_modified = date_modified
        self.done = done

    def __repr__():
        return "<{} {} {} {} {} >".format(self,userid, self.name, self.date_created, self.date_modified, self.done)


class User(db.Model):

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__():
        return "<{} {} {}>".format(self.id, self.username, self.password)

    def validate_password():
        # validate if password supplied is correct
        pass

    def hash_password():
        self.password = sha256_crypt.encrypt(self.password)

    def generate_auth_token():
        # generate authentication token based on the unique userid field
        s = Serializer(app.config['SECRET_KEY'], expires_in=600)
        return s.dumps(self.id)

    @staticmethod
    # this is static as it is called before the user object is created
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'], expires_in=600)
        try:
            # this should return the user id
            userid = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return userid
