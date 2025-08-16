import re
from typing import List

from feedunify.models import FeedItem
from .rss import RssConnector

CHANNEL_ID_REGEX = re.compile(r'(?:channelId":"|content=")(UC[a-zA-Z0-9_-]{22})')

class YouTubeConnector(RssConnector):
    async def fetch(self) -> List[FeedItem]:
        if "youtube.com/feeds/" in self.source_url:
            return await super().fetch()
        
        print(f"Attempting to find Channel ID for: {self.source_url}")
        response = await self.http_client.get(self.source_url)
        response.raise_for_status()
        html_content = response.text

        match = CHANNEL_ID_REGEX.search(html_content)

        if not match:
            print(f"Error: Could not find Channel ID for URL: {self.source_url}")
            return []
        
        channel_id = match.group(1)

        self.source_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        print(f"Found RSS feed: {self.source_url}")

        return await super().fetch()