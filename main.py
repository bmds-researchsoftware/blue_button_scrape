from flask import Flask
from flask import request
import requests
app = Flask(__name__)

CLIENT_ID = 'c3IP1q7AktCVRKQa7QpwRXI7Hhqo8izlgtx6UsGD'
CLIENT_SECRET = 'bqJucbcrMhD3oKYOkSDsMBlhOX4oLMUCfYPKX8Jq8nN3d6IMjRixIkSLqbB7nEwCQpVzcVVqeoQGSWJJ8OYGfXgwrkFNFhnvZnGsBGVuWrWESlFxT4zQcAXFy63jvKX7'

# Callback from manuaally entered authorization GET request
@app.route('/get_token')
def get_token():
    auth_code = request.args.get('code')
    post_url = 'https://sandbox.bluebutton.cms.gov/v1/o/token/'
    post_payload = {
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:5000/get_data' }
    response = requests.post(post_url, auth=(CLIENT_ID, CLIENT_SECRET), data=post_payload)
    print(response.text)
    return 'foo'

# Callback from get_token
@app.route('/get_data')
def get_data():
    return 'bar'
