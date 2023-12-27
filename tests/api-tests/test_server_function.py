import unittest
import socket
import time
from server.Network.ServerMainThread import ServerMainThread
from client.Service.ServerAPI import ServerAPI
from server.DAO.AccountDAO import AccountDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO


class TestServerFunctions(unittest.TestCase):
    def setUp(self):
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.server = ServerMainThread(
            self.server_ip_address, self.server_port)
        self.server.start()
        self.api = ServerAPI(self.server_ip_address, self.server_port)
        self.api2 = ServerAPI(self.server_ip_address, self.server_port)
        self.account_dao = AccountDAO()
        self.online_user_dao = OnlineUserDAO()
        self.username1 = "Mina"
        self.password1 = "1234"
        self.username2 = "MoMo"
        self.password2 = "5678"

    def tearDown(self):
        time.sleep(0.25)
        self.server.stop()
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        time.sleep(0.25)

    def test_signup(self):
        response = self.api.create_account(self.username1, self.password1)
        try:
            self.assertTrue(response)
            user_account = self.account_dao.get_account(self.username1)
            self.assertIsNotNone(user_account)
        finally:
            self.api.server_connection_manager.disconnect()
            self.api2.server_connection_manager.disconnect()

    def test_login(self):
        self.api.create_account(self.username1, self.password1)
        try:
            response = self.api.login(self.username1, self.password1)
            self.assertTrue(response)
            user_account = self.online_user_dao.get_user(self.username1)
            self.assertIsNotNone(user_account)
        finally:
            self.api.server_connection_manager.disconnect()
            self.api2.server_connection_manager.disconnect()

    def test_invalid_login(self):
        self.api.create_account(self.username1, self.password1)
        try:
            response = self.api.login(self.username1, "invalid_password")
            self.assertFalse(response)
        finally:
            self.api.server_connection_manager.disconnect()
            self.api2.server_connection_manager.disconnect()

    def test_logout(self):
        self.api.create_account(self.username1, self.password1)
        try:
            self.api.login(self.username1, self.password1)
            self.api.logout()
            user_account = self.online_user_dao.get_user(self.username1)
            self.assertIsNone(user_account)
        finally:
            self.api.server_connection_manager.disconnect()
            self.api2.server_connection_manager.disconnect()

    def test_get_online_users(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        try:
            self.api.login(self.username1, self.password1)
            self.api2.login(self.username2, self.password2)
            online_users = self.api.list_users()
            self.assertEqual(len(online_users), 2)
        finally:
            self.api.server_connection_manager.disconnect()
            self.api2.server_connection_manager.disconnect()
