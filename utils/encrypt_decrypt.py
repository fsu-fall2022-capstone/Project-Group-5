from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


def decrypt(encrypted_password):
    fernet = Fernet(os.getenv("s_key"))    # pass the secret key to fernet to create an instance
    decryptedPassword = fernet.decrypt(    # decrypts encrypted_password and sets it equal to decryptedPassword
        encrypted_password              
    ).decode()
    return decryptedPassword                

def encrypt(password):
    fernet = Fernet(os.getenv("s_key"))     # pass the secret key to fernet to create an instance
    encryptedPassword = fernet.encrypt(     # ecnrypts the password and sets it equal to encryptedPassword
        password.encode()
    )
    return encryptedPassword