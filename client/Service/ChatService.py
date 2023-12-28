from client.Network.ChatThread import ChatThread

import logging


class ChatService:
    def __init__(self, room_id, username, to_chat_queue):
        self.room_id = room_id
        self.username = username
        self.chat_thread = ChatThread(room_id, username, to_chat_queue)
        self.address = self.chat_thread.get_address()
        self.chat_thread.start()

    def get_address(self):
        return self.address

    def get_messages(self):
        return self.chat_thread.get_messages()

    def send_message(self, message):
        self.chat_thread.broadcast_message(message)

    def end_chat(self):
        self.chat_thread.stop()
        self.chat_thread.join()
        self.chat_thread.udp_socket.close()

