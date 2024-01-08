import socket
import time
import unittest

from client.Service.ServiceOrchestrator import ServiceOrchestrator
from server.DAO.OnlineUserDAO import OnlineUserDAO
from server.DAO.RoomDAO import RoomDAO
from server.DAO.AccountDAO import AccountDAO
from server.Network.ServerMainThread import ServerMainThread


class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.server = ServerMainThread(
            self.server_ip_address, self.server_port)
        self.server.start()

        self.account_dao = AccountDAO()
        self.online_user_dao = OnlineUserDAO()
        self.room_dao = RoomDAO()
        self.username1 = "Mina"
        self.password1 = "1234"
        self.username2 = "MoMo"
        self.password2 = "5678"
        self.username3 = "Mimi"
        self.password3 = "9012"
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()

    def tearDown(self):
        self.server.stop()
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()

    def test_signup(self):
        orchestrator = ServiceOrchestrator(self.server_ip_address)
        try:
            orchestrator.create_account(self.username1, self.password1)

            user_account = self.account_dao.get_account(self.username1)
            self.assertIsNotNone(user_account)
        finally:
            orchestrator.close()

    def test_login(self):
        orchestrator = ServiceOrchestrator(self.server_ip_address)
        try:
            orchestrator.create_account(self.username1, self.password1)
            orchestrator.login(self.username1, self.password1)
            user_account = self.online_user_dao.get_user(self.username1)
            self.assertIsNotNone(user_account)
        finally:
            orchestrator.close()

    def test_logout(self):
        orchestrator = ServiceOrchestrator(self.server_ip_address)
        orchestrator.create_account(self.username1, self.password1)
        orchestrator.login(self.username1, self.password1)
        orchestrator.close()
        user_account = self.online_user_dao.get_user(self.username1)
        self.assertIsNone(user_account)

    def test_get_online_users(self):
        orchestrator1 = ServiceOrchestrator(self.server_ip_address)
        orchestrator2 = ServiceOrchestrator(self.server_ip_address)
        try:
            orchestrator1.create_account(self.username1, self.password1)
            orchestrator2.create_account(self.username2, self.password2)
            orchestrator1.login(self.username1, self.password1)
            orchestrator2.login(self.username2, self.password2)
            online_users = orchestrator1.list_users()
            self.assertEqual(len(online_users), 2)
        finally:
            orchestrator1.close()
            orchestrator2.close()

    def test_room_chatting(self):
        orchestrator1 = ServiceOrchestrator(self.server_ip_address)
        orchestrator2 = ServiceOrchestrator(self.server_ip_address)
        orchestrator3 = ServiceOrchestrator(self.server_ip_address)
        try:
            orchestrator1.create_account(self.username1, self.password1)
            orchestrator2.create_account(self.username2, self.password2)
            orchestrator3.create_account(self.username3, self.password3)
            orchestrator1.login(self.username1, self.password1)
            orchestrator2.login(self.username2, self.password2)
            orchestrator3.login(self.username3, self.password3)
            room_name = "test_room"
            self.assertTrue(orchestrator1.create_room(room_name))
            self.assertTrue(orchestrator2.join_room(room_name))
            self.assertTrue(orchestrator3.join_room(room_name))
            orchestrator1.send_message("Hello")
            time.sleep(1)
            orchestrator3.send_message("World")
            orchestrator2.send_message("Bye")
            time.sleep(0.1)
            messages = orchestrator2.get_new_messages()
            self.assertEqual(len(messages), 3)
            print(messages)
        finally:
            orchestrator1.close()
            orchestrator2.close()
            orchestrator3.close()

