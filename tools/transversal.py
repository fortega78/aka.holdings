"""Cross-site upgrades for hand-written pages (not in src/): js class, canonical, unified header with mobile
menu, site.js, AVIF <picture> for /img/*.jpg. Idempotent."""
import re, os, sys, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV = [('/', 'AKA Holdings'), ('/technologies', '01 / Technologies'), ('/productions', '02 / Art Productions'), ('/interior', '03 / Interior Design'), ('/fabian', 'Fabian')]
def unit_of(name):
    for u in ('interior', 'productions', 'technologies', 'fabian'):
        if name.startswith(u): return '/' + u
    return '/'
def nav(cur, home):
    items = NAV[1:] if home else NAV
    links = '\n'.join(f'      <a href="{h}"' + (' aria-current="page"' if h == cur else '') + f'>{t}</a>' for h, t in items)
    return ('<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav"><i></i>Menu</button>\n'
            f'    <nav class="idx" id="site-nav" aria-label="Main">\n{links}\n    </nav>')
def pic(m):
    tag = m.group(0)
    src = re.search(r'src="(/img/[^"]+\.jpg)"', tag)
    if not src: return tag
    av = src.group(1)[:-4] + '.avif'
    if not os.path.exists(R + av): return tag
    if 'loading=' not in tag and 'fetchpriority' not in tag: tag = tag.replace('<img ', '<img loading="lazy" decoding="async" ', 1)
    return f'<picture><source type="image/avif" srcset="{av}">{tag}</picture>'
def run(f):
    name = os.path.basename(f)[:-5]; t = open(f).read(); o = t
    if "className+=' js'" not in t:
        t = t.replace('<meta name="viewport" content="width=device-width,initial-scale=1">', '<meta name="viewport" content="width=device-width,initial-scale=1">\n<script>document.documentElement.className+=\' js\'</script>', 1)
    slug = '' if name == 'index' else name
    if 'rel="canonical"' not in t and name != '404':
        t = t.replace('<link rel="icon"', f'<link rel="canonical" href="https://aka.holdings/{slug}">\n<link rel="icon"', 1)
    t = t.replace('<header class="top rise">', '<header class="top">')
    t = re.sub(r'<button class="menu-btn"[^>]*>.*?</button>\s*', '', t)
    t = re.sub(r'<nav class="idx"[^>]*>.*?</nav>', lambda m: nav(unit_of(name) if name != 'index' else None, name == 'index'), t, count=1, flags=re.S)
    # picture-ise images not already inside <picture>
    parts = re.split(r'(<picture>.*?</picture>)', t, flags=re.S)
    t = ''.join(p if p.startswith('<picture>') else re.sub(r'<img [^>]*src="/img/[^"]+\.jpg"[^>]*>', pic, p) for p in parts)
    if '/assets/site.js' not in t: t = t.replace('</body>', '<script src="/assets/site.js" defer></script>\n</body>')
    if t != o: open(f, 'w').write(t); print('upgraded', name)
srcs = {os.path.basename(x) for x in glob.glob(R + '/src/*.html')}
for f in sorted(glob.glob(R + '/*.html')):
    if os.path.basename(f) not in srcs: run(f)
