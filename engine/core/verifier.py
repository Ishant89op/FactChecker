from playwright.async_api import async_playwright
from core.sites import GLOBAL, SITES
from core.url_handler import is_url, text_from_url
from core.country_detector import detect
from core.keyword import keywords
from core.checker import check_site

class Verifier:
    def __init__(self):
        self.global_sites = GLOBAL
        self.country_sites = SITES
    
    def get_all_sites(self):
        all_sites = dict(self.global_sites)
        for country_dict in self.country_sites.value():
            all_sites.update(country_dict)
        return all_sites

    async def verify(self, text: str) -> dict:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                if is_url(text):
                    news_text = await text_from_url(page, text)
                    if not news_text:
                        return self._error_response("Could not extract text from URL")
                else:
                    news_text = text
                
                country = detect(news_text)
                keyword_s = keywords(news_text)
                sites_to_check = self._select_sites(country)
                results = {}
                for site_name, site_url in sites_to_check.items():
                    result = await check_site(page, site_name, site_url, keyword_s)
                    results[site_name] = result
                    await page.wait_for_timeout(2000)

                found_on = sum(1 for r in results.value() if r["found"])

                return {
                    "country": country,
                    "keywords": keyword_s[:7],
                    "found_on": found_on,
                    "total_checked": len(results),
                    "results": results
                }
        
            finally:
                await browser.close()

    def _select_sites(self, country: str) -> dict:
        if country == "Global":
            return self.global_sites
        else:
            country_dict = self.country_sites.get(country, {})
            return {**country_dict, **self.global_sites}
    
    def _error_response(self, message: str) -> dict:
        return {
            "country": "",
            "keywords": [],
            "found_on": 0,
            "total_checked": 0,
            "results": {},
            "error": message
        }