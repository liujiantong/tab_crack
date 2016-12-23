#!/home/tao.liu1/anaconda/bin/python
# coding: utf8

import requests
from flask import Flask, make_response, render_template, escape
from flask import session, request, redirect, url_for

import os
from datetime import datetime
import logging

import tab_api
import mail
import db
import conf


app = Flask(__name__)
app.secret_key = '380fec53-b210-4864-925f-6b0da3b56268'


@app.route('/')
def index():
    if 'token' in session:
        return render_template('tab_report_zaixing.html', token=session['token'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        login_ok = mail.email_login(email, password)

        if login_ok:
            token = db.token_by_email(email)
            if token is None:
                return render_template('login.html')

            session['token'] = token
            resp = make_response(render_template('tab_report_zaixing.html', token=token))
            resp.set_cookie('XSRF-TOKEN', xsrf_token, domain=conf.IKANG_DOMAIN)
            resp.set_cookie('workgroup_session_id', workgroup_session_id, domain=conf.IKANG_DOMAIN)
            return resp

        return render_template('login.html')
    else:
        if 'token' in session:
            return render_template('tab_report_zaixing.html', token=session['token'])
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('token', None)
    return redirect(url_for('login'))


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('50x.html'), 500


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    work_dir, _ = os.path.split(os.path.abspath(__file__))
    log_dir = work_dir + '/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # console_handler = logging.StreamHandler()
    file_suffix = datetime.strftime(datetime.today(), '%Y%m%d')
    logfile_name = '%s/%s.%s' % (log_dir, 'sms_reminder.log', file_suffix)
    file_handler = logging.FileHandler(logfile_name)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # logger.addHandler(console_handler)
    logger.addHandler(file_handler)


if __name__ == "__main__":
    init_logger()

    # Establish a session so we can retain the cookies
    session = requests.Session()
    xsrf_token, workgroup_session_id = tab_api.tab_login(session)

    app.run(debug=True)

