from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def financial_times(page):
    site_name = "Financial Times"
    site_url = "https://www.ft.com"

    print(f"Checking {site_name}...")

    await page.goto(site_url, wait_until='networkidle', timeout=30000)
    await page.wait_for_timeout(3000)

    # if accept cookies come up, accept them
    try:
        await page.get_by_role(
            "button",
            name="Accept Cookies"
        ).click(timeout=2000)
    except:
        pass

    
    await page.get_by_role("button", name="Search").click()

    await page.get_by_role("searchbox").fill("inflation")
    await page.keyboard.press("Enter")