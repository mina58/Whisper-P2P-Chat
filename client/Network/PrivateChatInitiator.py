import socket

from client.Network.PrivateChatThread import PrivateChatThread
from common.MessageParser import MessageParser


class PrivateChatInitiator:
    """
    This class has the methods responsible for requesting, accepting and rejecting a private chat request.
    """

    @staticmethod
    def request_chat(address, username, logger=None):
        """
        This method takes an address, creates a tcp socket and connects to this address, and asks the other peer if it wants to chat. If the peer accepts, the method returns a PrivateChatThread with the socket, if the peer refuses, the method returns False.
        """
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.settimeout(10)
        try:
            my_socket.connect(address)
            message = f"CHAT_REQUEST {username}"
            my_socket.sendall(message.encode("utf-8"))
            if logger is not None:
                logger.info(
                    f"{username} sent a private chat request to {address}")
            response = my_socket.recv(1024).decode("utf-8")
            if logger is not None:
                logger.info(
                    f"{username} receive private chat response: {response} from {address}")
            response = MessageParser.parse_message(response)
            if response["status_code"] == "0":
                return False
            private_chat_thread = PrivateChatThread(username, my_socket)
            return private_chat_thread
        except socket.timeout:
            my_socket.close()
            return False

    @staticmethod
    def accept_chat(other_peers_socket, username):
        """
        Accept a private chat request by sending a accept message and returns a PrivateChatThread with the socket.
        """
        message = f"1 ACCEPT"
        other_peers_socket.sendall(message.encode("utf-8"))
        return PrivateChatThread(username, other_peers_socket)

    @staticmethod
    def reject_chat(other_peers_socket, username):
        """
        Reject a private chat request by sending a reject message.
        """
        message = f"0 REJECT"
        other_peers_socket.sendall(message.encode("utf-8"))
