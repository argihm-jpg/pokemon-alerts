import os
import sys

from fetch_prices import fetch_all_cards, extract_best_price
from filter_deals import apply_filters
from seen_deals import load_seen, save_seen, get_seen_ids, mark_seen
from screenshot import take_screenshot
from tweet_writer import generate_tweet
from notifier import send_deal, send_text

SEEN_DEALS_PATH = "seen_deals.json"


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    api_key = os.environ.get("POKEMONTCG_API_KEY")

    print("Fetching card prices from PokémonTCG.io...")
    try:
        cards = fetch_all_cards(api_key)
    except Exception as exc:
        print(f"API error: {exc}")
        send_text(token, chat_id, "⚠️ PokémonTCG.io API no disponible hoy.")
        sys.exit(1)

    price_entries = [extract_best_price(c) for c in cards]
    price_entries = [e for e in price_entries if e is not None]

    seen_data = load_seen(SEEN_DEALS_PATH)
    seen_ids = get_seen_ids(seen_data)

    deals = apply_filters(price_entries, seen_ids)

    if not deals:
        print("No qualifying deals today.")
        send_text(token, chat_id, "📭 Sin gangas hoy (criterios: $5+, 40% off)")
        return

    total = len(deals)
    print(f"Found {total} deals. Sending notifications...")

    for i, deal in enumerate(deals, start=1):
        print(f"Processing deal {i}/{total}: {deal['card_name']}")
        try:
            screenshot = take_screenshot(deal["tcgplayer_url"])
            tweet = generate_tweet(deal)
            send_deal(token, chat_id, deal, tweet, screenshot, index=i, total=total)
        except Exception as exc:
            print(f"Failed to send deal {i}: {exc}")
        seen_data = mark_seen(seen_data, deal["card_id"], deal["card_name"])

    save_seen(seen_data, SEEN_DEALS_PATH)
    print("Done.")


if __name__ == "__main__":
    main()
