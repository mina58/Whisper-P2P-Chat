from client.Network.ServerConnectionManager import ServerConnectionManager


class ServerAPI:
    def __init__(self, server_ip, server_port, to_chat_queue, name="peer"):
        self.server_connection_manager = ServerConnectionManager(
            server_ip, server_port, name, to_chat_queue)
        self.server_connection_manager.connect_to_server()
        self.username = None

    def login(self, username, password):
        self.server_connection_manager.send_login_message(
            username, password)
        response = self.server_connection_manager.get_response()
        if response["status_code"] == "1":
            self.username = username
            return True
        else:
            return False

    def create_account(self, username, password):
        self.server_connection_manager.send_create_account_message(
            username, password)
        response = self.server_connection_manager.get_response()

        if response["status_code"] == "1":
            self.username = username
            return True
        else:
            return False

    def logout(self):
        self.server_connection_manager.send_logout_message(self.username)

    def list_users(self):
        self.server_connection_manager.send_list_users_message()
        response = self.server_connection_manager.get_response()
        return response["users"]

    def list_rooms(self):
        self.server_connection_manager.send_list_rooms_message()
        response = self.server_connection_manager.get_response()
        return response["rooms"]

    def create_room(self, room_id):
        self.server_connection_manager.send_create_room_message(
            self.username, room_id)
        response = self.server_connection_manager.get_response()
        return response["status_code"] == "1"

    def leave_room(self, room_id):
        self.server_connection_manager.send_leave_room_message(
            self.username, room_id)

    def join_room(self, room_id, udp_port):
        self.server_connection_manager.send_join_room_message(
            self.username, room_id, udp_port)
        response = self.server_connection_manager.get_response()
        return response["status_code"] == "1"
