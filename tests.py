#!/usr/bin/env python

import unittest

import requests
from aes import AESCipher
import conf

aes_cipher = AESCipher(conf.mail_relay_key)


def mail_pop3_login(email, passwd):
    payload = {
        'email': aes_cipher.encrypt(email),
        'password': aes_cipher.encrypt(passwd)
    }
    r = requests.post('http://localhost:5001/mail_login', data=payload)
    return r.status_code == 200


class TestCipherMailLogin(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
