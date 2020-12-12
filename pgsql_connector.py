from datetime import datetime
from celery import Celery

import pandas as pd
import psycopg2
import random
import time

ENV = 'prod'  # or prod

app = Celery('db_task')

# [Initial configuration here]
app.config_from_object('celeryconfig')

pgsql_host = 'localhost' if ENV == 'dev' else 'db'


@app.task
def pgsql_conn():
    try:
        with psycopg2.connect(dbname='mockaroo', host=pgsql_host, port='5432', user='postgres', password='password') as conn:
            # with conn.cursor() as curs:

            randn = str(random.randint(0, 20))  # generate random number

            # declare sql contexts here
            sql_contexts = f'''
                SELECT * FROM mock_data LIMIT {randn}
            '''

            df = pd.read_sql(sql_contexts, conn)

            time.sleep(int(randn))

    except Exception as e:
        print(f'[ERROR - {datetime.now()}] -> @{e}')
        df = pd.DataFrame()

    return df.to_json()


if __name__ == '__main__':
    x = pgsql_conn()
    print(pd.read_json(x))
