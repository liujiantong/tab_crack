#!/home/tao.liu1/anaconda/bin/python
# coding: utf8


import os
import logging
from datetime import datetime
import argparse
from flask import Flask, request

import mail


app = Flask(__name__)


@app.route('/mail_login', methods=['POST'])
def mail_login():
    email, password = request.form['email'], request.form['password']
    logging.debug('email:%s, password:%s', email, password)

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
    file_suffix = datetime.strftime(datetime.today(), '%Y%m%d')
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
