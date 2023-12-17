from server.DB.get_db import get_db


class AccountDAO:
    def __init__(self):
        self.db = get_db()

    def get_account(self, username):
        return self.db.accounts.find_one({"username": username})

    def add_account(self, username, password):
        self.db.accounts.insert_one(
            {"username": username, "password": password})

    def delete_account(self, username):
        self.db.accounts.delete_one({"username": username})

    def drop_collection(self):
        self.db.accounts.drop()
