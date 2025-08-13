# Feed-Forge

A high-performance, asynchronous Python library designed to unify and simplify data ingestion from multiple sources like RSS feeds and APIs into a single, clean format.

---

## About The Project

Developers often need to pull data from various inconsistent sources—RSS feeds, Atom feeds, JSON APIs, and more. Each source has its own data structure and quirks, leading to brittle, custom code for each one.

`Feed-Forge` solves this by providing a single, elegant interface to fetch, parse, and standardize content from any source into a predictable, easy-to-use `FeedItem` object.

### Key Features

* **Unified Schema:** All data is parsed into a standard `FeedItem` object with consistent fields like `.title`, `.url`, and `.published_at`.
* **Asynchronous-First:** Built from the ground up with `asyncio` and `httpx` to handle hundreds of sources concurrently without blocking.
* **Extensible Architecture:** Designed around a `BaseConnector` class, allowing new connectors for different source types to be easily added.
* **Type-Safe & Robust:** Leverages `pydantic` for powerful data validation and parsing, preventing errors from malformed data.

---

## Installation

Currently, you can install `Feed-Forge` directly from the GitHub repository.

pip install git+[https://github.com/Rudra-K/feed-forge.git](https://github.com/Rudra-K/feed-forge.git)

---

## Quickstart

Here's how easy it is to fetch articles from multiple RSS feeds at the same time.

```python

import asyncio
from feed_forge import Forge

# A list of RSS feeds to fetch from.
SOURCES = [
    "[https://www.theverge.com/rss/index.xml](https://www.theverge.com/rss/index.xml)",
    "[https://www.wired.com/feed/rss](https://www.wired.com/feed/rss)",
    "[https://hnrss.org/frontpage](https://hnrss.org/frontpage)"
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

---

## The `FeedItem` Object

The primary output of `Feed-Forge` is a list of `FeedItem` objects. This object provides a standardized interface to the data, regardless of the original source.

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

`Feed-Forge` is actively being developed. Future goals include:

* [ ] Adding a connector for common JSON APIs.
* [ ] Implementing intelligent HTTP caching (ETags, Last-Modified) to be a good internet citizen.
* [ ] Improving source detection logic.
* [ ] Exploring support for more complex sources like newsletters.

---

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.