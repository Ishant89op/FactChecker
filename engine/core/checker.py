from urllib.parse import urlparse, quote_plus
import asyncio

async def check_site(page, site_name: str, site_url: str, keywords: list) -> dict:
    try:
        domain = urlparse(site_url).netloc
        search_keywords = ' '.join(keywords[:5])
        google_query = f"site:{domain} {search_keywords}"

        encoded_query = quote_plus(google_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)

        no_results = await page.query_selector('text="did not match any documents"')
        if no_results:
            print(f"   ❌ No results found")
            return {
                "found": False,
                "url": "",
                "snippet": ""
            }
        
        result_divs = await page.query_selector_all('div.g')
        
        if not result_divs or len(result_divs) == 0:
            print(f"   ❌ No results found")
            return {
                "found": False,
                "url": "",
                "snippet": ""
            }
        
        first_result = result_divs[0]

        link = await first_result.query_selector('a')
        if not link:
            print(f"   ❌ Could not extract URL")
            return {
                "found": False,
                "url": "",
                "snippet": ""
            }
        
        article_url = await link.get_attribute('href')

        if not article_url or not article_url.startswith('http'):
            print(f"   ❌ Invalid URL")
            return {
                "found": False,
                "url": "",
                "snippet": ""
            }
        
        snippet_text = await first_result.inner_text()
        snippet_clean = ' '.join(snippet_text.split())

        return {
            "found": True,
            "url": article_url,
            "snippet": snippet_clean[:300]
        }

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {
            "found": False,
            "url": "",
            "snippet": ""
        }
    
# async def check_site_direct(page, site_name: str, site_url: str, keywords: list) -> dict:
#     """
#     ALTERNATIVE: Check site directly using their own search
    
#     PROBLEMS WITH THIS APPROACH:
#     1. Every site has different search URLs
#     2. Some sites need login
#     3. Some sites have no search
#     4. Search results HTML is different for each site
    
#     That's why we use Google instead.
    
#     This function is kept for reference only.
#     """
#     try:
#         # Example for Reuters (would need custom code for each site)
#         search_query = '+'.join(keywords[:5])
#         search_url = f"{site_url}/search/news?query={search_query}"
        
#         await page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        
#         # Each site has different HTML structure
#         # Would need custom selectors for each site
#         articles = await page.query_selector_all('article')
        
#         if articles and len(articles) > 0:
#             first = articles[0]
#             link = await first.query_selector('a')
#             url = await link.get_attribute('href')
#             text = await first.inner_text()
            
#             return {
#                 "found": True,
#                 "url": url,
#                 "snippet": text[:300]
#             }
        
#         return {"found": False, "url": "", "snippet": ""}
    
#     except Exception as e:
#         return {"found": False, "url": "", "snippet": ""}