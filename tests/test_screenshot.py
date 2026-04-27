from unittest.mock import MagicMock, patch


def test_take_screenshot_returns_bytes():
    mock_page = MagicMock()
    mock_page.screenshot.return_value = b"\x89PNG\r\n"

    mock_browser = MagicMock()
    mock_browser.__enter__ = MagicMock(return_value=mock_browser)
    mock_browser.__exit__ = MagicMock(return_value=False)
    mock_browser.new_page.return_value = mock_page

    mock_chromium = MagicMock()
    mock_chromium.launch.return_value = mock_browser

    mock_playwright = MagicMock()
    mock_playwright.__enter__ = MagicMock(return_value=mock_playwright)
    mock_playwright.__exit__ = MagicMock(return_value=False)
    mock_playwright.chromium = mock_chromium

    with patch("screenshot.sync_playwright", return_value=mock_playwright):
        from screenshot import take_screenshot
        result = take_screenshot("https://tcgplayer.com/123")

    assert isinstance(result, bytes)


def test_take_screenshot_returns_none_on_error():
    mock_playwright = MagicMock()
    mock_playwright.__enter__ = MagicMock(side_effect=Exception("browser failed"))
    mock_playwright.__exit__ = MagicMock(return_value=False)

    with patch("screenshot.sync_playwright", return_value=mock_playwright):
        from screenshot import take_screenshot
        result = take_screenshot("https://tcgplayer.com/123")

    assert result is None
