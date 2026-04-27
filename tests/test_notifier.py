from unittest.mock import MagicMock, patch
from notifier import send_deal, send_text

FAKE_TOKEN = "123:ABC"
FAKE_CHAT_ID = "456789"


def _make_deal(name="Charizard VMAX", market=20.00, low=8.00, score=0.60):
    return {
        "card_name": name,
        "market_price": market,
        "low_price": low,
        "deal_score": score,
        "tcgplayer_url": "https://tcgplayer.com/1",
        "set_name": "Darkness Ablaze",
        "set_year": "2020",
    }


def test_send_deal_with_screenshot_calls_sendPhoto():
    tweet = "Don't sleep on this Charizard VMAX for under $8! 🔥\nhttps://tcgplayer.com/1"
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()

    with patch("notifier.requests.post", return_value=mock_resp) as mock_post:
        send_deal(FAKE_TOKEN, FAKE_CHAT_ID, _make_deal(), tweet, b"\x89PNG", index=1, total=10)

    mock_post.assert_called_once()
    assert "sendPhoto" in mock_post.call_args[0][0]


def test_send_deal_without_screenshot_calls_sendMessage():
    tweet = "You can still grab Pikachu for just $5! 🔥\nhttps://tcgplayer.com/2"
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()

    with patch("notifier.requests.post", return_value=mock_resp) as mock_post:
        send_deal(FAKE_TOKEN, FAKE_CHAT_ID, _make_deal("Pikachu", 10.00, 5.00, 0.50), tweet, None, index=1, total=10)

    mock_post.assert_called_once()
    assert "sendMessage" in mock_post.call_args[0][0]


def test_send_deal_caption_contains_key_info():
    tweet = "You can still grab Charizard VMAX for just $8! 🔥\nhttps://tcgplayer.com/1"
    captured_kwargs = {}
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()

    def capture_post(url, **kwargs):
        captured_kwargs.update(kwargs)
        return mock_resp

    with patch("notifier.requests.post", side_effect=capture_post):
        send_deal(FAKE_TOKEN, FAKE_CHAT_ID, _make_deal(), tweet, None, index=3, total=10)

    text = captured_kwargs.get("json", {}).get("text", "")
    assert "#3 de 10" in text
    assert "Charizard VMAX" in text
    assert "60%" in text


def test_send_text_calls_sendMessage():
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()

    with patch("notifier.requests.post", return_value=mock_resp) as mock_post:
        send_text(FAKE_TOKEN, FAKE_CHAT_ID, "Sin gangas hoy")

    mock_post.assert_called_once()
    assert "sendMessage" in mock_post.call_args[0][0]
