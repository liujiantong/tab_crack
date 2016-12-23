#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import smtplib
import logging
import conf


def email_login(email, passwd):
    logging.debug('login by email:%s', email)
    smtp = smtplib.SMTP()
    connected = False
    for i in xrange(3):
        try:
            code, _ = smtp.connect(conf.mail_server)
            if int(code/100) == 2:
                connected = True
                break
            else:
                logging.warning('connection %d failed', i)
                time.sleep(1 + 0.5*i)
        except Exception as e:
            logging.warning('connect to `%s` error: `%s`', conf.mail_server, e)

    if not connected:
        return False

    code, _ = smtp.login(email, passwd)
    smtp.close()
    return int(code/100) == 2


if __name__ == '__main__':
    import time
    st = time.time()
    assert email_login("auth@ikang.com", "Ikang@$1jk!")
    print 'I took %d ms to login' % int((time.time()-st) * 1000)

