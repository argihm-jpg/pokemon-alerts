from playwright.sync_api import sync_playwright


def take_screenshot(url: str) -> bytes | None:
    try:
        with sync_playwright() as p:
            with p.chromium.launch(headless=True) as browser:
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.goto(url, wait_until="networkidle", timeout=30000)
                return page.screenshot(full_page=False)
    except Exception as exc:
        print(f"Screenshot failed for {url}: {exc}")
        return None
