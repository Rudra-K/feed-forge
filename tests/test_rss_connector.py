import pytest
from feedunify.connectors.rss import RssConnector
from feedunify.models import FeedItem

TEST_FEED_URL = "https://www.theverge.com/rss/index.xml"

@pytest.mark.asyncio
async def test_rss_connector_fetches_and_parses_data():
    connector = RssConnector(source_url=TEST_FEED_URL)

    items = await connector.fetch()

    #check if we got list back
    assert isinstance(items, list)

    #check if list is not empty
    assert len(items) > 0

    first_item = items[0]

    #check if first_item is an instance of FeedItem model.
    # to prove parsing and pydantic validation works.
    assert isinstance(first_item, FeedItem)

    #check key fields
    assert first_item.title is not None
    assert first_item.url is not None
    assert str(first_item.source_url) == TEST_FEED_URL

    await connector.close()