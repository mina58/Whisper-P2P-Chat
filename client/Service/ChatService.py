from client.Network.ChatThread import ChatThread

import logging


class ChatService:
    def __init__(self, room_id, username, to_chat_queue):
        self.room_id = room_id
        self.username = username
        self.chat_thread = ChatThread(room_id, username, to_chat_queue)
        self.address = self.chat_thread.get_address()
        self.chat_thread.start()
        self.to_chat_queue = to_chat_queue

    def get_address(self):
        return self.address

    def get_messages(self):
        messages_json = self.chat_thread.get_messages()
        messages = [
            f'{message["username"]}: {message["message"]}' for message in messages_json]
        return messages

    def send_message(self, message):
        self.chat_thread.broadcast_message(message)
        message = {
            "username": self.username,
            "message": message,
            "message_type": "CHAT_ROOM",
            "room_id": self.room_id
        }
        self.to_chat_queue.put(message)

    def end_chat(self):
        self.chat_thread.stop()
        self.chat_thread.join()
        self.chat_thread.udp_socket.close()
