#!/usr/bin/env python

import json
import requests

from flask import Flask, jsonify, make_response, request
from httplib import HTTPException
from urllib2 import HTTPError, URLError

# Flask app should start in global layout
APP = Flask(__name__)
LOG = APP.logger


@APP.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    action = req.get('result').get('action')

    #if action == 'translate.text':
    text = req['result']['parameters'].get('text')
    langto = req['result']['parameters'].get('lang-to')
    lang =""
    if langto == "Spanish":
        lang = "es"
    elif langto == "Arabic":
        lang = "ar"
    elif langto == "French":
        lang = "fr"
    elif langto == "Urdu":
        lang = "ur"
    else:
        lang = "en"

    response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e.c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text=' + text + '&lang=en-' + lang)
    data = response.json()

    tr_txt = data['text']

    speech = "Translation is " + tr_txt

    print("Response:")
    print(speech)

    res_sp = {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
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
