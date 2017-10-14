#!/usr/bin/env python

from flask import Flask, jsonify, render_template, Response, request
import json
import requests


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


def rest_to_apic(payload):

    r = requests.post(full_uri, json.dumps(params), headers=spark_headers)


def add_template():

    ''' Add Template to Multi-Site Controller '''

    message = 'call to template occurred'

    return message


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/add_template', methods=['POST'])
def add_template():
    print('You are here!!')

    payload = request.form
    action = payload['action']

    if action == "template":
        # image_path = "//path_to_image"
        result = 'Added Template'
        print(result)
    else:
        print('Something went wrong in Template definition')

    returnMessage = {'message': result}

    print (returnMessage)
    resp = json.dumps(returnMessage)
    return Response(resp, status=200, mimetype='application/json')

app.run(host='127.0.0.1', port=8089)
