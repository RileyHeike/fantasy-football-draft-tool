import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
from playwright.sync_api import sync_playwright

def fetch_bettingpros_props(player_slug: str):
    url = f"https://www.bettingpros.com/nfl/odds/player-futures/{player_slug}/"
    logging.debug(f"Fetching URL with Playwright: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        
        # Wait for general page structure to load
        try:
            page.wait_for_selector("body", timeout=5000)
            logging.debug("Page body loaded successfully.")
        except Exception as e:
            logging.error(f"Failed waiting for page body: {e}")
            browser.close()
            return {}

        # Optional: log full page content to diagnose further
        html_content = page.content()
        logging.debug(f"Page HTML snapshot:\n{html_content[:1000]}...")  # Log first 1000 chars

        # Now attempt your target selector
        try:
            page.wait_for_selector("h3.odds-table-title", timeout=10000)
        except Exception as e:
            logging.warning("Primary selector not found. Trying fallback...")
            try:
                page.wait_for_selector("div.odds-table-section", timeout=5000)
            except Exception as fallback_e:
                logging.error(f"Fallback also failed: {fallback_e}")
                logging.debug("Final page snapshot:\n" + page.content()[:2000])
                browser.close()
                return {}

        props = {}
        current_stat = None

        sections = page.query_selector_all("div.odds-table-section")
        for section in sections:
            stat_header = section.query_selector("h3.odds-table-title")
            if not stat_header:
                continue
            stat_title = stat_header.inner_text().strip()
            logging.debug(f"Found stat section: {stat_title}")
            props[stat_title] = []

            rows = section.query_selector_all("table tbody tr")
            for row in rows:
                cells = [cell.inner_text().strip() for cell in row.query_selector_all("td")]
                if cells:
                    logging.debug(f"Adding row to {stat_title}: {cells}")
                    props[stat_title].append(cells)

        browser.close()

    return {
        "player": player_slug.replace('-', ' ').title(),
        "props": props,
        "source": "BettingPros"
    }