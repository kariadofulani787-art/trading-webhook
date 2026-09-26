import json
import re
from flask import Flask, jsonify, request

app = Flask(__name__)


def parse_alert_message(raw_text):
    if not raw_text:
        return {}

    # Clean out escaped line breaks, carriage returns, and non-breaking spaces
    clean_text = (
        str(raw_text)
        .replace("\\r", "")
        .replace("\\n", "")
        .replace("\r", "")
        .replace("\n", "")
        .replace("\xa0", " ")
        .strip()
    )

    # Try standard JSON parsing first
    try:
        return json.loads(clean_text)
    except Exception:
        pass

    # Fallback regex parsing for raw text values
    action = re.search(r'"action"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)
    symbol = re.search(r'"symbol"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)
    price = re.search(r'"price"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)
    sl = re.search(r'"sl"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)
    tp = re.search(r'"tp"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)

    return {
        "action": action.group(1) if action else None,
        "symbol": symbol.group(1) if symbol else None,
        "price": price.group(1) if price else None,
        "sl": sl.group(1) if sl else None,
        "tp": tp.group(1) if tp else None,
    }


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    raw_message = data.get("message", "")

    parsed = parse_alert_message(raw_message)

    action = parsed.get("action")
    symbol = parsed.get("symbol")
    price = parsed.get("price")
    sl = parsed.get("sl")
    tp = parsed.get("tp")

    print(
        f"SUCCESS: Executing {action} order for {symbol} at {price} (SL: {sl}, TP: {tp})"
    )

    return jsonify({"status": "success", "parsed": parsed}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
