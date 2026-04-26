MIN_MARKET_PRICE = 5.00
MIN_DISCOUNT = 0.40
TOP_N = 10


def apply_filters(price_entries: list[dict], seen_ids: set[str]) -> list[dict]:
    qualifying = []
    for entry in price_entries:
        if entry["card_id"] in seen_ids:
            continue
        if entry["market_price"] < MIN_MARKET_PRICE:
            continue
        deal_score = (entry["market_price"] - entry["low_price"]) / entry["market_price"]
        if deal_score < MIN_DISCOUNT:
            continue
        qualifying.append({**entry, "deal_score": deal_score})

    qualifying.sort(key=lambda x: x["deal_score"], reverse=True)
    return qualifying[:TOP_N]
