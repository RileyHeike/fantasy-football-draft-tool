MARKET_ID_MAP = {
    "300": "Passing Yards",
    "304": "Passing TDs",
    "301": "Rushing Yards",
    "305": "Rushing TDs",
    "302": "Receiving Yards",
    "306": "Receiving TDs"
}

def filter_lines_by_market_ids(props, market_id_map=MARKET_ID_MAP):
    """Filter and format lines by market IDs."""
    filtered_lines = {v: [] for v in market_id_map.values()}
    for prop_list in props.get("props", {}).values():
        for entry in prop_list:
            market_id = str(entry.get("market_id"))
            if market_id in market_id_map:
                filtered_lines[market_id_map[market_id]].append(entry)
    output = []
    for prop_type, lines in filtered_lines.items():
        if not lines:
            continue
        for line in lines:
            output.append({
                "type": prop_type,
                "label": line.get("label"),
                "line": line.get("line"),
                "cost": line.get("cost"),
                "book_id": line.get("book_id"),
                "link": line.get("link")
            })
    return output