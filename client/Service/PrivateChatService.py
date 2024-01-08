from client.Network.TCPServerThread import TCPServerThread
from client.Network.PrivateChatInitiator import PrivateChatInitiator
from common.ErrorLogger import ErrorLogger


class PrivateChatService:
    def __init__(self, username):
        self.username = username
        self.tcp_server = TCPServerThread()
        self.tcp_server.start()
        self.tcp_server_port = int(self.tcp_server.get_address()[1])
        self.private_chat_request_socket = None
        self.private_chat_request_message = None
        self.private_chat_thread = None
        self.is_connected = False

    def is_chat_requested(self):
        if self.tcp_server.is_chat_requested():
            self.private_chat_request_socket, self.private_chat_request_message = self.tcp_server.get_private_chat()
            return True
        else:
            return False

    def get_private_chat_request_username(self):
        if self.private_chat_request_message is not None:
            return self.private_chat_request_message["username"]
        else:
            return None

    def accept_private_chat(self):
        if self.private_chat_thread is not None:
            self.private_chat_thread.send_bye()

        if self.private_chat_request_socket is None or self.private_chat_request_message is None:
            return False

        try:
            self.private_chat_thread = PrivateChatInitiator.accept_chat(
                self.private_chat_request_socket, self.username)
            self.private_chat_thread.start()
            self.private_chat_request_message = None
            self.private_chat_request_socket = None
            self.is_connected = True
            return True
        except Exception as e:
            ErrorLogger.get_logger().error(f"Error accepting private chat.")
            return False

    def reject_private_chat(self):
        PrivateChatInitiator.reject_chat(
            self.private_chat_request_socket, self.username)
        self.private_chat_request_message = None
        self.private_chat_request_socket = None

    def get_tcp_server_port(self):
        return self.tcp_server_port

    def end_private_chat(self):
        if self.is_connected and self.private_chat_thread.is_running:
            self.private_chat_thread.send_bye()
            self.private_chat_thread.close()
            self.private_chat_thread.join()
            self.private_chat_thread = None
        self.is_connected = False

    def get_messages(self):
        if self.private_chat_thread is not None:
            return self.private_chat_thread.get_messages()
        else:
            return []

    def send_message(self, message):
        if self.private_chat_thread is not None:
            self.private_chat_thread.send_message(message)

    def start_private_chat(self, address):
        chat_thread = PrivateChatInitiator.request_chat(address, self.username)
        if chat_thread:
            self.private_chat_thread = chat_thread
            self.private_chat_thread.start()
            self.is_connected = True
            return True
        else:
            return False

    def close(self):
        self.end_private_chat()
        self.tcp_server.stop()
        self.tcp_server.join()

    def get_is_connected(self):
        if self.private_chat_thread is not None and self.private_chat_thread.is_running:
            return True
        else:
            self.is_connected = False
            self.private_chat_thread = None
            return False

    def set_username(self, username):
        self.username = username
