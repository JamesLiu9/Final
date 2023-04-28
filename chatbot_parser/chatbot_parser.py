from flask import Flask, request, jsonify
import os
import psycopg2
import requests

app = Flask(__name__)

# Connect to the PostgreSQL database
DB_HOST = os.environ['POSTGRES_HOST']
DB_PORT = os.environ['POSTGRES_PORT']
DB_NAME = os.environ['POSTGRES_DB']
DB_USER = os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']

connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

def create_commands_table_if_not_exists():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS commands (
        id SERIAL PRIMARY KEY,
        command VARCHAR(255) UNIQUE NOT NULL,
        server_url TEXT NOT NULL
    );
    '''

    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
        connection.commit()

# Register a new command
@app.route('/register', methods=['POST'])
def register():
    if not request.json:
        return jsonify({"status": "error", "message": "Empty input. Please provide a JSON payload.", "error_code": 1})

    data = request.json

    if 'command' not in data or 'server_url' not in data:
        return jsonify({"status": "error", "message": "Incorrect input format. 'command' and 'server_url' are required.", "error_code": 2})

    command = data['command']
    server_url = data['server_url']

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO commands (command, server_url) VALUES (%s, %s) ON CONFLICT (command) DO UPDATE SET server_url = %s", (command, server_url, server_url))
        connection.commit()

    return jsonify({"status": "success", "message": f"Command '{command}' registered with server URL: {server_url}"})


# Execute a command
@app.route('/execute', methods=['POST'])
def execute():
    if not request.json:
        return jsonify({"status": "error", "message": "Empty input. Please provide a JSON payload.", "error_code": 3})

    data = request.json

    if 'command' not in data or 'message' not in data:
        return jsonify({"status": "error", "message": "Incorrect input format. 'command' and 'message' are required.", "error_code": 4})

    command = data['command']
    message = data['message']

    with connection.cursor() as cursor:
        cursor.execute("SELECT server_url FROM commands WHERE command = %s", (command,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"status": "error", "message": f"Command '{command}' not found.", "error_code": 5})

        server_url = result[0]

    try:
        response = requests.post(server_url, json={"data": {"command": command, "message": message}})
        response_data = response.json()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error executing command '{command}': {str(e)}", "error_code": 6})

    return jsonify(response_data)


if __name__ == '__main__':
    create_commands_table_if_not_exists()
    app.run(host='0.0.0.0', port=5050)
