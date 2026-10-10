#!/usr/bin/env python3
"""Build articles.json from root-level artigo-*.html files for GitHub Pages."""
import json
import re
import subprocess
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = False
        self.title_text = []
        self.meta = {}
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == 'title': self.title = True
        if tag.lower() == 'meta':
            key = (attrs.get('property') or attrs.get('name') or '').strip().lower()
            value = attrs.get('content', '').strip()
            if key and value: self.meta[key] = value
    def handle_endtag(self, tag):
        if tag.lower() == 'title': self.title = False
    def handle_data(self, data):
        if self.title: self.title_text.append(data)

def last_commit_time(path):
    try:
        value = subprocess.check_output(['git', 'log', '-1', '--format=%cI', '--', str(path.relative_to(ROOT))], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        if value:
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
            return dt
    except Exception:
        pass
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)

def pt_date(dt):
    months = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
    return f'{dt.day} de {months[dt.month-1]} de {dt.year}'

articles = []
for path in sorted(ROOT.glob('artigo-*.html')):
    parser = MetaParser()
    parser.feed(path.read_text(encoding='utf-8', errors='replace'))
    meta = parser.meta
    title = meta.get('og:title') or ' '.join(''.join(parser.title_text).split())
    title = re.sub(r'\s*\|\s*MegaHQ Online\s*$', '', title, flags=re.I).strip()
    description = meta.get('description') or meta.get('og:description') or ''
    image = meta.get('og:image') or ''
    category = meta.get('article:section') or meta.get('article:category') or 'QUADRINHOS'
    label = meta.get('article:label') or 'ARTIGO'
    dt = last_commit_time(path)
    article = {
        'title': unescape(title),
        'description': unescape(description),
        'url': path.name,
        'image': image,
        'imageAlt': unescape(meta.get('og:image:alt') or title),
        'category': unescape(category).upper(),
        'label': unescape(label).upper(),
        'date': dt.date().isoformat(),
        'dateLabel': pt_date(dt),
        'publishedAt': dt.isoformat(timespec='seconds'),
        'meta': meta.get('article:reading_time') or 'Leia o artigo'
    }
    articles.append(article)

# Sort newest first; stable filename order resolves exact timestamp ties.
articles.sort(key=lambda item: (item['publishedAt'], item['url']), reverse=True)
out = ROOT / 'articles.json'
out.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Catálogo gerado: {len(articles)} artigo(s) em {out}')
