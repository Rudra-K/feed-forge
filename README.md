# FeedUnify

A high-performance, asynchronous Python library designed to unify and simplify data ingestion from multiple sources like RSS feeds and APIs into a single, clean format.

---

## About The Project

Developers often need to pull data from various inconsistent sources like RSS feeds, Atom feeds, JSON APIs, and more. Each source has its own data structure and quirks, leading to brittle, custom code for each one.

`feedunify` solves this by providing a single, elegant interface to fetch, parse, and standardize content from any source into a predictable, easy-to-use `FeedItem` object.

### Key Features

* **Unified Schema:** All data is parsed into a standard `FeedItem` object with consistent fields like `.title`, `.url`, and `.published_at`.
* **Asynchronous-First:** Built from the ground up with `asyncio` and `httpx` to handle hundreds of sources concurrently without blocking.
* **Extensible Architecture:** Designed around a `BaseConnector` class, allowing new connectors for different source types to be easily added.
* **Type-Safe & Robust:** Leverages `pydantic` for powerful data validation and parsing, preventing errors from malformed data.

---
## Installation

you can install the library with:

```bash
pip install feedunify
```
---
## Changelog

See the [CHANGELOG.md] file for a detailed history of changes to the project.

## Quickstart

Here's how easy it is to fetch articles from multiple RSS feeds at the same time.

```python
import asyncio
from feedunify import Forge

# A list of RSS feeds to fetch from.
SOURCES = [
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://hnrss.org/frontpage"
]

async def main():
    """Main function to run the fetching process."""
    
    # 1. Create an instance of the main Forge class.
    forge = Forge()
    
    # 2. Fetch all items concurrently.
    print(f"Fetching from {len(SOURCES)} sources")
    all_items = await forge.fetch_all(sources=SOURCES)
    print(f"Found {len(all_items)} total items.")
    
    # 3. Work with the clean, standardized data.
    print("\nLatest from The Verge:")
    for item in all_items:
        if "theverge.com" in str(item.source_url):
            print(f"- {item.title}")

if __name__ == "__main__":
    asyncio.run(main())

```
## Usage

First, fetch a list of items from your desired sources.

```python
import asyncio
from feedunify import Forge

SOURCES = ["https://www.theverge.com/rss/index.xml", "https://hnrss.org/frontpage"]

async def get_items():
    forge = Forge()
    all_items = await forge.fetch_all(sources=SOURCES)
    return all_items

items = asyncio.run(get_items())
```
Once you have the items list, you can easily work with the standardized data.


### Example 1: Find All Articles About "AI"

```python

ai_articles = [
    item for item in items 
    if "ai" in item.title.lower()
]

print("AI Articles Found:")
for article in ai_articles:
    print(f"- {article.title}")
```
### Example 2: Get the 5 Most Recent Articles

```python

# Filter out items that might not have a publication date.
dated_items = [item for item in items if item.published_at]

# Sort the items by date.
dated_items.sort(key=lambda item: item.published_at, reverse=True)

print("\nMost Recent Articles:")
for article in dated_items[:5]:
    print(f"- {article.title} (Published: {article.published_at.strftime('%Y-%m-%d')})")
```

---

## The `FeedItem` Object

The primary output of `feedunify` is a list of `FeedItem` objects. This object provides a standardized interface to the data, regardless of the original source.

### Key Attributes

* `item.id` (`str`): A unique identifier for the item.
* `item.title` (`str`): The headline or title.
* `item.url` (`HttpUrl`): A validated Pydantic URL object for the original content.
* `item.source_url` (`HttpUrl`): The URL of the feed this item came from.
* `item.summary` (`str | None`): A short summary or description.
* `item.published_at` (`datetime | None`): A timezone-aware datetime object of when the item was published.
* `item.authors` (`List[Author]`): A list of `Author` objects, each with `.name` and `.url` attributes.
* `item.tags` (`List[str]`): A list of tags or categories.
* `item.raw` (`dict | None`): The original, unprocessed data from the source, useful for debugging.

---

## Future Plans

`feedunify` is actively being developed. Future goals include:

* [ ] Adding a connector for common JSON APIs.
* [ ] Implementing intelligent HTTP caching (ETags, Last-Modified).
* [ ] Improving source detection logic.
* [ ] Exploring support for more complex sources like newsletters.

---

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch 
3.  Commit your Changes 
4.  Push to the Branch
5.  Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.