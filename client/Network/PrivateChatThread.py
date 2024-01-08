import logging
import socket
import threading

from common.ErrorLogger import ErrorLogger
from common.MessageParser import MessageParser


class PrivateChatThread(threading.Thread):
    """
    This class handle the private chatting happening through TCP
    """
    def __init__(self, username, other_peer_socket):
        super(PrivateChatThread, self).__init__()
        self.other_peer_socket = other_peer_socket
        self.messages = []
        self.username = username
        self.other_peer_socket.settimeout(0.001)
        self.is_running = True
        self.logger = None

    def configure_logger(self):
        self.logger = logging.getLogger(f"{self.username}private-chat-logger")
        self.logger.setLevel(level=logging.INFO)
        logger_file_handler = logging.FileHandler(f"peer.log")
        logger_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        logger_file_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_file_handler)

    def run(self):
        self.configure_logger()
        while self.is_running:
            try:
                data = self.other_peer_socket.recv(1024)
                if data.decode() == "":
                    self.close()
                self.logger.info(f"{self.username} private chat thread received message: {data.decode()}")
                message = MessageParser.parse_message(data.decode())
                if message["message_type"] == "CHAT_PRIVATE":
                    self.messages.append(message)
                elif message["message_type"] == "BYE":
                    self.close()
            except socket.timeout:
                continue
            except Exception as e:
                ErrorLogger.get_logger().error(e)

    def send_message(self, message):
        if self.is_running:
            message = f"CHAT_PRIVATE {self.username} {message}"
            self.other_peer_socket.sendall(message.encode())
            self.logger.info(f"{self.username} private chat thread sent message: {message}")

    def send_bye(self):
        if self.is_running:
            message = f"BYE {self.username}"
            self.other_peer_socket.sendall(message.encode())
            self.logger.info(f"{self.username} private chat thread sent message: {message}")

    def get_messages(self):
        messages = self.messages
        self.messages = []
        return messages

    def close(self):
        self.is_running = False
        if self.other_peer_socket:
            self.other_peer_socket.close()
            self.other_peer_socket = None
