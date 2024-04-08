import sys

import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from flask import Flask, url_for, request, redirect

import datetime

from app.urls import manage_urls

app = Flask(__name__)

manage_urls(app)

# from sentry_sdk import init
# sentry_sdk.init(
#     dsn="your_sentry_dsn_here",
#     traces_sample_rate=1.0
# )

@app.route('/status')
def status():

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return 'OK - {}'.format(time)


@app.route('/make_error')
def make_error():
    1/0
    return 'error'

if __name__ == """__main__""":

    # app.run(port = 8050)
    app.run(port = 8050)