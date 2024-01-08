from common.ErrorLogger import ErrorLogger


class MessageParser:
    @staticmethod
    def parse_message(input_message):
        try:
            input_message = input_message.strip()
            words = input_message.split()
            content = {}

            if words[0] not in ['0', '1']:
                message_type = words[0]

                if message_type == "CREATE_ACC":
                    content["username"] = words[1]
                    content["password"] = words[2]
                elif message_type == "LOGIN":
                    content["username"] = words[1]
                    content["password"] = words[2]
                    content["tcp_port"] = words[3]
                elif message_type == "LOGOUT":
                    content["username"] = words[1]
                elif message_type == "CREATE_ROOM":
                    content["username"] = words[1]
                    content["room_id"] = words[2]
                elif message_type == "JOIN_ROOM":
                    content["username"] = words[1]
                    content["room_id"] = words[2]
                    content["udp_port"] = words[3]
                elif message_type == "REQUEST_INFO_ROOM":
                    content["username"] = words[1]
                    content["ip"] = words[2]
                    content["port"] = words[3]
                    content["room_id"] = words[4]
                elif message_type == "PEER_INFO_ROOM":
                    content["username"] = words[1]
                    content["room_id"] = words[2]
                elif message_type == "LEAVE_ROOM":
                    content["username"] = words[1]
                    content["room_id"] = words[2]
                elif message_type == "LEFT_ROOM":
                    content["username"] = words[1]
                    content["room_id"] = words[2]
                elif message_type == "KEEP":
                    content["username"] = words[1]
                elif message_type == "CHAT_REQUEST":
                    content["username"] = words[1]
                elif message_type == "REQUEST_INFO_PRIVATE":
                    content["username"] = words[1]
                elif message_type == "CHAT_PRIVATE":
                    content["username"] = words[1]
                    content["message"] = " ".join(words[2:])
                elif message_type == "BYE":
                    content["username"] = words[1]
                elif message_type == "CHAT_ROOM":
                    content["username"] = words[1]
                    content["room_id"] = words[2]
                    content["message"] = " ".join(words[3:])

                content["message_type"] = message_type

            else:
                message_type = words[1]
                status_code = words[0]
                content["message_type"] = message_type
                content["status_code"] = status_code

                if message_type == "USERS_LIST":
                    content["users"] = words[2:]
                elif message_type == "ROOMS_LIST":
                    content["rooms"] = words[2:]
                elif message_type == "PEER_INFO_PRIVATE":
                    content["username"] = words[2]
                    content["ip"] = words[3]
                    content["port"] = words[4]

            return content

        except Exception as e:
            ErrorLogger.get_logger().error(f"Error parsing the message: {e}")
            return None
