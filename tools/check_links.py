"""Internal links, anchors and srcset files across all pages; writes external URL list. Exit 1 on any broken."""
import re, glob, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
pages = {os.path.basename(p)[:-5]: open(p).read() for p in glob.glob(R + '*.html')}
ids = {k: set(re.findall(r'id="([^"]+)"', v)) for k, v in pages.items()}
bad, ext = [], set()
for k, v in pages.items():
    for h in re.findall(r'(?:href|src)="([^"]+)"', v):
        if h.startswith('http'): ext.add(h.split('#')[0]); continue
        if h.startswith('mailto:'): continue
        path, _, frag = h.partition('#'); p = path.lstrip('/').split('?')[0]
        if path == '': tgt = k
        elif p == '': tgt = 'index'
        elif os.path.exists(R + p): tgt = None
        elif p in pages: tgt = p
        else: bad.append((k, h)); continue
        if frag and tgt and frag not in ids.get(tgt, set()): bad.append((k, h))
    for s in re.findall(r'srcset="([^"]+)"', v):
        for u in s.split(','):
            u = u.strip().split(' ')[0]
            if u.startswith('/') and not os.path.exists(R + u.lstrip('/')): bad.append((k, u))
print('pages', len(pages), 'broken', len(bad)); [print('  ', b) for b in bad]
open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ext.txt', 'w').write('\n'.join(sorted(ext)) + '\n')
sys.exit(1 if bad else 0)
