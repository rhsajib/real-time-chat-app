### Redis

```sh
# mac os installation
$ brew install redis
```

```zsh
# start the Redis Server
$ redis-server
```

```zsh
# ensure that your Redis server is running
$ redis-cli

# inside redis server shell
$ ping
```

```
broker_url = 'redis://127.0.0.1:6379/0'
result_backend = 'redis://127.0.0.1:6379/0'

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
```

### Celery

```sh
$ pip install celery
```

```python
# Project structure

-app/
    -worker/
        -__init__.py
        -celery.py
        -tasks.py
    -main.py

```

```python
# celery.py
from celery import Celery

from app.core.config import settings

celery_app = Celery(
    'app.main',                       # Specify the path to your main module
    include=['app.worker.tasks'],     # Make sure to provide the correct path to your tasks
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True
)
```

```python
# tasks.py
from celery import shared_task
import time
from .celery import celery_app


@celery_app.task(name='celery_task')
def celery_task(x:int):
    time.sleep(x)
    print('celery task started.')
    return (4+5)
```

```python
from fastapi import FastAPI
from app.worker.tasks import celery_task
from celery.result import AsyncResult

app = FastAPI()

@app.post("/")
async def first_celery_task(time: int):
    result = celery_task.delay(time)
    # print('result', result, dir(result))
    # Wait for the Celery task to complete and get the result
    result_value = result.get()     # same as      result_value = AsyncResult(result.id).get()

    return {
        "message": "Task triggered",
        "task_id": result.id,
        "result": result_value
        }
```

```sh
# celery server
$ celery -A app.worker.celery worker --loglevel=info 
```

```sh
# fastapi server
$ uvicorn app.main:app --reload  
```