import unittest
from server.DAO.OnlineUserDAO import OnlineUserDAO


class TestOnlineUserDAO(unittest.TestCase):
    def setUp(self):
        self.dao = OnlineUserDAO()

    def tearDown(self):
        self.dao.drop_collection()

    def test_add_user(self):
        self.dao.add_user("testuser", "127.0.0.1", 12345)
        user = self.dao.get_user("testuser")
        self.assertEqual(user["username"], "testuser")
        self.assertEqual(user["ip"], "127.0.0.1")
        self.assertEqual(user["port"], 12345)

    def test_delete_user(self):
        self.dao.add_user("testuser", "127.0.0.1", 12345)
        self.dao.delete_user("testuser")
        user = self.dao.get_user("testuser")
        self.assertIsNone(user)
