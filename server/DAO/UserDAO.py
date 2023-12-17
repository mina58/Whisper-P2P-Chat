from server.DB.get_db import get_db

class UserDAO:
    def __init__(self):
        self.db = get_db
    