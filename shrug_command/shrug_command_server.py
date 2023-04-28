from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    if not request.json or 'data' not in request.json:
        return jsonify({"error": {"code": 400, "message": "Invalid input format"}}), 400

    data = request.json.get('data')
    command = data.get('command')
    message = data.get('message')

    if command == "shrug":
        message = message.lstrip('/' + command + ' ')
        message += " ¯\_(ツ)_/¯"

    return jsonify({"data": {"command": command, "message": message}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5053)
