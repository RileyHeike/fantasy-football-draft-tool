from flask import Flask, jsonify, request
from scraper import fetch_sample_props
from scraper_bettingpros import fetch_bettingpros_props
from filters import filter_lines_by_market_ids, MARKET_ID_MAP

app = Flask(__name__)

@app.route("/props", methods=["GET"])
def get_props():
    """Return sample/mock props data."""
    props = fetch_sample_props()
    return jsonify(props)

@app.route("/props/<player_slug>", methods=["GET"])
def get_bettingpros_props(player_slug):
    """Return the full, raw BettingPros API response for a player."""
    props = fetch_bettingpros_props(player_slug)
    return jsonify(props)

@app.route("/lines/<player_slug>", methods=["GET"])
def get_filtered_lines(player_slug):
    """
    Return only filtered, formatted lines for Passing/Rushing/Receiving Yards & TDs.
    """
    result = fetch_bettingpros_props(player_slug)
    output = filter_lines_by_market_ids(result, MARKET_ID_MAP)

    # Optional: Print to server log for debugging
    print(f"Filtered lines for {result.get('player')}:")
    for item in output:
        print(f"{item['type']}: {item['label']} | Line: {item['line']} | Cost: {item['cost']} | Book: {item['book_id']} | Link: {item['link']}")

    return jsonify({
        "player": result.get("player"),
        "lines": output
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)