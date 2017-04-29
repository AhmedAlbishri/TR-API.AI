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
        # "data": {},
        # "contextOut": [],
        "source": "Ahmed"
    }
    res = res_sp

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
"""
def makeWebhookResult(req):
    if req.get("result").get("action") != "translate.text":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    word = parameters.get("text")
    langto = parameters.get("lang-to")

    lang = ""

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

    response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e.c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text=' + word + '&lang=en-' + lang)

    data = response.json()

    tr_txt = data['text']
    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "Translation is " + tr_txt

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "Ahmed"
    }
"""

if __name__ == '__main__':
    PORT = 8080

    APP.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )
