#!/home/tao.liu1/anaconda/bin/python
# coding: utf8


import os
import logging
import hashlib
from datetime import datetime
import argparse
from flask import Flask, request

import aes
import mail
import conf


app = Flask(__name__)

aes_cipher = aes.AESCipher(conf.mail_relay_key)


@app.route('/mail_login', methods=['POST'])
def mail_login():
    enc_email, enc_password, sign = request.form['email'], request.form['password'], request.form['sign']
    email, password = aes_cipher.decrypt(enc_email), aes_cipher.decrypt(enc_password)
    logging.debug('email:%s, password:%s, sign:%s', email, password, sign)

    sign_computed = hashlib.sha1('%s:%s:%s' % (email, password, conf.mail_relay_key)).hexdigest()
    if sign != sign_computed:
        return '', 401

    login_ok = mail.pop3_login(email, password)
    return '', 200 if login_ok else 401


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    work_dir, _ = os.path.split(os.path.abspath(__file__))
    log_dir = work_dir + '/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    console_handler = logging.StreamHandler()
    file_suffix = datetime.today().strftime('%Y%m%d')
    logfile_name = '%s/%s.%s' % (log_dir, 'mail_relay.log', file_suffix)
    file_handler = logging.FileHandler(logfile_name)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


init_logger()
mail.connect_mailbox()
logging.info('mail relay started')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5001, help='Service Port')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=False)
