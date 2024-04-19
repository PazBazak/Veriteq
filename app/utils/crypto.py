from typing import NewType

from cryptography.fernet import Fernet

EncryptionKey = NewType("EncryptionKey", bytes)


def generate_key() -> EncryptionKey:
    return EncryptionKey(Fernet.generate_key())


def encrypt_data(key: EncryptionKey, data: bytes) -> bytes:
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(data)


def decrypt_data(key: EncryptionKey, data: bytes) -> bytes:
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(data)
