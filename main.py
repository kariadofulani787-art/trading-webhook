import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# This line creates your webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # 1. Catch the signal sent from TradingView
        data = request.get_json()
        print("Signal Received:", data)
        
        # 2. Extract trade details (US100, Buy/Sell, Price, SL, TP)
        action = data.get('action')
        symbol = data.get('symbol')
        price = data.get('price')
        sl = data.get('sl')
        tp = data.get('tp')

        # 3. Print confirmation (Broker execution will go here later)
        print(f"Executing {action} order for {symbol} at {price} (SL: {sl}, TP: {tp})")
        
        return jsonify({"status": "success", "message": "Signal received"}), 200
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Keep the server open to listen 24/7
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
