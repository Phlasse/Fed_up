## API File ##

from datetime import datetime

import joblib
import pandas as pd
import pytz
from flask import Flask
from flask import request
from flask_cors import CORS
from termcolor import colored

api = Flask(__name__)
CORS(api)

#PATH_TO_MODEL = "data/model.joblib" ## Will need to insert here the model
API_VERSION = "v1"

def format_input(input):
    ## TO DO : Define elements needed to be inputed in order to call the API
    pass

## Route for Documentation
@api.route('/API/')
def api_doc():
    return 'Fed Up! Here you will find our API documentation'

# Route for API version
@api.route(f'/API/{API_VERSION}/')
def api_doc_version():
    return f'Hey this is our {API_VERSION} API. Fed Up!'

# Route for Recommendations
@api.route(f'/API/{API_VERSION}/recommendations', methods=['GET', 'POST'])
def recommendations():
    return {"recommendations": "Eat Vegan ! Fed Up !"}



if __name__ == '__main__':
    api.run(host='127.0.0.1', port=8080, debug=True)
