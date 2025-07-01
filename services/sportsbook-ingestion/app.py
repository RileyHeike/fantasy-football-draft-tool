from flask import Flask, jsonify
from scraper import fetch_sample_props
from scraper_bettingpros import fetch_bettingpros_props

app = Flask(__name__)

@app.route("/props", methods=["GET"])
def get_props():
    props = fetch_sample_props()
    return jsonify(props)

@app.route("/props/<player_slug>", methods=["GET"])
def get_bettingpros_props(player_slug):
    props = fetch_bettingpros_props(player_slug)
    return jsonify(props)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)