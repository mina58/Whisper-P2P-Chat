import time
import unittest
import socket

from client.Service.ServerAPI import ServerAPI
from common.MessageParser import MessageParser
from server.DAO.AccountDAO import AccountDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO
from server.DAO.RoomDAO import RoomDAO
from server.Network.ServerMainThread import ServerMainThread
from client.Network.TCPServerThread import TCPServerThread
from client.Network.PrivateChatThread import PrivateChatThread
from queue import Queue


class TestPrivateChat(unittest.TestCase):
    def setUp(self):
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.server = ServerMainThread(
            self.server_ip_address, self.server_port)
        self.server.start()
        self.to_chat_queue = Queue()
        self.to_chat_queue2 = Queue()
        self.api = ServerAPI(self.server_ip_address, self.server_port, self.to_chat_queue, name="mina")
        self.api2 = ServerAPI(self.server_ip_address, self.server_port, self.to_chat_queue2, name="momo")
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
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        self.tcp_server1 = TCPServerThread()
        self.tcp_server1.start()
        self.tcp_server2 = TCPServerThread()
        self.tcp_server2.start()
        self.tcp_port1 = self.tcp_server1.get_address()[1]
        self.tcp_port2 = self.tcp_server2.get_address()[1]

        self.api.login(self.username1, self.password1, self.tcp_port1)
        self.api2.login(self.username2, self.password2, self.tcp_port2)

    def test_private_chat(self):
        user1_info = self.api2.request_peer_info(self.username1)
        private_chat_thread1 = None
        private_chat_thread2 = None
        chat_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(0.1)
        try:
            chat_socket2.connect((user1_info["ip"], int(user1_info["port"])))
            chat_socket2.sendall(f"CHAT_REQUEST {self.username2}".encode("utf-8"))
            time.sleep(0.1)
            chat_socket1, _ = self.tcp_server1.get_private_chat()
            chat_socket1.sendall(f"1 ACCEPT_CHAT".encode("utf-8"))
            time.sleep(0.1)
            response = MessageParser.parse_message(chat_socket2.recv(1024).decode("utf-8"))
            private_chat_thread1 = PrivateChatThread(self.username1, chat_socket1)
            private_chat_thread2 = PrivateChatThread(self.username2, chat_socket2)
            private_chat_thread1.start()
            private_chat_thread2.start()
            time.sleep(0.1)
            private_chat_thread1.send_message("Hello")
            time.sleep(0.1)
            private_chat_thread2.send_message("Hi")
            private_chat_thread1.send_message("How are you?")
            private_chat_thread2.send_message("I'm fine")
            private_chat_thread1.send_message("Bye")
            time.sleep(0.1)
            messages1 = private_chat_thread1.get_messages()
            messages2 = private_chat_thread2.get_messages()
            self.assertEqual(len(messages1), 2)
            self.assertEqual(len(messages2), 3)
            private_chat_thread1.send_bye()
            time.sleep(0.1)
            self.assertFalse(private_chat_thread1.is_alive())
            self.assertFalse(private_chat_thread2.is_alive())
        finally:
            if private_chat_thread1 and private_chat_thread2:
                private_chat_thread1.close()
                private_chat_thread2.close()
            self.api.logout()
            self.api2.logout()
            self.tcp_server1.stop()
            self.tcp_server2.stop()
            self.server.stop()
