import unittest
from server.DAO.AccountDAO import AccountDAO


class TestAccountDAO(unittest.TestCase):
    def setUp(self):
        self.dao = AccountDAO()

    def tearDown(self):
        self.dao.drop_collection()

    def test_add_account(self):
        self.dao.add_account("testuser", "testpassword")
        user = self.dao.get_account("testuser")
        self.assertEqual(user["username"], "testuser")
        self.assertEqual(user["password"], "testpassword")

    def test_delete_account(self):
        self.dao.add_account("testuser", "testpassword")
        self.dao.delete_account("testuser")
        user = self.dao.get_account("testuser")
        self.assertIsNone(user)
