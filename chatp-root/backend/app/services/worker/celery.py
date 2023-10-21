from celery import Celery

from app.core.config import settings

TASK_PATH = 'app.services.worker.tasks'

celery = Celery(
    'app.main',                       # Specify the path to your main module
    include=[TASK_PATH],     # Make sure to provide the correct path to your tasks
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True
)
