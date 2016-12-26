#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import logging
from mysql.connector.pooling import MySQLConnectionPool
import conf


def token_by_email(cnx_pool, email):
    cnx = cnx_pool.get_connection()
    cursor = cnx.cursor()
    try:
        cursor.execute("select a.token from etl_ctl.t_user a "
                       "where a.email_address=lower(%s) and a.user_type='1' "
                       "and a.is_enabled='1'", (email,))
        result = cursor.fetchone()
        return None if result is None else result[0]
    finally:
        cursor.close()
        cnx.close()


def get_reports_by_token(cnx_pool, token):
    cnx = cnx_pool.get_connection()
    cursor = cnx.cursor()
    try:
        cursor.execute("SELECT c.func_name, c.func_url, c.func_code "
                       "FROM etl_ctl.t_user_func_permission a "
                       "JOIN etl_ctl.t_user b ON a.user_id=b.user_id "
                       "JOIN etl_ctl.t_permission_func_def c ON a.func_id=c.func_id "
                       "WHERE b.token=%s", (token,))
        return cursor.fetchall()
    finally:
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.DEBUG)
    pool = MySQLConnectionPool(pool_name="tab_pool", pool_size=conf.mysql_pool_size, **conf.dbconfig)
    st = time.time()
    assert token_by_email(pool, 'sandy.cheng@ikang.com') == 'YR2Sn6QLqGkb'
    assert len(get_reports_by_token(pool, 'G2n3ALiWdtg5ws')) == 2
    print 'I took %d ms to login' % int((time.time()-st) * 1000)

