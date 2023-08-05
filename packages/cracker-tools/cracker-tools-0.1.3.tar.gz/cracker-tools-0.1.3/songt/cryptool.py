# encoding: utf-8
# Date: 2022/12/12 14:27
# 方法命名规范： base64(content) 和 base64_decode()
__author__ = 'songt'
import hashlib
import base64 as b64
from Crypto.Cipher import AES
from constants import AesMode

def md5(content):
    """
    md5
    :param content:
    :return:
    """
    hash = hashlib.md5()
    hash.update(content.encode('utf-8'))
    return hash.hexdigest()


def base64(content):
    return b64.b64encode(content.encode('utf-8')).decode('utf-8')


def base64_decode(content):
    return b64.b64decode(content.encode('utf-8'))


def aes(plain_text: bytes, key: bytes, iv: bytes = b'', mode=AesMode.CBC):

    if mode == AES.MODE_CBC:
        aes = AES.new(key, AES.MODE_CBC, iv)
    elif mode == AES.MODE_ECB:
        aes = AES.new(key, mode)
    return aes.encrypt(plain_text)


def aes_decrypt(plain_text: bytes, key: bytes, iv: bytes = b'', mode=AES.MODE_CBC):
    if mode == AES.MODE_CBC:
        aes = AES.new(key, AES.MODE_CBC, iv)
    elif mode == AES.MODE_ECB:
        aes = AES.new(key, mode)
    return aes.decrypt(plain_text)


if __name__ == '__main__':
    # 1.md5
    print("md5:", md5('s'))
    # 2.base64 encode
    print("base64:", base64('s'))
    # 3.base64 decode
    print("base64_encode:", base64_decode(base64('s')))
    # 4.aes
    key = b'1234567812345678'
    iv = b'1234567812345678'
    plain_text = '好好学习天天向上'.encode("gbk")
    aes_enc = aes(plain_text, key=key, mode=AES.MODE_ECB)
    print("aes:", aes_enc)
    # 5.aes decrypt
    aes_de = aes_decrypt(aes_enc, key=key, mode=AES.MODE_ECB)
    print("aes decrypt:", aes_de)
    print(aes_de.decode("gbk"))

