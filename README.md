<!-- pixeltable-example-app: 20260922-bookmark-shelf -->
# Bookmark Shelf API built with Pixeltable

![Bookmark Shelf API built with Pixeltable](.github/social-preview.png)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/pierrebrunelle/pixeltable-bookmark-shelf?quickstart=1)
[![Built with Pixeltable](https://img.shields.io/badge/built%20with-Pixeltable-5b4bff)](https://pixeltable.com)
[![PyPI - pixeltable](https://img.shields.io/pypi/v/pixeltable?label=pixeltable)](https://pypi.org/project/pixeltable/)
[![GitHub stars](https://img.shields.io/github/stars/pixeltable/pixeltable?style=social)](https://github.com/pixeltable/pixeltable)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Save a link and Pixeltable does the bookkeeping: the bookmark's **domain** is parsed from the URL, comma-separated tags are counted, and the title gets an upper-cased and a truncated variant, all as **incremental computed columns** that are filled on insert and refreshed on update. A `FastAPIRouter` exposes save, edit, delete, a `/domain` preview route and a per-domain shelf query.

[Pixeltable](https://pixeltable.com) is open-source, Python-native **multimodal AI data infrastructure**: tables, incremental computed columns, UDFs, indexes and serving in one library, running locally or on Pixeltable Cloud.

> ⭐ **Like this example?** Star [pixeltable/pixeltable](https://github.com/pixeltable/pixeltable) on GitHub. It helps other developers find it.

## What this example shows

- **FastAPI serving**: one `FastAPIRouter` turns tables and `@pxt.query` functions into typed REST routes (insert, update, delete, compute and query) with OpenAPI docs
- **Incremental computed columns** powered by plain Python UDFs (`@pxt.udf`)
- **Importable UDF module**: UDFs live in `udfs.py`; tables, queries and routes live together in `app.py` (Pixeltable resolves UDFs by module path)
- **`pixeltable.toml`** declares a local database and a **Pixeltable Cloud** database, so the same code deploys with `pxt db update`

## Why computed columns for bookmarks?

Derived fields like `domain` and `n_tags` usually end up recomputed in request handlers, or stored and forgotten when the logic changes. Here they're declared once on the table:

- **On insert:** they're computed and stored with the row.
- **On update:** only the columns whose inputs changed are recomputed (edit `tags` → `n_tags` updates, `domain` doesn't).
- **When the logic changes:** `pxt recompute` refreshes existing rows.

The `/domain` compute route reuses the exact same UDF, so the preview your UI shows always matches what gets stored.

## What's inside

| File | What it is |
|------|------------|
| `.devcontainer/devcontainer.json` | GitHub Codespaces / Dev Container config: Python 3.12, installs `requirements.txt`, forwards port 8000 |
| `.github/social-preview.png` | Social preview image (1280x640) |
| `CITATION.cff` | Citation metadata (authors, license, release date, keywords) |
| `app.py` | The app: tables declared as Python classes, `@pxt.query` functions, and the `FastAPIRouter` routes |
| `client_demo.py` | Save, preview, edit and browse bookmarks through the API |
| `pixeltable.toml` | Project config: the local database plus a Pixeltable Cloud database (sizing, deploy excludes) |
| `seed.py` | Seed a few bookmarks |
| `udfs.py` | Pixeltable UDFs (`@pxt.udf`) in their own importable module, imported by `app.py` |
| `requirements.txt` / `pyproject.toml` | Dependencies (`pixeltable[serve]>=0.7.14`) |

**Tables**

| Table | Stored columns | Computed columns |
|-------|---------|------------------|
| `bookmarks` | `url`, `title`, `tags`, `notes` | `id`, `domain`, `title_upper`, `n_tags`, `blurb` |

**API routes** (service `bookmarks_api`)

| Method | Path | Kind | Backed by | Notes |
|--------|------|------|-----------|-------|
| `POST` | `/bookmarks` | insert | `Bookmarks` |  |
| `POST` | `/bookmarks/update` | update | `Bookmarks` |  |
| `POST` | `/bookmarks/delete` | delete | `Bookmarks` |  |
| `POST` | `/domain` | compute | `Bookmarks` |  |
| `GET` | `/shelf` | query | `shelf` |  |

## Run in your browser (GitHub Codespaces)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/pierrebrunelle/pixeltable-bookmark-shelf?quickstart=1)

1. Click **Open in GitHub Codespaces** above (or [this link](https://codespaces.new/pierrebrunelle/pixeltable-bookmark-shelf?quickstart=1)). The dev container installs Python 3.12 and `pixeltable[serve]>=0.7.14` from `requirements.txt`.
2. In the codespace terminal, create the tables, seed them and start the API:

   ```bash
   pxt schema update app.py shelf
   python seed.py shelf
   pxt service run app.py shelf --port 8000   # open http://localhost:8000/docs
   python client_demo.py                     # in another terminal
   ```

3. Codespaces forwards port 8000: open it from the **Ports** tab (or the pop-up) and add `/docs` to the URL for the interactive OpenAPI docs.

## Quickstart

Requires Python 3.11+ and `pixeltable[serve]>=0.7.14`.

```bash
git clone https://github.com/pierrebrunelle/pixeltable-bookmark-shelf.git
cd pixeltable-bookmark-shelf
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Create the tables in a local catalog directory named `shelf`
pxt schema update app.py shelf

python seed.py shelf
pxt service run app.py shelf --port 8000   # open http://localhost:8000/docs
python client_demo.py                     # in another terminal
```

Try it:

```bash
curl -s -X POST localhost:8000/domain -H 'Content-Type: application/json' -d '{"url": "https://www.example.org/a"}'
curl -s 'localhost:8000/shelf?domain=python.org'
```

## Deploy to Pixeltable Cloud

The same `app.py` runs on [Pixeltable Cloud](https://pixeltable.com). Sign in (or get a free trial database with `pxt new`), point the second database entry in `pixeltable.toml` at your own database, then deploy:

```bash
pxt login                       # or: export PIXELTABLE_API_KEY=<your-api-key>
# edit pixeltable.toml: name = 'pxt://<your-org>:<your-db>'
pxt db update pxt://<your-org>:<your-db>                 # build the image and upload the project
pxt schema update app.py pxt://<your-org>:<your-db>/shelf   # create the tables in the hosted database
pxt service update app.py pxt://<your-org>:<your-db>/shelf  # start the API there
pxt service list pxt://<your-org>:<your-db>              # list hosted services
```

Hosted routes require an API key: send it in the `X-api-key` header (for example `-H "X-api-key: $PIXELTABLE_API_KEY"`). Keep keys in environment variables or `pxt secret set`, never in code.

## Code walkthrough

**1. Business logic is plain Python, in `udfs.py`.** A `@pxt.udf` function can be used as a column expression. Pixeltable records UDFs by module path (`udfs.extract_domain`), so they live in their own importable module rather than inline in the app: the daemon, serving workers and Pixeltable Cloud import it again by that path.

```python
# udfs.py
@pxt.udf
def extract_domain(url: str) -> str:
    """'https://www.example.com/a?b' -> 'example.com'."""
    host = (urlparse(url if '://' in url else 'https://' + url).hostname or '').lower()
    return host[4:] if host.startswith('www.') else host
```

**2. Tables are Python classes (`app.py`).** Annotated attributes are stored columns; attributes assigned an expression are **computed columns** (`id`, `domain`, `title_upper`, `n_tags`, `blurb`), evaluated incrementally on every insert or update and recomputed when their inputs change.

```python
# app.py
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
```

**3. Queries are functions (`app.py`).** `@pxt.query` wraps a Pixeltable query so it can be called from Python or exposed as a route:

```python
# app.py
@pxt.query
def shelf(domain: str):
    """Everything saved from one domain."""
    return Bookmarks.where(Bookmarks.domain == domain).select(
        Bookmarks.id, Bookmarks.blurb, Bookmarks.url, Bookmarks.n_tags
    ).order_by(Bookmarks.title)
```

**4. One router, a full REST API.** `FastAPIRouter` generates request/response models from the column types, validates input, and publishes OpenAPI docs at `/docs`:

```python
# app.py
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
```

## Learn more

- 🌐 Website: https://pixeltable.com
- 📚 Docs: https://docs.pixeltable.com
- 💻 Source: https://github.com/pixeltable/pixeltable (⭐ star it if Pixeltable is useful to you)
- 📦 PyPI: https://pypi.org/project/pixeltable/
- 🧩 More example apps: https://pierrebrunelle.github.io/awesome-pixeltable-apps/

**[More Pixeltable example apps →](https://pierrebrunelle.github.io/awesome-pixeltable-apps/)**

---

<sub>Built as part of a daily series of Pixeltable example apps · Pixeltable 0.7.14 · Python, FastAPI, incremental computed columns · Licensed under Apache-2.0.</sub>
