from . import app
from .models import db
from flask import request, jsonify, g, json
from .models import User, Bucketlist, Items
from flask_httpauth import HTTPTokenAuth
import datetime
from datetime import datetime

auth = HTTPTokenAuth(scheme="Bearer")
db.create_all()


@auth.verify_token
def verify_auth_token(token):
    """ login_required is going to call verify token since this is an instance
    of HTTPTokenAuth verify_token is going to look at the value in the
    Authorization header which we set to Authorization : Bearer <key> according
    to OAuth 2 standards, parse it for us and return the token part inside of
    token parameter
    """
    # they supply a token in place of the username in HTTPBasicAuthentication
    if not token:
        return False
    userid = User.verify_auth_token(token=token)
    if userid is None:
        return False
    g.user = db.session.query(User).filter_by(id=userid).first()
    return True


@app.route("/auth/login", methods=["POST"])
def login():
    if not request.json:
        return jsonify({"message": "Expected username and password sent via JSON"}), 400
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        """ we expect the username and password passed as json """
        return jsonify({"message": "Requires username and password to be\
         provided"}), 401
    new_user = db.session.query(User).filter_by(username=username).first()
    if not new_user or not new_user.validate_password(password):  # case of invalid credentials
        return jsonify({"message": "Invalid login credentials"}), 401
    # create user and store in db
    token = new_user.generate_auth_token()
    return json.dumps({"token": token.decode("utf-8"), "id": new_user.id}), 200


@app.route("/auth/register", methods=["POST"])
def register():
    if not request.json:
        return jsonify({"message": "Expected username and password sent via JSON"}), 400
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Requires username and password to be provided"}), 401
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        return jsonify({"message": "Cannot created user, already exists"}), 401
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()
    token = new_user.generate_auth_token()
    # return json.dumps({"token": str(token)}), 201
    return json.dumps({"token": token.decode('utf-8')}), 201


@app.route("/bucketlists", methods=["POST"])
@auth.login_required
def create_bucketlist():
    # we are logged in, we have access to g, where we have a field, g.userid
    if not request.json or request.json.get("name") == "":
        return jsonify({
            "message": "You are require to supply the name of the bucketlist"
            }), 401
    bl = Bucketlist(name=request.json.get("name"), date_created=datetime.now(), created_by=g.user.id, date_modified=datetime.now())
    db.session.add(bl)
    db.session.commit()
    return jsonify({"message": "Added bucketlist for use"}), 201


@app.route("/bucketlists", methods=["GET"])
@auth.login_required
def list_created_bucketlist():
    """ return the bucketlists belonging to the user """
    bls = []
    bl = db.session.query(Bucketlist).filter_by(created_by=1).all()
    bls.append(bl)
    return jsonify(bls), 200
    return "done"


@app.route("/bucketlists/<id>", methods=["GET"])
@auth.login_required
def get_bucket(id):
    pass


@app.route("/bucketlists/<id>", methods=["PUT"])
@auth.login_required
def update_bucketlist(id):
    pass


@app.route("/bucketlists/<id>", methods=["DELETE"])
@auth.login_required
def delete_bucketlist(id):
    pass


@app.route("/bucketlists/<id>/items/", methods=["POST"])
@auth.login_required
def create_new_item(id, items):
    pass


@app.route("/bucketlists/<id>/<items>/<item_id>", methods=["PUT"])
@auth.login_required
def update_bucket_list_item(id, items, item_id):
    pass


@app.route("/bucketlists/<id>/<items>/<item_id>", methods=["DELETE"])
@auth.login_required
def delete_bucket_list_item(id, items, item_id):
    pass


@app.errorhandler(500)
def handle500(e):
    db.session.rollback()
    return jsonify({"messgae": "We are experiencing technical issues right now, please be patient"}), 500


@app.errorhandler(404)
def handle404(e):
    return jsonify({"message": ""}), 404
