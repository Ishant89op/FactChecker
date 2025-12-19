from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from core2.sites import financial_times
from core2.model import Result
import asyncio

async def launcher(text: str) -> list[Result]:
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

        ft = "Financial Times"
        ft_items = await financial_times(page, text)
        results.append(Result(ft, ft_items))

        await browser.close()

        return results