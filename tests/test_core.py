import pytest
from feedunify.core import Forge
from feedunify.models import FeedItem

VALID_SOURCE_1 = "https://www.theverge.com/rss/index.xml"
VALID_SOURCE_2 = "https://www.wired.com/feed/rss"

INVALID_SOURCE = "https://www.google.com"


@pytest.mark.asyncio
async def test_forge_fetches_and_skips_sources(capsys):
    
    forge = Forge()
    sources_to_fetch = [VALID_SOURCE_1, INVALID_SOURCE, VALID_SOURCE_2]

    all_items = await forge.fetch_all(sources=sources_to_fetch)

    #Check that we got a valid list of FeedItem objects.
    assert isinstance(all_items, list)
    assert len(all_items) > 0
    assert all(isinstance(item, FeedItem) for item in all_items)

    #Verify that the final list ONLY contains items from the VALID sources.
    unique_sources_in_results = {str(item.source_url) for item in all_items}
    assert unique_sources_in_results == {VALID_SOURCE_1, VALID_SOURCE_2}

    #Check that warning was printed to the screen.
    captured = capsys.readouterr()
    assert "Warning: No suitable connector found" in captured.out
    assert INVALID_SOURCE in captured.out


