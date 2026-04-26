import json
import os
from datetime import date, timedelta

DEDUP_WINDOW_DAYS = 7
DEFAULT_PATH = "seen_deals.json"


def load_seen(path: str = DEFAULT_PATH) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def save_seen(data: dict, path: str = DEFAULT_PATH) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_seen_ids(data: dict) -> set[str]:
    cutoff = date.today() - timedelta(days=DEDUP_WINDOW_DAYS)
    return {
        card_id
        for card_id, info in data.items()
        if date.fromisoformat(info["first_seen"]) > cutoff
    }


def mark_seen(data: dict, card_id: str, card_name: str) -> dict:
    updated = dict(data)
    updated[card_id] = {"first_seen": date.today().isoformat(), "card_name": card_name}
    return updated
