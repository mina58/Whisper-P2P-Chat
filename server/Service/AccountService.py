from server.DAO.AccountDAO import AccountDAO
from common.PasswordHasher import PasswordHasher


class AccountService:
    def __init__(self):
        self.account_dao = AccountDAO()
        self.password_hasher = PasswordHasher()

    def create_account(self, username, password):
        if self.account_dao.get_account(username) is None:
            hashed_password = self.password_hasher.encrypt(password)
            self.account_dao.add_account(username, hashed_password)
            return True
        else:
            return False

    def login(self, username, password):
        if self.account_dao.get_account(username) is not None:
            correct_password = self.account_dao.get_account(username)[
                "password"]
            return self.password_hasher.decrypt(correct_password, password)
        else:
            return False
