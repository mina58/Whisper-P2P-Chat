import threading
import socket
import logging
from common.MessageParser import MessageParser


class ChatThread(threading.Thread):
    """
    This class sends and receives chat messages from the udp socket
    """

    def __init__(self, room_id, username, to_chat_queue):
        super(ChatThread, self).__init__()
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = (socket.gethostbyname(socket.gethostname()))
        self.udp_socket.bind((self.ip, 0))
        self.udp_port = self.udp_socket.getsockname()[1]
        self.udp_socket.settimeout(0.001)
        self.is_running = True
        self.messages_buffer = []
        self.lock = threading.Lock()
        self.room_id = room_id
        self.username = username
        self.users_in_room = set()
        self.logger = None
        self.lock = threading.Lock()
        self.to_chat_queue = to_chat_queue
        self.to_chat_queue.queue.clear()

    def configure_logger(self):
        with self.lock:
            self.logger = logging.getLogger(self.username)
            self.logger.setLevel(level=logging.INFO)
            logger_file_handler = logging.FileHandler(f"udp-thread.log")
            logger_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
            logger_file_handler.setFormatter(logger_formatter)
            self.logger.addHandler(logger_file_handler)

    def run(self):
        self.configure_logger()
        while self.is_running:
            try:
                with self.lock:
                    address = None
                    if self.to_chat_queue.empty():
                        data, address = self.udp_socket.recvfrom(1024)
                        self.logger.info(
                            f"{self.username} received a message from {address}: {data.decode()}")
                        message = MessageParser.parse_message(data.decode())
                    else:
                        message = self.to_chat_queue.get()

                    if message["message_type"] == "CHAT_ROOM":
                        self.messages_buffer.append(message)
                    elif message["message_type"] == "PEER_INFO_ROOM":
                        self.add_to_addresses(message, address)
                    elif message["message_type"] == "REQUEST_INFO_ROOM":
                        self.send_info_and_add_to_addresses(message)
                    elif message["message_type"] == "LEFT_ROOM":
                        self.handle_leave_room(message)
            except socket.timeout:
                continue

    def broadcast_message(self, message):
        with self.lock:
            message = f"CHAT_ROOM {self.username} {self.room_id} {message}"
            # self.logger.info(f"broadcasting {message} to {[user['username'] for user in self.users_in_room]}")
            for username, address in self.users_in_room:
                self.udp_socket.sendto(message.encode("utf-8"), address)

    def get_address(self):
        return self.ip, self.udp_port

    def stop(self):
        self.is_running = False

    def get_messages(self):
        with self.lock:
            messages = self.messages_buffer
            self.messages_buffer = []
            return messages

    def send_info_and_add_to_addresses(self, message):
        if message["room_id"] != self.room_id:
            return
        response = f"PEER_INFO_ROOM {self.username} {self.room_id}"
        address = (message["ip"], int(message["port"]))
        self.udp_socket.sendto(response.encode("utf-8"), address)
        self.logger.info(
            f"{self.username} sent to {address} message: {response}")
        self.users_in_room.add((message["username"], address))

    def handle_leave_room(self, message):
        username = message["username"]
        for user in self.users_in_room:
            if user[0] == username:
                self.users_in_room.remove(user)
                break

    def add_to_addresses(self, message, address):
        if message["room_id"] != self.room_id:
            return
        self.users_in_room.add((message["username"], address))
