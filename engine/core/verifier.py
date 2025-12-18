import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth, ALL_EVASIONS_DISABLED_KWARGS
from core.sites import GLOBAL, SITES
from core.url_handler import is_url, text_from_url
from core.country_detector import detect
from core.extractor import extract_keywords, extract_numbers, create_phrases
from core.checker import check_site
from dataclasses import dataclass
from core.checker import Result
from typing import Optional

@dataclass
class VerifierResult:
    def __init__(
            self,
            country: str = "",
            keywords: list[str] = [],
            numbers: list[str] = [],
            phrases: list[str] = [],
            found_on: int = -1,
            total_checked: int = -1,
            results: list[Result] = [],
            error: Optional[str] = None

    ):
        self.country = country
        self.keywords = keywords
        self.numbers = numbers
        self.phrases = phrases
        self.found_on = found_on
        self.total_checked = total_checked
        self.results = results
        self.error = error

class Verifier:
    def __init__(self):
        self.global_sites = GLOBAL
        self.country_sites = SITES
    
    def get_all_sites(self):
        all_sites = dict(self.global_sites)
        for country_dict in self.country_sites.values():
            all_sites.update(country_dict)
        return all_sites

    async def verify(self, text: str) -> VerifierResult:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-site-isolation-trials',
                    '--disable-infobars',
                    '--window-size=1920,1080',
                    '--start-maximized'
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='en-US',
                timezone_id='America/New_York',
                permissions=['geolocation'],
                geolocation={'latitude': 40.7128, 'longitude': -74.0060},
                color_scheme='light',
                device_scale_factor=1,
                has_touch=False,
                is_mobile=False,
                java_script_enabled=True
            )

            stealth = Stealth()
            page = await context.new_page()
            await stealth.apply_stealth_async(page)
            
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = {runtime: {}};
            """)

            try:
                print(f"\n{'='*60}")
                print(f"Starting verification...")
                print(f"{'='*60}\n")
                
                if is_url(text):
                    print(f"Extracting text from URL: {text}")
                    news_text = await text_from_url(page, text)
                    if not news_text:
                        return self._error_response("Could not extract text from URL")
                    print(f"Extracted {len(news_text)} characters\n")
                else:
                    news_text = text
                
                country = detect(news_text)
                keyword_list = extract_keywords(news_text)
                numbers = extract_numbers(news_text)
                phrases = create_phrases(keyword_list)
                
                print(f"Detected Country: {country}")
                print(f"Keywords: {keyword_list[:10]}\n")
                
                sites_to_check = self._select_sites(country)
                
                print(f"Checking {len(sites_to_check)} sites...\n")
                
                results = []
                found_on = 0
                for site_name, site_url in sites_to_check.items():
                    result = await check_site(page, site_name, site_url, keyword_list, numbers, phrases)
                    
                    if result.error is not None:
                        return VerifierResult(
                            error = result.error
                        )
                    
                    verdict = result.verdict
                    if verdict: 
                        found_on += 1
                    results.append(result)
                    await page.wait_for_timeout(3000)


                print(f"\n{'='*60}")
                print(f"Verification complete: Found on {found_on}/{len(results)} sites")
                print(f"{'='*60}\n")

                return VerifierResult(
                    country = country,
                    keywords=keyword_list[:10],
                    numbers=numbers[:10],
                    phrases=phrases[:10],
                    found_on=found_on,
                    total_checked=len(results),
                    results=results
                )
        
            finally:
                await context.close()
                await browser.close()

    def _select_sites(self, country: str) -> dict:
        if country == "Global":
            return self.global_sites
        
        country_dict = self.country_sites.get(country, {})
        return {**country_dict, **self.global_sites}
    
    def _error_response(self, message: str) -> dict:
        return VerifierResult(
            error = message
        )