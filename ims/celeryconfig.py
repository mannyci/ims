from datetime import timedelta


BROKER_URL = 'pyamqp://localhost:5672'
CELERY_RESULT_BACKEND = 'rpc://localhost:5672'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE = {
    'hostcheck_scheduler': {
        'task': 'core.tasks.host_status',
        'schedule': timedelta(seconds=30),
        'options': {'expires': 20}
    }
}
