from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from sites.financial_times import financial_times
import asyncio

async def launcher(text: str) -> str:
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

        await financial_times(page)

        browser.close()

async def main():
    await launcher("What is this?")

if __name__ == "__main__":
    asyncio.run(main())