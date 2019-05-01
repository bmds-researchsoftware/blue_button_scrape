from flask import Flask
from flask import request
import requests
import json
import csv
import pandas as pd
import synthetic_users
app = Flask(__name__)

CLIENT_ID = 'c3IP1q7AktCVRKQa7QpwRXI7Hhqo8izlgtx6UsGD'
CLIENT_SECRET = 'bqJucbcrMhD3oKYOkSDsMBlhOX4oLMUCfYPKX8Jq8nN3d6IMjRixIkSLqbB7nEwCQpVzcVVqeoQGSWJJ8OYGfXgwrkFNFhnvZnGsBGVuWrWESlFxT4zQcAXFy63jvKX7'
URL_BASE = 'https://sandbox.bluebutton.cms.gov'
TOKEN_EXTENSION = '/v1/o/token/'
PATIENT_EXTENSION = '/v1/fhir/Patient/'
EOB_EXTENSION = '/v1/fhir/ExplanationOfBenefit/?patient='
COVERAGE_EXTENSION = '/v1/fhir/Coverage/?beneficiary='

@app.route('/get_token')
def get_token():
    auth_code = request.args.get('code')
    if auth_code:
        post_url = URL_BASE + TOKEN_EXTENSION
        post_payload = {
                'code': auth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:5000/get_token' }
        token_response = requests.post(post_url, auth=(CLIENT_ID, CLIENT_SECRET), data=post_payload)
        response_json = json.loads(token_response.text) 
        access_token = response_json['access_token']
        patient_id = response_json['patient']
        headers = {'Authorization': 'Bearer ' + access_token}
        file_name_ending = '_' + patient_id + '.json'
        patient_response = requests.get(URL_BASE + PATIENT_EXTENSION, headers=headers)
        patient_data = patient_response.json()
        with open('output/patient_data' + file_name_ending, 'w') as outfile:
            json.dump(patient_data, outfile, indent=4)
        eob_response = requests.get(URL_BASE + EOB_EXTENSION, headers=headers)
        eob_data = eob_response.json()
        with open('output/eob_data' + file_name_ending, 'w') as outfile:
            json.dump(eob_data, outfile, indent=4)
        coverage_response = requests.get(URL_BASE + COVERAGE_EXTENSION, headers=headers)
        coverage_data = coverage_response.json()
        with open('output/coverage_data' + file_name_ending, 'w') as outfile:
            json.dump(coverage_data, outfile, indent=4)
        return 'saved patient data for ' + patient_id
