from urllib.parse import urlparse, quote_plus
import asyncio
from core.extractor import phrase_matcher, number_matcher
from typing import Optional
from dataclasses import dataclass

from typing import Optional

@dataclass
class Result:
    def __init__(
        self,
        found: bool = False,
        site: str = "",
        url: str = "",
        snippet: str = "",
        numbers_matched: int = -1,
        phrases_matched: int = -1,
        verdict: bool = False,
        error: Optional[str] = None
    ):
        self.found = found
        self.site = site
        self.url = url
        self.snippet = snippet
        self.numbers_matched = numbers_matched
        self.phrases_matched = phrases_matched
        self.verdict = verdict
        self.error = error


async def check_site(page, site_name: str, site_url: str, keywords: list, numbers: list, phrases: list) -> dict:
    try:
        domain = urlparse(site_url).netloc
        search_keywords = ' '.join(keywords[:10])
        google_query = f"site:{domain} {search_keywords}"
        encoded_query = quote_plus(google_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        print(f"   Checking {site_name}...")
        print(f"   Query: {google_query}")

        await page.goto(search_url, wait_until="networkidle", timeout=30000)
        await page.wait(2000)

        page_content = await page.content()
        
        if "unusual traffic" in page_content.lower() or "captcha" in page_content.lower():
            print(f"    CAPTCHA detected")
            return Result(
                error = "CAPTCHA detected"
            )

        no_results_selectors = [
            'text="did not match any documents"',
            'text="No results found"',
            '.mnr-c'
        ]
        
        for selector in no_results_selectors:
            no_results = await page.query_selector(selector)
            if no_results:
                print(f"   ✗ No results found")
                return {"found": False, "url": "", "snippet": ""}
        
        result_selectors = [
            'div.g',
            'div[data-sokoban-container]',
            '.tF2Cxc',
            'div[jscontroller]'
        ]
        
        result_divs = []
        for selector in result_selectors:
            result_divs = await page.query_selector_all(selector)
            if result_divs and len(result_divs) > 0:
                break
        
        if not result_divs or len(result_divs) == 0:
            print(f"   ✗ No result divs found")
            return {"found": False, "url": "", "snippet": ""}
        
        print(f"   Found {len(result_divs)} results")
        
        first_result = result_divs[0]
        link = await first_result.query_selector('a[href^="http"]')
        
        if not link:
            print(f"   ✗ No link found")
            return {"found": False, "url": "", "snippet": ""}
        
        article_url = await link.get_attribute('href')

        if not article_url or not article_url.startswith('http'):
            print(f"   ✗ Invalid URL")
            return {"found": False, "url": "", "snippet": ""}
        
        snippet_text = await first_result.inner_text()
        snippet_clean = ' '.join(snippet_text.split())

        phrases_matched = phrase_matcher(snippet_clean[:500], phrases)
        numbers_matched = number_matcher(snippet_clean[:500], numbers)
        verdict: bool = False

        if phrases_matched > 0:
            if len(numbers) > 0:
                if numbers_matched > 0:
                    verdict = True
                else:
                    verdict = False
            else:
                verdict = True

        print(f"   ✓ Found: {article_url[:60]}...")

        return Result(
            found = True,
            site = site_name,
            url = article_url,
            snippet = snippet_clean,
            numbers_matched = numbers_matched,
            phrases_matched = phrases_matched,
            verdict = verdict
        )

    except Exception as e:
        print(f"    Error: {str(e)}")
        return Result(
            error = str(e)
        )