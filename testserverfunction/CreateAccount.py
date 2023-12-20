import socket
import unittest
from server.Network.ServerMainThread import ServerMainThread

class CreateAcc(unittest.TestCase):
    def setUp(self):
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.server = ServerMainThread(
            self.server_ip_address, self.server_port)
        self.server.start()

    def tearDown(self):
         self.server.stop()

    def send_create_account_request():
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ( 12121)
        client_socket.connect(server_address)

        try:
            request = f"CREATE_ACC mina123 AnaMina123"
            client_socket.sendall(request.encode())

            response = client_socket.recv(1024)
            print(f"Server Response: {response.decode()}")

        finally:
            client_socket.close()

    def test_account_creation(self): 
        server_host ='localhost'
        server_port = 12121 
        new_username = 'mina123'
        new_password = 'AnaMina123'

            # self.send_create_account_request(server_host, server_port, new_username, new_password)
            
            # account_exists = self.server.account_dao.get_account(new_username)
            # self.assertTrue(account_exists)

        request_successful = self.send_create_account_request(server_host, server_port, new_username, new_password)
        self.assertTrue(request_successful)

        account_exists = self.server.account_dao.get_account(new_username)  
        self.assertTrue(account_exists) 

        if not request_successful:
             non_existent_account = self.server.account_dao.get_account("non_existent_username")
             self.assertIsNone(non_existent_account)
       

if __name__ == "__main__":
    unittest.main()
        
        