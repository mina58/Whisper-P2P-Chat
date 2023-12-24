import threading
import logging
from common.MessageParser import MessageParser
from server.Service.OnlineUserService import OnlineUserService
from server.Service.AccountService import AccountService
from server.Service.RoomService import RoomService


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        super(ClientThread, self).__init__()
        self.client_socket = client_socket
        self.ip = client_address[0]
        self.port = client_address[1]
        self.is_running = False
        self.username = None
        self.logger = None
        self.online_user_service = OnlineUserService()
        self.account_service = AccountService()
        self.room_service = RoomService()

    def configure_logger(self):
        self.logger = logging.getLogger("client-thread-logger")
        self.logger.setLevel(level=logging.INFO)
        self.logger_file_handler = logging.FileHandler("client-thread.log")
        self.logger_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        self.logger_file_handler.setFormatter(self.logger_formatter)
        self.logger.addHandler(self.logger_file_handler)

    def run(self):
        self.is_running = True

        self.configure_logger()

        while self.is_running:
            try:
                request_bytes = self.client_socket.recv(1024)
                request = request_bytes.decode("utf-8")
                if request == "":
                    self.stop()
                    continue
                self.logger.info(
                    f"Received request from {self.ip}:{self.port}: {request}")
                message = MessageParser.parse_message(request)

                if message["message_type"] == "LOGIN":
                    self.login(message)
                elif message["message_type"] == "CREATE_ACC":
                    self.create_account(message)
                elif message["message_type"] == "LOGOUT":
                    self.logout(message)
                elif message["message_type"] == "LIST_USERS":
                    self.list_users(message)
                elif message["message_type"] == "CREATE_ROOM":
                    self.create_room(message)
                elif message["message_type"] == "JOIN_ROOM":
                    self.join_room(message)
                elif message["message_type"] == "LEAVE_ROOM":
                    self.leave_room(message)
                elif message["message_type"] == "LIST_ROOMS":
                    self.list_rooms(message)

            except Exception as e:
                self.logger.error(f"Error: {e}")

    def stop(self):
        self.is_running = False
        if self.client_socket:
            self.client_socket.close()

    def login(self, message):
        response = ""

        if self.account_service.login(message["username"], message["password"]):
            self.username = message["username"]
            response = "1 LOGIN_SUCC"
            self.online_user_service.add_online_user(
                self.username, self.ip, self.port)
            self.logger.info(f"User {self.username} logged in")
        else:
            response = "0 AUTH_FAIL"

        self.client_socket.sendall(response.encode("utf-8"))

    def create_account(self, message):
        response = ""

        if self.account_service.create_account(message["username"], message["password"]):
            response = "1 ACC_CREATED"
        else:
            response = "0 USERNAME_TAKEN"

        self.client_socket.sendall(response.encode("utf-8"))

    def logout(self, message):
        self.online_user_service.remove_online_user(message["username"])
        self.stop()

    def list_users(self, message):
        response = ""

        users = self.online_user_service.get_online_users()
        usernames = [user["username"] for user in users]

        response = "1 USERS_LIST "
        response += " ".join(usernames)

        self.client_socket.sendall(response.encode("utf-8"))

    def create_room(self, message):
        response = ""

        if self.room_service.create_room(message["username"], message["room_id"]):
            response = "1 ROOM_CREATED"
        else:
            response = "0 ROOM_ID_UNAVAILABLE"

        self.client_socket.sendall(response.encode("utf-8"))

    def join_room(self, message):
        response = ""
        
        if not self.room_service.add_user(message["room_id"], message["username"]):
            response = "0 ROOM_UNAVAILABLE"
        else:
            response = "1 JOINED_ROOM"
            
        self.client_socket.sendall(response.encode("utf-8"))

    def leave_room(self, message):
        self.room_service.remove_user(message["room_id"], message["username"])

    def list_rooms(self, message):
        response = ""

        rooms = self.room_service.get_rooms()
        response = "1 ROOMS_LIST "
        response += " ".join([room["room_id"] for room in rooms])

        self.client_socket.sendall(response.encode("utf-8"))
