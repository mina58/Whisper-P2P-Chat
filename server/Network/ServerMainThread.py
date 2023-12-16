import socket
import logging
import threading

class ServerMainThread(threading.Thread):
    def __init__(self, ip, port):
        super(ServerMainThread, self).__init__()
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.logger = None


    def configure_logger(self):
        self.logger = logging.getLogger("server-logger")
        self.logger.setLevel(level=logging.INFO)
        self.logger_file_handler = logging.FileHandler("server.log")
        self.logger_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.logger_file_handler.setFormatter(self.logger_formatter)
        self.logger.addHandler(self.logger_file_handler)


    def run(self):
        self.is_running = True

        self.configure_logger()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        
        self.logger.info(f"Server listening on {self.ip}:{self.port}")

        while self.is_running:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.logger.info(f"Connection from {client_address}")

                data = client_socket.recv(1024)
                self.logger.info(f"Received data: {data.decode('utf-8')}")

                response = "Hello, I am up and running :)"
                client_socket.send(response.encode("utf-8"))

                client_socket.close()
            except Exception as e:
                # Handle exceptions (e.g., if the server is stopped)
                self.logger.error(f"Error: {e}")


    def stop(self):
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
            self.logger.info("Server stopped")

