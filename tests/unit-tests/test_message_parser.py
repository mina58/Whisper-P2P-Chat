import unittest
from common.MessageParser import MessageParser


class TestMessageParser(unittest.TestCase):
    def setUp(self):
        self.username = "mina"
        self.password = "123456"
        self.room_id = "123"
        self.rooms = ["room_1", "room_2", "room_3"]
        self.users = ["user_1", "user_2", "user_3"]
        self.chat_message = "Hello, world!"
        self.ip = "127.0.0.1"
        self.port = "12345"
        self.udp_port = "54321"
        self.tcp_port = "12345"
        self.username2 = "maria"

    def test_create_acc(self):
        message = f"CREATE_ACC {self.username} {self.password}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "CREATE_ACC")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["password"], self.password)

    def test_create_acc_response_succ(self):
        message = "1 ACC_CREATED"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ACC_CREATED")
        self.assertEqual(content["status_code"], "1")

    def test_create_acc_response_fail(self):
        message = "0 USERNAME_TAKEN"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "USERNAME_TAKEN")
        self.assertEqual(content["status_code"], "0")

    def test_login(self):
        message = f"LOGIN {self.username} {self.password} {self.tcp_port}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LOGIN")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["password"], self.password)
        self.assertEqual(content["tcp_port"], self.tcp_port)

    def test_login_response_succ(self):
        message = f"1 LOGIN_SUCC"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LOGIN_SUCC")
        self.assertEqual(content["status_code"], "1")

    def test_login_response_fail(self):
        message = f"0 AUTH_FAIL"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "AUTH_FAIL")
        self.assertEqual(content["status_code"], "0")

    def test_logout(self):
        message = f"LOGOUT {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LOGOUT")
        self.assertEqual(content["username"], self.username)

    def test_create_room(self):
        message = f"CREATE_ROOM {self.username} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "CREATE_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)

    def test_create_room_response_succ(self):
        message = f"1 ROOM_CREATED"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ROOM_CREATED")
        self.assertEqual(content["status_code"], "1")

    def test_create_room_response_fail(self):
        message = f"0 ROOM_ID_UNAVAILABLE"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ROOM_ID_UNAVAILABLE")
        self.assertEqual(content["status_code"], "0")

    def test_list_rooms(self):
        message = f"LIST_ROOMS"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LIST_ROOMS")

    def test_rooms_list(self):
        message = f"1 ROOMS_LIST {' '.join(self.rooms)}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ROOMS_LIST")
        self.assertEqual(content["status_code"], "1")
        self.assertEqual(content["rooms"], self.rooms)

    def test_list_users(self):
        message = f"LIST_USERS"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LIST_USERS")

    def test_users_list(self):
        message = f"1 USERS_LIST {' '.join(self.users)}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "USERS_LIST")
        self.assertEqual(content["status_code"], "1")
        self.assertEqual(content["users"], self.users)

    def test_keep(self):
        message = f"KEEP {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "KEEP")

    def test_room_chat(self):
        message = f"CHAT_ROOM {self.username} {self.room_id} {self.chat_message}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "CHAT_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)
        self.assertEqual(content["message"], self.chat_message)

    def test_private_chat(self):
        message = f"CHAT_PRIVATE {self.username} {self.chat_message}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "CHAT_PRIVATE")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["message"], self.chat_message)

    def test_bye(self):
        message = f"BYE {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "BYE")
        self.assertEqual(content["username"], self.username)

    def test_join_room(self):
        message = f"JOIN_ROOM {self.username} {self.room_id} {self.udp_port}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "JOIN_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)
        self.assertEqual(content["udp_port"], self.udp_port)

    def test_request_info_room(self):
        message = f"REQUEST_INFO_ROOM {self.username} {self.ip} {self.port} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "REQUEST_INFO_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["ip"], self.ip)
        self.assertEqual(content["port"], self.port)
        self.assertEqual(content["room_id"], self.room_id)

    def test_request_info_private(self):
        message = f"REQUEST_INFO_PRIVATE {self.username2}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "REQUEST_INFO_PRIVATE")
        self.assertEqual(content["username"], self.username2)

    def test_peer_info_user(self):
        message = f"1 PEER_INFO_PRIVATE {self.username} {self.ip} {self.tcp_port}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "PEER_INFO_PRIVATE")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["ip"], self.ip)
        self.assertEqual(content["port"], self.tcp_port)

    def test_peer_info_room(self):
        message = f"PEER_INFO_ROOM {self.username} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "PEER_INFO_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)

    def test_already_joined(self):
        message = f"0 ALREADY_JOINED"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ALREADY_JOINED")
        self.assertEqual(content["status_code"], "0")

    def test_room_unavailable(self):
        message = f"0 ROOM_UNAVAILABLE"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ROOM_UNAVAILABLE")
        self.assertEqual(content["status_code"], "0")

    def test_leave_to_server(self):
        message = f"LEAVE_ROOM {self.username} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LEAVE_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)

    def test_leave_to_peers(self):
        message = f"LEFT_ROOM {self.username} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LEFT_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)

    def test_not_in_room(self):
        message = f"0 NOT_IN_ROOM"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "NOT_IN_ROOM")
        self.assertEqual(content["status_code"], "0")

    def test_chat_request(self):
        message = f"CHAT_REQUEST {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "CHAT_REQUEST")
        self.assertEqual(content["username"], self.username)

    def test_user_not_online(self):
        message = f"0 USER_NOT_AVAILABLE"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "USER_NOT_AVAILABLE")
        self.assertEqual(content["status_code"], "0")

    def test_accept_chat(self):
        message = f"1 ACCEPT_CHAT"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ACCEPT_CHAT")
        self.assertEqual(content["status_code"], "1")

    def test_reject_chat(self):
        message = f"0 REJECT_CHAT"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "REJECT_CHAT")
        self.assertEqual(content["status_code"], "0")
