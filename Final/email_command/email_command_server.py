from flask import Flask, request, jsonify
import os
import psycopg2
import redis
import json
app = Flask(__name__)

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

DB_HOST = os.environ['POSTGRES_HOST']
DB_PORT = os.environ['POSTGRES_PORT']
DB_NAME = os.environ['POSTGRES_DB']
DB_USER = os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']

def get_db_connection():
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return connection

def create_emails_table_if_not_exists():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS emails (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        body TEXT NOT NULL
    );
    '''

    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()

@app.route('/send_email', methods=['POST'])
def send_email():
    if not request.json:
        return jsonify({"status": "error", "message": "Empty input. Please provide a JSON payload.", "error_code": 1})

    data = request.json

    if 'email' not in data or 'subject' not in data or 'body' not in data:
        return jsonify({"status": "error", "message": "Incorrect input format. 'email', 'subject', and 'body' are required.", "error_code": 2})

    email = data['email']
    subject = data['subject']
    body = data['body']

    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO emails (email, subject, body) VALUES (%s, %s, %s)", (email, subject, body))
        connection.commit()

    email_data = {
        "email": email,
        "subject": subject,
        "body": body
    }

    r.lpush('email_queue', json.dumps(email_data))

    return jsonify({"status": "success", "message": "Email added to the queue."})

if __name__ == '__main__':
    create_emails_table_if_not_exists()
    app.run(host='0.0.0.0', port=5052)
