from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import requests
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
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

#response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e.c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text='+text+'&lang=en-'+langueges[lang])

def processRequest(req):

    result = req.get("result")
    parameters = result.get("parameters")
    word = parameters.get("text")
    targetlang = parameters.get("targetlang")


    #if req.get("result").get("action") != "translate.text":
     #   return {}
    #baseurl = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e.c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text='+word+'&lang=en-'+targetlang

    response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20151023T145251Z.bf1ca7097253ff7e.c0b0a88bea31ba51f72504cc0cc42cf891ed90d2&text=' + word + '&lang=en-' +targetlang)

    #yql_query = makeYqlQuery(req)
    #if yql_query is None:
    #    return {}
    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
   # result = urlopen(baseurl).read()
    #data = json.loads(result)
    data = response.json()
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):

    text = data.get('text')
    if text is None:
        return {}

    speech = "Translation is " + text

    print("Response: Translation is " + text)
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "Ahmed"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')