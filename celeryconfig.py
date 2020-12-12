# [Broker host]
# broker_url = 'amqp://guest:guest@localhost//'
broker_url = 'amqp://guest:guest@rabbit//'

# [Result Backend]
result_backend = 'redis://redis/0'
# result_backend = 'redis://localhost'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Bangkok'
enable_utc = True
result_expires = 10
