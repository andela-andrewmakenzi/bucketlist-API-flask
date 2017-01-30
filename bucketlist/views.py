from datetime import datetime
from flask import request, jsonify, g, json
from flask_httpauth import HTTPTokenAuth
from . import app
from .models import db
from .models import User, Bucketlist, Items


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
    """ This function logs the user in.
    checks for supplied parameters against db
    generates token and sends to the user if valid user"""
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
    """ This function registers a new user.
    checks credentials provided against existing ones
    makes sure every user is unique
    sends auth token to the user"""
    if not request.json:
        return jsonify({"message": "Expected username and password sent via JSON"}), 400
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Requires username and password to be provided"}), 401
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        return jsonify({"message": "Cannot created user, already exists"}), 400
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()
    token = new_user.generate_auth_token()
    # return json.dumps({"token": str(token)}), 201
    return json.dumps({"token": token.decode('utf-8')}), 201


@app.route("/bucketlists", methods=["POST"])
@auth.login_required
def create_bucketlist():
    """ This function creates a new bucketlist.
    make sure the user has a valid token before creating"""
    # we are logged in, we have access to g, where we have a field, g.userid
    if not request.json or request.json.get("name") is None or request.json.get("name") == "":
        return jsonify({
            "message": "You are require to supply the name of the bucketlist"
            }), 400
    bucketlist = db.session.query(Bucketlist).filter_by(created_by=g.user.id, name=request.json.get("name")).first()
    if bucketlist:
        return jsonify({
            "message": "The item you are trying to create already exists"}), 400
    bucketlist = Bucketlist(name=request.json.get("name"), date_created=datetime.now(), created_by=g.user.id, date_modified=datetime.now())
    db.session.add(bucketlist)
    db.session.commit()
    return jsonify({"message": "Added bucketlist for use"}), 201


@app.route("/bucketlists", methods=["GET"])
@auth.login_required
def list_created_bucketlist():
    """ Return the bucketlists belonging to the user.
    we determine the user from the supplied token """
    search_name = False
    search_limit = False
    if request.args.get("q"):
        search_name = True
    if request.args.get("limit"):
        search_limit = True
    if search_name and search_limit:
        bucketlist = db.session.query(Bucketlist).filter_by(created_by=g.user.id).filter(Bucketlist.name.like("%{}%".format(request.args.get("q")))).limit(request.args.get("limit")).all()
    elif search_name:
        bucketlist = db.session.query(Bucketlist).filter(Bucketlist.created_by == g.user.id, Bucketlist.name.like('%{}%'.format(request.args.get("q")))).all()
    elif search_limit:
        bucketlist = db.session.query(Bucketlist).filter_by(created_by=g.user.id).limit(request.args.get("limit")).all()
    else:
        bucketlist = db.session.query(Bucketlist).filter_by(created_by=g.user.id).all()
    ls = []
    if not bucketlist:
        if not search_name:
            return jsonify(
                {"message": "Need to supply name of item you are looking for"}
                ), 400
        else:
            return jsonify(
                {"message": "No item with that name belonging to user"}
                ), 401
    for item in bucketlist:
        ls.append(item.returnthis())
    return jsonify(ls), 200


@app.route("/bucketlists/<itemid>", methods=["GET"])
@auth.login_required
def get_bucket(itemid):
    """ Return the certain bucketlist for user. """
    ls = []
    bucketlist = db.session.query(Bucketlist).get(itemid)
    if not bucketlist:
        return jsonify({"message": "No item with that id"}), 400
    if not bucketlist.created_by == g.user.id:
        return jsonify({
            "message": "That item does not belong to you "}), 401
    ls.append(bucketlist.returnthis())
    return jsonify(ls), 200


@app.route("/bucketlists/<id>", methods=["PUT"])
@auth.login_required
def update_bucketlist(id):
    """ Update name or done status of a bucketlist """
    if not request.json or request.json.get("name") is None or request.json.get("name") == "":
        return jsonify({"message": "you need to supply new edits in json"}), 400
    bucketlist = db.session.query(Bucketlist).filter_by(id=id).first()
    if not bucketlist:
        return jsonify({"message": "The item you request does not exist"}), 400
    if not bucketlist.created_by == g.user.id:
        return jsonify({"message": "You don't have permission to modify this item"}), 401
    bucketlist.name = request.json.get("name")
    bucketlist.date_modified = datetime.now()
    db.session.commit()
    return jsonify({"message": "successful update"}), 200


@app.route("/bucketlists/<id>", methods=["DELETE"])
@auth.login_required
def delete_bucketlist(id):
    bucketlist = db.session.query(Bucketlist).filter_by(id=id).first()
    if not bucketlist:
        return jsonify({"message": "The item you request does not exist"}), 400
    if not bucketlist.created_by == g.user.id:
        return jsonify(
            {"message": "You don't have permission to modify this item"}), 400
    db.session.delete(bucketlist)
    db.session.commit()
    return jsonify({"message": "Deleted bucketlist"}), 200


@app.route("/bucketlists/<id>/items", methods=["POST"])
@auth.login_required
def create_new_item(id):
    """ This function created a new item in the bucketlist."""
    if not request.json:
        return jsonify(
            {"message": "you need to supply name of new item as JSON"}), 400
    item_name = request.json.get("name")
    if item_name is None or item_name == "":
        return jsonify(
            {"message": "you need to supply name of new item as JSON"}
            ), 400
    bucketlist = db.session.query(Items).filter_by(name=item_name).first()
    if bucketlist:
        return jsonify({"message": "User has already created that item"}), 400
    bucketlist = db.session.query(Bucketlist).filter_by(id=id).first()
    if not bucketlist:
        return jsonify({"message": "Bucketlist does not exist"}), 400
    new_item = Items(
        name=item_name,
        date_created=datetime.now(),
        date_modified=datetime.now(),
        bucketlistid=id
        )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Successfuly created item"}), 200


@app.route("/bucketlists/<id>/items/<item_id>", methods=["PUT"])
@auth.login_required
def update_bucket_list_item(id, item_id):
    """ Update name and done status of a bucketlist list item"""
    if not request.json:
        return jsonify(
            {"message": "you need to supply new name as JSON"}), 400
    item_name = request.json.get("name")
    done = request.json.get("done")
    if item_name is None or item_name == "":
        return jsonify({"message": "you need to supply new name as JSON"}), 400
    bucketlist = db.session.query(Bucketlist).filter_by(id=id).first()
    if not bucketlist:
        return jsonify({
            "message": "The bucketlist does not exist, it was probably deleted"
            }), 400
    buckettlistitem = db.session.query(Items).filter_by(id=item_id).first()
    if not buckettlistitem:
        return jsonify(
            {"message": "Item does not exist, no item with that id"}
            ), 400
    if buckettlistitem.name == item_name:
        return jsonify(
            {"message": "No change to be recorded, set a new value for whatever you want to update"}
            ), 400
    if done:
        if done.lower() == "true":
            buckettlistitem.done = True
        else:
            buckettlistitem.done = False
    buckettlistitem.name = item_name
    buckettlistitem.date_modified = datetime.now()
    db.session.commit()
    return jsonify({"message": "Successfully updated item"}), 200


@app.route("/bucketlists/<id>/items/<item_id>", methods=["DELETE"])
@auth.login_required
def delete_bucket_list_item(id, item_id):
    bucketlist = db.session.query(Bucketlist).filter_by(id=id).first()
    if not bucketlist:
        return jsonify(
            {"message": "Bucketlist does not exist, cannot delete"}
            ), 400
    if not bucketlist.created_by == g.user.id:
        return jsonify({
            "message": "You dont own the bucketlist, cannot delete"}), 401
    bucketlistitem = db.session.query(Items).filter_by(id=item_id).first()
    if not bucketlistitem:
        return jsonify({"message": "User does not have that item, cannot delete"}), 400
    db.session.delete(bucketlistitem)
    db.session.commit()
    return jsonify({"message": "Successfully deleted item"}), 200


@app.errorhandler(500)
def handle500(e):
    db.session.rollback()
    return jsonify({"messgae": "We are experiencing technical issues right now, please be patient"}), 500


@app.errorhandler(404)
def handle404(e):
    return jsonify({"message": "Invalid endpoint"}), 404
