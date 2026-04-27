from playwright.sync_api import sync_playwright


def take_screenshot(url: str) -> bytes | None:
    try:
        with sync_playwright() as p:
            with p.chromium.launch(headless=True) as browser:
                context = browser.new_context(
                    viewport={"width": 1280, "height": 900},
                    user_agent=(
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                # TCGPlayer renders listings via JS — wait for the price table or fall back to a fixed delay
                try:
                    page.wait_for_selector(".listing-item__listing-data", timeout=8000)
                except Exception:
                    page.wait_for_timeout(4000)
                return page.screenshot(full_page=False)
    except Exception as exc:
        print(f"Screenshot failed for {url}: {exc}")
        return None
