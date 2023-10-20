from celery import shared_task
import time

from app.core.email import send_signup_email
from app.core.security import generate_activation_token
from .celery import celery



# @celery.task(name='celery_task')
# def celery_task(x:int):
#     time.sleep(x)
#     print('celery task started.')
#     return (4+5)

@celery.task(name='send_signup_activation_email')
def send_signup_activation_email(recipient_email):
    
    activation_token = generate_activation_token(recipient_email)
    print('activation_token', activation_token)

    activation_link = f"http://127.0.0.1:8000/api/v1/auth/account/activate/{activation_token}"
    send_signup_email(recipient_email, activation_link)
    return f'Email sent to {recipient_email}.'