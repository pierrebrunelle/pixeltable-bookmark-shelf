"""Pixeltable UDFs for the bookmark shelf (recorded by module path, e.g. `udfs.extract_domain`)."""
from urllib.parse import urlparse

import pixeltable as pxt


@pxt.udf
def extract_domain(url: str) -> str:
    """'https://www.example.com/a?b' -> 'example.com'."""
    host = (urlparse(url if '://' in url else 'https://' + url).hostname or '').lower()
    return host[4:] if host.startswith('www.') else host


@pxt.udf
def tag_count(tags: str | None) -> int:
    """Number of non-empty comma-separated tags."""
    return len([t for t in (tags or '').split(',') if t.strip()])


@pxt.udf
def title_blurb(title: str) -> str:
    """Title trimmed to 32 characters for compact lists."""
    return title if len(title) <= 32 else title[:31].rstrip() + '…'
