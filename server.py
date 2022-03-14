import logging

from cogs.utils.time import now
from flask import Flask
from threading import Thread


app = Flask('')
app.logger.disabled = True

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def home():
    return "o.o"


@app.after_request
def after_request_func(response):
    print(f'{now()}: Request: "{response}"')
    return response


def run():
  app.run(host='0.0.0.0',port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()