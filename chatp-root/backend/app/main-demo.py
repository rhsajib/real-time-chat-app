from fastapi import FastAPI
from app.services.worker.tasks import send_account_activation_email
from celery.result import AsyncResult

app = FastAPI()

@app.post("/send-email")
async def send_email(recipient_email: str):
    # recipient_email = 'rhxyz777@gmail.com'
    result = send_account_activation_email.delay(recipient_email)
    # print('result', result, dir(result))
    # Wait for the Celery task to complete and get the result
    # result_value = result.get()     # same as      result_value = AsyncResult(result.id).get()
    
    return {"message": "Task triggered", "task_id": result.id}
    # return {"message": "Task triggered", "task_id": result.id, "result": result_value}