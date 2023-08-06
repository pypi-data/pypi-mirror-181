import base64
import hashlib
import logging

from Crypto import Random
from Crypto.Cipher import AES

logger = logging.getLogger(__name__)


class AESCipher(object):
    """ Utility class for encrypting and decrypting a string.

    Args:
        secret_key: The secret key for encryption.
    """

    def __init__(self, secret_key):
        self.BS = 16
        self.key = hashlib.sha256(secret_key.encode()).digest()

    def _pad(self, s):
        return s + (self.BS - len(s) % self.BS) * \
            chr(self.BS - len(s) % self.BS)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        """ Encrypts a `raw` string.

        Args:
            raw: The string to encrypt.
        """
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode("utf8")))

    def decrypt(self, enc):
        """ Decrypts a string.

        Args:
            enc: The encrypted string.
        """
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(
            enc[AES.block_size:])).decode('utf-8')
