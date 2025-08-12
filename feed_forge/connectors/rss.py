import feedparser
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo

from feed_forge.models import FeedItem, Author
from .base import BaseConnector

class RssConnector(BaseConnector):
    def _parse(self, raw_content: bytes) -> List[FeedItem]:
        parsed_feed = feedparser.parse(raw_content)

        items = []

        for entry in parsed_feed.entries:
            published_dt = self._to_datetime(entry.get("published_parsed"))
            authors = [Author(name=author.get("name", "Unknown")) for author in entry.get("authors", [])]

            item = FeedItem(
                id=entry.get("id", entry.link),
                source_url=self.source_url,
                url=entry.link,
                title=entry.title,
                summary=entry.get("summary"),
                published_at=published_dt,
                authors=authors,
                tags=[tag.term for tag in entry.get("tags", [])],
                raw=entry,  #for debugging
            )
            items.append(item)

        return items
    
    def _to_datetime(self, time_struct) -> datetime | None:
        if not time_struct:
            return None
        
        return datetime(*time_struct[:6], tzinfo=ZoneInfo("UTC"))