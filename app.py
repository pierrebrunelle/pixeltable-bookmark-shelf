"""Bookmark Shelf API built with Pixeltable.

    pxt schema update app.py shelf
    pxt service run app.py shelf
"""
import pixeltable as pxt
import pixeltable.functions as pxtf
from pixeltable.serving import FastAPIRouter

from udfs import extract_domain, tag_count, title_blurb

# ---- tables ----
TableModel = pxt.model_base()


class Bookmarks(TableModel, name='bookmarks'):
    id = pxt.Column(value=pxtf.uuid.uuid7(), primary_key=True)
    url: pxt.String
    title: pxt.String
    tags: pxt.String | None
    notes: pxt.String | None

    domain = extract_domain(url)
    title_upper = pxtf.string.upper(title)
    n_tags = tag_count(tags)
    blurb = title_blurb(title)


# ---- queries ----
@pxt.query
def shelf(domain: str):
    """Everything saved from one domain."""
    return Bookmarks.where(Bookmarks.domain == domain).select(
        Bookmarks.id, Bookmarks.blurb, Bookmarks.url, Bookmarks.n_tags
    ).order_by(Bookmarks.title)


# ---- routes ----
bookmarks_api = FastAPIRouter(name='bookmarks_api')
bookmarks_api.add_insert_route(
    Bookmarks, path='/bookmarks',
    inputs=[Bookmarks.url, Bookmarks.title, Bookmarks.tags, Bookmarks.notes],
    outputs=[Bookmarks.id, Bookmarks.domain, Bookmarks.title_upper, Bookmarks.n_tags, Bookmarks.blurb],
)
bookmarks_api.add_update_route(
    Bookmarks, path='/bookmarks/update',
    inputs=[Bookmarks.title, Bookmarks.tags],
    outputs=[Bookmarks.id, Bookmarks.n_tags, Bookmarks.blurb],
)
bookmarks_api.add_delete_route(Bookmarks, path='/bookmarks/delete')
bookmarks_api.add_compute_route(Bookmarks, path='/domain', inputs=[Bookmarks.url], outputs=[Bookmarks.domain])
bookmarks_api.add_query_route(path='/shelf', query=shelf, method='get')
