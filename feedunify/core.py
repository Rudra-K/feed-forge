import asyncio
from typing import List, Callable, Optional

from .connectors.youtube import YouTubeConnector
from .connectors.rss import RssConnector
from .models import FeedItem

class Forge:
    """
    The main entry point for using the feedunify library.

    Dispatches URLs to the appropriate connector based on a set of detection rules.
    """
    def __init__(self):
        self._connectors = [
            {
                'name': 'youtube',
                'detector': lambda url: 'youtube.com/' in url,
                'class': YouTubeConnector,
            },
            {
                'name': 'rss',
                'detector': lambda url: (
                    url.endswith(('.xml', '.rss', '.atom')) or 
                    'rss' in url or 
                    '/feed/' in url or 
                    '/atom/' in url
                ),
                'class': RssConnector,
            }
            #add more connectors here
        ]
    
    def _find_connector_for_url(self, url: str) -> Optional[Callable]:
        """
        Finds the appropriate connector class for a given URL.

        Args:
            url: The URL of the data source.

        Returns:
            The connector class if a match is found, otherwise None.
        """
        for connector_info in self._connectors:
            if connector_info['detector'](url):
                return connector_info['class']
        return None
        

    async def fetch_all(self, sources: List[str]) -> List[FeedItem]:
        """
        Fetches and parses items from a list of source URLs concurrently.

        Args:
            sources: A list of URLs.

        Returns:
            A single list of FeedItem objects from all successful sources.
        """
        tasks = []
        for url in sources:
            connector_class = self._find_connector_for_url(url)

            if connector_class:
                connector = connector_class(source_url=url)
                task = asyncio.create_task(connector.fetch())
                tasks.append(task)
            else:
                print(f"Warning: No suitable connector found for URL: {url}")

        # Gathers and run all scheduled tasks concurrently.
        results_from_all_sources = await asyncio.gather(*tasks, return_exceptions=True)

        all_items = []
        for item_list in results_from_all_sources:
            if isinstance(item_list, list):
                all_items.extend(item_list)

        return all_items