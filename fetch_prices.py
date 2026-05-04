import time

import requests

POKEMONTCG_API_BASE = "https://api.pokemontcg.io/v2"
PAGE_SIZE = 250
_RETRY_DELAYS = [5, 10, 15]


def _get_with_retry(url: str, headers: dict, params: dict) -> requests.Response:
    last_exc: Exception | None = None
    delays = [None] + _RETRY_DELAYS  # first attempt has no pre-sleep
    for attempt, delay in enumerate(delays, start=1):
        if delay is not None:
            print(f"  API request failed, retrying in {delay}s (attempt {attempt}/{len(delays)})...")
            time.sleep(delay)
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            return resp
        except Exception as exc:
            last_exc = exc
            print(f"  Attempt {attempt} failed: {exc}")
    raise last_exc  # type: ignore[misc]


def fetch_all_cards(api_key: str | None = None) -> list[dict]:
    headers = {"X-Api-Key": api_key} if api_key else {}
    cards = []
    page = 1

    while True:
        resp = _get_with_retry(
            f"{POKEMONTCG_API_BASE}/cards",
            headers=headers,
            params={
                "page": page,
                "pageSize": PAGE_SIZE,
                "select": "id,name,set,tcgplayer,rarity",
            },
        )
        batch = resp.json().get("data", [])
        cards.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        page += 1

    return cards


def extract_best_price(card: dict) -> dict | None:
    tcgplayer = card.get("tcgplayer", {})
    prices = tcgplayer.get("prices", {})
    url = tcgplayer.get("url", "")

    best = None
    for variant, price_data in prices.items():
        market = price_data.get("market")
        low = price_data.get("low")
        if market is None or low is None:
            continue
        if best is None or market > best["market_price"]:
            best = {
                "card_id": card.get("id", ""),
                "card_name": card.get("name", "Unknown"),
                "set_name": card.get("set", {}).get("name", ""),
                "set_year": (card.get("set", {}).get("releaseDate") or "")[:4],
                "rarity": card.get("rarity", ""),
                "variant": variant,
                "market_price": market,
                "low_price": low,
                "tcgplayer_url": url,
            }
    return best
