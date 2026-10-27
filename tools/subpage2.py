"""Interior subpages, monograph system (v7, 27-oct): whole photographs in rows sized by their proportions."""
import json, sys, re
CAL = "https://calendar.app.google/4LDyrF8XGdGuoazj6"
HEAD = open('tools/_sub_head.html').read()
def rows_html(rows):
    out = []
    first = [True]
    def E():
        if first[0]: first[0] = False; return '|eager'
        return ''
    for r in rows:
        if r and r[0] == 'LEAD':
            n, alt, cap = r[1]
            out.append(f'    <div class="lead-row"><span aria-hidden="true"></span><div class="plates">{{{{fig:{n}|{alt}|{cap}{E()}}}}}</div></div>')
        else:
            out.append('    <div class="plates">' + ''.join(f'{{{{fig:{n}|{alt}|{cap}{E()}}}}}' for n, alt, cap in r) + '</div>')
    return '\n'.join(out)
def build(s):
    ld = '<script type="application/ld+json">' + json.dumps({'@context':'https://schema.org','@type':'CreativeWork','name':s['title'],'description':s['desc'],'url':'https://aka.holdings/'+s['slug'],'creator':{'@type':'Organization','name':'AKA Interior Design','url':'https://aka.holdings/interior','parentOrganization':{'@type':'Organization','name':'AKA Holdings','url':'https://aka.holdings/'}},'author':{'@type':'Person','name':'Fabian J. Ortega A.','url':'https://aka.holdings/fabian'},'inLanguage':'en'}, ensure_ascii=False) + '</script>\n'
    o = HEAD.replace('{title}', s['title']).replace('{desc}', s['desc']).replace('{slug}', s['slug']).replace('{preload}', s.get('preload', ''))
    o += f'''<main id="main" class="wide">
  <section class="sp-head" data-hide-bar>
    <div><h1>{s['h1']}</h1><p class="facts">{s['facts']}</p></div>
    <div>{''.join(f'<p>{p}</p>' for p in s['paras'])}<p class="more"><a class="tl" href="/interior#{s['anchor']}">All projects</a></p></div>
  </section>
{rows_html(s['rows'])}
{s.get('extra','')}
  <p class="credits">{s['credits']}</p>
  <nav class="next" aria-label="More projects">{s.get('next','')}</nav>
  <section class="close-i" aria-labelledby="start" data-hide-bar>
    <h2 id="start">Tell us about your home</h2>
    <div class="act"><a class="btn" href="{CAL}" target="_blank" rel="noopener" data-place="sub-close">Book a consultation</a><a class="tl" href="/interior#start">Or use the form</a></div>
  </section>
</main>
<div class="wide">
  <footer>
    <div class="grid">
      <img src="/assets/AKA_Interior_Design_Small_OnBone.svg" alt="AKA Interior Design" width="66" height="40">
      <div class="mid"><span class="k">Part of AKA Holdings</span><span class="k sub"><a href="/technologies">Technologies</a> · <a href="/productions">Art Productions</a> · <a href="/interior">Interior Design</a> · <a href="https://teherrugs.com" target="_blank" rel="noopener">TeHer Art Rugs</a></span></div>
      <div><a class="k" href="mailto:fabian@aka.holdings">fabian@aka.holdings</a><span class="k sub">Miami</span></div>
    </div>
  </footer>
</div>
<nav class="mbar" aria-label="Quick actions"><a href="{CAL}" target="_blank" rel="noopener" data-place="mbar">Book a consultation</a><a class="ghost" href="/interior#start">Form</a></nav>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''
    o = o.replace('<style>', ld + '<style>', 1)
    return o
if __name__ == '__main__':
    for s in json.load(open(sys.argv[1])):
        open(f"src/{s['slug']}.html", 'w').write(build(s)); print('src', s['slug'])
