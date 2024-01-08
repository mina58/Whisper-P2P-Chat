import socket
import threading
import time
import unittest
from queue import Queue

from client.Service.PrivateChatService import PrivateChatService
from client.Service.ServerAPI import ServerAPI
from server.DAO.AccountDAO import AccountDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO
from server.DAO.RoomDAO import RoomDAO
from server.Network.ServerMainThread import ServerMainThread


class TestPrivateChatService(unittest.TestCase):
    def setUp(self):
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
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()
        self.private_chat_service1 = PrivateChatService(self.username1)
        self.private_chat_service2 = PrivateChatService(self.username2)
        self.private_chat_service3 = PrivateChatService(self.username3)
        self.tcp_port1 = self.private_chat_service1.get_tcp_server_port()
        self.tcp_port2 = self.private_chat_service2.get_tcp_server_port()
        self.tcp_port3 = self.private_chat_service3.get_tcp_server_port()
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        self.api3.create_account(self.username3, self.password3)
        self.api.login(self.username1, self.password1, self.tcp_port1)
        self.api2.login(self.username2, self.password2, self.tcp_port2)
        self.api3.login(self.username3, self.password3, self.tcp_port3)
        time.sleep(0.2)

    def test_chatting(self):
        try:
            user2_info = self.api.request_peer_info(self.username2)
            self.assertTrue(user2_info)

            def start_chat():
                self.private_chat_service1.start_private_chat((user2_info["ip"], int(user2_info["port"])))

            threading.Thread(target=start_chat).start()
            time.sleep(0.1)
            self.assertTrue(self.private_chat_service2.is_chat_requested())
            self.assertTrue(self.private_chat_service2.get_private_chat_request_username(), self.username1)
            self.private_chat_service2.accept_private_chat()
            time.sleep(0.1)
            self.assertFalse(self.private_chat_service2.is_chat_requested())
            self.private_chat_service1.send_message("Hello")
            self.private_chat_service1.send_message("How are you?")
            self.private_chat_service2.send_message("I'm fine")
            time.sleep(0.3)
            messages1 = self.private_chat_service1.get_messages()
            messages2 = self.private_chat_service2.get_messages()
            self.assertEqual(len(messages1), 1)
            self.assertEqual(len(messages2), 2)
            self.private_chat_service1.end_private_chat()
            time.sleep(0.1)
            self.private_chat_service2.end_private_chat()
            time.sleep(0.1)
            self.private_chat_service3.end_private_chat()

        finally:
            self.private_chat_service1.close()
            self.private_chat_service2.close()
            self.private_chat_service3.close()
            self.api.logout()
            self.api2.logout()
            self.api3.logout()
            time.sleep(0.1)
            self.server.stop()

    def test_switching_chat(self):
        try:
            user2_info = self.api.request_peer_info(self.username2)
            user1_info = self.api3.request_peer_info(self.username1)
            self.assertTrue(user2_info)

            def start_chat():
                self.private_chat_service1.start_private_chat((user2_info["ip"], int(user2_info["port"])))

            threading.Thread(target=start_chat).start()
            time.sleep(0.1)
            self.assertTrue(self.private_chat_service2.is_chat_requested())
            self.assertTrue(self.private_chat_service2.get_private_chat_request_username(), self.username1)
            self.private_chat_service2.accept_private_chat()
            time.sleep(0.1)
            self.assertFalse(self.private_chat_service2.is_chat_requested())
            self.private_chat_service1.send_message("Hello")
            self.private_chat_service1.send_message("How are you?")
            self.private_chat_service2.send_message("I'm fine")
            time.sleep(0.2)
            messages1 = self.private_chat_service1.get_messages()
            messages2 = self.private_chat_service2.get_messages()
            self.assertEqual(len(messages1), 1)
            self.assertEqual(len(messages2), 2)

            def start_chat2():
                response = self.private_chat_service3.start_private_chat((user1_info["ip"], int(user1_info["port"])))
                self.assertTrue(response)

            threading.Thread(target=start_chat2).start()
            time.sleep(0.1)
            self.assertTrue(self.private_chat_service1.is_chat_requested())
            self.private_chat_service1.accept_private_chat()
            time.sleep(0.1)
            self.assertFalse(self.private_chat_service1.is_chat_requested())
            self.assertFalse(self.private_chat_service2.get_is_connected())
            self.assertTrue(self.private_chat_service1.get_is_connected())
            self.assertTrue(self.private_chat_service3.get_is_connected())
            self.private_chat_service3.send_message("Hi2")
            self.private_chat_service3.send_message("How are you?2")
            self.private_chat_service1.send_message("I'm fine2")
            time.sleep(0.2)
            messages1 = self.private_chat_service1.get_messages()
            messages3 = self.private_chat_service3.get_messages()
            self.assertEqual(len(messages1), 2)
            self.assertEqual(len(messages3), 1)
            self.private_chat_service1.end_private_chat()
            time.sleep(0.1)
            self.private_chat_service3.end_private_chat()
            self.assertFalse(self.private_chat_service1.get_is_connected())
            self.assertFalse(self.private_chat_service2.get_is_connected())
            self.assertFalse(self.private_chat_service3.get_is_connected())

        finally:
            self.private_chat_service1.close()
            self.private_chat_service2.close()
            self.private_chat_service3.close()
            self.api.logout()
            self.api2.logout()
            self.api3.logout()
            time.sleep(0.1)
            self.server.stop()
