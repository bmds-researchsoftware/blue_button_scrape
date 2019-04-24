from flask import Flask
from flask import request
import requests
app = Flask(__name__)

@app.route('/get_auth_code')
def get_auth_code():
    return request.args.get('code')
