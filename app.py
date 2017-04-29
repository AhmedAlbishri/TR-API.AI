#!/usr/bin/env python

import json
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
APP = Flask(__name__)
LOG = APP.logger

@APP.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    text = req['result']['parameters'].get('text')
    langto = req['result']['parameters'].get('lang-to')

    speech = "Translation is " + text

    print("Response:")
    print(speech)

    res_sp = {
        "speech": speech,
        "displayText": speech,
        "source": "Ahmed"
    }
    res = res_sp
    res = json.dumps(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    PORT = 8080

    APP.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )
