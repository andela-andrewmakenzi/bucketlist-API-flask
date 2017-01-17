import unittest
from bucketlist import app
from bucketlist.model import db


class TestBucketList(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./testbucketlist.db"
        app.config["TESTING"] = True
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()  # will call session remove
        db.drop_all()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        pass

    def test_login_no_username(self):
        pass

    def test_login_no_password(self):
        pass

    def test_login_no_credentials(self):
        pass

    def test_register_user(self):
        pass

    def test_register_user_pass_no_username(self):
        pass

    def test_register_user_pass_no_password(self):
        pass

    def test_register_user_pass_no_username_or_password(self):
        pass

    def test_register_with_existing_username(self):
        pass

    def test_create_bucketlist(self):
        pass

    def test_create_bucketlist_no_bucketlistname(self):
        # when they try create a bucketlist but dont supply a name for it
        pass

    def test_create_bucketlist_unauthorized(self):
        """ test what will happen if they try to create a password but they are
        not logged in """
        pass

    def test_get_bucketlists(self):
        pass

    def test_get_bucketlists_invalid_id(self):
        pass

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


if __name__ == "__main__":
    unittest.main()
