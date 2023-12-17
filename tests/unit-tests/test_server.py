import unittest
import socket
import time
from server.Network.ServerMainThread import ServerMainThread


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.server = ServerMainThread(
            self.server_ip_address, self.server_port)
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_server_connection(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.server_address)
        data = "Hello, this is a test!"
        client_socket.sendall(data.encode("utf-8"))
        time.sleep(1)
        client_socket.close()
        self.server.connection_manager.stop_all_threads()

    # def test_login(self):
    #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     client_socket.connect(self.server_address)
    #     data = "LOGIN mina 12345"
    #     client_socket.sendall(data.encode("utf-8"))
    #     response = client_socket.recv(1024)
    #     print(response.decode("utf-8"))
    #     client_socket.close()
    #     self.server.connection_manager.stop_all_threads()
