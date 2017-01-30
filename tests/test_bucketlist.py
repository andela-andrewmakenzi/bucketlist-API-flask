from datetime import datetime
import unittest
from flask import json
from .test_base import BaseTestCase
from bucketlist.models import db, User, Bucketlist, Items


class TestBucketList(BaseTestCase):

    def login_user(self):
        """ We use this to login the user.
        we generate a token we use user whenever we send a request."""
        self.user = db.session.query(User).filter_by(username="admin").first()
        # simulate login
        self.token = self.user.generate_auth_token().decode("utf-8")

    def create_bucketlist(self):
        self.new_bucketlist = Bucketlist(
            name="testbucketlist",
            date_created=datetime.now(),
            created_by=self.user.id,
            date_modified=datetime.now())
        db.session.add(self.new_bucketlist)
        db.session.commit()

    def create_bucketlist_item(self):
        self.new_item = Items(
            name="cook something",
            date_created=datetime.now(),
            bucketlistid=1,
            date_modified=datetime.now())
        db.session.add(self.new_item)
        db.session.commit()

    def create_user(self):
        new_user = User(username="testuser", password="testuser")
        db.session.add(new_user)
        db.session.commit()
        self.new_user = db.session.query(User).filter_by(username="testuser").first()
        self.token = new_user.generate_auth_token().decode("utf-8")
        """we use this new user when we are going to be testing if a user can do
        something to a bucketlist that does not belong to them"""

    def test_access_route_invalid_token(self):
        self.login_user()
        self.token = ""
        bucketname = "games to buy"
        response1 = self.client.post("/bucketlists", data=json.dumps(
            {"name": bucketname}),
            headers={"Authorization": "Bearer {}".format(self.token)})
        response2 = self.client.get("/bucketlists", data=json.dumps(
            {"name": bucketname}),
            headers={"Authorization": "Bearer {}".format(self.token)})
        response3 = self.client.put("/bucketlists/<1>", data=json.dumps(
            {"name": bucketname}),
            headers={"Authorization": "Bearer {}".format(self.token)})
        response4 = self.client.delete("/bucketlists/<1>", data=json.dumps(
            {"name": bucketname}),
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response1.status_code, 401)
        self.assertEqual(response2.status_code, 401)
        self.assertEqual(response3.status_code, 401)
        self.assertEqual(response4.status_code, 401)

    def test_create_bucketlist(self):
        self.login_user()
        bucketname = "games to buy"
        response = self.client.post(
            "/bucketlists",
            data=json.dumps({"name": bucketname}),
            headers={"Authorization": "Bearer {}".format(self.token)},
            content_type="application/json")
        # we get this on successful creation
        self.assertEqual(response.status_code, 201)
        # also check if there is bucketlist in the db with that name
        name = db.session.query(Bucketlist).filter_by(name=bucketname).first()
        self.assertTrue(name is not None)

    def test_create_bucketlist_no_bucketlistname(self):
        self.login_user()
        bucketname = ""  # blank and invalid name
        response = self.client.post(
            "/bucketlists", data=json.dumps({"name": bucketname}),
            headers={"Authorization": "Bearer {}".format(self.token)},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_get_bucketlists(self):
        self.login_user()
        self.create_bucketlist()
        response = self.client.get("/bucketlists", headers={
            "Authorization": "Bearer {}".format(self.token)})
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_get_bucketlists_with_id(self):
        self.login_user()
        self.create_bucketlist()
        response = self.client.get("/bucketlists/1", headers={
            "Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_get_bucketlists_invalid_id(self):
        # invalid bucketlist id, bucketlist that does not exist
        self.login_user()
        response = self.client.get("/bucketlists/<1>", headers={
            "Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        # test we return error json containing error message
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_get_bucketlist_unauthorized(self):
        # when  they try to access a resource that is not theirs
        self.login_user()
        # create the only bucket list in the system, it belongs to admin id 1
        self.create_bucketlist()
        """ the bucketlist belongs to member one, i.e admin
        created another user and attempt to access the bucketlist """
        self.create_user()
        # try to gain access with thier token to admins bucketlist
        response = self.client.get("/bucketlists/1", headers={
            "Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_update_bucketlist(self):
        self.login_user()
        self.create_bucketlist()
        response = self.client.put("/bucketlists/1", data=json.dumps(
            {"name": "newname"}),
            headers={"Authorization": "Bearer {}".format(self.token)},
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # we need to check that indeed the name was changed
        r = db.session.query(Bucketlist).filter_by(id=1).first()
        self.assertTrue(r.name == "newname")

    def test_update_bucketlist_invalid_id(self):
        self.login_user()
        # we dont have any bucketlist in the system
        response = self.client.put(
            "/bucketlists/1", data=json.dumps({"name": "newname"}),
            headers={"Authorization": "Bearer {}".format(self.token)},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_update_bucket_unauthorized(self):
        # when a user tries to get another users bucketlist
        self.login_user()
        self.create_bucketlist()
        self.create_user()  # the new user who should not have access to this bucketlist
        response = self.client.put("/bucketlists/1", data=json.dumps(
            {"name": "newname"}), headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_update_bucketlist_wrong_parameters(self):
        self.login_user()
        self.create_bucketlist()
        # pass non existing parameter in json body before update
        response = self.client.put(
            "/bucketlists/1",
            data=json.dumps({"sajdkbasjkd": "newname"}),
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_delete_bucketlist(self):
        self.login_user()
        self.create_bucketlist()
        response = self.client.delete(
            "/bucketlists/1",
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 200)
        r = db.session.query(Bucketlist).filter_by(name="testbucketlist").first()
        self.assertTrue(r is None)

    def test_delete_bucketlist_invalid_id(self):
        self.login_user()
        # there is no bucketlist in the system
        response = self.client.delete(
            "/bucketlists/1",
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_delete_bucketlist_unauthorized(self):
        # when a user tries to delete another users bucketlist
        self.login_user()
        self.create_bucketlist()
        # the new user should not have access to the bucketlist
        self.create_user()
        response = self.client.delete(
            "/bucketlists/1",
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_create_new_item_bucketlist(self):
        self.login_user()
        self.create_bucketlist()
        # test if we can created a new item in the bucketlist created above
        response = self.client.post(
            "/bucketlists/1/items",
            data=json.dumps(
                {"name": "do this"}
                ),
            headers={"Authorization": "Bearer {}".format(self.token)},
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        bucketlist = db.session.query(
            Bucketlist).filter_by(name="testbucketlist").first()
        self.assertTrue(bucketlist.items[0].name == "do this")

    def test_create_bucketlist_item_no_name(self):
        self.login_user()
        self.create_bucketlist()
        # test if we can created a new item in the bucketlist created above
        response = self.client.post("/bucketlists/1/items", data=json.dumps(
            {"name": "", "date_created": "asd", "bucketlist_id": 1}),
            headers={"Authorization": "Bearer {}".format(self.token)},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_update_item_bucketlist(self):
        self.login_user()
        self.create_bucketlist()
        self.create_bucketlist_item()
        response = self.client.put("/bucketlists/1/items/1", data=json.dumps(
            {
                "name": "do this",
                "bucketlist_id": 1
            }), content_type="application/json",
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist_item_invalid_id(self):
        self.login_user()
        self.create_bucketlist()
        # there is no item to delete in database attempting to delete item id 1
        response = self.client.put(
            "/bucketlists/1/items/1",
            data=json.dumps({
                "name": "do this", "date_created": "asd", "bucketlist_id": 1
                }), content_type="application/json",
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))

    def test_delete_item_bucketlist(self):
        self.login_user()
        self.create_bucketlist()
        self.create_bucketlist_item()
        response = self.client.delete(
            "/bucketlists/1/items/1",
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 200)
        item = db.session.query(Items).get(1)
        self.assertTrue(item is None)

    def test_delete_bucketlist_item_invalid_id(self):
        self.login_user()
        self.create_bucketlist()
        # no item to delete in database
        response = self.client.delete(
            "/bucketlists/1/items/1",
            headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data) == "json"))


if __name__ == "__main__":
    unittest.main()
