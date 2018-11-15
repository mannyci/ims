BROKER_URL = 'pyamqp://localhost:5672'
CELERY_RESULT_BACKEND = 'rpc://localhost:5672'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'