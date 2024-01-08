from server.Network.ClientThread import ClientThread


class ConnectionManager:
    def __init__(self):
        self.client_threads = set()
        self.clients_count = 0

    def add_client(self, client_thread):
        self.client_threads.add(client_thread)

    def remove_client(self, client_thread):
        client_thread.stop()
        self.client_threads.remove(client_thread)

    def handle_connection(self, client_address, client_socket):
        client_thread = ClientThread(client_address, client_socket, self, f"client-{self.clients_count + 1}")
        self.clients_count += 1
        client_thread.start()

    def stop_all_threads(self):
        for client_thread in self.client_threads:
            client_thread.stop()
        self.client_threads.clear()

    def broadcast(self, message, sender):
        for client_thread in self.client_threads:
            if client_thread != sender:
                client_thread.send_message(message)
