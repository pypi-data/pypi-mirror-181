# encoding: utf-8
# Date: 2022/12/13 09:53

__author__ = 'songt'

from enum import Enum
from Crypto.Cipher.AES import MODE_CBC, MODE_ECB


class AesMode(Enum):
    CBC = MODE_CBC
    ECB = MODE_ECB