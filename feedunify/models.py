from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field

class Author(BaseModel):
    """A simple model to represent a content author."""
    name: str
    url: Optional[HttpUrl] = None

class FeedItem(BaseModel):
    """
    The standardized data model for a single piece of content from any source.

    This class is the core output of the library. Every item fetched, regardless
    of its origin (RSS, API, etc.), is parsed and validated into this structure.
    """

    #required fields
    id: str = Field(..., description="A unique identifier for the item.")
    source_url: HttpUrl = Field(..., description="The URL of the feed or API endpoint this item came from.")
    url: HttpUrl = Field(..., description="The direct URL to the full content.")
    title: str

    #optional recommended fields
    summary: Optional[str] = None
    content_html: Optional[str] = None

    #datetime fields
    published_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    #other data
    authors: List[Author] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    #media
    image_url: Optional[HttpUrl] = None

    #debugging
    #this won't be analyzled or used by the library; instead preserved for end-users.
    raw: Optional[Dict[str, Any]] = Field(None, description="The original, unprocessed data. Useful for debugging or accessing non-standard fields.")