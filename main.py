from flask import Flask
from flask import request
import requests
import json
import csv
app = Flask(__name__)

# Constants
CLIENT_ID = 'c3IP1q7AktCVRKQa7QpwRXI7Hhqo8izlgtx6UsGD'
CLIENT_SECRET = 'bqJucbcrMhD3oKYOkSDsMBlhOX4oLMUCfYPKX8Jq8nN3d6IMjRixIkSLqbB7nEwCQpVzcVVqeoQGSWJJ8OYGfXgwrkFNFhnvZnGsBGVuWrWESlFxT4zQcAXFy63jvKX7'
URL_BASE = 'https://sandbox.bluebutton.cms.gov'
TOKEN_EXTENSION = '/v1/o/token/'
PATIENT_EXTENSION = '/v1/fhir/Patient/'
EOB_EXTENSION = '/v1/fhir/ExplanationOfBenefit/?patient='
COVERAGE_EXTENSION = '/v1/fhir/Coverage/?beneficiary='

# Must match redirect_uri in project configuration at bluebutton.cms.gov
@app.route('/get_patient_data')
def get_patient_data():
    auth_code = request.args.get('code')
    if auth_code:
        # POST request to get access token and patient ID
        post_url = URL_BASE + TOKEN_EXTENSION
        post_payload = {
                'code': auth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:5000/get_patient_data' }
        response_json = requests.post(post_url, auth=(CLIENT_ID, CLIENT_SECRET), data=post_payload).json()
        access_token = response_json['access_token']
        patient_id = response_json['patient']
        headers = {'Authorization': 'Bearer ' + access_token}
        file_name_ending = '_' + patient_id + '.json'

        # GET patient data 
        patient_response = requests.get(URL_BASE + PATIENT_EXTENSION + patient_id, headers=headers)
        patient_data = patient_response.json()
        with open('output/patient_data' + file_name_ending, 'w') as outfile:
            json.dump(patient_data, outfile, indent=4)


        # GET EOB data 
        eob_response = requests.get(URL_BASE + EOB_EXTENSION + patient_id, headers=headers)
        eob_data = eob_response.json()
        with open('output/eob_data' + file_name_ending, 'w') as outfile:
            json.dump(eob_data, outfile, indent=4)

        # GET coverage data 
        coverage_response = requests.get(URL_BASE + COVERAGE_EXTENSION + patient_id, headers=headers)
        coverage_data = coverage_response.json()
        with open('output/coverage_data' + file_name_ending, 'w') as outfile:
            json.dump(coverage_data, outfile, indent=4)

        return 'saved patient data for ' + patient_id
