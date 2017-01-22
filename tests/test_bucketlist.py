from .test_base import BaseTestCase
from bucketlist.models import db, User, Bucketlist
from flask import json
import datetime
import unittest


class TestBucketList(BaseTestCase):

    def login_user(self):
        self.user = db.session.query(User).filter_by(username="admin").first()
        self.token = self.user.generate_auth_token().decode("utf-8")  # simulate login

    def create_bucket(self):
        self.new_bucketlist = Bucketlist(name="testbucketlist", date_created="asd", created_by=self.user.username)

    def test_access_route_invalid_token(self):
        self.login_user()
        self.token = ""
        bucketname = "games to buy"
        response1 = self.client.post("/bucketlists", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(self.token)})
        response2 = self.client.get("/bucketlists", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(self.token)})
        response3 = self.client.put("/bucketlists/<1>", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(self.token)})
        response4 = self.client.delete("/bucketlists/<1>", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response1.status_code, 401)
        self.assertEqual(response2.status_code, 401)
        self.assertEqual(response3.status_code, 401)
        self.assertEqual(response4.status_code, 401)

    def test_create_bucketlist(self):
        self.login_user()
        bucketname = "games to buy"
        response = self.client.post("/bucketlists", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 201)  # we get this on successful creation
        # also check if there is bucketlist in the db with that name
        name = db.session.query(Bucketlist).filter_by(name=bucketname).first()
        self.assertTrue(name is not None)

    def test_create_bucketlist_no_bucketlistname(self):
        self.login_user()
        bucketname = ""  # blank and invalid name
        response = self.client.post("/bucketlists", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)  # must supply a name for the bucketlist

    def test_get_bucketlists(self):
        self.login_user()
        response = self.client.get("/bucketlists", headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data))  # we are going to fetch every single bucketlist that belongs to them

    def test_get_bucketlists_with_id(self):
        self.login_user()
        response = self.client.get("/bucketlists<{}>".format(self.user.id), headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.data) == "json")

    def test_get_bucketlists_invalid_id(self):
        # invalid bucketlist id, bucketlist that does not exist
        self.login_user()
        response = self.client.get("/bucketlists<{}>".format(""), headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(type(json.loads(response.data)))  # test we return json contains error

    def test_get_bucketlist_unauthorized(self):
        # when  they try to access a resource that is not theirs
        self.login_user()
        self.create_bucket()  # the only bucketlist in the systen, belonging to admin
        """ the bucketlist belongs to member one, i.e admin
        created another user and attempt to access the bucketlist """
        new_user = User(username="test", password="test")
        db.session.add(new_user)
        db.session.commit()
        new_user = db.session.query(User).filter_by(username="test").first()
        self.token = new_user.generate_auth_token().decode("utf-8")
        # try to gain access with thier token to admins bucketlist
        response = self.client.get("/bucketlists/1", headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.loads(response.data))

    def test_update_bucketlist(self):
        self.login_user()
        self.create_bucket()
        response = self.client.put("/bucketlists/1", data=json.dumps({"name": "newname"}), headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 200)
        # we need to check that indeed the name was changed
        r = db.session.query(Bucketlist).filter_by(id=1).first()
        self.assertTrue(r.name == "newname")

    def tests_update_bucketlist_invalid_id(self):
        self.login_user()
        # we dont have any bucketlist in the system
        response = self.client.put("/bucketlists/1", headers={"Authorization": "Bearer {}".format(self.token)})
        self.assertEqual(response.status_code, 401)
        self.assertTrue(json.dumps(response.data))

    def test_update_bucket_unauthorized(self):
        pass

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
