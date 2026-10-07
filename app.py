"""Bookmark Shelf API built with Pixeltable.

    pxt schema update app.py shelf
    pxt service run app.py shelf
"""
from pixeltable.serving import FastAPIRouter

from models import Bookmarks, TableModel  # noqa: F401  (TableModel lets `pxt schema` find the models)
from queries import shelf

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
