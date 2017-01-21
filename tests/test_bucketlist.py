from .test_base import BaseTestCase
from bucketlist.model import db, User, Bucketlist
from flask import json


class TestBucketList(BaseTestCase):

    def login_user():
        user = db.session.query(User).filter_by(username="admin").first()
        token = user.generate_auth_token().decode("utf-8")  # simulate login       

    def test_create_bucketlist(self):
        self.login_user()
        bucketname = "games to buy"
        response = self.client.post("/bucketlists", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(token)})
        self.assertEqual(response.status_code, 201)  # we get this on successful creation
        # also check if there is bucketlist in the db with that name
        name = db.session.query(Bucketlist).filter_by(name=bucketname).first()
        self.assertTrue(name is not None)

    def test_create_bucketlist_no_bucketlistname(self):
        self.login_user()
        bucketname = ""  # blank and invalid name
        response = self.client.post("/bucketlists", data=json.dumps({"name": bucketname}), headers={"Authorization": "Bearer {}".format(token)})
        self.assertEqual(response.status_code, 401)  # must supply a name for the bucketlist

    def test_get_bucketlists(self):
        self.login_user()
        response = self.client.get("/bucketlists", headers={"Authorization": "Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.data) == "json")

    def test_get_bucketlists_with_id(self):
        self.login_user()
        response = self.client.get("/bucketlists<{}>".format(user.id), headers={"Authorization": "Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.data) == "json")

    def test_get_bucketlists_invalid_id(self):
        self.login_user()
        response = self.client.get("/bucketlists<{}>".format(user.id), headers={"Authorization": "Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.data) == "json")

    def test_get_bucketlist_unauthorized(self):
        pass

    def tests_update_bucketlist(self):
        pass

    def test_update_bucketlist_invalid_id(self):
        pass

    def test_update_bucket_unauthorized(self):
        pass

    def test_delete_bucketlist(self):
        pass

    def test_delete_bucketlist_invalid_id(self):
        pass

    def test_delete_bucketlist_unauthorized(self):
        pass

    def test_create_new_item_bucketlist(self):
        pass

    def test_create_bucketlist_item_no_name(self):
        pass

    def test_create_bucketlist_item_unauthorized(self):
        pass

    def test_update_item_bucketlist(self):
        pass

    def test_update_bucketlist_item_invalid_id(self):
        pass

    def test_update_bucketlist_unauthorized(self):
        pass

    def test_delete_item_bucketlist(self):
        pass

    def test_delete_bucketlist_item_invalid_id(self):
        pass

    def test_delete_bucketlist_item_unauthorized(self):
        pass

    def test_access_expired_token():
        pass

    def test_access_invalid_token():
        pass


if __name__ == "__main__":
    unittest.main()
