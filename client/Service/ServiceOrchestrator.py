import threading
import time

from client.Service.ServerAPI import ServerAPI
from client.Service.ChatService import ChatService
from queue import Queue


class ServiceOrchestrator:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.server_port = 12121
        self.to_chat_queue = Queue()
        self.server_api = ServerAPI(
            self.server_ip, self.server_port, self.to_chat_queue)
        self.chat_service = None
        self.username = ""
        self.current_room = ""
        self.udp_port = ""
        self.messages = []
        self.is_chatting = False
        self.receiver_thread = None

    def create_account(self, username, password):
        if username == "" or password == "":
            return False
        if self.server_api.create_account(username, password):
            return True
        else:
            return False

    def login(self, username, password):
        if username == "" or password == "":
            return False
        if self.server_api.login(username, password):
            self.username = username
            return True
        else:
            return False

    def logout(self):
        self.server_api.logout()

    def list_rooms(self):
        return self.server_api.list_rooms()

    def list_users(self):
        return self.server_api.list_users()

    def create_room(self, room_name):
        self.chat_service = ChatService(
            room_name, self.username, self.to_chat_queue)

        if self.server_api.create_room(room_name):
            self.current_room = room_name
            self.messages = []
            return True
        else:
            self.chat_service.end_chat()
            self.chat_service = None
            return False

    def join_room(self, room_name):
        self.chat_service = ChatService(
            room_name, self.username, self.to_chat_queue)
        self.udp_port = self.chat_service.get_address()[1]

        if self.server_api.join_room(room_name, self.udp_port):
            self.current_room = room_name
            return True
        else:
            self.chat_service.end_chat()
            self.chat_service = None
            return False

    def leave_room(self):
        self.is_chatting = False
        self.chat_service.end_chat()
        self.server_api.leave_room(self.current_room)
        self.current_room = ""

    def send_message(self, message):
        if self.chat_service is not None:
            self.chat_service.send_message(message)

    def get_new_messages(self):
        return self.chat_service.get_messages()

    def close(self):
        self.is_chatting = False
        if self.chat_service is not None:
            self.chat_service.end_chat()
            self.chat_service = None

        if self.username != "":
            self.server_api.logout()

        self.server_api.server_connection_manager.disconnect()
