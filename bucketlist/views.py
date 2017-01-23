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
    if not request.json or request.json.get("name") is None or request.json.get("name") == "":
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
    ls = []
    # filter only the ones belonging to the user
    bl = db.session.query(Bucketlist).filter_by(created_by=g.user.id).all()
    if not bl:
        return jsonify({"message": "user has not created any items yet"}), 401
    for item in bl:
        ls.append(item.returnthis())
    return jsonify(ls), 200


@app.route("/bucketlists/<itemid>", methods=["GET"])
@auth.login_required
def get_bucket(itemid):
    """ return the certain bucketlist for user """
    ls = []
    bl = db.session.query(Bucketlist).get(itemid)
    if not bl:
        return jsonify({"message": "No item with that id"}), 401
    if not bl.created_by == g.user.id:
        return jsonify({
            "message": "That item does not belong to you {} {}".format(type(
                bl.created_by), type(g.user.id))}), 401
    ls.append(bl.returnthis())
    return jsonify(ls), 200


@app.route("/bucketlists/<id>", methods=["PUT"])
@auth.login_required
def update_bucketlist(id):
    if not request.json or request.json.get("name") is None or request.json.get("name") == "":
        return jsonify({"message": "you need to supply new edits in json"}), 401
    bl = db.session.query(Bucketlist).filter_by(id=id).first()
    if not bl:
        return jsonify({"message": "The item you request does not exist"}), 401
    if not bl.created_by == g.user.id:
        return jsonify({"message": "You don't have permission to modify this item"}), 401
    bl.name = request.json.get("name")
    db.session.commit()
    return jsonify({"message": "successful update"}), 200


@app.route("/bucketlists/<id>", methods=["DELETE"])
@auth.login_required
def delete_bucketlist(id):
    bl = db.session.query(Bucketlist).filter_by(id=id).first()
    if not bl:
        return jsonify({"message": "The item you request does not exist"}), 401
    if not bl.created_by == g.user.id:
        return jsonify({"message": "You don't have permission to modify this item"}), 401
    db.session.delete(bl)
    db.session.commit()
    return jsonify({"message": "Deleted bucketlist"}), 200


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
