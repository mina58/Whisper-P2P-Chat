import socket
import threading

from hashlib import sha256
from common.MessageParser import MessageParser
from common.PasswordHasher import PasswordHasher
import logging


class ServerConnectionManager:
    """
    This class manages all the TCP interactions with the server.
    """

    class ServerConnectionListener(threading.Thread):
        """
        This class listens for incoming messages from the server on a separate thread.
        """

        def __init__(self, client_socket, logger, name, to_chat_queue):
            super().__init__()
            self.client_socket = client_socket
            client_socket.settimeout(0.001)
            self.logger = logger
            self.is_running = False
            self.is_listening = False
            self.response = None
            self.name = name
            self.to_chat_queue = to_chat_queue

        def run(self):
            self.is_running = True
            self.is_listening = True

            while self.is_running:
                try:
                    if self.is_listening:
                        data = self.client_socket.recv(1024)
                        if data.decode() == "":
                            break
                        self.logger.info(f"{self.client_socket.getsockname()} received message: {data.decode('utf-8')}")
                        message = MessageParser.parse_message(data.decode('utf-8'))
                        if "status_code" in message:
                            self.response = message
                        else:
                            self.to_chat_queue.put(message)

                except socket.timeout:
                    continue
                except Exception as e:
                    self.logger.error(
                        f"Error occurred while receiving data from {self.client_socket.getsockname()}: {e}")
                    break

        def stop(self):
            self.is_running = False

    def __init__(self, server_ip, server_port, name, to_chat_queue):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.password_hasher = PasswordHasher()
        self.logger = logging.getLogger(f"{name}-logger")
        self.logger.setLevel(level=logging.INFO)
        self.logger_file_handler = logging.FileHandler("peer.log")
        self.logger_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger_file_handler.setFormatter(self.logger_formatter)
        self.logger.addHandler(self.logger_file_handler)
        self.server_connection_listener = self.ServerConnectionListener(self.client_socket, self.logger, name,
                                                                        to_chat_queue)
        self.name = name

    def get_response(self):
        while self.server_connection_listener.response is None:
            pass
        response = self.server_connection_listener.response
        self.server_connection_listener.response = None
        return response

    def connect_to_server(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        self.server_connection_listener.start()

    def send_create_account_message(self, username, password):
        sha = sha256()
        sha.update(password.encode('utf-8'))
        encrypted_password = sha.hexdigest()

        message = f"CREATE_ACC {username} {encrypted_password}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")

    def send_login_message(self, username, password):
        sha = sha256()
        sha.update(password.encode('utf-8'))
        encrypted_password = sha.hexdigest()
        message = f"LOGIN {username} {encrypted_password}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")

    def send_logout_message(self, username):
        message = f"LOGOUT {username}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")
        self.disconnect()

    def send_list_users_message(self):
        message = "LIST_USERS"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")

    def send_create_room_message(self, username, room_id):
        message = f"CREATE_ROOM {username} {room_id}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")

    def send_join_room_message(self, username, room_id, udp_port):
        message = f"JOIN_ROOM {username} {room_id} {udp_port}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")

    def send_leave_room_message(self, username, room_id):
        message = f"LEAVE_ROOM {username} {room_id}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")

    def send_list_rooms_message(self):
        message = "LIST_ROOMS"
        self.client_socket.sendall(message.encode("utf-8"))
        self.logger.info(f"{self.client_socket.getsockname()} sent message: {message}")

    def disconnect(self):
        self.server_connection_listener.stop()
        if self.server_connection_listener.is_alive():
            self.server_connection_listener.join()
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
