#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import logging
import smtplib
import poplib
import conf


mailbox_login_timeout = 5


def connect_mailbox():
    try:
        pop3 = poplib.POP3(conf.mail_server, timeout=mailbox_login_timeout)
        pop3.quit()
    except Exception as e:
        logging.error('connect_mailbox error: %s', e)
        return False

    logging.info('connected to `%s`', conf.mail_server)
    return True


def smtp_login(email, passwd):
    logging.debug('login by email:%s', email)
    try:
        smtp = smtplib.SMTP(conf.mail_server, timeout=mailbox_login_timeout)
        code, _ = smtp.login(email, passwd)
        smtp.quit()
    except Exception as e:
        logging.error('smtp_login error: %s', e)
        return False

    logging.debug('smtp response code:%d', code)
    return int(code/100) == 2


def pop3_login(email, passwd):
    logging.debug('login by email:%s', email)
    try:
        pop3 = poplib.POP3(conf.mail_server, timeout=mailbox_login_timeout)
        pop3.user(email)
        pass_resp = pop3.pass_(passwd)
        pop3.quit()
    except Exception as e:
        logging.error('pop3_login error: %s', e)
        return False

    logging.debug('pop3 response code:%s', pass_resp)
    return True


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.DEBUG)
    st = time.time()
    # assert smtp_login("auth@ikang.com", "Ikang@$1jk!")
    assert pop3_login("auth@ikang.com", "Ikang@$1jk!")
    print 'I took %d ms to login' % int((time.time()-st) * 1000)

