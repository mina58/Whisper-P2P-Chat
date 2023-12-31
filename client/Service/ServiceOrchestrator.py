import threading
import time

from client.Service.ServerAPI import ServerAPI
from client.Service.ChatService import ChatService
from client.Service.PrivateChatService import PrivateChatService
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
        self.private_chat_service = PrivateChatService("")
        self.tcp_server_port = self.private_chat_service.tcp_server_port

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
        if self.server_api.login(username, password, self.tcp_server_port):
            self.username = username
            self.private_chat_service.set_username(username)
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
        self.private_chat_service.close()

    def request_private_chat(self, username):
        user = self.server_api.request_peer_info(username)
        if not user:
            return False
        address = (user["ip"], int(user["port"]))
        return self.private_chat_service.start_private_chat(address)

    def is_chat_requested(self):
        return self.private_chat_service.is_chat_requested()

    def get_requested_chat_username(self):
        return self.private_chat_service.get_private_chat_request_username()

    def accept_private_chat(self):
        return self.private_chat_service.accept_private_chat()

    def reject_private_chat(self):
        self.private_chat_service.reject_private_chat()

    def end_private_chat(self):
        self.private_chat_service.end_private_chat()

    def get_private_chat_messages(self):
        return self.private_chat_service.get_messages()

    def send_private_chat_message(self, message):
        self.private_chat_service.send_message(message)

    def get_is_connected_to_private_chat(self):
        # checks if the other user has ended the chat
        return self.private_chat_service.get_is_connected()
