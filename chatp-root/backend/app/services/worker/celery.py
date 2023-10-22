import os
from celery import Celery
from app.core.config import settings

TASK_PATH = 'app.services.worker.tasks'
BROKER = settings.CELERY_BROKER_URL
BACKEND = settings.CELERY_RESULT_BACKEND

celery = Celery(
    'app.main',                       # Specify the path to your main module
    include=[TASK_PATH],     # Make sure to provide the correct path to your tasks
    broker=BROKER,
    backend=BACKEND,
    broker_connection_retry_on_startup=True
)
