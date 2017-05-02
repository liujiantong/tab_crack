#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import requests
from flask import Flask, make_response, render_template
from flask import session, request, redirect, url_for
# from flask_sslify import SSLify

from mysql.connector.pooling import MySQLConnectionPool

import os
import redis
import argparse
from datetime import datetime, timedelta
import logging

import tab_api
# import mail
from aes import AESCipher
import db
import conf


app = Flask(__name__)
# sslify = SSLify(app)
app.secret_key = "\xb2'\xb7\xff\xd3\xb0@s+q\x86M\xf9\x0e4PRVL\xa0\xa31\xe9z"
app.permanent_session_lifetime = timedelta(hours=3)

r = redis.StrictRedis(**conf.redis_conf)


@app.route('/')
def index():
    if 'token' in session:
        return redirect(url_for('report_list'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('token', None)
        session.pop('email', None)

        email, password = request.form['email'], request.form['password']
        # login_ok = mail.pop3_login(email, password)
        login_ok = mail_pop3_login(email, password)
        logging.info('email:%s login: %s', email, login_ok)

        if login_ok:
            token = db.token_by_email(cnx_pool, email)
            logging.debug('email:%s token:%s', email, token)

            if token is None:
                return render_template('login.html', err_msg=u'该邮箱没有授权, 请联系管理员')

            # xsrf_token, workgroup_session_id = tab_api.tab_login(req_session)
            xsrf_token, workgroup_session_id = get_tab_token_session()

            session['token'] = token
            session['email'] = email
            resp = make_response(redirect(url_for('report_list')))
            resp.set_cookie('XSRF-TOKEN', xsrf_token, domain=conf.IKANG_DOMAIN)
            resp.set_cookie('workgroup_session_id', workgroup_session_id, domain=conf.IKANG_DOMAIN)
            return resp

        return render_template('login.html', err_msg=u'邮箱验证失败')
    else:
        if 'token' in session:
            return redirect(url_for('report_list'))
    return render_template('login.html', err_msg='')


@app.route('/logout')
def logout():
    # remove the token from the session if it's there
    session.pop('token', None)
    session.pop('email', None)
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('XSRF-TOKEN', '', expires=0)
    resp.set_cookie('workgroup_session_id', '', expires=0)
    return resp


@app.route('/alive')
def alive():
    return 'ok'


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('50x.html'), 500


@app.route('/report_list')
def report_list():
    token = session.get('token', None)
    if token is None:
        return redirect(url_for('login'))

    reports = db.get_reports_by_token(cnx_pool, token=token)
    reports = [(rpt[0], report_full_url(rpt[0], rpt[1], token)) for rpt in reports]
    return render_template('tab_report_list.html', reports=reports)


@app.route('/report')
def report():
    token = session.get('token', None)
    if token is None:
        return redirect(url_for('login'))

    name = request.args.get('name', None)
    url = request.args.get('url', None)
    if name is None or url is None:
        return '', 400

    reports = db.get_reports_by_token(cnx_pool, token=token)
    reports = [(rpt[0], report_full_url(rpt[0], rpt[1], token)) for rpt in reports]
    return render_template('tab_report.html', token=token, tab_name=name, tab_url=url, reports=reports)


def report_full_url(report_name, report_url, token):
    # return '%s%s?:embed=y&:showShareOptions=false&TOKEN=%s' % (conf.dashboard_server, report_url, token)
    return '/report?name=%s&url=%s' % (report_name, report_url)


def mail_pop3_login(email, passwd):
    payload = {
        'email': aes_cipher.encrypt(email),
        'password': aes_cipher.encrypt(passwd)
    }

    r = requests.post(conf.mail_relay_url, data=payload)
    return r.status_code == 200


def get_tab_token_session():
    tsess = r.hgetall('tableau_session')
    if len(tsess) == 2:
        return tsess['xsrf_token'], tsess['workgroup_session_id']

    # Establish a session so we can retain the cookies
    req_sess = requests.Session()
    xsrf_token, workgroup_session_id = tab_api.tab_login(req_sess)

    r.hset('tableau_session', 'xsrf_token', xsrf_token)
    r.hset('tableau_session', 'workgroup_session_id', workgroup_session_id)
    r.expire('tableau_session', timedelta(hours=3))

    return xsrf_token, workgroup_session_id


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    work_dir, _ = os.path.split(os.path.abspath(__file__))
    log_dir = work_dir + '/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    console_handler = logging.StreamHandler()
    file_suffix = datetime.strftime(datetime.today(), '%Y%m%d')
    logfile_name = '%s/%s.%s' % (log_dir, 'tab_report.log', file_suffix)
    file_handler = logging.FileHandler(logfile_name)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


init_logger()
cnx_pool = MySQLConnectionPool(pool_name="tab_pool", pool_size=conf.mysql_pool_size, **conf.dbconfig)
logging.info('connected to mysql db:%s', conf.dbconfig['host'])

aes_cipher = AESCipher(conf.mail_relay_key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000, help='Service Port')
    args = parser.parse_args()

    # mail.connect_mailbox()
    app.run(host='0.0.0.0', port=args.port, debug=False)
