import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


def decrypt(encrypted_password):
    fernet = Fernet(os.getenv("ENCRYPTION_KEY"))
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


def encrypt(password: str):
    fernet = Fernet(os.getenv("ENCRYPTION_KEY"))
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password
