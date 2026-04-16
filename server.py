import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CDSS_BASE = "https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations"

@app.route("/latest")
def latest():
    station = request.args.get("station")
    param = request.args.get("param")
    if not station or not param:
        return jsonify({"error": "station and param are required"}), 400

    url = f"{CDSS_BASE}/telemetrytimeserieslatest/?format=json&abbrev={station}&parameter={param}"
    r = requests.get(url, timeout=10)
    return jsonify(r.json())

@app.route("/hourly")
def hourly():
    station = request.args.get("station")
    param = request.args.get("param")
    if not station or not param:
        return jsonify({"error": "station and param are required"}), 400

    url = (
        f"{CDSS_BASE}/telemetrytimeserieshourly/"
        f"?format=json&abbrev={station}&parameter={param}&days=10&sortDirection=ASC"
    )
    r = requests.get(url, timeout=10)
    return jsonify(r.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
