#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

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

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#"https://translate.yandex.net/api/v1.5/tr.json/translate?" + "key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e." +
#                    "c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text=" + word +"&" + "lang=en-"+targetlang+"&[format=plain]&[options=1]&[callback=set]";


def processRequest(req):

    result = req.get("result")
    parameters = result.get("parameters")
    word = parameters.get("text")
    targetlang = parameters.get("targetlang")


    #if req.get("result").get("action") != "translate.text":
     #   return {}
    baseurl = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e.c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text='+word+'&lang=en-'+targetlang

    #yql_query = makeYqlQuery(req)
    #if yql_query is None:
    #    return {}
    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

"""
def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    word = parameters.get("text")
    targetlang = parameters.get("targetlang")
    if word is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
"""

def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    text = result.get('text')
    if text is None:
        return {}

    #item = channel.get('item')
    #location = channel.get('location')
    #units = channel.get('units')
    #if (location is None) or (item is None) or (units is None):
    #   return {}

    #condition = item.get('condition')
    #if condition is None:
    #   return {}

    # print(json.dumps(item, indent=4))

    speech = "Translation is " + text

    print("Response: Translation is " + text)
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "Ahmed"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')