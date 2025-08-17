import abc
from typing import List, Optional, Dict, Any
import httpx

from feedunify.models import FeedItem

#base blueprint of all data source connectors
class BaseConnector(abc.ABC):
    """
    An abstract base class that serves as a blueprint for all data source connectors.

    Defines a contract that all subclasses must follow by implementing
    the `_parse` method.
    """
    def __init__(self, source_url: str, config: Optional[Dict[str, Any]] = None):
        """
        Initializes the connector with a source URL and an HTTP client.

        Args:
            source_url: The primary URL for the data source.
            config: An optional dictionary for connector-specific settings.
        """
        self.source_url = source_url
        self.config = config or {}

        # Added this to avoid connection_timeout errors.
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }
        
        self.http_client = httpx.AsyncClient(
            headers=headers,
            follow_redirects=True,
            timeout=30.0
        )

    async def fetch(self) -> List[FeedItem]:
        """
        Fetches and parses data from the source URL.

        Returns:
            A list of FeedItem objects, or an empty list if an error occurs.
        """
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
        """
        Parses the raw fetched content into a list of FeedItems.

        Args:
            raw_content: The raw content of the response from the source.

        Returns:
            A list of standardized FeedItem objects.
        """
        pass

    async def close(self):
        await self.http_client.aclose()