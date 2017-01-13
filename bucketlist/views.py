from . import app
from .model import db

db.create_all()


@app.route("/")
def main():
    return "Wassuh ! :) This is an API yoh "


@app.route("/auth/login", methods=["POST"])
def login():
    pass


@app.route("/auth/register", methods=["POST"])
def register():
    pass


@app.route("/bucketlists", methods=["GET"])
def show_bucketlist():
    pass


@app.route("/bucketlists/<id>", methods=["GET"])
def show_bucketlists():
    pass


@app.route("/bucketlists/<id>", methods=["PUT"])
def update_bucketlist():
    pass


@app.route("/bucketlists/<id>", methods=["DELETE"])
def create_bucketlist():
    pass


@app.route("/bucketlists/<id>/items/", methods=["POST"])
def create_new_item():
    pass


@app.route("/bucketlists/<id>/items/<item_id>", methods=["PUT"])
def update_bucket_list_item():
    pass


@app.route("/bucketlists/<id>/items/<item_id>", methods=["DELETE"])
def delete_bucket_list_item():
    pass

