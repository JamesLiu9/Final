# chatbot_parser/Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY chatbot_parser.py .

CMD ["python", "chatbot_parser.py"]
