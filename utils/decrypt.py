from typing import Collection
from cryptography.fernet import Fernet
from dotenv import load_dotenv


encryptPassword = b'gAAAAABjUcFBvMfpihkC-lyLPCcV-yvFdzrBjy4MyRgfKjkUJKVwLYHweeBNLYplGvU-Yf-O9xO8KYKsV1KZAKoAcbTpmeeLWQ==' #pull of password from database
                        
fernet = Fernet(key)  #pass the key to fernet 
decryptPassword = fernet.decrypt(encryptPassword).decode() #decrypted the encrypted password that is eventually pulled from the database

print("decrypted password: ", decryptPassword)
