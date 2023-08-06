from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BLOCK_SIZE = 16

def encrypt(msg: bytes, d2l_key: bytes, d2l_iv: bytes):
    cipher = AES.new(d2l_key, AES.MODE_CBC, d2l_iv)
    return cipher.encrypt(msg)


def decrypt(msg: bytes, d2l_key: bytes, d2l_iv: bytes) -> bytes:
    if len(msg) % BLOCK_SIZE:
        msg = pad(msg, BLOCK_SIZE)
    cipher = AES.new(d2l_key, AES.MODE_CBC, d2l_iv)
    return cipher.decrypt(msg)
