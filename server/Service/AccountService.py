from server.DAO.AccountDAO import AccountDAO


class AccountService:
    def __init__(self):
        self.account_dao = AccountDAO()

    def create_account(self, username, password):
        if self.account_dao.get_account(username) is None:
            self.account_dao.add_account(username, password)
            return True
        else:
            return False

    def login(self, username, password):
        if self.account_dao.get_account(username) is not None:
            return self.account_dao.get_account(username)["password"] == password
        else:
            return False
