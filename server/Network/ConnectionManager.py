from server.Network.ClientThread import ClientThread


class ConnectionManager:
    def __init__(self):
        self.client_threads = set()

    def add_client(self, client_thread):
        self.client_threads.add(client_thread)

    def remove_client(self, client_thread):
        self.stop_thread(client_thread)
        self.client_threads.remove(client_thread)

    def handle_connection(self, client_address, client_socket):
        client_thread = ClientThread(client_address, client_socket)
        self.add_client(client_thread)
        client_thread.start()

    def stop_thread(self, client_thread):
        client_thread.stop()

    def stop_all_threads(self):
        for client_thread in self.client_threads:
            self.stop_thread(client_thread)
        self.client_threads.clear()
