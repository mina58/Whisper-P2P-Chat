from server.DB.get_db import get_db


class RoomDAO:
    def __init__(self):
        self.db = get_db()

    def get_room(self, room_id):
        return self.db.rooms.find_one({"room_id": room_id})

    def add_room(self, room_id):
        self.db.rooms.insert_one({"room_id": room_id, "users": []})

    def delete_room(self, room_id):
        self.db.rooms.delete_one({"room_id": room_id})

    def drop_collection(self):
        self.db.rooms.drop()

    def get_all_rooms(self):
        return self.db.rooms.find()

    def add_user(self, room_id, username):
        self.db.rooms.update_one({"room_id": room_id}, {
                                 "$push": {"users": username}})

    def remove_user(self, room_id, username):
        self.db.rooms.update_one({"room_id": room_id}, {
                                 "$pull": {"users": username}})
