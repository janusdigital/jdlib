import logging
import random
import time

from playwright.sync_api import sync_playwright

from jdlib.scrapers.exceptions import HttpError

logger = logging.getLogger(__name__)


class Scraper:
    """A web scraper that maintains a reusuble Playwright browser instance."""

    def __init__(self):
        self._playwright = None
        self._browser = None

    def __enter__(self):
        return self
    
    def __exit__(self):
        self.close()

    @property
    def browser(self):
        """Return the browser instance, launching one if needed."""
        if self._browser is None or not self._browser.is_connected():
            self._ensure_playwright()
            logger.info('Launching browser.')
            kwargs = {'headless': True}
            self._browser = self._playwright.chromium.launch(**kwargs)
        return self._browser
    
    def _close_browser(self):
        """Close browser. Will be restarted when `self.browser` is called."""
        if self._browser is None:
            logger.info('Shutting down browser.')
            self._browser.close()
            self._browser = None

    def _ensure_playwright(self):
        """Start the Playwright instance if not already running."""
        if self._playwright is None:
            self._playwright = sync_playwright().start()

    def get(self, url, *, raise_exception=False, wait_until='networkidle'):
        context = self.browser.new_context()
        try:
            page = context.new_page()
            logger.info('GET %s', url)
            response = page.goto(url, wait_until=wait_until)
            if response is None or response.status >= 400:
                if raise_exception:
                    status = 0 if response is None else response.status
                    raise HttpError(url, status)
                return None
            return page.content()
        finally:
            context.close()

    def get_with_retry(self, url, *, wait_until='networkidle', max_retries=8, base_delay=1.0):
        for attempt in range(max_retries + 1):
            try:
                return self.get(url, wait_until=wait_until)
            except Exception:
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                logger.warning(
                    'Attempt %d/%d failed for %s. retrying in %.1fs.',
                    attempt + 1,
                    max_retries + 1,
                    url,
                    delay,
                )
                time.sleep(delay)
                self._close_browser()
        logger.warning('Max retries for %s exceeded.', url)
        return None


    def close(self):
        """Close browser and playwright."""
        self._close_browser()
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None
