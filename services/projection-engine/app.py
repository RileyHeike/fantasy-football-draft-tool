from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

SPORTSBOOK_API_BASE = "http://sportsbook-ingestion:5000"

def get_player_lines(player_slug):
    """Fetch filtered prop lines for a player from sportsbook-ingestion."""
    url = f"{SPORTSBOOK_API_BASE}/lines/{player_slug}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def implied_prob(american_odds):
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)

def average_line_for_category(lines, category):
    category_lines = [l for l in lines if l['type'] == category]
    if not category_lines:
        return None, 0
    weighted_sum = 0
    total_weight = 0
    for line in category_lines:
        odds = line.get('cost')
        value = line.get('line')
        if odds is None or value is None:
            continue
        prob = implied_prob(odds)
        weighted_sum += value * prob
        total_weight += prob
    if total_weight == 0:
        return None, len(category_lines)
    return round(weighted_sum / total_weight, 2), len(category_lines)

@app.route("/player-props-summary/<player_slug>", methods=["GET"])
def player_props_summary(player_slug):
    try:
        data = get_player_lines(player_slug)
        lines = data.get("lines", [])

        # Try to extract team and position from the first line, if present
        team = None
        position = None
        if lines:
            team = lines[0].get("team")
            position = lines[0].get("position")

        categories = set(l['type'] for l in lines)
        summary = {}
        for cat in categories:
            avg, sample_size = average_line_for_category(lines, cat)
            if avg is not None:
                summary[cat] = {
                    "average": avg,
                    "sample_size": sample_size
                }

        return jsonify({
            "player": data.get("player"),
            "team": team,
            "position": position,
            "summary": summary,
            "note": "Projection logic to be expanded."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
