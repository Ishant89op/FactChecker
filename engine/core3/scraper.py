import asyncio
import random
import logging
from datetime import datetime, timezone
from urllib.parse import quote_plus

from playwright.async_api import async_playwright, Page, BrowserContext
from playwright_stealth import Stealth

from core3.models import SourceEvidence
from core3.sources import SourceConfig, select_sources
from core3.stance import detect_stance

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
]

SOURCE_TIMEOUT_MS = 15000
BATCH_SIZE = 3


async def _scrape_single_source(
    page: Page,
    source: SourceConfig,
    query: str,
) -> SourceEvidence | None:
    encoded = quote_plus(query)
    url = source.search_url_template.format(query=encoded)

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=SOURCE_TIMEOUT_MS)
        await page.wait_for_timeout(random.randint(800, 2000))

        results = await page.query_selector_all(source.result_selector)
        if not results:
            logger.info(f"{source.name}: no results found")
            return None

        first_result = results[0]
        snippet_el = await first_result.query_selector(source.snippet_selector)

        if snippet_el:
            text = await snippet_el.inner_text()
        else:
            text = await first_result.inner_text()

        text = " ".join(text.split())
        if len(text) > 500:
            text = text[:497] + "..."

        if len(text.strip()) < 10:
            logger.info(f"{source.name}: snippet too short, skipping")
            return None

        link_el = await first_result.query_selector("a[href]")
        result_url = url
        if link_el:
            href = await link_el.get_attribute("href")
            if href and href.startswith("http"):
                result_url = href

        stance = detect_stance(text)

        return SourceEvidence(
            source_name=source.name,
            url=result_url,
            relevant_text=text,
            stance=stance,
            scraped_at=datetime.now(timezone.utc),
        )

    except Exception as e:
        logger.warning(f"{source.name}: scrape failed - {str(e)[:100]}")
        return None


async def _scrape_batch(
    context: BrowserContext,
    sources: list[SourceConfig],
    query: str,
) -> list[SourceEvidence]:
    results = []
    for source in sources:
        ua = random.choice(USER_AGENTS)
        page = await context.new_page()
        try:
            await page.set_extra_http_headers({"User-Agent": ua})
            stealth = Stealth()
            await stealth.apply_stealth_async(page)

            evidence = await _scrape_single_source(page, source, query)
            if evidence:
                results.append(evidence)
        finally:
            await page.close()

        delay = random.uniform(1.0, 3.0)
        await asyncio.sleep(delay)

    return results


async def scrape_all(claim_text: str) -> list[SourceEvidence]:
    sources = select_sources(claim_text)
    all_evidence: list[SourceEvidence] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
            ],
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
            java_script_enabled=True,
        )

        try:
            batches = []
            for i in range(0, len(sources), BATCH_SIZE):
                batches.append(sources[i : i + BATCH_SIZE])

            for batch in batches:
                batch_results = await _scrape_batch(context, batch, claim_text)
                all_evidence.extend(batch_results)

        finally:
            await context.close()
            await browser.close()

    logger.info(f"Scraping complete: {len(all_evidence)} sources returned evidence")
    return all_evidence
