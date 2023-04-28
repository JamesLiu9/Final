import os
import json
import redis
import sendgrid
from sendgrid.helpers.mail import Mail

from celery import Celery

app = Celery('worker', broker=os.environ.get('REDIS_HOST'))

redis_host = os.environ.get('REDIS_HOST', 'redis_container')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_client = redis.Redis(host=redis_host, port=redis_port)

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

@app.task
def send_email(email_data):
    email = email_data.get('email')
    subject = email_data.get('subject')
    body = email_data.get('body')

    message = Mail(
        from_email='noreply@chatbot.com',
        to_emails=email,
        subject=subject,
        html_content=body
    )

    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
