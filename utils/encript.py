from typing import Collection
from cryptography.fernet import Fernet
from dotenv import load_dotenv

password = "test" #query from databse

key = b'3tUuiRRx1aKsEeBX3S8JMcMkgMT1wkftur1Ss7dHf_M='  #store secret key in .env
fernet = Fernet(key)    # create fernet instance of the key

encryptPassword = fernet.encrypt(password.encode()) #pass the password to be encrypted and then post that to database

print("original password: ", password)
print("encrypted password: ", encryptPassword)
print("key: ", key)

