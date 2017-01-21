import unittest
from bucketlist import app
from bucketlist.model import db, User, Bucketlist
from flask import json


class TestBucketList(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../testbucketlist.db"
        app.config["TESTING"] = True
        db.drop_all()
        db.create_all()  # create all tables based 
        new_user = User("admin", "admin")
        db.session.add(new_user)
        db.session.commit()  # user is now in our database
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()  # will call session remove
        db.drop_all()

    def test_access_invalid_endpoint(self):
        response = self.client.post("/")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(json.loads(response.data))  # if we don't generate JSON here, we will error

    def test_login(self):
        # attempt to create new valid user and login
        credentials = {"username": "admin", "password": "admin"}
        response = self.client.post("/auth/login", data=json.dumps(credentials), content_type="application/json")
        self.assertTrue(response.status_code, 200)

    def test_login_no_username(self):
        credentials = {"username": "", "password": "admin"}
        response = self.client.post("/auth/login", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_login_no_password(self):
        credentials = {"username": "admin", "password": ""}
        response = self.client.post("/auth/login", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_login_no_credentials(self):
        credentials = {"username": "", "password": ""}
        response = self.client.post("/auth/login", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_login_no_required_field(self):
        credentials = {"username": "andrew"}
        response = self.client.post("/auth/login", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_register_user(self):
        credentials = {"username": "andrew", "password": "andrew"}  # this should be the second user we are registering
        response = self.client.post("/auth/register", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_register_user_no_username(self):
        credentials = {"username": "", "password": "andrew"}  # this should be the second user we are registering
        response = self.client.post("/auth/register", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_register_user_pass_no_password(self):
        credentials = {"username": "andrew", "password": ""}  # this should be the second user we are registering
        response = self.client.post("/auth/register", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))

    def test_register_user_pass_no_username_or_password(self):
        credentials = {"username": "", "password": ""}  # this should be the second user we are registering
        response = self.client.post("/auth/register", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_register_with_existing_username(self):
        credentials = {"username": "admin", "password": "admin"}  # this should be the second user we are registering
        response = self.client.post("/auth/register", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_register_user_required_field_not_passed(self):
        # if the dev forgets to add fields in required format as API requires
        credentials = {"username": "admin"}  # this should be the second user we are registering
        response = self.client.post("/auth/register", data=json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))  # test return JSON err msg

    def test_create_bucketlist(self):
        user = db.session.query(User).filter_by(username="admin").first()
        # token = str(user.generate_auth_token())  # simulate login
        token = user.generate_auth_token().decode('utf-8')
        print("{} {}".format(token, type(token)))
        bucketname = "games to buy"
        response = self.client.post("/bucketlists", data=json.dumps({"name": bucketname}), headers="Authorization : Bearer {}".format(token))
        self.assertEqual(response.status_code, 201)  # we get this on successful creation
        # also check if there is bucketlist in the db with that name
        name = db.session.query(Bucketlist).filter_by(name=bucketname).first()
        self.assertTrue(name is not None)

    def test_create_bucketlist_no_bucketlistname(self):
        user = db.session.query(User).filter_by(username="admin").first()
        token = user.generate_auth_token().decode("utf-8")  # simulate login
        bucketname = ""  # blank and invalid name
        response = self.client.post("/bucketlists", data=json.dumps({"name": bucketname}), headers="Authorization : Bearer {}".format(token))
        self.assertEqual(response.status_code, 401)  # must supply a name for the bucketlist

    # def test_get_bucketlists(self):
    #     pass

    # def test_get_bucketlists_invalid_id(self):
    #     pass

    # def test_get_bucketlist_unauthorized(self):
    #     pass

    # def tests_update_bucketlist(self):
    #     pass

    # def test_update_bucketlist_invalid_id(self):
    #     pass

    # def test_update_bucket_unauthorized(self):
    #     pass

    # def test_delete_bucketlist(self):
    #     pass

    # def test_delete_bucketlist_invalid_id(self):
    #     pass

    # def test_delete_bucketlist_unauthorized(self):
    #     pass

    # def test_create_new_item_bucketlist(self):
    #     pass

    # def test_create_bucketlist_item_no_name(self):
    #     pass

    # def test_create_bucketlist_item_unauthorized(self):
    #     pass

    # def test_update_item_bucketlist(self):
    #     pass

    # def test_update_bucketlist_item_invalid_id(self):
    #     pass

    # def test_update_bucketlist_unauthorized(self):
    #     pass

    # def test_delete_item_bucketlist(self):
    #     pass

    # def test_delete_bucketlist_item_invalid_id(self):
    #     pass

    # def test_delete_bucketlist_item_unauthorized(self):
    #     pass

    # def test_access_expired_token():
    #     pass

    # def test_access_invalid_token():
    #     pass


if __name__ == "__main__":
    unittest.main()
