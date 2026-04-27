from tweet_writer import generate_tweet, TEMPLATES


def make_deal(name, low_price, url):
    return {
        "card_name": name,
        "set_name": "Paldea Evolved",
        "set_year": "2023",
        "low_price": low_price,
        "market_price": 12.50,
        "tcgplayer_url": url,
    }


def test_tweet_contains_card_name():
    deal = make_deal("Dewgong ex", 5.00, "https://tcgplayer.com/123")
    tweet = generate_tweet(deal)
    assert "Dewgong ex" in tweet


def test_tweet_contains_price():
    deal = make_deal("Dewgong ex", 5.00, "https://tcgplayer.com/123")
    tweet = generate_tweet(deal)
    assert "$5" in tweet


def test_tweet_contains_url():
    deal = make_deal("Dewgong ex", 5.00, "https://tcgplayer.com/123")
    tweet = generate_tweet(deal)
    assert "https://tcgplayer.com/123" in tweet


def test_tweet_contains_fire_emoji():
    deal = make_deal("Dewgong ex", 5.00, "https://tcgplayer.com/123")
    tweet = generate_tweet(deal)
    assert "🔥" in tweet


def test_tweet_under_280_chars():
    deal = make_deal("Extremely Long Pokemon Card Name VMAX GX EX", 99.99, "https://tcgplayer.com/123")
    tweet = generate_tweet(deal)
    assert len(tweet) <= 280


def test_all_templates_contain_required_elements():
    for template in TEMPLATES:
        assert "🔥" in template
        assert "{url}" in template
        assert "{name}" in template
        assert "${price}" in template
