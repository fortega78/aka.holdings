"""Generate interior project subpages (src/*.html, then tools/render.py expands images)."""
import json, sys, html
CAL = "https://calendar.app.google/4LDyrF8XGdGuoazj6"
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>{title} — AKA Interior Design</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://aka.holdings/{slug}">
<meta property="og:title" content="{title} — AKA Interior Design">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://aka.holdings/og/interior.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="https://aka.holdings/{slug}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/assets/AKA_Mark_Small_Deep.svg">
<link rel="preload" href="/fonts/archivo-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/aka.css">
<style>
body.interior{{background-image:none}}
figure{{margin:0}}
.serif{{font-family:'Bodoni Moda',serif}}
.cap{{font-size:12.5px;line-height:1.5;color:var(--graphite);margin-top:10px;max-width:60ch}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:48px;background:var(--deep);color:var(--bone);font-family:Questrial,sans-serif;text-transform:uppercase;letter-spacing:.28em;font-size:12px;padding:16px 26px 15px;border:1px solid var(--deep)}}
.btn:hover{{background:transparent;color:var(--deep)}}
.alt{{font-family:Questrial,sans-serif;text-transform:uppercase;letter-spacing:.28em;font-size:11px;color:var(--deep);border-bottom:1px solid var(--deep);padding:12px 0 4px}}
.sp-head{{display:grid;grid-template-columns:5fr 7fr;gap:56px;align-items:end;padding:clamp(40px,7vh,80px) 0 36px}}
.sp-head .no{{font-family:Questrial,sans-serif;letter-spacing:.3em;font-size:11px;color:var(--deep);display:block;margin-bottom:14px}}
.sp-head h1{{font-size:clamp(36px,4.6vw,64px);line-height:1.02;color:var(--deep);letter-spacing:-.01em}}
.sp-head .mline{{display:block;font-family:Questrial,sans-serif;text-transform:uppercase;letter-spacing:.22em;font-size:11px;color:var(--deep);margin-top:16px}}
.sp-head p{{color:var(--graphite);max-width:58ch}}
.sp-head p+p{{margin-top:12px}}
.sp-head .act{{display:flex;flex-wrap:wrap;gap:14px 26px;margin-top:22px;align-items:center}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}}
.grid .w6{{grid-column:span 6}}.grid .w4{{grid-column:span 4}}.grid .w3{{grid-column:span 3}}.grid .w2{{grid-column:span 2}}
.grid .t img{{aspect-ratio:4/5;object-fit:cover}}
.lab{{display:inline-block;font-family:Questrial,sans-serif;text-transform:uppercase;letter-spacing:.22em;font-size:10.5px;color:var(--bone);background:var(--deep);padding:5px 8px 4px;margin:10px 8px 0 0;vertical-align:middle}}
.paper{{background:#fff;border:1px solid var(--line)}}
.block{{display:grid;grid-template-columns:5fr 7fr;gap:56px;padding:64px 0 8px}}
.block h2{{font-size:clamp(28px,2.8vw,38px);line-height:1.1;color:var(--deep)}}
.rows{{border-top:1px solid var(--deep)}}
.rowi{{display:grid;grid-template-columns:5fr 7fr;gap:28px;padding:18px 0;border-bottom:1px solid var(--line)}}
.rowi b{{display:block;font-weight:500;font-size:16.5px;color:var(--ink)}}
.rowi span{{display:block;font-size:13.5px;color:var(--graphite);margin-top:2px}}
.rowi p{{color:var(--graphite);font-size:15px}}
.rowi p em{{font-family:'Bodoni Moda',serif;font-style:italic;font-size:17px;color:var(--deep)}}
.credits{{font-size:12.5px;color:var(--graphite);margin-top:28px;padding-top:14px;border-top:1px solid var(--line)}}
.next{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 28px;margin-top:20px}}
.close{{border-top:1px solid var(--deep);border-bottom:1px solid var(--deep);padding:48px 0;margin-top:64px;display:grid;grid-template-columns:7fr 5fr;gap:32px;align-items:center}}
.close h2{{font-size:clamp(32px,3.4vw,46px);line-height:1.08;color:var(--deep)}}
.close p{{margin-top:12px;color:var(--graphite);max-width:52ch}}
.close .act{{display:flex;justify-content:flex-end}}
@media (max-width:900px){{.sp-head,.block,.close,.rowi{{grid-template-columns:1fr;gap:14px}}.close .act{{justify-content:flex-start}}.grid .w4,.grid .w3{{grid-column:span 6}}.grid .w2{{grid-column:span 3}}}}
@media (max-width:600px){{.grid{{gap:8px}}.btn{{width:100%}}}}
</style>
</head>
<body class="interior has-mbar">
<a class="skip" href="#main">Skip to content</a>
<div class="wrap">
  <header class="top">
    <a href="/interior" aria-label="AKA Interior Design"><img src="/assets/AKA_Interior_Design_Small_OnBone.svg" alt="AKA Interior Design" width="59" height="36"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav"><i></i>Menu</button>
    <nav class="idx" id="site-nav" aria-label="Main">
      <a href="/">AKA Holdings</a>
      <a href="/technologies">01 / Technologies</a>
      <a href="/productions">02 / Art Productions</a>
      <a href="/interior" aria-current="page">03 / Interior Design</a>
      <a href="/fabian">Fabian</a>
    </nav>
  </header>
</div>
<main id="main" class="wrap">
"""
FOOT = """  <section class="close" aria-labelledby="start" data-hide-bar>
    <div><h2 class="serif" id="start">Let’s start with your home.</h2><p>Pick a time, or tell us about the home first. Or write to <a href="mailto:fabian@aka.holdings?subject=Interior%20consultation" style="border-bottom:1px solid var(--line)">fabian@aka.holdings</a>.</p></div>
    <div class="act" style="gap:18px;flex-wrap:wrap"><a class="btn" href="{cal}" target="_blank" rel="noopener" data-place="sub-close">Book a consultation</a><a class="alt" href="/interior#start">Tell us about your home</a></div>
  </section>
</main>
<div class="wrap">
  <footer>
    <div class="grid" style="display:grid">
      <img src="/assets/AKA_Interior_Design_Small_OnBone.svg" alt="AKA Interior Design" width="66" height="40">
      <div class="mid"><span class="k">Part of AKA Holdings</span><span class="k sub"><a href="/technologies">Technologies</a> · <a href="/productions">Art Productions</a> · <a href="/interior">Interior Design</a> · <a href="https://teherrugs.com" target="_blank" rel="noopener">TeHer Art Rugs</a></span></div>
      <div><a class="k" href="mailto:fabian@aka.holdings">fabian@aka.holdings</a><span class="k sub">Miami</span></div>
    </div>
  </footer>
</div>
<nav class="mbar" aria-label="Quick actions"><a href="{cal}" target="_blank" rel="noopener" data-place="mbar">Book a consultation</a><a class="ghost" href="/interior#start">Form</a></nav>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
def build(spec):
    o = HEAD.format(**spec)
    o += f"""  <section class="sp-head" data-hide-bar>
    <div><span class="no">{spec['no']}</span><h1 class="serif">{spec['h1']}</h1><span class="mline">{spec['mline']}</span></div>
    <div>{''.join(f'<p>{p}</p>' for p in spec['paras'])}
      <div class="act"><a class="btn" href="{CAL}" target="_blank" rel="noopener" data-place="sub-top">Book a consultation</a><a class="alt" href="/interior#{spec['anchor']}">All projects</a></div>
    </div>
  </section>
"""
    for part in spec['body']:
        o += part + '\n'
    o += f"""  <p class="credits">{spec['credits']}</p>
  <div class="next"><a class="alt" href="/interior#{spec['anchor']}">← All projects</a>{spec.get('next','')}</div>
"""
    o += FOOT.format(cal=CAL)
    return o
if __name__ == '__main__':
    for spec in json.load(open(sys.argv[1])):
        open(f"src/{spec['slug']}.html", 'w').write(build(spec)); print('src', spec['slug'])
