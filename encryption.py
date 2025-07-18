from cryptography.fernet import Fernet
import os

key_file = 'key.key'

if not os.path.exists(key_file):
    with open(key_file, 'wb') as f:
        f.write(Fernet.generate_key())

with open(key_file, 'rb') as f:
    key = f.read()

cipher = Fernet(key)

def encrypt_message(msg):
    return cipher.encrypt(msg.encode()).decode()

def decrypt_message(token):
    return cipher.decrypt(token.encode()).decode()
