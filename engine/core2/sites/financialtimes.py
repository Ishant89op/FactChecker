from core2.model import Item

async def financial_times(page, text: str = "inflation") -> list[Item]:
    site_name = "Financial Times"
    site_url = "https://www.ft.com"

    print(f"Checking {site_name}...")

    await page.goto(site_url, wait_until='networkidle', timeout=30000)

    print(f"Page Loaded.")

    # if accept cookies come up, accept them
    try:
        print(f"Trying to accept cookies page.")

        # await page.locator('button:text("Accept Cookies")').click(timeout=5000)
        # await page.click('Button[title="Accept Cookies"]')

        frame = page.frame_locator('iframe[src*="consent"]')
        print(f"Selected iFrame")
        await frame.get_by_role("button", name="Accept Cookies").click(timeout=5000)
        print(f"Accepted Cookies")
    except:
        print(f"Cookies page passed")
        pass

    print(f"Trying to find the search button")

    await page.get_by_role("button", name="Search").click()
    print(f"Search Button Selected")

    search = page.locator('#o-header-search-term-primary')
    print(f"Found Search Input Field")

    await search.click()
    print(f"Search Field Selected")

    await search.fill("Inflation")
    print(f"Input Field Filled")

    await page.keyboard.press('Enter')
    print(f"Pressed Enter")

    await page.wait_for_timeout(2000)

    print(f"Selecting Results List")
    await page.wait_for_selector('ul.search-results__list li.search-results__list-item', timeout=10000)
    print(f"Selected Results List")

    elements = page.locator('a.js-teaser-heading-link')

    headings = await elements.all_text_contents()
    urls = await elements.evaluate_all("els => els.map(e => e.href)")

    print(f"Got all the headings and urls of the headings.")

    items: list[Item] = [
        Item(heading=h.strip(), url=u)
        for h, u in zip(headings, urls)
    ]

    # for i, item in enumerate(items, 1):
    #   print(f"{i:02}. {item.heading}\n    {item.url}\n")

    return items