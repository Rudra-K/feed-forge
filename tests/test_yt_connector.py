import pytest
from feedunify.connectors.youtube import YouTubeConnector
from feedunify.models import FeedItem

TEST_CHANNEL_URL = "https://www.youtube.com/@theRadBrad"

@pytest.mark.asyncio
async def test_youtube_connector_finds_feed_and_parses():

    connector = YouTubeConnector(source_url=TEST_CHANNEL_URL)

    items = await connector.fetch()

    # Check the results.
    assert isinstance(items, list)
    assert len(items) > 0

    first_item = items[0]
    assert isinstance(first_item, FeedItem)

    # Check that the source_url was correctly transformed into the RSS feed URL.
    assert "youtube.com/feeds/videos.xml" in str(first_item.source_url)
    
    # Check that key fields were populated.
    assert first_item.title is not None
    assert "theRadBrad" in first_item.authors[0].name

    await connector.close()