from model.result import Result

async def times_of_india(page, text: str  = "inflation") -> Result:
    site_name = "The Times of India"
    site_url = "https://timesofindia.indiatimes.com/"

    print(f"Checking {site_name}...")

    await page.goto(site_url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(5000)
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

    await page.locator("span.OG1TB").click()
    print(f"Search Button Selected")

    search = page.locator("#searchField")
    print(f"Found Search Input Field")

    # await search.click()
    # print(f"Search Field Selected")

    await search.fill(text)
    print(f"Input Field Filled")

    await page.keyboard.press('Enter')
    print(f"Pressed Enter")

    print(f"Selecting Results List")
    await page.wait_for_selector('div.tabs_common', timeout=10000)
    print(f"Got the List")

    # await page.wait_for_timeout(200000)

    print("Trying to get first entry")

    await page.wait_for_selector("a[href*='articleshow']", state="attached")

    element = page.locator("a[href*='articleshow']").first

    url = await element.get_attribute("href")
    heading = (await element.inner_text()).split("\n")[0]
    print(f"Got the url and heading")

    found = True

    if(found):
        return Result(
            found = found,
            site = site_name,
            url = url,
            snippet = heading,
            verdict = found
        )
    else:
        return Result(
            error = "Cannot fetch. Something happened!"
        )
