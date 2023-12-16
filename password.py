import argon2


class Password:
    def encrypt(self, password):
        hasher=argon2.PasswordHasher()
        encrypted_password=hasher.hash(password)
        return encrypted_password
    

    def decrypt(self, encrypted_password,password):

        hasher=argon2.PasswordHasher()
        try:
            hasher.verify(encrypted_password,password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        

if __name__ == "__main__":
   password_manager = Password()

   
plaintext_password = "my_secure_password"
encrypted_password = password_manager.encrypt(plaintext_password)
print("Encrypted Password:", encrypted_password)

  
input_password = input("Enter password to verify: ")
if password_manager.decrypt(encrypted_password, input_password):
    print("Password is valid!")
else:
      print("Password is invalid.")


   





































# from argon2 import PasswordHasher

# # Create an instance of PasswordHasher
# class Password:
#     def __init__(self):
#         self.ph = PasswordHasher()

#     def encrypt(self, plaintext_password):
#         """
#         Encrypt a plaintext password using Argon2.

#         Parameters:
#         - plaintext_password (str): The password to be encrypted.

#         Returns:
#         - str: The encrypted password.
#         """
#         hashed_password = self.ph.hash(plaintext_password)
#         return hashed_password

#     def decrypt(self, hashed_password, input_password):
#         """
#         Decrypt a hashed password and check if it matches the input password.

#         Parameters:
#         - hashed_password (str): The hashed password to be checked.
#         - input_password (str): The password to be compared.

#         Returns:
#         - bool: True if the passwords match, False otherwise.
#         """
#         try:
#             self.ph.verify(hashed_password, input_password)
#             return True
#         except Exception as e:
#             print("Password verification failed:", e)
#             return False

# # Example usage:
# if __name__ == "__main__":
#     password_manager = Password()

#     # Encrypt a password
#     encrypted_password = password_manager.encrypt("my_secure_password")
#     print("Encrypted Password:", encrypted_password)

#     # Decrypt and verify a password
#     input_password = input("Enter password to verify: ")
#     if password_manager.decrypt(encrypted_password, input_password):
#         print("Password is valid!")
#     else:
#         print("Password is invalid.")

