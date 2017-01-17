import unittest
from ..bucketlist import app
from ..bucketlist.model import db


class TestBucketList(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./testbucketlist.db"
        app.config["TESTING"] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()  # will call session remove
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
