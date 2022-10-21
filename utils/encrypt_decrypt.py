from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


def decrypt(encrypted_password):
    fernet = Fernet(os.getenv("s_key"))
    decryptedPassword = fernet.decrypt(    
        encrypted_password              
    ).decode()
    return decryptedPassword                

def encrypt(password):
    fernet = Fernet(os.getenv("s_key"))     
    encryptedPassword = fernet.encrypt(     
        password.encode()
    )
    return encryptedPassword