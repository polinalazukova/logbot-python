from flask import Flask, jsonify
from threading import Thread
from logger import generate_logs

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Сервер 1 работает!", "status": "ok"}), 200

if __name__ == '__main__':
    log_thread = Thread(target=generate_logs, args=("Сервер 1",), daemon=True)
    log_thread.start()
    app.run(host='0.0.0.0', port=5001)
