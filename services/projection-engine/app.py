from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/projected-points", methods=["GET"])
def projected_points():
    try:
        response = requests.get("http://sportsbook-ingestion:5000/props")
        data = response.json()
        projected = data["receiving_yards"] * 0.1 + data["touchdowns"] * 6
        return jsonify({
            "player": data["player"],
            "team": data["team"],
            "projected_fantasy_points": projected
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
