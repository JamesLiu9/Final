FROM python:3.9

WORKDIR /app

RUN pip install redis sendgrid celery[redis]

COPY worker.py .

CMD ["celery", "-A", "worker", "worker", "--loglevel=INFO"]
