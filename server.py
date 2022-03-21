import json
import logging

from cogs.utils.time import now
from config import jdata
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
    html = ''
    for key in db.keys():
        html += f'<p>"{key}": {json.dumps(json.loads(dumps(db[key])), indent=4)}</p>'
    return html


@app.after_request
def after_request_func(response):
    # API: https://tedboy.github.io/flask/interface_api.response_object.html
    print(f'{now()}: Request: {response}')
    return response


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
