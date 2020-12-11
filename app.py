from flask import Flask, render_template

from pgsql_connector import pgsql_conn


import os
import time
import random
import celery
import logging
import pandas as pd


# [Logging]
logging.basicConfig(filename=os.path.join(
    os.getcwd(), 'log', 'debug.log'), level=logging.DEBUG)

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'),
            template_folder=os.path.join(os.getcwd(), 'templates'))

@app.route('/hello')
def hello():
    try:
        df = pgsql_conn.delay()
        print(df)
        print(df.ready())
        print(df.status)
        # res = df.get(timeout=21, propagate=False)
        # df.forget()
        # df = pd.read_json(res)

    except celery.exceptions.TimeoutError:
        return 'timeout'

    return 'Hi there'
    # return render_template('result.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
