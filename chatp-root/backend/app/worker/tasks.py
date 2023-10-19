from celery import shared_task
import time
from .celery import celery_app


# @shared_task
@celery_app.task(name='celery_task')
def celery_task(x:int):
    time.sleep(x)
    print('celery task started.')
    return (4+5)