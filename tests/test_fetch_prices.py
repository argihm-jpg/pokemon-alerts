from unittest.mock import MagicMock
from fetch_prices import extract_best_price, fetch_all_cards


def test_extract_best_price_picks_highest_market():
    card = {
        "id": "swsh1-1",
        "name": "Caterpie",
        "set": {"name": "Sword & Shield", "releaseDate": "2020-02-07"},
        "tcgplayer": {
            "url": "https://www.tcgplayer.com/product/12345",
            "prices": {
                "normal": {"market": 1.50, "low": 0.80},
                "reverseHolofoil": {"market": 3.00, "low": 1.20},
            },
        },
    }
    result = extract_best_price(card)
    assert result["market_price"] == 3.00
    assert result["low_price"] == 1.20
    assert result["variant"] == "reverseHolofoil"
    assert result["card_id"] == "swsh1-1"
    assert result["card_name"] == "Caterpie"
    assert result["set_name"] == "Sword & Shield"
    assert result["set_year"] == "2020"
    assert result["tcgplayer_url"] == "https://www.tcgplayer.com/product/12345"


def test_extract_best_price_skips_missing_market():
    card = {
        "id": "xy1-1",
        "name": "Venusaur",
        "set": {"name": "XY", "releaseDate": "2014-02-05"},
        "tcgplayer": {
            "url": "https://www.tcgplayer.com/product/99",
            "prices": {
                "holofoil": {"market": None, "low": 2.00},
                "reverseHolofoil": {"market": 3.00, "low": None},
            },
        },
    }
    result = extract_best_price(card)
    assert result is None


def test_extract_best_price_no_tcgplayer():
    card = {"id": "base1-1", "name": "Bulbasaur", "set": {}}
    result = extract_best_price(card)
    assert result is None


def test_fetch_all_cards_paginates(mocker):
    page1 = {"data": [{"id": f"card-{i}"} for i in range(250)]}
    page2 = {"data": [{"id": "card-250"}]}
    mock_get = mocker.patch("fetch_prices.requests.get")
    mock_get.return_value.json.side_effect = [page1, page2]
    mock_get.return_value.raise_for_status = MagicMock()

    cards = fetch_all_cards()
    assert len(cards) == 251
    assert mock_get.call_count == 2
