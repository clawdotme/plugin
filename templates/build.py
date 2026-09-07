#!/usr/bin/env python3
"""Build inspectable, self-contained official Page templates (Python 3.11+)."""
import argparse
import base64
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class SourceCheck(HTMLParser):
    """Conservative authoring lint; hosted publication also runs its security scanner."""
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        assert tag not in {'script', 'iframe', 'object', 'embed', 'svg', 'form', 'input', 'base'}, tag
        assert not any(key.startswith('on') or key in {'srcset', 'srcdoc'} for key in values), tag
        if 'style' in values:
            assert re.fullmatch(r'[a-z-]+:[#a-z0-9.% ]+', values['style'] or ''), 'Unsupported inline CSS'
        if tag == 'meta':
            assert 'http-equiv' not in values, 'Active meta elements are unsupported'
        for key in ('src', 'href'):
            if key in values:
                value = values[key] or ''
                assert value.startswith('#') or re.fullmatch(r'\.\./_shared/[a-z0-9.-]+', value) or (tag == 'a' and key == 'href' and value.startswith(('https://', 'mailto:'))), value
                if value.startswith('../_shared/'):
                    assert (ROOT / '_shared' / value.rsplit('/', 1)[1]).is_file(), value
        if tag == 'img':
            assert (values.get('src') or '').endswith('.png'), 'Use bundled raster PNG artwork'


def build(slug):
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug), 'Invalid slug'
    shared = ROOT / '_shared'
    html = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
    SourceCheck().feed(html)
    css = (shared / 'portal.css').read_text(encoding='utf-8')
    # Keep the small official stylesheet straightforward and easy to audit.
    assert '\\' not in css and not re.search(r'@import|image-set|expression', css, re.I), 'Unsupported CSS'
    fonts = {path.name: path for path in shared.glob('*.ttf')}
    urls = re.findall(r'url\((.*?)\)', css, re.I)
    assert all(value.strip("\"' ") in fonts for value in urls), 'CSS may load bundled fonts only'
    for name, font in sorted(fonts.items()):
        data = base64.b64encode(font.read_bytes()).decode('ascii')
        css = css.replace(f"url('{name}')", f"url('data:font/ttf;base64,{data}')")
    licenses = '\n'.join(path.read_text(encoding='utf-8') for path in sorted(shared.glob('*-license.txt')))
    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
    html = html.replace('<link rel="stylesheet" href="../_shared/portal.css">', f'<style>{css}</style>\n<!-- {license_text}\n{licenses} -->')
    for photo in sorted(shared.glob('*.png')):
        html = html.replace(f'../_shared/{photo.name}', 'data:image/png;base64,' + base64.b64encode(photo.read_bytes()).decode('ascii'))
    assert '../_shared/' not in html, 'Unbundled resource'
    return html.encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write one self-contained HTML file per template')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    assert len({item['slug'] for item in catalog}) == len(catalog), 'Duplicate slug'
    for entry in catalog:
        metadata = json.loads((ROOT / entry['slug'] / 'template.json').read_text(encoding='utf-8'))
        assert all(metadata.get(key) == value for key, value in entry.items()), 'Catalog metadata drift'
        payload = build(entry['slug'])
        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            (args.output / (entry['slug'] + '.html')).write_bytes(payload)
        print(entry['slug'], hashlib.sha256(payload).hexdigest())


if __name__ == '__main__':
    main()
