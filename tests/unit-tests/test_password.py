import unittest
from common.password import Password

class Test(unittest.TestCase):
    def test_encryption_true(self):
        password_manager = Password()

        plaintext_password = "yellow"
        encrypted_password = password_manager.encrypt(plaintext_password)

        input_password = "yellow"
        self.assertTrue(password_manager.decrypt(encrypted_password, input_password))

    def test_decryption_false(self):
        password_manager = Password()

        plaintext_password = "hello."
        encrypted_password = password_manager.encrypt(plaintext_password)

        input_password = "red"
        self.assertFalse(password_manager.decrypt(encrypted_password, input_password))



# if __name__ == "__main__":
#     unittest.main()