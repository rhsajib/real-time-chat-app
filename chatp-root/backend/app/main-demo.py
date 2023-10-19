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
    
    return {"message": "Task triggered", "task_id": result.id, "result": result_value}