import asyncio
from typing import List, Callable, Optional

from .connectors.rss import RssConnector
from .models import FeedItem

class Forge:
    def __init__(self):
        self._connectors = [
            {
                'name': 'rss',
                'detector': lambda url: url.endswith(('.xml', '/rss')),
                'class': RssConnector,
            }
            #add more connectors here
        ]
    
    def _find_connector_for_url(self, url: str) -> Optional[Callable]:
        for connector_info in self._connectors:
            if connector_info['detector'](url):
                return connector_info['class']
        return None
        

    async def fetch_all(self, sources: List[str]) -> List[FeedItem]:
        tasks = []
        for url in sources:
            connector_class = self._find_connector_for_url(url)

            if connector_class:
                connector = connector_class(source_url=url)
                task = asyncio.create_task(connector.fetch())
                tasks.append(task)
            else:
                print(f"Warning: No suitable connector found for URL: {url}")

        results_from_all_sources = await asyncio.gather(*tasks, return_exceptions=True)

        all_items = []
        for item_list in results_from_all_sources:
            if isinstance(item_list, list):
                all_items.extend(item_list)

        return all_items