import asyncio
from typing import List

from .connectors.rss import RssConnector
from .models import FeedItem

class Forge:
    def __init__(self):
        #(in future) add a more dynamic system for discovering and 
        # registering all available connectors.

        #for now, list of connectors will do.
        self._connectors = {
            'rss': RssConnector,
        }

    async def fetch_all(self, sources: List[str]) -> List[FeedItem]:
        tasks = []
        #(in future) add logic to detect the source type.
        connector_class = self._connectors['rss'] #assuming all sources are RSS feeds.

        for url in sources:
            connector = connector_class(source_url=url)

            task = asyncio.create_task(connector.fetch())
            tasks.append(task)

        results_from_all_sources = await asyncio.gather(*tasks)

        all_items = []
        for item_list in results_from_all_sources:
            all_items.extend(item_list)

        return all_items