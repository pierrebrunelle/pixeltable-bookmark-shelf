"""Seed a few bookmarks.

Usage:
    python seed.py            # seeds the local `shelf` catalog directory
    python seed.py my_dir     # or another directory you passed to `pxt schema update`
"""
import sys
from pathlib import Path

import pixeltable as pxt

target = sys.argv[1] if len(sys.argv) > 1 else 'shelf'
HERE = Path(__file__).resolve().parent

SEED = {
    'bookmarks': [
        {'url': 'https://docs.pixeltable.com', 'title': 'Pixeltable docs', 'tags': 'python,ai,data', 'notes': None},
        {'url': 'https://github.com/pixeltable/pixeltable', 'title': 'Pixeltable on GitHub', 'tags': 'oss', 'notes': 'star it'},
        {'url': 'https://www.python.org/dev/peps/pep-0008/', 'title': 'PEP 8 style guide', 'tags': 'python,style', 'notes': None},
    ],
}

for table_name, rows in SEED.items():
    t = pxt.get_table(f'{target}/{table_name}')
    if t.count() > 0:
        print(f'{target}/{table_name} already has {t.count()} rows; skipping')
        continue
    for row in rows:
        for k, v in row.items():
            if isinstance(v, str) and v.startswith('data/'):
                row[k] = str(HERE / v)   # local sample media file
    t.insert(rows)
    print(f'inserted {len(rows)} rows into {target}/{table_name}')
