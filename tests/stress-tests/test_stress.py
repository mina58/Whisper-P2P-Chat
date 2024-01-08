import socket
import time
import unittest

from server.Network.ServerMainThread import ServerMainThread
from server.DAO.AccountDAO import AccountDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO
from client.Service.ServiceOrchestrator import ServiceOrchestrator


class TestStress(unittest.TestCase):

    def setUp(self):
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.server_port = 12121
        self.server_address = (self.server_ip_address, self.server_port)
        self.account_dao = AccountDAO()
        self.online_user_dao = OnlineUserDAO()
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.server = ServerMainThread(
            self.server_ip_address, self.server_port)
        self.server.start()
        time.sleep(0.5)

    def tearDown(self):
        self.account_dao.drop_collection()
        self.online_user_dao.drop_collection()
        self.server.stop()

    def test_stress_server(self):
        num_threads = 100
        orchestrators = [ServiceOrchestrator(
            self.server_ip_address) for i in range(num_threads) if time.sleep(0.1) or True]
        print("created")
        try:
            for username, orchestrator in enumerate(orchestrators):
                orchestrator.create_account(str(username), str(username))
                print(f"Loading... {username * 10}%", end='\r', flush=True)

            time.sleep(1)

            self.assertEqual(
                self.account_dao.count_accounts(), num_threads)
            for username, orchestrator in enumerate(orchestrators):
                orchestrator.login(str(username), str(username))
                print(f"Loading... {username * 10}%", end='\r', flush=True)

            time.sleep(1)

            self.assertEqual(
                self.online_user_dao.count_online_users(), num_threads)

        finally:
            for orchestrator in orchestrators:
                orchestrator.close()
