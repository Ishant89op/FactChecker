import re
from urllib.parse import urlparse

def is_url(text: str) -> bool:
    try:
        if not text.startswith(('http://', 'https://')):
            return False
        
        result  = urlparse(text)

        return all([result.scheme, result.netloc])
    
    except Exception:
        return False
    
async def text_from_url(page, url: str) -> str:
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        selectors = [
            'article',
            'main',
            '[role="article"]',
            '.article-body',
            '.article-content',
            '.post-content',
            '#article-body',
            '.entry-content'
        ]

        for selector in selectors:
            element = await page.query_selector(selector)

            if element:
                text = await element.inner_text()
                text = text.strip()
                if len(text) > 100:
                    return text
        
        body_text = await page.evaluate('document.body.innerText')
        body_text = body_text.strip()
        return body_text
    
    except Exception as e:
        return ""