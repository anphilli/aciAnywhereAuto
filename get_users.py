#!/usr/bin/env python

from flask import Flask, jsonify, render_template, Response, request
import json
import requests


def login_to_msc():

    '''
        This function retrieves a login token used to authenticate
        to the MSC for future REST requests.
    '''

    msc_uri = "https://10.8.253.134"
    api_uri = "/api/v1/auth/login"

    full_uri = "{0}{1}".format(msc_uri, api_uri)


    msc_headers = {'content-type': 'application/json; charset=utf-8'}
    msc_username = "api_user"
    msc_password = "Cisco12345!"

    login_json = {"username": "admin","password": "Cisco12345!"}

    params= json.dumps(login_json)

    r = requests.post(full_uri, params, headers=msc_headers, verify=False)

    token_data = json.loads(r.text)
    token = token_data['token']
    return token


def get_users(token):

    print(token)
    msc_uri = "http://10.8.253.134"
    api_uri = "/api/v1/users"

    # Build full URI
    #full_uri = "{0}{1}".format(msc_uri, api_uri)

    msc_headers = {'content-type': 'application/json; charset=utf-8','Authorization': 'Bearer {}'.format(token)}
    print(msc_headers)
    username = "api_user"
    password = "Cisco12345!"

    full_uri = "{0}{1}".format(msc_uri, api_uri)

    r = requests.get(full_uri, headers=msc_headers, verify=False)

    result = r.text
    print result
    return result

if __name__ == "__main__":

    token = login_to_msc()
    response = get_users(token)
    print response