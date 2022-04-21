import json
import logging

from cogs.utils.trm import trmprint
from flask import Flask
from replit import db
from replit.database import dumps
from threading import Thread


app = Flask('')
app.logger.disabled = True

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def home():
    pre = '<body>\n\n'
    suf = '</pre>\n\n</body>'
    key_pre = '<p style="font-family:\'Courier New\'"><pre>'
    key_suf = '</pre></p>\n'
    html = ''

    for key in db.keys():
        html += key_pre + f'"{key}": {json.dumps(json.loads(dumps(db[key])), indent=4)}' + key_suf

    return pre + html + suf


@app.after_request
def after_request_func(response):
    # API: https://tedboy.github.io/flask/interface_api.response_object.html
    trmprint(f'Request: {response}')
    return response


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()