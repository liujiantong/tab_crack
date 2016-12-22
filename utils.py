#!/anaconda/bin/python
# coding: utf8

import time
import smtplib
import mysql.connector


mail_server = 'mail.ikang.com'


def email_login(email, passwd, logger=None):
    smtp = smtplib.SMTP()

    connected = False
    for i in xrange(3):
        try:
            code, _ = smtp.connect(mail_server)
            if int(code/100) == 2:
                connected = True
                break
            else:
                # print 'connection %d failed' % i
                time.sleep(1)
        except Exception as e:
            msg = 'connect to %s error: %s'.format(mail_server, e)
            if logger:
                logger.warning(msg)
            else:
                print msg
    if not connected:
        return False
    code, _ = smtp.login(email, passwd)
    # print 'login code:', code

    if int(code/100) == 2:
        return True
    return False


def token_by_email(email):
    cnx = mysql.connector.connect(user='scott', password='tiger',
                                  host='127.0.0.1',
                                  database='employees')
    try:
        cursor = cnx.cursor()
        cursor.execute("select token from tab_user where email=%s", email)
        result = cursor.fetchone()
        print result[0]
    finally:
        cnx.close()


if __name__ == '__main__':
    # assert email_login("auth@ikang.com", "Ikang@$1jk!")
    assert token_by_email('email@ikang.com') == 'xxxx'

