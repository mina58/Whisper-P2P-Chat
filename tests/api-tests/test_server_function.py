import unittest
import socket
import time

from server.Network.ServerMainThread import ServerMainThread
from client.Service.ServerAPI import ServerAPI
from server.DAO.AccountDAO import AccountDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO
from server.DAO.RoomDAO import RoomDAO
from queue import Queue


class TestServerFunctions(unittest.TestCase):
    def setUp(self):
        time.sleep(1)
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.server = ServerMainThread(
            self.server_ip_address, self.server_port)
        self.server.start()
        self.to_chat_queue = Queue()
        self.to_chat_queue2 = Queue()
        self.to_chat_queue3 = Queue()
        self.api = ServerAPI(self.server_ip_address, self.server_port, self.to_chat_queue, name="mina")
        self.api2 = ServerAPI(self.server_ip_address, self.server_port, self.to_chat_queue2, name="momo")
        self.api3 = ServerAPI(self.server_ip_address, self.server_port, self.to_chat_queue3, name="mimi")
        self.account_dao = AccountDAO()
        self.online_user_dao = OnlineUserDAO()
        self.room_dao = RoomDAO()
        self.username1 = "Mina"
        self.password1 = "1234"
        self.username2 = "MoMo"
        self.password2 = "5678"
        self.username3 = "Mimi"
        self.password3 = "9012"
        self.room_id = "1234"
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()
        self.udp_port1 = 12345
        self.udp_port2 = 12346
        self.udp_port3 = 12347
        self.tcp_port1 = "12348"
        self.tcp_port2 = "12349"
        self.tcp_port3 = "12350"

    def tearDown(self):
        self.api.server_connection_manager.disconnect()
        self.api2.server_connection_manager.disconnect()
        self.api3.server_connection_manager.disconnect()
        self.server.stop()
        self.server.join()
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()
        time.sleep(1)

    def test_signup(self):
        response = self.api.create_account(self.username1, self.password1)
        self.assertTrue(response)
        user_account = self.account_dao.get_account(self.username1)
        self.assertIsNotNone(user_account)

    def test_login(self):
        try:
            self.api.create_account(self.username1, self.password1)
            response = self.api.login(self.username1, self.password1, self.tcp_port1)
            self.assertTrue(response)
            time.sleep(0.0001)
            user_account = self.online_user_dao.get_user(self.username1)
            self.assertIsNotNone(user_account)
        finally:
            self.api.logout()

    def test_invalid_login(self):
        self.api.create_account(self.username1, self.password1)
        response = self.api.login(self.username1, "invalid_password", self.tcp_port1)
        self.assertFalse(response)

    def test_logout(self):
        self.api.create_account(self.username1, self.password1)
        self.api.login(self.username1, self.password1, self.tcp_port1)
        self.api.logout()
        user_account = self.online_user_dao.get_user(self.username1)
        self.assertIsNone(user_account)

    def test_get_online_users(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)
            online_users = self.api.list_users()
            self.assertEqual(len(online_users), 2)
        finally:
            self.api.logout()
            self.api2.logout()

    def test_create_room_success(self):
        self.api.create_account(self.username1, self.password1)
        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            response = self.api.create_room(self.room_id)
            self.assertTrue(response)

            # Check if the room was created in the server
            room = self.room_dao.get_room(self.room_id)
            self.assertIsNotNone(room)
        finally:
            self.api.logout()

    def test_create_room_failure_existing_room(self):
        self.api.create_account(self.username1, self.password1)
        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)

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

    def test_join_room_success(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        self.api3.create_account(self.username3, self.password3)
        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)
            self.api3.login(self.username3, self.password3, self.tcp_port3)
            self.api.create_room(self.room_id)
            response = self.api2.join_room(self.room_id, self.udp_port2)
            self.assertTrue(response)
            response = self.api3.join_room(self.room_id, self.udp_port3)
            self.assertTrue(response)
            users = self.room_dao.get_room(self.room_id)["users"]
            user_in_room = self.username2 in users and self.username3 in users
            self.assertTrue(user_in_room)
        finally:
            self.api.logout()
            self.api2.logout()
            self.api3.logout()

    def test_leave_room_success(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)

            self.api.create_room(self.room_id)
            self.api2.join_room(self.room_id, self.udp_port2)

            self.api2.leave_room(self.room_id)
            time.sleep(0.0001)

            users = self.room_dao.get_room(self.room_id)[
                "users"]
            user_in_room = self.username2 in users
            self.assertFalse(user_in_room)
        finally:
            self.api.logout()
            self.api2.logout()

    def test_list_rooms(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)

            self.api.create_room(self.room_id)

            time.sleep(0.1)

            rooms = self.api2.list_rooms()
            self.assertEqual(len(rooms), 1)
        finally:
            self.api.logout()
            self.api2.logout()

    def test_ended_room_list(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)

            self.api.create_room(self.room_id)
            self.api2.join_room(self.room_id, self.udp_port2)

            time.sleep(0.1)

            self.api2.leave_room(self.room_id)
            self.api.leave_room(self.room_id)

            rooms = self.api2.list_rooms()
            self.assertEqual(len(rooms), 0)
        finally:
            self.api.logout()
            self.api2.logout()

    def test_broadcasting(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        self.api3.create_account(self.username3, self.password3)

        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)
            self.api3.login(self.username3, self.password3, self.tcp_port3)

            self.api.create_room(self.room_id)
            time.sleep(0.25)
            self.api2.join_room(self.room_id, self.udp_port2)
            time.sleep(0.25)
            self.api3.join_room(self.room_id,  self.udp_port3)
            time.sleep(0.25)
        finally:
            self.api.logout()
            self.api2.logout()
            self.api3.logout()

    def test_request_info_private_user_available(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)

        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)

            response = self.api2.request_peer_info(self.username1)
            self.assertTrue(response)
            self.assertEqual(response["username"], self.username1)
            self.assertEqual(response["port"], self.tcp_port1)

        finally:
            self.api.logout()
            self.api2.logout()

    def test_request_info_private_user_unavailable(self):
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)

        try:
            self.api.login(self.username1, self.password1, self.tcp_port1)
            self.api2.login(self.username2, self.password2, self.tcp_port2)

            response = self.api2.request_peer_info(self.username3)
            self.assertFalse(response)

        finally:
            self.api.logout()
            self.api2.logout()
            