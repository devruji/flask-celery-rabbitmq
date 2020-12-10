from datetime import datetime
from celery import Celery

import pandas as pd
import psycopg2

ENV = 'prod'

# app = Celery('hello', broker='amqp://guest:guest@rabbit//',
#              backend='redis://redis/0')
app = Celery('hello', broker='amqp://guest:guest@localhost//',
             backend='redis://localhost')

sql_contexts = '''
    SELECT * FROM mock_data
'''

pgsql_host = '127.0.0.1' if ENV == 'dev' else '192.168.1.35'


@app.task
def pgsql_conn():
    try:
        with psycopg2.connect(dbname='mockaroo_v1', host=pgsql_host, port='5432', user='postgres', password='postgres') as conn:
            # with conn.cursor() as curs:
            df = pd.read_sql(sql_contexts, conn)

    except Exception as e:
        print(f'[ERROR - {datetime.now()}] -> @{e}')
        df = pd.DataFrame()

    import time
    time.sleep(5)

    return df.to_json()
