from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest
import random
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total App Requests'
)

ERROR_COUNT = Counter(
    'app_errors_total',
    'Total Error Requests'
)

BUGGY_MODE = False


@app.route('/')
def home():
    REQUEST_COUNT.inc()

    if random.random() < 0.4:
        ERROR_COUNT.inc()

        return jsonify({
            "status": "error",
            "message": "Buggy deployment failure!"
        }), 500

    return jsonify({
        "status": "success",
        "message": "Safety-Net Guardian Buggy Version Running"
    })


@app.route('/health')
def health():
    return "OK", 200


@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-type': CONTENT_TYPE_LATEST}


@app.route('/toggle-bug')
def toggle_bug():
    global BUGGY_MODE

    BUGGY_MODE = not BUGGY_MODE

    return jsonify({
        "buggy_mode": BUGGY_MODE
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
