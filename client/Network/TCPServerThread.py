import logging
import threading
import socket

from common.MessageParser import MessageParser


class TCPServerThread(threading.Thread):
    """
    This class is the server side if the peer. Chat requests from other peers will arrive to this class
    """

    def __init__(self):
        super(TCPServerThread, self).__init__()
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.tcp_socket.bind((self.ip, 0))
        self.tcp_socket.listen(5)
        self.port = self.tcp_socket.getsockname()[1]
        self.logger = None
        self.is_running = False
        self.chat_request = None
        self.private_chat_socket = None

    def configure_logger(self):
        self.logger = logging.getLogger("peer-server-logger")
        self.logger.setLevel(level=logging.INFO)
        self.logger_file_handler = logging.FileHandler("peer.log")
        self.logger_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        self.logger_file_handler.setFormatter(self.logger_formatter)
        self.logger.addHandler(self.logger_file_handler)

    def run(self):
        self.is_running = True

        self.configure_logger()

        while self.is_running:
            try:
                peer_socket, peer_address = self.tcp_socket.accept()
                self.logger.info(
                    f"{self.ip, self.port} received connection from {peer_address}")
                request = peer_socket.recv(1024).decode("utf-8")
                self.logger.info(
                    f"{self.ip, self.port} received message: {request}")
                message = MessageParser.parse_message(request)
                if message["message_type"] == "CHAT_REQUEST":
                    self.chat_request = message
                    self.private_chat_socket = peer_socket

            except Exception as e:
                self.logger.error(e)
                break

    def stop(self):
        self.is_running = False
        if self.tcp_socket:
            self.tcp_socket.close()
            self.tcp_socket = None

    def get_address(self):
        return self.ip, self.port

    def get_private_chat(self):
        """:return: tuple of (private_chat_socket, chat_request)"""
        private_chat = (self.private_chat_socket, self.chat_request)
        self.private_chat_socket = None
        self.chat_request = None
        return private_chat

    def is_chat_requested(self):
        return self.chat_request is not None
