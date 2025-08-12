import pytest
from feed_forge.core import Forge
from feed_forge.models import FeedItem

SOURCE_URL_1 = "https://www.theverge.com/rss/index.xml"
SOURCE_URL_2 = "https://www.wired.com/feed/rss"

@pytest.mark.asyncio
async def test_forge_fetches_from_multiple_sources():
    forge = Forge()
    sources_to_fetch = [SOURCE_URL_1, SOURCE_URL_2]

    all_items = await forge.fetch_all(sources=sources_to_fetch)

    #check for single, flat list.
    assert isinstance(all_items, list)
    assert len(all_items) > 0

    #check if every item in the list is a valid FeedItem.
    assert all(isinstance(item, FeedItem) for item in all_items)

    #check if final list contains items from both sources.
    unique_sources_in_results = {str(item.source_url) for item in all_items}

    assert unique_sources_in_results == set(sources_to_fetch)