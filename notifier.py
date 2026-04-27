import io
import requests

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


def _build_caption(deal: dict, tweet: str, index: int, total: int) -> str:
    discount_pct = int(deal["deal_score"] * 100)
    return (
        f"🚨 GANGA DETECTADA — #{index} de {total}\n\n"
        f"🃏 {deal['card_name']} ({deal['set_name']}, {deal['set_year']})\n"
        f"💰 Mercado: ${deal['market_price']:.2f}  →  Precio actual: ${deal['low_price']:.2f}\n"
        f"📉 Descuento: {discount_pct}% off\n\n"
        f"📝 Tweet listo para copiar:\n{tweet}"
    )


def send_deal(
    token: str,
    chat_id: str,
    deal: dict,
    tweet: str,
    screenshot: bytes | None,
    index: int,
    total: int,
) -> None:
    caption = _build_caption(deal, tweet, index, total)

    if screenshot is not None:
        resp = requests.post(
            TELEGRAM_API.format(token=token, method="sendPhoto"),
            data={"chat_id": chat_id, "caption": caption},
            files={"photo": ("screenshot.png", io.BytesIO(screenshot), "image/png")},
        )
    else:
        resp = requests.post(
            TELEGRAM_API.format(token=token, method="sendMessage"),
            json={"chat_id": chat_id, "text": caption},
        )
    resp.raise_for_status()


def send_text(token: str, chat_id: str, text: str) -> None:
    resp = requests.post(
        TELEGRAM_API.format(token=token, method="sendMessage"),
        json={"chat_id": chat_id, "text": text},
    )
    resp.raise_for_status()
