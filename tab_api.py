#!/anaconda/bin/python
# coding: utf8

import requests
import json
import logging

import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

import conf


tab_server_url = "https://dashboard.health.cloudvision.com"
vizportal_api_url = "/vizportal/api/web/v1/"


tab_headers = {
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json, text/plain, */*",
    'cache-control': "no-cache",
    'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6'
}


def _encode_for_display(text):
    return text.encode('ascii', errors="backslashreplace").decode('utf8')


def generate_public_key(session):
    endpoint = "generatePublicKey"
    url = tab_server_url + vizportal_api_url + endpoint

    payload = {
        'method': 'generatePublicKey',
        'params': {}
    }

    resp = session.post(url, json=payload, headers=tab_headers)
    resp_text = json.loads(_encode_for_display(resp.text))
    resp_values = {
        "keyId": resp_text["result"]["keyId"],
        "n": resp_text["result"]["key"]["n"],
        "e": resp_text["result"]["key"]["e"]
    }
    return resp_values


def asymmetric_encrypt(val, public_key):
    """
    Encrypt with RSA public key (it's important to use PKCS11)
    """
    modulus_decoded = long(public_key["n"], 16)
    exponent_decoded = long(public_key["e"], 16)
    key_pub = RSA.construct((modulus_decoded, exponent_decoded))
    # Generate a cypher using the PKCS1.5 standard
    cipher = PKCS1_v1_5.new(key_pub)
    return cipher.encrypt(val)


def vizportal_login(session, tab_user, encrypted_passwd, keyid):
    encoded_passd = binascii.b2a_hex(encrypted_passwd)
    payload = {
        'method': 'login',
        'params': {
            'username': tab_user,
            'encryptedPassword': encoded_passd,
            'keyId': keyid
        }
    }

    endpoint = "login"
    url = tab_server_url + vizportal_api_url + endpoint
    resp = session.post(url, json=payload, headers=tab_headers)
    return resp


def update_extract_schedule(session, task_id, schedule_id, xsrf_token):
    payload = {
        'method': 'setExtractTasksSchedule',
        'params': {
            'ids': task_id,
            'scheduleId': schedule_id
        }
    }

    headers = tab_headers.copy()
    headers['X-XSRF-TOKEN'] = xsrf_token

    endpoint = "setExtractTasksSchedule"
    url = tab_server_url + vizportal_api_url + endpoint

    resp = session.post(url, json=payload, headers=headers)
    print resp.status_code
    return resp


def tab_login(session, tab_user=conf.tab_username, tab_passwd=conf.tab_password):
    # Generate a pubilc key that will be used to encrypt the user's password
    public_key = generate_public_key(session)
    keyId = public_key["keyId"]
    logging.debug('keyId: %s', keyId)

    # Encrypt the user’s password with RSA PKCS1 encryption
    encrypted_passwd = asymmetric_encrypt(tab_passwd, public_key)

    # Login to Vizportal and Capture the response
    login_resp = vizportal_login(session, tab_user, encrypted_passwd, keyId)

    # Parse the cookie
    sc = login_resp.headers["Set-Cookie"]
    cookies = (item.strip().split("=") for item in sc.split(";"))
    set_cookie = dict([c for c in cookies if len(c) == 2])
    # print 'set_cookie:', set_cookie

    # Retain the workgroup_session_id and XSRF-TOKEN so we can submit other calls to Vizportal
    xsrf_token, workgroup_session_id = set_cookie["HttpOnly, XSRF-TOKEN"], set_cookie["workgroup_session_id"]
    return xsrf_token, workgroup_session_id


if __name__ == '__main__':
    # Establish a session so we can retain the cookies
    req_session = requests.Session()
    xsrf_token, workgroup_session_id = tab_login(req_session)
    print 'xsrf_token:{}, workgroup_session_id:{}'.format(xsrf_token, workgroup_session_id)
