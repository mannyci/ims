from datetime import timedelta


BROKER_URL = 'pyamqp://localhost:5672'
CELERY_RESULT_BACKEND = 'rpc://localhost:5672'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE = {
    'hostcheck_scheduler': {
        'task': 'core.tasks.host_status',
        'schedule': timedelta(seconds=60),
        'options': {'expires': 20}
    },
    'hostfact_scheduler': {
        'task': 'core.tasks.host_facts',
        'schedule': timedelta(seconds=600),
        'options': {'expires': 20}
    },
    'network_update_scheduler': {
        'task': 'network.tasks.update_network',
        'schedule': timedelta(seconds=10),
        'options': {'expires': 20}
    },
}
