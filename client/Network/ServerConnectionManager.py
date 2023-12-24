import socket

from hashlib import sha256
from common.MessageParser import MessageParser
from common.PasswordHasher import PasswordHasher


class ServerConnectionManager:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.password_hasher = PasswordHasher()

    def connect_to_server(self):
        self.client_socket.connect((self.server_ip, self.server_port))

    def send_create_account_message(self, username, password):
        sha = sha256()
        sha.update(password.encode('utf-8'))
        encrypted_password = sha.hexdigest()

        message = f"CREATE_ACC {username} {encrypted_password}"
        self.client_socket.sendall(message.encode("utf-8"))
        response_message = self.client_socket.recv(1024).decode("utf-8")
        response = MessageParser.parse_message(response_message)
        return response

    def send_login_message(self, username, password):
        sha = sha256()
        sha.update(password.encode('utf-8'))
        encrypted_password = sha.hexdigest()

        message = f"LOGIN {username} {encrypted_password}"
        self.client_socket.sendall(message.encode("utf-8"))
        response_message = self.client_socket.recv(1024).decode("utf-8")
        response = MessageParser.parse_message(response_message)
        return response

    def send_logout_message(self, username):
        message = f"LOGOUT {username}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.disconnect()

    def send_list_users_message(self):
        message = "LIST_USERS"
        self.client_socket.sendall(message.encode("utf-8"))
        response_message = self.client_socket.recv(1024).decode("utf-8")
        response = MessageParser.parse_message(response_message)
        return response

    def send_create_room_message(self, username, room_id):
        message = f"CREATE_ROOM {username} {room_id}"
        self.client_socket.sendall(message.encode("utf-8"))
        response_message = self.client_socket.recv(1024).decode("utf-8")
        response = MessageParser.parse_message(response_message)
        return response

    def send_join_room_message(self, username, room_id):
        message = f"JOIN_ROOM {username} {room_id}"
        self.client_socket.sendall(message.encode("utf-8"))
        response_message = self.client_socket.recv(1024).decode("utf-8")
        response = MessageParser.parse_message(response_message)
        return response

    def send_leave_room_message(self, username, room_id):
        message = f"LEAVE_ROOM {username} {room_id}"
        self.client_socket.sendall(message.encode("utf-8"))

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
