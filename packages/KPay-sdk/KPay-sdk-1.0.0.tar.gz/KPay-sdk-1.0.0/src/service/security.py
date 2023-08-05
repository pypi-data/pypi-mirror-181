import hmac
import hashlib
from datetime import datetime
import math
import hashlib
from Crypto.Cipher import AES
import base64

class Security:
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls)

    def genarateSign(self, data, clientId, timestamp, secretKey):
        message = clientId + "|" + str(timestamp) + "|" + str(data)
        signature = hmac.new(
            bytes(secretKey, 'utf-8'),
            msg=bytes(message, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return signature

    def verifySign(self, data: str, dataVilidate: str, clientId: str, timestamp: int, secretKey: str) -> bool:
        dt = datetime.now()
        if (timestamp > math.floor(datetime.timestamp(dt) * 1000)):
            return False
        sign = self.genarateSign(data, clientId, timestamp, secretKey)
        if (dataVilidate != sign):
            return False
        return True

    def aesEcrypt(self, data: str, encryptKey: str):
        key = bytes.fromhex(encryptKey)
        data_bytes = bytes(data, 'utf8')
        data_pad = self.__pad(data_bytes)
        cipher = AES.new(key, AES.MODE_CBC, key[0:16])
        encrypt = cipher.encrypt(data_pad)
        return base64.b64encode(encrypt)

    def aesDecrypt(self, data: str, encryptKey: str):
        key = bytes.fromhex(encryptKey)
        message = base64.b64decode(data)
        cipher = AES.new(key, AES.MODE_CBC, key[0:16])
        decrypt = cipher.decrypt(message)
        return self.__unpad(decrypt.decode('utf-8'))

    def __pad(self,byte_array:bytearray, block_size: int=16):
        """
        pkcs5 padding
        """
        pad_len = block_size - len(byte_array) % block_size
        return byte_array + (bytes([pad_len]) * pad_len)

    def __unpad(self,byte_array:bytearray):
        return byte_array[:-ord(byte_array[-1:])]