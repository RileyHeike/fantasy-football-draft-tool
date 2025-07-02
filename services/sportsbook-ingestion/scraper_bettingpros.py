import requests
import logging

def fetch_bettingpros_props(player_slug: str):
    url = (
        "https://api.bettingpros.com/v3/offers"
        "?sport=NFL"
        "&market_id=5:7:77:6:23:22:4:47:49:50:300:301:302:303:304:305:306:51:330:52:53:54:55:48:56:57:125"
        f"&player_slug={player_slug}"
        "&season=2025"
        "&location=WA"
        "&limit=10"
        "&page=1"
    )
    headers = {
        "accept": "application/json, text/plain, */*",
        "x-api-key": "CHi8Hy5CEE4khd46XNYL23dCFX96oUdw6qOt1Dnh",
        "referer": "https://www.bettingpros.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    logging.debug(f"Fetching BettingPros API: {url}")
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        logging.error(f"API error: {resp.status_code} {resp.text}")
        return {}

    data = resp.json()
    props = {}
    for offer in data.get("offers", []):
        market_id = offer.get("market_id")
        selections = offer.get("selections", [])
        for sel in selections:
            label = sel.get("label")
            books = sel.get("books", [])
            for book in books:
                for line in book.get("lines", []):
                    entry = {
                        "market_id": market_id,
                        "label": label,
                        "book_id": book.get("id"),
                        "line": line.get("line"),
                        "cost": line.get("cost"),
                        "link": line.get("link"),
                    }
                    props.setdefault(label, []).append(entry)

    return {
        "player": player_slug.replace('-', ' ').title(),
        "props": props,
        "source": "BettingPros"
    }