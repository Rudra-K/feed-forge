import feedparser
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo

from feedunify.models import FeedItem, Author
from .base import BaseConnector

class RssConnector(BaseConnector):
    """
    A concrete connector for fetching and parsing RSS and Atom feeds.

    """
    def _parse(self, raw_content: bytes) -> List[FeedItem]:
        """
        Parses the raw XML feed content into a list of FeedItem objects.

        Args:
            raw_content: The raw bytes of the XML feed.

        Returns:
            A list of standardized FeedItem objects.
        """
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
                raw=entry,  # Store original entry for debugging.
            )
            items.append(item)

        return items
    
    def _to_datetime(self, time_struct) -> datetime | None:
        """
        Convert feedparser's time_struct to a timezone-aware datetime.

        Args:
            time_struct: A time.struct_time object from feedparser, or None.

        Returns:
            A timezone-aware datetime object set to UTC, or None if input is invalid.
        """
        if not time_struct:
            return None
        
        return datetime(*time_struct[:6], tzinfo=ZoneInfo("UTC"))