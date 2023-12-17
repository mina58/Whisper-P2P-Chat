from server.DAO.OnlineUserDAO import OnlineUserDAO


class OnlineUserService:
    def __init__(self):
        self.online_user_dao = OnlineUserDAO()

    def get_online_user(self, username):
        return self.online_user_dao.get_user(username)

    def get_online_users(self):
        return self.online_user_dao.get_all_users()

    def add_online_user(self, username, ip, port):
        if self.online_user_dao.get_user(username) is None:
            self.online_user_dao.add_user(username, ip, port)
            return True
        else:
            return False

    def remove_online_user(self, username):
        if self.online_user_dao.get_user(username) is not None:
            self.online_user_dao.delete_user(username)
            return True
        else:
            return False

    def is_online(self, username):
        return self.online_user_dao.get_user(username) is not None
