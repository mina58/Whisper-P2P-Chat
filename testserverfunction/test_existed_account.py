from server.DB.get_db import get_db


class AccountDAO:
    def __init__(self):
        self.db = get_db()

    def get_account(self, username):
        account = self.db.accounts.find_one({"username": username})
        return account is not None

    def add_account(self, username, password):
        if self.get_account(username):
            return False  

        self.db.accounts.insert_one(
            {"username": username, "password": password})
        return True  

  
