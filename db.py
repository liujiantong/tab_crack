#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import logging
# import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import conf


'''
def token_by_email1(email):
    cnx = mysql.connector.connect(user=conf.mysql_user,
                                  password=conf.mysql_passwd,
                                  host=conf.mysql_host,
                                  database=conf.mysql_db)
    try:
        cursor = cnx.cursor()
        cursor.execute("select a.token from etl_ctl.t_user a "
                       "where a.email_address=lower(%s) and a.user_type='1' "
                       "and a.is_enabled='1'", (email,))
        result = cursor.fetchone()
        return None if result is None else result[0]
    finally:
        cursor.close()
        cnx.close()
'''


def token_by_email(cnx_pool, email):
    cnx = cnx_pool.get_connection()
    try:
        cursor = cnx.cursor()
        cursor.execute("select a.token from etl_ctl.t_user a "
                       "where a.email_address=lower(%s) and a.user_type='1' "
                       "and a.is_enabled='1'", (email,))
        result = cursor.fetchone()
        return None if result is None else result[0]
    finally:
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.DEBUG)
    pool = MySQLConnectionPool(pool_name="tab_pool", pool_size=conf.mysql_pool_size, **conf.dbconfig)
    st = time.time()
    assert token_by_email(pool, 'sandy.cheng@ikang.com') == 'YR2Sn6QLqGkb'
    print 'I took %d ms to login' % int((time.time()-st) * 1000)

