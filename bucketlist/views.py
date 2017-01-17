from . import app
from .model import db
from flask import request, jsonify, g
from .model import User
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth()
db.create_all()


@auth.login_required
def verify_token(token, password):
    # they supply a token in place of the username in HTTPBasicAuthentication
    userid = User.verify_auth_token(token)
    if userid is None:
        return jsonify({"message": "Invalid or expired token"}), 401
    g.user_id = userid
    return True


@app.route("/")
def main():
    return jsonify({"message": "This is an API yoh"})


@app.route("/auth/login", methods=["POST"])
def login():
    if not request.json:
        return jsonify({"message": "Expected username and password sent via JSON"}), 400
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        """ we expect the username and password passed as json """
        return jsonify({"message": "Requires username and password to be provided"}), 400
    user = db.query("User").filter_by(username=username).first()
    if not user or not user.validate_password():  # case of invalid credentials
        return jsonify({"message": "Invalid login credentials"}), 401
    token = User.generate_auth_token()
    return jsonify(token), 200


@app.route("/auth/register", methods=["POST"])
def register():
    if not request.json:
        return jsonify({"message": "Expected username and password sent via JSON"}), 400
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Requires username and password to be provided"}), 400
    user = User(username, password)
    user.hash_password()
    db.session.add(user)
    # get the current state of this object in session from db
    db.session.flush() 
    db.session.commit()
    token = User.generate_auth_token()
    return jsonify(token), 200


@app.route("/bucketlists", methods=["GET"])
@auth.login_required
def show_bucketlist():
    pass


@app.route("/bucketlists/<id>", methods=["GET"])
@auth.login_required
def show_bucketlists():
    pass


@app.route("/bucketlists/<id>", methods=["PUT"])
@auth.login_required
def update_bucketlist():
    pass


@app.route("/bucketlists/<id>", methods=["DELETE"])
@auth.login_required
def create_bucketlist():
    pass


@app.route("/bucketlists/<id>/items/", methods=["POST"])
@auth.login_required
def create_new_item():
    pass


@app.route("/bucketlists/<id>/items/<item_id>", methods=["PUT"])
@auth.login_required
def update_bucket_list_item():
    pass


@app.route("/bucketlists/<id>/items/<item_id>", methods=["DELETE"])
@auth.login_required
def delete_bucket_list_item():
    pass


@app.errorhandler(500)
def handle500():
    db.session.rollback()
    return jsonify({"messgae": "We are experiencing technical issues right now, please be patient"}), 500


@app.errorhandler(404)
def handle404():
    return jsonify({"message": "Arent you lost"})
