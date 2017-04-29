#!/usr/bin/env python

import urllib
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
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
<<<<<<< HEAD

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
=======
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
>>>>>>> origin/master
