import unittest
from common.MessageParser import MessageParser


# class MessageParser:
#     @staticmethod
#     def parse_message(input_message):
#         try:
#             input_message = input_message.strip()
#             words = input_message.split()
#             content = {}

#             if words[0] not in ['0', '1']:
#                 message_type = words[0]

#                 # User Requests & Peers Responses
#                 if message_type in ["CREATE_ACC", "LOGIN", "LOGOUT", "CREATE_ROOM", "LIST_ROOMS",
#                                     "LIST_USERS", "KEEP", "CHAT", "BYE", "JOIN_ROOM", "LEAVE_ROOM",
#                                     "CHAT_REQUEST", "REQUEST_INFO", "PEER_INFO", "LEAVE"]:
#                     content = {"message_type": message_type}
#                     if message_type in ["CREATE_ACC", "LOGIN", "LOGOUT", "CREATE_ROOM",
#                                         "KEEP", "CHAT", "BYE", "JOIN_ROOM", "LEAVE_ROOM", "CHAT_REQUEST", "REQUEST_INFO", "PEER_INFO", "LEAVE"]:
#                         content["username"] = words[1]

#                     if message_type in ["CREATE_ACC", "LOGIN", "CHAT_REQUEST"]:
#                         content["password"] = words[2]

#                     if message_type == "REQUEST_INFO":
#                         content["ip"] = words[2]
#                         content["port"] = int(words[3])
#                         if len(words) == 5:
#                             content["room_id"] = words[4]

#                     if message_type == "PEER_INFO" and len(words) == 3:
#                         content["room_id"] = words[2]

#                     if message_type == "CHAT":
#                         content["chat_message"] = " ".join(words[2:])

#                     if message_type == "JOIN_ROOM":
#                         content["room_id"] = words[2]

#                     if message_type == "LEAVE" and len(words) == 3:
#                         content["room_id"] = words[2]

#             else:
#                 message_type = words[1]

#                 # Server Responses
#                 if words[0] == '1':
#                     if message_type == "ACC_CREATED":
#                         content = {
#                             "status_code": words[0], "message_type": message_type}
#                     elif message_type == "LOGIN_SUCC":
#                         content = {
#                             "status_code": words[0], "message_type": message_type}
#                 elif words[0] == '0':
#                     if message_type == "USERNAME_TAKEN":
#                         content = {
#                             "status_code": words[0], "message_type": message_type}
#                     elif message_type == "AUTH_FAIL":
#                         content = {
#                             "status_code": words[0], "message_type": message_type}

#                 if message_type in ["ROOM_CREATED", "ROOM_LIST", "USERS_LIST"]:
#                     content["status_code"] = words[0]
#                     content["message_type"] = words[1]
#                     if message_type == "ROOM_CREATED":
#                         content["room_id"] = words[2]
#                     elif message_type == "ROOM_LIST":
#                         content["rooms"] = words[2:]
#                     elif message_type == "USERS_LIST":
#                         content["users"] = words[2:]

#                 if message_type in ["ROOM_UNAVAILABLE", "ALREADY_JOINED", "NOT_IN_ROOM", "USER_NOT_ONLINE"]:
#                     content = {
#                         "status_code": words[0], "message_type": message_type}

#             return content

#         except Exception as e:
#             print(f"Error parsing the message: {e}")
#             return None


class TestMessageParser(unittest.TestCase):
    def setUp(self):
        self.username = "mina"
        self.password = "123456"
        self.room_id = "123"
        self.rooms = ["room_1", "room_2", "room_3"]
        self.users = ["user_1", "user_2", "user_3"]
        self.chat_message = "Hello, world!"
        self.ip = "127.0.0.1"
        self.port = 12345

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
        message = f"LOGIN {self.username} {self.password}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LOGIN")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["password"], self.password)

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
        message = f"CREATE_ROOM {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "CREATE_ROOM")
        self.assertEqual(content["username"], self.username)

    def test_create_room_response(self):
        message = f"1 ROOM_CREATED {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ROOM_CREATED")
        self.assertEqual(content["status_code"], "1")
        self.assertEqual(content["room_id"], self.room_id)

    def test_list_rooms(self):
        message = f"LIST_ROOMS"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LIST_ROOMS")

    def test_rooms_list(self):
        message = f"1 ROOM_LIST {' '.join(self.rooms)}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "ROOM_LIST")
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

    def test_chat(self):
        message = f"CHAT {self.username} {self.chat_message}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "CHAT")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["chat_message"], self.chat_message)

    def test_bye(self):
        message = f"BYE {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "BYE")
        self.assertEqual(content["username"], self.username)

    def test_join_room(self):
        message = f"JOIN_ROOM {self.username} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "JOIN_ROOM")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)

    def test_request_info_room(self):
        message = f"REQUEST_INFO {self.username} {self.ip} {self.port} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "REQUEST_INFO")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["ip"], self.ip)
        self.assertEqual(content["port"], self.port)
        self.assertEqual(content["room_id"], self.room_id)

    def test_request_info_user(self):
        message = f"REQUEST_INFO {self.username} {self.ip} {self.port}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "REQUEST_INFO")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["ip"], self.ip)
        self.assertEqual(content["port"], self.port)

    def test_peer_info_room(self):
        message = f"PEER_INFO {self.username} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "PEER_INFO")
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["room_id"], self.room_id)

    def test_peer_info_user(self):
        message = f"PEER_INFO {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "PEER_INFO")
        self.assertEqual(content["username"], self.username)

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
        message = f"LEAVE {self.username}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LEAVE")
        self.assertEqual(content["username"], self.username)

    def test_leave_to_peers(self):
        message = f"LEAVE {self.username} {self.room_id}"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "LEAVE")
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
        message = f"0 USER_NOT_ONLINE"
        content = MessageParser.parse_message(message)
        self.assertEqual(content["message_type"], "USER_NOT_ONLINE")
        self.assertEqual(content["status_code"], "0")
