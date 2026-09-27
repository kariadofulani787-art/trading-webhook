from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

# This memory slot holds your latest trade signal
latest_signal = {}

@app.route('/')
def home():
    return "Server is live and running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal
    # Get raw text sent by Zapier
    raw_data = request.get_data(as_text=True) or ""
    
    # Simple search for Buy/Sell commands
    action = "BUY" if "BUY" in raw_data.upper() else "SELL" if "SELL" in raw_data.upper() else "UNKNOWN"
    
    # Store the signal inside server memory
    latest_signal = {
        "action": action,
        "raw_text": raw_data,
        "status": "PENDING"
    }
    
    return jsonify({"status": "received", "signal": latest_signal}), 200

@app.route('/get-signal', methods=['GET'])
def get_signal():
    global latest_signal
    if not latest_signal:
        return jsonify({"status": "NONE"}), 200
    
    # Send signal to MT5 and clear it so it doesn't execute twice
    sig = latest_signal.copy()
    latest_signal = {}
    return jsonify(sig), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
