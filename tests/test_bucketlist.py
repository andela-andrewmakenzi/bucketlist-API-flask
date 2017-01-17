import unittest
from bucketlist import app
import tempfile
import os


class TestBucketList(unittest.TestCase):
    def SetUp(self):
        self.db_handle, app.config["SQLALCHEMY_DATABASE_URI"] = tempfile.mkstemp()
        app.config["TESTING"] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_handle)
        os.unlink(app.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":
    unittest.main()
