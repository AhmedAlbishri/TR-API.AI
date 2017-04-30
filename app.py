#!/usr/bin/env python


from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import json
import os

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    print('get data from request...')
    data = request.get_json(silent=True, force=True)
    print('get TR Service...')
    
    
    req = makeWebhookResult(data)
    req = json.dumps(req, indent=4)

    print('make the response...')

    result = make_response(req)
    result.headers['Content-Type'] = 'application/json'
    
    print(json.dumps(req, indent=4))
    
return result

def makeWebhookResult(req): 
    baseurl = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e.c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text=&lang=en-es'
    result = urlopen(baseurl).read().decode('utf-8')
    data = json.loads(result)
    
    #text = req['result']['parameters'].get('text')
    #langto = req['result']['parameters'].get('lang-to')
    text = data['text']
    speech = "Translation is hello" + text

    #print("Response:")
    #print(speech)

    return {
        'speech': speech,
        'displayText': speech,
        'source': 'apiai'
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
