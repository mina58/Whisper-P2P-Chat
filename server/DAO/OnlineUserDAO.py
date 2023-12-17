from server.DB.get_db import get_db


class OnlineUserDAO:
    def __init__(self):
        self.db = get_db()

    def get_user(self, username):
        return self.db.online_users.find_one({"username": username})

    def add_user(self, username, ip, port):
        self.db.online_users.insert_one({
            "username": username,
            "ip": ip,
            "port": port
        })

    def delete_user(self, username):
        self.db.online_users.delete_one({"username": username})

    def drop_collection(self):
        self.db.online_users.drop()

    def get_all_users(self):
        return self.db.online_users.find()
