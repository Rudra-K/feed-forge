import re
from typing import List

from feedunify.models import FeedItem
from .rss import RssConnector

# Captures the 24-character ID (UC + 22 characters).
CHANNEL_ID_REGEX = re.compile(r'(?:channelId":"|content=")(UC[a-zA-Z0-9_-]{22})')

class YouTubeConnector(RssConnector):
    """
    A smart connector for YouTube that inherits from RssConnector.

    It can handle both direct YouTube RSS feed URLs and standard, channel URLs (e.g.,
    youtube.com/@username).
    """
    async def fetch(self) -> List[FeedItem]:
        """
        Overrides the parent fetch method to add URL detection.

        If a standard channel URL is provided, this method first fetches the
        channel's HTML page, finds the unique channel ID, constructs the
        correct RSS feed URL, and then conducts the final fetching and
        parsing back to the parent RssConnector's fetch method.

        Returns:
            A list of FeedItem objects representing the channel's latest videos,
            or an empty list if the channel ID cannot be found.
        """
        # If the URL is already a feed URL, use the parent's method directly.
        if "youtube.com/feeds/" in self.source_url:
            return await super().fetch()
        
        # If standard YouTube channel URL is provided
        print(f"Attempting to find Channel ID for: {self.source_url}")
        response = await self.http_client.get(self.source_url)
        response.raise_for_status()
        html_content = response.text

        match = CHANNEL_ID_REGEX.search(html_content)

        if not match:
            print(f"Error: Could not find Channel ID for URL: {self.source_url}")
            return []
        
        channel_id = match.group(1)

        # The converted RSS feed URL
        self.source_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        print(f"Found RSS feed: {self.source_url}")

        return await super().fetch()