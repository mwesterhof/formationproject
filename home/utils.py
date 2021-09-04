# TODO: investigate if it makes sense to just generate random key and iv
# this would invalidate a token open restart
from base64 import b64encode, b64decode
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class TokenProcessor:
    def __init__(self):
        key = os.urandom(32)
        self.iv = os.urandom(16)
        self.cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv))

    def generate_token(self, page_id, block_id):
        to_encrypt = bytes(f'{str(page_id).ljust(11)}:{block_id}', 'utf-8')
        encryptor = self.cipher.encryptor()
        return str(
            b64encode(encryptor.update(to_encrypt) + encryptor.finalize()),
            'utf-8'
        )

    def unpack_token(self, token_encoded):
        token = b64decode(token_encoded)
        decryptor = self.cipher.decryptor()
        decrypted = decryptor.update(token) + decryptor.finalize()
        page_id, block_id = str(decrypted, 'utf-8').split(':')
        page_id = int(page_id)
        return page_id, block_id


token_processor = TokenProcessor()
