# shrug_command/Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY shrug_command_server.py .

CMD ["python", "shrug_command_server.py"]
