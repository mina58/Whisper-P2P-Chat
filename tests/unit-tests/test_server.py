import unittest
import socket
from server.Network.ServerMainThread import ServerMainThread

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.server = ServerMainThread(self.server_ip_address, self.server_port)
        self.server.start()
        
        
    def tearDown(self):
        self.server.stop()
        
    
    
    def test_server_connection(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.server_address)
        data = "Hello, this is a test!"
        client_socket.sendall(data.encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode("utf-8"))
        client_socket.close()


if __name__ == "__main__":
    unittest.main()