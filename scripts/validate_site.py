"""Offline static-site integrity checks. Run with Python 3, no dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '/short-form-content-engine-compliance/'
REQUIRED = {PREFIX, PREFIX+'tiktok/', PREFIX+'tiktok/privacy/', PREFIX+'tiktok/terms/', PREFIX+'privacy.html', PREFIX+'terms.html'}
VERIFICATION = 'tiktokOuUwdD00b28U2i2Xn0hwTrjQJu43ibCP.txt'
EXPECTED = b'tiktok-developers-site-verification=OuUwdD00b28U2i2Xn0hwTrjQJu43ibCP'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.h1=0; self.main=0; self.footer=False; self.footer_links=set(); self.description=False; self.title=False; self.language=False; self.viewport=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='script': raise AssertionError('JavaScript is not needed')
        if tag in {'iframe','form'}: raise AssertionError('No embeds or forms')
        if tag=='html': self.language=a.get('lang')=='en'
        if tag=='title': self.title=True
        if tag=='h1': self.h1+=1
        if tag=='main': self.main+=1
        if tag=='footer': self.footer=True
        if 'id' in a:
            assert a['id'] not in self.ids, 'Duplicate ID'; self.ids.add(a['id'])
        if tag=='meta':
            if a.get('name')=='description': self.description=bool(a.get('content'))
            if a.get('name')=='viewport': self.viewport='width=device-width' in a.get('content','')
        if tag=='img': assert a.get('alt'), 'Image needs meaningful alt'
        for k in ('href','src'):
            if k in a: self.links.append(a[k])
        if self.footer and tag=='a': self.footer_links.add(a.get('href'))
    def handle_endtag(self, tag):
        if tag=='footer': self.footer=False

count=0
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts: continue
    parser=Page(); parser.feed(path.read_text())
    assert parser.language and parser.title and parser.description and parser.viewport, path
    assert parser.h1==1 and parser.main==1, path
    assert REQUIRED <= parser.footer_links, f'Missing visible footer links: {path}'
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme:
            assert u.scheme in {'https','mailto'}, f'Unsafe link: {path}'
            continue
        if not u.path:
            if u.fragment: assert u.fragment in parser.ids, path
            continue
        if u.path.startswith('/'):
            assert u.path.startswith(PREFIX), path
            dest=ROOT/unquote(u.path[len(PREFIX):])
        else: dest=path.parent/unquote(u.path)
        if dest.is_dir(): dest=dest/'index.html'
        assert dest.is_file(), f'Broken internal link: {path}: {link}'
    count+=1
assert (ROOT/VERIFICATION).read_bytes()==EXPECTED, 'Verification bytes changed'
assert (ROOT/'.nojekyll').exists()
# Credential signatures only; public verification signature is intentionally public.
patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'ya29\.[A-Za-z0-9_-]{12,}',r'1//[A-Za-z0-9_-]{20,}',r'gh[pousr]_[A-Za-z0-9]{20,}',r'(?i)["\'](?:access_token|refresh_token|client_secret|authorization_code)["\']\s*:\s*["\'][^"\']+["\']']
scanned=0
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts or path==Path(__file__).resolve(): continue
    try: value=path.read_text()
    except UnicodeError: continue
    for pattern in patterns: assert not re.search(pattern,value), f'Potential secret in {path.relative_to(ROOT)}; value redacted'
    scanned+=1
print(f'PASS: {count} HTML pages, internal links, visible policy navigation, semantic basics, verification bytes; credential-pattern scan ({scanned} text files).')
