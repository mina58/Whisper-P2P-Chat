import unittest
import socket
import time
from server.Network.ServerMainThread import ServerMainThread
from client.Service.ServerAPI import ServerAPI
from server.DAO.AccountDAO import AccountDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO
from server.DAO.RoomDAO import RoomDAO


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
        self.room_dao = RoomDAO()
        self.username1 = "Mina"
        self.password1 = "1234"
        self.username2 = "MoMo"
        self.password2 = "5678"
        self.room_id = "1234"

    def tearDown(self):
        time.sleep(0.25)
        self.server.stop()
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()
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

    def test_create_room_success(self):
        self.api.create_account(self.username1, self.password1)
        try:
            self.api.login(self.username1, self.password1)
            response = self.api.create_room(self.room_id)
            self.assertTrue(response)

            # Check if the room was created in the server
            room = self.room_dao.get_room(self.room_id)
            self.assertIsNotNone(room)
        finally:
            self.api.logout()
            self.api.server_connection_manager.disconnect()

    def test_create_room_failure_existing_room(self):
        self.api.create_account(self.username1, self.password1)
        try:
            self.api.login(self.username1, self.password1)

            # Create a room with the same ID
            self.api.create_room(self.room_id)

            # Try creating the same room again
            response = self.api.create_room(self.room_id)
            self.assertFalse(response)

            # Check that the existing room is still in the server
            room = self.room_dao.get_room(self.room_id)
            self.assertIsNotNone(room)
        finally:
            self.api.logout()
            self.api.server_connection_manager.disconnect()

    def test_create_room_failure_not_logged_in(self):
        # Try creating a room without logging in
        response = self.api.create_room(self.room_id)
        self.assertFalse(response)

        # Check that no room was created in the server
        room = self.room_dao.get_room(self.room_id)
        self.assertIsNone(room)

    def test_join_room_success(self):
        self.api.create_account(self.username1, self.password1)
        try:
            self.api.login(self.username1, self.password1)

            # Create a room
            self.api.create_room(self.room_id)

            # Join the room
            response = self.api.join_room(self.room_id)
            self.assertTrue(response)

            # Check if the user is in the room
            user_in_room = self.username1 in self.room_dao.get_room(self.room_id)[
                "users"]
            self.assertTrue(user_in_room)
        finally:
            self.api.logout()
            self.api.server_connection_manager.disconnect()

    def test_leave_room_success(self):
        self.api.create_account(self.username1, self.password1)
        try:
            self.api.login(self.username1, self.password1)

            # Create and join a room
            self.api.create_room(self.room_id)
            self.api.join_room(self.room_id)

            # Leave the room
            self.api.leave_room(self.room_id)

            # Check if the user is no longer in the room
            user_in_room = self.username1 in self.room_dao.get_room(self.room_id)[
                "users"]
            self.assertFalse(user_in_room)
        finally:
            self.api.logout()
            self.api.server_connection_manager.disconnect()
