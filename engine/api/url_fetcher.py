import logging
from typing import Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

FETCH_TIMEOUT = 15.0
MAX_TEXT_LENGTH = 3000

UNSUPPORTED_CONTENT_TYPES = [
    "application/pdf",
    "image/",
    "video/",
    "audio/",
    "application/zip",
    "application/octet-stream",
]


class URLFetchError(Exception):
    pass


class UnsupportedContentError(Exception):
    pass


async def fetch_url_text(url: str) -> str:
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=FETCH_TIMEOUT,
        ) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36",
                },
            )
            response.raise_for_status()

        content_type = response.headers.get("content-type", "").lower()

        for unsupported in UNSUPPORTED_CONTENT_TYPES:
            if unsupported in content_type:
                raise UnsupportedContentError(
                    f"Unsupported content type: {content_type}. "
                    "Only HTML pages are supported."
                )

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        parts = []

        title = soup.find("title")
        if title and title.string:
            parts.append(title.string.strip())

        for heading in soup.find_all(["h1", "h2", "h3"], limit=5):
            text = heading.get_text(strip=True)
            if text:
                parts.append(text)

        for paragraph in soup.find_all("p"):
            text = paragraph.get_text(strip=True)
            if len(text) > 20:
                parts.append(text)

        combined = "\n".join(parts)
        combined = " ".join(combined.split())

        if len(combined) > MAX_TEXT_LENGTH:
            combined = combined[:MAX_TEXT_LENGTH]

        if len(combined.strip()) < 50:
            raise URLFetchError(
                "Could not extract meaningful text from the URL."
            )

        return combined

    except httpx.HTTPStatusError as e:
        raise URLFetchError(f"HTTP {e.response.status_code} when fetching URL")
    except httpx.TimeoutException:
        raise URLFetchError("Request timed out while fetching URL")
    except httpx.RequestError as e:
        raise URLFetchError(f"Failed to fetch URL: {str(e)[:200]}")
    except (UnsupportedContentError, URLFetchError):
        raise
    except Exception as e:
        raise URLFetchError(f"Unexpected error fetching URL: {str(e)[:200]}")
