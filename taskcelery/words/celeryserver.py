from celery import Celery


app = Celery(
    'counter',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0'
)

app.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE='Europe/Kiev',
    CELERY_ACCEPT_CONTENT=['msgpack'],
    CELERY_TASK_SERIALIZER='msgpack',
    CELERY_RESULT_SERIALIZER ='msgpack'
)
