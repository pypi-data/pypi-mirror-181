from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class AesHelper:
    def __init__(self, rawKey: bytes) -> None:
        self._rawKey = rawKey

    def encrypt(self, clearMessage: str) -> str:
        cipher = AES.new(self._rawKey, AES.MODE_CBC)
        clearBytes = clearMessage.encode("utf-8")
        encrypted = cipher.encrypt(pad(clearBytes, 16, "pkcs7"))
        encrypted = cipher.iv + encrypted
        return b64encode(encrypted).decode('utf-8')

    def decrypt(self, cipherMessage: str) -> str:
        fullData = b64decode(cipherMessage)
        iv = fullData[0:16]
        cipherData = fullData[16:]
        cipher = AES.new(self._rawKey, AES.MODE_CBC, iv)
        ctBytes = unpad(cipher.decrypt(cipherData), AES.block_size)
        return ctBytes.decode("utf-8")

def isBase64(s: str) -> bool:
    try:
        return b64encode(b64decode(s)).decode("utf-8") == s
    except Exception:
        return False