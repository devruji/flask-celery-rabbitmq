from datetime import datetime
from celery import Celery

import pandas as pd
import psycopg2
import random

ENV = 'prod'

# app = Celery('hello', broker='amqp://guest:guest@rabbit//',
#              backend='redis://redis/0')
app = Celery('db_task')

# [Initial configuration here]
app.config_from_object('celeryconfig')

pgsql_host = '127.0.0.1' if ENV == 'dev' else 'localhost'


@app.task
def pgsql_conn():
    try:
        with psycopg2.connect(dbname='mockaroo_v1', host=pgsql_host, port='5432', user='postgres', password='banana') as conn:
            # with conn.cursor() as curs:

            randn = str(random.randint(0,20))

            sql_contexts = f'''
                SELECT * FROM mock_data LIMIT {randn}
            '''
            
            import time
            time.sleep(int(randn)
)
            df = pd.read_sql(sql_contexts, conn)

    except Exception as e:
        print(f'[ERROR - {datetime.now()}] -> @{e}')
        df = pd.DataFrame()

    return df.to_json()

if __name__ == '__main__':
    x = pgsql_conn()
    print(pd.read_json(x))
