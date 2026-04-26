import json
import pytest
from datetime import date, timedelta
from seen_deals import load_seen, save_seen, get_seen_ids, mark_seen


@pytest.fixture
def tmp_json(tmp_path):
    return str(tmp_path / "seen_deals.json")


def test_load_seen_empty_file(tmp_json):
    with open(tmp_json, "w") as f:
        json.dump({}, f)
    data = load_seen(tmp_json)
    assert data == {}


def test_load_seen_missing_file(tmp_json):
    data = load_seen(tmp_json)
    assert data == {}


def test_get_seen_ids_excludes_within_7_days():
    today = date.today()
    data = {
        "old-card": {"first_seen": (today - timedelta(days=8)).isoformat(), "card_name": "Old"},
        "new-card": {"first_seen": today.isoformat(), "card_name": "New"},
    }
    ids = get_seen_ids(data)
    assert "new-card" in ids
    assert "old-card" not in ids


def test_mark_seen_adds_entry():
    data = {}
    today = date.today().isoformat()
    updated = mark_seen(data, "swsh1-25", "Charizard VMAX")
    assert "swsh1-25" in updated
    assert updated["swsh1-25"]["first_seen"] == today
    assert updated["swsh1-25"]["card_name"] == "Charizard VMAX"


def test_mark_seen_does_not_mutate_original():
    data = {}
    mark_seen(data, "xy1-1", "Venusaur")
    assert "xy1-1" not in data


def test_save_and_reload(tmp_json):
    data = {"xy1-1": {"first_seen": "2026-04-20", "card_name": "Venusaur"}}
    save_seen(data, tmp_json)
    reloaded = load_seen(tmp_json)
    assert reloaded == data
