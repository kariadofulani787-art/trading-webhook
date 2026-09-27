from flask import Flask, request, jsonify

app = Flask(__name__)

# Memory slot to store trade signals
latest_signal = {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Server is live and running!"}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal
    raw_data = request.get_data(as_text=True) or ""
    
    action = "BUY" if "BUY" in raw_data.upper() else ("SELL" if "SELL" in raw_data.upper() else "NONE")
    
    latest_signal = {
        "action": action,
        "raw": raw_data
    }
    return jsonify({"status": "received", "action": action}), 200

@app.route('/get-signal', methods=['GET'])
def get_signal():
    global latest_signal
    if not latest_signal:
        return jsonify({"status": "NONE"}), 200
    
    signal_to_send = latest_signal.copy()
    latest_signal = {}  # Clear after reading
    return jsonify(signal_to_send), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
