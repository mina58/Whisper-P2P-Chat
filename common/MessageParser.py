class MessageParser:
    @staticmethod
    def parse_message(input_message):
        try:
            input_message = input_message.strip()
            words = input_message.split()
            content = {}

            if words[0] not in ['0', '1']:
                message_type = words[0]

                # User Requests & Peers Responses
                if message_type in ["CREATE_ACC", "LOGIN", "LOGOUT", "CREATE_ROOM", "LIST_ROOMS",
                                    "LIST_USERS", "KEEP", "CHAT", "BYE", "JOIN_ROOM", "LEAVE_ROOM",
                                    "CHAT_REQUEST", "REQUEST_INFO", "PEER_INFO", "LEAVE"]:
                    content = {"message_type": message_type}
                    if message_type in ["CREATE_ACC", "LOGIN", "LOGOUT", "CREATE_ROOM",
                                        "KEEP", "CHAT", "BYE", "JOIN_ROOM", "LEAVE_ROOM", "CHAT_REQUEST", "REQUEST_INFO", "PEER_INFO", "LEAVE"]:
                        content["username"] = words[1]

                    if message_type in ["CREATE_ACC", "LOGIN"]:
                        content["password"] = words[2]

                    if message_type == "REQUEST_INFO":
                        content["ip"] = words[2]
                        content["port"] = int(words[3])
                        if len(words) == 5:
                            content["room_id"] = words[4]

                    if message_type == "PEER_INFO" and len(words) == 3:
                        content["room_id"] = words[2]

                    if message_type == "CHAT":
                        content["chat_message"] = " ".join(words[2:])

                    if message_type == "JOIN_ROOM":
                        content["room_id"] = words[2]

                    if message_type == "LEAVE" and len(words) == 3:
                        content["room_id"] = words[2]

            else:
                message_type = words[1]

                # Server Responses
                if words[0] == '1':
                    if message_type == "ACC_CREATED":
                        content = {
                            "status_code": words[0], "message_type": message_type}
                    elif message_type == "LOGIN_SUCC":
                        content = {
                            "status_code": words[0], "message_type": message_type}
                elif words[0] == '0':
                    if message_type == "USERNAME_TAKEN":
                        content = {
                            "status_code": words[0], "message_type": message_type}
                    elif message_type == "AUTH_FAIL":
                        content = {
                            "status_code": words[0], "message_type": message_type}

                if message_type in ["ROOM_CREATED", "ROOM_LIST", "USERS_LIST"]:
                    content["status_code"] = words[0]
                    content["message_type"] = words[1]
                    if message_type == "ROOM_CREATED":
                        content["room_id"] = words[2]
                    elif message_type == "ROOM_LIST":
                        content["rooms"] = words[2:]
                    elif message_type == "USERS_LIST":
                        content["users"] = words[2:]

                if message_type in ["ROOM_UNAVAILABLE", "ALREADY_JOINED", "NOT_IN_ROOM", "USER_NOT_ONLINE"]:
                    content = {
                        "status_code": words[0], "message_type": message_type}

            return content

        except Exception as e:
            print(f"Error parsing the message: {e}")
            return None
