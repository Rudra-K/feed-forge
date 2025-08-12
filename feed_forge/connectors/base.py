import abc
from typing import List, Optional, Dict, Any
import httpx

from feed_forge.models import FeedItem

#base blueprint of all data source connectors
class BaseConnector(abc.ABC):
    def __init__(self, source_url: str, config: Optional[Dict[str, Any]] = None):
        self.source_url = source_url
        self.config = config or {}
        self.http_client = httpx.AsyncClient(follow_redirects=True)


    async def fetch(self) -> List[FeedItem]:
        try:
            response = await self.http_client.get(self.source_url)
            response.raise_for_status()

            items = self._parse(response.content)
            return items
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
            return []
        
    @abc.abstractmethod
    def _parse(self, raw_content: bytes) -> List[FeedItem]:
        pass

    async def close(self):
        await self.http_client.aclose()