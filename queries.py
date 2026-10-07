"""Queries over the bookmarks table."""
import pixeltable as pxt

from models import Bookmarks


@pxt.query
def shelf(domain: str):
    """Everything saved from one domain."""
    return Bookmarks.where(Bookmarks.domain == domain).select(
        Bookmarks.id, Bookmarks.blurb, Bookmarks.url, Bookmarks.n_tags
    ).order_by(Bookmarks.title)
