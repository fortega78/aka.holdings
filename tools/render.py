"""Expand image placeholders in src/*.html into <picture> markup -> site root.
{{pic:NAME|ALT|SIZES|eager}}  -> image from img/v2 (manifest.json: avif + jpg srcset, width/height)
{{img:/img/path.jpg|ALT|SIZES}} -> legacy image: avif twin at native size if present, jpg fallback
{{fact:a.b}} -> value from data/facts.json"""
import json, re, os, sys, glob
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(f'{R}/img/v2/manifest.json'))
F = json.load(open(f'{R}/data/facts.json'))
def pic(m):
    name, alt, sizes, *rest = m.group(1).split('|') + ['']
    eager = 'eager' in rest
    e = M[name]; h = round(e['h'] * 1)
    ratio = e['h'] / e['w']
    av = ', '.join(f"/img/v2/{name}-{w}.avif {w}w" for w in e['avif'])
    jp = ', '.join(f"/img/v2/{name}-{w}.jpg {w}w" for w in e['jpg'])
    jw = e['jpg'][-1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{av}" sizes="{sizes or "100vw"}">'
            f'<img src="/img/v2/{name}-{jw}.jpg" srcset="{jp}" sizes="{sizes or "100vw"}" width="{jw}" height="{round(jw*ratio)}" alt="{alt}" {load}></picture>')
def img(m):
    path, alt, sizes, *rest = m.group(1).split('|') + ['', '']
    full = R + path; w, h = Image.open(full).size
    av = path.rsplit('.', 1)[0] + '.avif'
    s = f' sizes="{sizes}"' if sizes else ''
    src = f'<source type="image/avif" srcset="{av} {w}w"{s}>' if os.path.exists(R + av) else ''
    return f'<picture>{src}<img src="{path}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async"></picture>'

def fig(m):
    """{{fig:NAME|alt|caption}} / {{fig:/img/legacy.jpg|alt|caption}} -> plate that keeps the photo's full frame; in a .plates row, width is proportional to aspect ratio so heights match and nothing is cropped."""
    name, alt, cap, *rest = m.group(1).split('|') + ['', '']
    eager = 'eager' in rest
    if name.startswith('/'):
        w, h = Image.open(R + name).size
        inner = img(re.match(r'(.*)', f'{name}|{alt}|(max-width:700px) 100vw, 60vw'))
        if eager: inner = inner.replace('loading="lazy" decoding="async"', 'fetchpriority="high"')
        native = ''
    else:
        e = M[name]; w, h = e['w'], e['h']
        inner = pic(re.match(r'(.*)', f'{name}|{alt}|(max-width:700px) 100vw, 60vw' + ('|eager' if eager else '')))
        native = ''
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="pl" style="--r:{w/h:.4f}{native}">{inner}{c}</figure>'

def fact(m):
    v = F
    for k in m.group(1).split('.'): v = v[k]
    return str(v['value'] if isinstance(v, dict) else v)
for f in ([a for a in sys.argv[1:] if not a.startswith('--')] or ([] if '--svg' in sys.argv else glob.glob(f'{R}/src/*.html'))):
    t = open(f).read()
    t = re.sub(r'\{\{fig:([^}]+)\}\}', fig, t); t = re.sub(r'\{\{pic:([^}]+)\}\}', pic, t); t = re.sub(r'\{\{img:([^}]+)\}\}', img, t); t = re.sub(r'\{\{fact:([^}]+)\}\}', fact, t)
    out = f'{R}/{os.path.basename(f)}'; open(out, 'w').write(t); print('rendered', out)

# ---- post-pass on every page: intrinsic size for SVG logos without width/height (prevents layout shift) ----
def svg_dims(html):
    def fix(m):
        tag = m.group(0)
        if ' width=' in tag: return tag
        p = R + m.group(1)
        if not os.path.exists(p): return tag
        vb = re.search(r'viewBox="([\d.\s-]+)"', open(p).read())
        if not vb: return tag
        _, _, w, h = [float(x) for x in vb.group(1).split()]
        return tag.replace('<img ', f'<img width="{round(w)}" height="{round(h)}" ', 1)
    return re.sub(r'<img [^>]*src="(/assets/[^"]+\.svg)"[^>]*>', fix, html)
if __name__ == '__main__' and '--svg' in sys.argv:
    for f in glob.glob(f'{R}/*.html'):
        t = open(f).read(); t2 = svg_dims(t)
        if t2 != t: open(f, 'w').write(t2); print('svg dims', os.path.basename(f))
