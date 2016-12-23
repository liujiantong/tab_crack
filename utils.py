#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import time
import smtplib
import mysql.connector


mail_server = 'mail.ikang.com'
mysql_url = '192.168.0.173'
mysql_user = 'u_user_view'
mysql_passwd = 'Fb7HM&TZ%Npd'
mysql_db = 'etl_ctl'


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
                time.sleep(1 + 0.5*i)
        except Exception as e:
            msg = 'connect to `{}` error: `{}`'.format(mail_server, e)
            if logger:
                logger.warning(msg)
            else:
                print msg
    if not connected:
        return False

    code, _ = smtp.login(email, passwd)
    smtp.close()
    # print 'login code:', code
    return int(code/100) == 2


def token_by_email(email):
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_passwd, host=mysql_url, database=mysql_db)
    try:
        cursor = cnx.cursor()
        cursor.execute("select a.token from etl_ctl.t_user a "
                       "where a.email_address=lower(%s) and a.user_type='1' "
                       "and a.is_enabled='1'", (email,))
        # cursor.execute("select username from users where email=%s", (email,))
        result = cursor.fetchone()
        return None if result is None else result[0]
    finally:
        cnx.close()


if __name__ == '__main__':
    st = time.time()
    assert email_login("auth@ikang.com", "Ikang@$1jk!")
    assert token_by_email('sandy.cheng@ikang.com') == 'YR2Sn6QLqGkb'
    print 'I took %d ms to login' % int((time.time()-st) * 1000)

