#!/usr/bin/env python

import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    #req = request.get_json(silent=True, force=True)

    #text = req['result']['parameters'].get('text')
    #langto = req['result']['parameters'].get('lang-to')

    speech = "Translation is hello" #+ text

    #print("Response:")
    #print(speech)

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
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port: %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
