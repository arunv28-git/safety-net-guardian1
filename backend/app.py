from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest
import random, time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
import threading, urllib.request

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

    if BUGGY_MODE and  random.random() < 0.4:
        ERROR_COUNT.inc()

        return jsonify({
            "status": "error",
            "message": "Buggy deployment failure!"
        }), 500

    return jsonify({
        "status": "success",
        "message": "Safety-Net Guardian Version 2 Running"
    })


def run_traffic_loop():
    # This function runs in the background and sends 100 requests to itself
    for _ in range(100):
        try:
            urllib.request.urlopen('http://localhost:5000/')
            time.sleep(0.05) # Small delay
        except:
            pass

@app.route("/generate-traffic")
def trigger_traffic():
    # Starts the traffic loop without freezing the browser page
    threading.Thread(target=run_traffic_loop).start()
    return "<h3>Traffic generation sequence initiated on Home Cluster! Check Grafana.</h3>"

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
