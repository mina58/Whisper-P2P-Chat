import time
import unittest

from client.Network.TCPServerThread import TCPServerThread

import socket


class TestTCPServerThread(unittest.TestCase):

    def setUp(self):
        self.tcp_server = TCPServerThread()
        self.address = self.tcp_server.get_address()

    def test_stop(self):
        self.tcp_server.start()
        self.tcp_server.stop()

    def test_chat_request(self):
        self.tcp_server.start()
        time.sleep(0.1)
        another_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            another_peer.connect(self.address)
            another_peer.send(b'CHAT_REQUEST mario')
            time.sleep(0.1)
            sock, message = self.tcp_server.get_private_chat()
            self.assertIsNotNone(sock)
            self.assertIsNotNone(message)
            print(message)
            sock, message = self.tcp_server.get_private_chat()
            self.assertIsNone(sock)
            self.assertIsNone(message)
        finally:
            another_peer.close()
            self.tcp_server.stop()
