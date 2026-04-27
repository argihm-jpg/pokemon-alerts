import random

TEMPLATES = [
    "You can still grab {name} for just ${price}! 🔥\n{url}",
    "Don't sleep on this {name} for under ${price}! 🔥\n{url}",
    "Last chance to snag {name} at ${price}! 🔥\n{url}",
    "Incredible deal on {name} — only ${price}! 🔥\n{url}",
]


def generate_tweet(deal: dict) -> str:
    price = f"{deal['low_price']:.2f}".rstrip("0").rstrip(".")
    template = random.choice(TEMPLATES)
    return template.format(
        name=deal["card_name"],
        price=price,
        url=deal["tcgplayer_url"],
    )
