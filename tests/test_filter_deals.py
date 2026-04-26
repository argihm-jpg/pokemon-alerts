import pytest
from filter_deals import apply_filters


def make_deal(card_id, market, low):
    return {
        "card_id": card_id,
        "card_name": f"Card {card_id}",
        "set_name": "Base Set",
        "set_year": "1999",
        "variant": "holofoil",
        "market_price": market,
        "low_price": low,
        "tcgplayer_url": f"https://tcgplayer.com/{card_id}",
    }


def test_filters_out_cheap_market_price():
    deals = [make_deal("a", market=4.99, low=0.50)]
    result = apply_filters(deals, seen_ids=set())
    assert result == []


def test_filters_out_small_discount():
    # 35% off — below the 40% threshold
    deals = [make_deal("a", market=10.00, low=6.50)]
    result = apply_filters(deals, seen_ids=set())
    assert result == []


def test_includes_qualifying_deal():
    deals = [make_deal("a", market=10.00, low=5.00)]  # 50% off, $10 market
    result = apply_filters(deals, seen_ids=set())
    assert len(result) == 1
    assert result[0]["deal_score"] == pytest.approx(0.50)


def test_sorts_by_deal_score_descending():
    deals = [
        make_deal("a", market=10.00, low=5.50),  # 45% off
        make_deal("b", market=10.00, low=4.00),  # 60% off
        make_deal("c", market=10.00, low=6.00),  # 40% off
    ]
    result = apply_filters(deals, seen_ids=set())
    assert [r["card_id"] for r in result] == ["b", "a", "c"]


def test_returns_top_10_only():
    deals = [make_deal(str(i), market=10.00, low=1.00) for i in range(20)]
    result = apply_filters(deals, seen_ids=set())
    assert len(result) == 10


def test_excludes_seen_ids():
    deals = [
        make_deal("a", market=10.00, low=5.00),
        make_deal("b", market=10.00, low=5.00),
    ]
    result = apply_filters(deals, seen_ids={"a"})
    assert len(result) == 1
    assert result[0]["card_id"] == "b"


def test_includes_deal_at_exact_40_percent_threshold():
    # filter is strictly less-than, so exactly 40% must pass
    deals = [make_deal("a", market=10.00, low=6.00)]
    result = apply_filters(deals, seen_ids=set())
    assert len(result) == 1


def test_empty_price_entries_returns_empty():
    result = apply_filters([], seen_ids=set())
    assert result == []
