import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from core2.sites import financial_times
from core2.sites import times_of_india

from model.result import Result
from model.verifier_result import VerifierResult

async def launcher(text: str = "inflation") -> VerifierResult:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False
        )

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            is_mobile=False,
            java_script_enabled=True
        )

        stealth = Stealth()
        page = await context.new_page()
        await stealth.apply_stealth_async(page)

        results: list[Result] = []
        found_on = 0

        # 1. Financial Times
        # ft_result = await financial_times(page, text)
        # if(ft_result.found):
        #   found_on += 1
        # results.append(ft_result)

        # 2. Times of India
        toi_result = await times_of_india(page, text)
        if(toi_result):
            found_on += 1
        results.append(toi_result)

        await browser.close()

        if(found_on > 0):
            return VerifierResult(
                found_on = found_on,
                total_checked = len(results),
                results = results
            )
        else:
            return VerifierResult(
                error = "Something happened, we are working on it!"
            )