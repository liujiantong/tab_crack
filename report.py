#!/anaconda/bin/python
# coding: utf8

import requests
from flask import Flask, make_response, render_template, escape
from flask import session, request, redirect, url_for

import tab_api
import utils


IKANG_DOMAIN = '.health.ikang.com'


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
        login_ok = utils.email_login(email, password, app.logger)

        if login_ok:
            token = get_token(email)
            if token is None:
                return render_template('login.html')

            session['token'] = token
            resp = make_response(render_template('tab_report_zaixing.html', token=token))
            resp.set_cookie('XSRF-TOKEN', xsrf_token, domain=IKANG_DOMAIN)
            resp.set_cookie('workgroup_session_id', workgroup_session_id, domain=IKANG_DOMAIN)
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
    return render_template('500.html'), 500


def get_token(email):
    # TODO: get token from mysql db
    # return utils.token_by_email(email)
    return '888888'

"""
def hello():
    # Establish a session so we can retain the cookies
    session = requests.Session()
    xsrf_token, workgroup_session_id = tab_api.tab_login(session)

    resp = make_response(render_template('tab_report_zaixing.html', token='88888'))
    resp.set_cookie('XSRF-TOKEN', xsrf_token, domain=IKANG_DOMAIN)
    resp.set_cookie('workgroup_session_id', workgroup_session_id, domain=IKANG_DOMAIN)
    return resp
"""


if __name__ == "__main__":
    # Establish a session so we can retain the cookies
    session = requests.Session()
    xsrf_token, workgroup_session_id = tab_api.tab_login(session)

    app.run(debug=True)

