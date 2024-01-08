from server.DAO.RoomDAO import RoomDAO
from server.DAO.OnlineUserDAO import OnlineUserDAO


class RoomService:
    def __init__(self):
        self.room_dao = RoomDAO()
        self.online_user_dao = OnlineUserDAO()

    def get_rooms(self):
        return self.room_dao.get_all_rooms()

    def get_room(self, room_id):
        return self.room_dao.get_room(room_id)

    def create_room(self, username, room_id):
        if self.room_dao.get_room(room_id) is None and self.online_user_dao.get_user(username):
            self.room_dao.add_room(room_id)
            self.room_dao.add_user(room_id, username)
            return True
        else:
            return False

    def delete_room(self, room_id):
        if self.room_dao.get_room(room_id) is not None:
            self.room_dao.delete_room(room_id)
            return True
        else:
            return False

    def add_user(self, room_id, username):
        if self.room_dao.get_room(room_id) is not None:
            self.room_dao.add_user(room_id, username)
            return True
        else:
            return False

    def remove_user(self, room_id, username):
        if self.room_dao.get_room(room_id) is not None:
            self.room_dao.remove_user(room_id, username)
            if len(self.get_room_users(room_id)) == 0:
                self.room_dao.delete_room(room_id)
            return True
        else:
            return False

    def get_room_users(self, room_id):
        room = self.room_dao.get_room(room_id)
        if room is not None:
            return room["users"]
        else:
            return None
