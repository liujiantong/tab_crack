# coding: utf8

MAIN_DOMAIN = '.somewhere.com'

dashboard_server = 'https://dashboard.somewhere.com'

mail_server = 'mail.somewhere.com'

mysql_host = '192.168.0.173'
mysql_user = 'mysql_user'
mysql_passwd = '*********'
mysql_db = 'etl_ctl'
mysql_pool_size = 5

tab_username = "the_universal_user"
tab_password = '***********'

dbconfig = {
    'host': mysql_host,
    'user': mysql_user,
    'password': mysql_passwd,
    'database': mysql_db
}

redis_conf = {
    'host': 'localhost',
    'port': 6379,
    'db': 1
}

mail_relay_url = 'http://188.188.188.188:8888/mail_login'
mail_relay_key = '***************************************'
