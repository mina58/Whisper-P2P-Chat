import socket
import time
import unittest

from client.Service.ChatService import ChatService
from client.Service.ServerAPI import ServerAPI
from server.DAO.AccountDAO import AccountDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO
from server.DAO.RoomDAO import RoomDAO
from server.Network.ServerMainThread import ServerMainThread
from queue import Queue


class TestChat(unittest.TestCase):
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
        self.room_id = "1234"
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()
        self.api.create_account(self.username1, self.password1)
        self.api2.create_account(self.username2, self.password2)
        self.api3.create_account(self.username3, self.password3)
        self.api.login(self.username1, self.password1)
        self.api2.login(self.username2, self.password2)
        self.api3.login(self.username3, self.password3)

    def tearDown(self):
        self.api.server_connection_manager.disconnect()
        self.api2.server_connection_manager.disconnect()
        self.api3.server_connection_manager.disconnect()
        self.server.stop()
        self.server.join()
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.room_dao.drop_collection()

    def test_join_room(self):
        try:
            chat_api1 = ChatService(self.room_id, self.username1, self.to_chat_queue)
            udp_port_1 = chat_api1.get_address()[1]
            self.api.create_room(self.room_id)
            chat_api2 = ChatService(self.room_id, self.username2, self.to_chat_queue2)
            udp_port_2 = chat_api2.get_address()[1]
            self.api2.join_room(self.room_id, udp_port_2)
            chat_api3 = ChatService(self.room_id, self.username3, self.to_chat_queue3)
            udp_port_3 = chat_api3.get_address()[1]
            self.api3.join_room(self.room_id, udp_port_3)

            time.sleep(0.1)

            self.assertEqual(len(chat_api1.chat_thread.users_in_room), 2)
            self.assertEqual(len(chat_api2.chat_thread.users_in_room), 2)
            self.assertEqual(len(chat_api3.chat_thread.users_in_room), 2)
            chat_api1.end_chat()
            chat_api2.end_chat()
            chat_api3.end_chat()
        finally:
            self.api.logout()
            self.api2.logout()
            self.api3.logout()

    def test_leave_room(self):
        try:
            chat_api1 = ChatService(self.room_id, self.username1, self.to_chat_queue)
            udp_port_1 = chat_api1.get_address()[1]
            self.api.create_room(self.room_id)
            chat_api2 = ChatService(self.room_id, self.username2, self.to_chat_queue2)
            udp_port_2 = chat_api2.get_address()[1]
            self.api2.join_room(self.room_id, udp_port_2)
            chat_api3 = ChatService(self.room_id, self.username3, self.to_chat_queue3)
            udp_port_3 = chat_api3.get_address()[1]
            self.api3.join_room(self.room_id, udp_port_3)

            time.sleep(0.1)

            self.api2.leave_room(self.room_id)

            time.sleep(0.1)

            self.assertEqual(len(chat_api1.chat_thread.users_in_room), 1)
            self.assertEqual(len(chat_api3.chat_thread.users_in_room), 1)

            self.api.leave_room(self.room_id)

            time.sleep(0.1)

            self.assertEqual(len(chat_api3.chat_thread.users_in_room), 0)

            chat_api1.end_chat()
            chat_api2.end_chat()
            chat_api3.end_chat()
        finally:
            self.api.logout()
            self.api2.logout()
            self.api3.logout()

    def test_chatting(self):
        try:
            chat_api1 = ChatService(self.room_id, self.username1, self.to_chat_queue)
            udp_port_1 = chat_api1.get_address()[1]
            self.api.create_room(self.room_id)
            chat_api2 = ChatService(self.room_id, self.username2, self.to_chat_queue2)
            udp_port_2 = chat_api2.get_address()[1]
            self.api2.join_room(self.room_id, udp_port_2)
            chat_api3 = ChatService(self.room_id, self.username3, self.to_chat_queue3)
            udp_port_3 = chat_api3.get_address()[1]
            self.api3.join_room(self.room_id, udp_port_3)

            time.sleep(0.1)

            chat_api1.send_message("hello")
            chat_api2.send_message("hi")
            chat_api3.send_message("If this works first time!!")

            time.sleep(0.1)

            messages1 = chat_api1.get_messages()
            messages2 = chat_api2.get_messages()
            messages3 = chat_api3.get_messages()

            print(messages1, messages2, messages3)

            self.assertEqual(len(messages1), 3)
            self.assertEqual(len(messages2), 3)
            self.assertEqual(len(messages3), 3)

            chat_api1.end_chat()
            chat_api2.end_chat()
            chat_api3.end_chat()

        finally:
            self.api.logout()
            self.api2.logout()
            self.api3.logout()

