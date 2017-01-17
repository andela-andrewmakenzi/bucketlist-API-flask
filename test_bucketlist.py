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
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
