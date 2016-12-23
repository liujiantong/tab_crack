#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import logging
import smtplib
import conf


def email_login(email, passwd):
    logging.debug('login by email:%s', email)
    try:
        smtp = smtplib.SMTP(conf.mail_server)
        code, _ = smtp.login(email, passwd)
        smtp.quit()
    except Exception as e:
        logging.error('email_login error: %s', e)
        return False

    logging.debug('smtp response code:%d', code)
    return int(code/100) == 2


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.DEBUG)
    st = time.time()
    assert email_login("auth@ikang.com", "Ikang@$1jk!")
    print 'I took %d ms to login' % int((time.time()-st) * 1000)

