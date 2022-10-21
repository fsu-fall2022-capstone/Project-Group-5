from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


def decrypt(encrypted_password):
    fernet = Fernet(os.getenv("s_key"))  #pass the secret key to fernet to create an instance
    decryptPassword = fernet.decrypt(
        encrypted_password              
    ).decode()

def encrypt(password):
    fernet = Fernet(os.getenv("s_key"))
    encryptedPassword = fernet.encrypt(
        password.encode()
    )