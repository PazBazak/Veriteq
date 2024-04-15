from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_data(key, data):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(data.encode())

def decrypt_data(key, data):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(data).decode()