from __future__ import annotations

import httpx
from bs4 import BeautifulSoup


_MAX_CHARS = 12_000


class Scraper:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def fetch(self, url: str) -> str:
        response = await self._client.get(url)
        if response.status_code >= 400:
            raise RuntimeError(f"HTTP {response.status_code} for {url}")

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        root = soup.find("article") or soup.body
        text = root.get_text(separator="\n", strip=True) if root else ""
        if not text:
            raise ValueError("Page body is empty")

        return text[:_MAX_CHARS]
