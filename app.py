from flask import Flask, render_template
from pgsql_connector import pgsql_conn

import os
import time
import celery
import logging
import pandas as pd

# [Logging]
logging.basicConfig(filename=os.path.join(
    os.getcwd(), 'log', 'debug.log'), level=logging.DEBUG)

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'),
            template_folder=os.path.join(os.getcwd(), 'templates'))
app.config.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
def hello():
    try:
        df = pgsql_conn.delay()
        print(df)
        print(df.ready())
        print(df.status)
        res = df.get(timeout=1, propagate=False)
        df.forget()
        df = pd.read_json(res)

    except celery.exceptions.TimeoutError:
        return 'timeout'

    return render_template('result.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
