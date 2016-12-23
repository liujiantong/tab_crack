#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import requests
from flask import Flask, make_response, render_template, escape
from flask import session, request, redirect, url_for

import os
import logging
from datetime import datetime

import mail
import db
import tab_api
import conf


app = Flask(__name__)
# sslify = SSLify(app)
app.secret_key = '380fec53-b210-4864-925f-6b0da3b56268'

# report_url = 'https://dashboard.health.ikang.com/views/_6/sheet0?:embed=y&:showShareOptions=false&TOKEN=YR2Sn6QLqGkb'


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


@app.route('/report_zx')
def report_zx():
    return render_template('tab_report_zaixing.html', token=session['token'])


@app.route('/signon', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('token', None)

        email, password = request.form['email'], request.form['password']
        login_ok = mail.email_login(email, password)
        logging.debug('email:%s login: %s', email, login_ok)

        if login_ok:
            token = db.token_by_email(email)
            logging.debug('email:%s token:%s', email, token)

            if token is None:
                return render_template('login.html')

            # Establish a session so we can retain the cookies
            req_session = requests.Session()
            xsrf_token, workgroup_session_id = tab_api.tab_login(req_session)

            session['token'] = token
            resp = make_response(redirect(url_for('report_zx')))
            resp.set_cookie('XSRF-TOKEN', xsrf_token, domain=conf.IKANG_DOMAIN)
            resp.set_cookie('workgroup_session_id', workgroup_session_id, domain=conf.IKANG_DOMAIN)
            return resp

        return render_template('login.html')
    else:
        if 'token' in session:
            return redirect(url_for('report_zx'))
    return render_template('login.html')


@app.route('/alive')
def alive():
    return 'ok'


if __name__ == "__main__":
    init_logger()
    app.run(host='0.0.0.0', debug=False)

