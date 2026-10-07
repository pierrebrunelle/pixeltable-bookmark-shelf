"""The bookmarks table."""
import pixeltable as pxt
import pixeltable.functions as pxtf

from udfs import extract_domain, tag_count, title_blurb

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
