import argon2


class PasswordHasher:
    def encrypt(self, password):
        hasher = argon2.PasswordHasher()
        encrypted_password = hasher.hash(password)
        return encrypted_password

    def decrypt(self, encrypted_password, password):
        hasher = argon2.PasswordHasher()
        try:
            hasher.verify(encrypted_password, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
