#!/usr/bin/env python

from flask import Flask, jsonify, render_template, Response, request
import json
import requests
import pprint

'''
    This script automates the the configuration of multipla aspects of the
    ACI Multi-Site controller configuration with the click of a button.
    
    1. Add Site and IPN Coniguration
    2. Add Tenant schema and template configurations
    3.
'''

app = Flask(__name__)

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = True


def login_to_msc():

    '''
        This function retrieves a login token used to authenticate
        to the MSC for future REST requests.
    '''

    msc_uri = "https://10.8.253.134"
    api_uri = "/api/v1/auth/login"

    full_uri = "{0}{1}".format(msc_uri, api_uri)
    print full_uri

    msc_headers = {'content-type': 'application/json; charset=utf-8'}
    msc_username = "api_user"
    msc_password = "Cisco12345!"

    login_json = {"username": "admin","password": "Cisco12345!"}

    params= json.dumps(login_json)

    r = requests.post(full_uri, params, headers=msc_headers, verify=False)

    token_data = json.loads(r.text)
    token = token_data['token']
    return token


def get_tenants(token):

    '''  get tenant info from MSC '''

    print(token)
    msc_uri = "http://10.8.253.134"
    api_uri = "/api/v1/tenants"

    # Build full URI
    full_uri = "{0}{1}".format(msc_uri, api_uri)

    msc_headers = {'content-type': 'application/json; charset=utf-8','Authorization': 'Bearer {}'.format(token)}
    print(msc_headers)
    username = "api_user"
    password = "Cisco12345!"

    # json.dumps(params)
    r = requests.get(full_uri, headers=msc_headers, verify=False)

    result = r.text
    print result
    return result


def add_tenant_call(token, full_uri, payload):

    print(token)
    msc_uri = "http://10.8.253.134"
    api_uri = "/api/v1/tenants"

    # Build full URI
    #full_uri = "{0}{1}".format(msc_uri, api_uri)

    msc_headers = {'content-type': 'application/json; charset=utf-8','Authorization': 'Bearer {}'.format(token)}
    print(msc_headers)
    username = "api_user"
    password = "Cisco12345!"

    # json.dumps(params)
    r = requests.post(full_uri, payload, headers=msc_headers, verify=False)

    result = r.text
    print result
    return result

def get_schema(token, full_uri):

    print(token)
    msc_uri = "http://10.8.253.134"
    api_uri = "/api/v1/tenants"

    # Build full URI
    #full_uri = "{0}{1}".format(msc_uri, api_uri)

    msc_headers = {'content-type': 'application/json; charset=utf-8','Authorization': 'Bearer {}'.format(token)}
    print(msc_headers)
    username = "api_user"
    password = "Cisco12345!"

    # json.dumps(params)
    r = requests.get(full_uri, headers=msc_headers, verify=False)

    result = r.text
    return result

def post_schema(token, full_uri, payload):

    msc_headers = {'content-type': 'application/json; charset=utf-8','Authorization': 'Bearer {}'.format(token)}

    r = requests.post(full_uri, payload, headers=msc_headers, verify=False)
    result = r.text
    return result

def add_template():
    ''' Add Template to Multi-Site Controller '''

    message = 'call to template occurred'

    return message


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/get_tenants', methods=['POST'])
def add_template():
    print('You are here!!')

    payload = request.form
    action = payload['action']
    print(action)

    if action == "gettenant":
        token = login_to_msc()
        tenantInfo = get_tenants(token)
        print(tenantInfo)
    else:
        print('Something went wrong in Template definition')
        quit()

    returnMessage = {'message': tenantInfo}

    print (returnMessage)
    resp = json.dumps(returnMessage)
    return Response(resp, status=200, mimetype='application/json')


@app.route('/add_tenant', methods=['POST'])
def add_tenant():


    ''' This function will add a tenant based on the payload varibale below '''
    print('You are here!!')

    payload = request.form
    action = payload['action']


    # JSON payload to add Tenant

    payload = {
                "displayName": "API Tenant",
                "name":"Tenant2",
                "description":"Tenant Added Via API",
                "siteAssociations":[
                    {
                    "siteId": "",
                    "securityDomains": ["false", "null"]
                    }
                ],
                "userAssociations": [
                    { "userId": "0000ffff0000000000000020" }
                ]
            }

    full_uri = "https://10.8.253.134/api/v1/tenants"

    if action == "addtenant":
        token = login_to_msc()
        tenantInfo = add_tenant_call(token,full_uri, payload)
        print(tenantInfo)
    else:
        print('Invalid information sent from web page')

    returnMessage = {'message': tenantInfo}

    print (returnMessage)
    resp = json.dumps(returnMessage)
    return Response(resp, status=200, mimetype='application/json')

@app.route('/get_schema', methods=['POST'])
def get_schemas():
    print('You are here!!')

    payload = request.form
    action = payload['action']
    print(action)

    full_uri = 'https://10.8.253.134/api/v1/schemas'

    if action == "getSchema":
        token = login_to_msc()
        tenantInfo = get_schema(token,full_uri)
        print(tenantInfo)
    else:
        print('Invalid information provided from web page')
        quit()

    returnMessage = {'message': tenantInfo}

    print (returnMessage)
    resp = json.dumps(returnMessage)
    return Response(resp, status=200, mimetype='application/json')

@app.route('/add_schema', methods=['POST'])
def add_schemas():
    print('You are here!!')

    payload = request.form
    action = payload['action']
    print(action)

    full_uri = 'https://10.8.253.134/api/v1/schemas'

    with open('schema.json', 'r') as schema:
        payload1 = json.load(schema)
        pprint.pprint(payload1)


    payload2 = json.dumps(payload1)

    if action == "addSchema":
        token = login_to_msc()
        schemaInfo = post_schema(token, full_uri, payload2)
        print(schemaInfo)
    else:
        print('Invalid information provided from web page')
        quit()

    returnMessage = {'message': schemaInfo}

    print (returnMessage)
    resp = json.dumps(returnMessage)
    return Response(resp, status=200, mimetype='application/json')



app.run(host='127.0.0.1', port=8089)
