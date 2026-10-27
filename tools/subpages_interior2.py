import json, re, sys
from PIL import Image
def legacy(f):
    t = open(f).read()
    return re.findall(r'\{\{img:(/img/[^|]+)\|([^|]*)\|[^}]*\}\}<figcaption class="cap">(.*?)</figcaption>', t)
def autorows(items):
    rows, cur, land = [], [], 0
    for p, alt, cap in items:
        w, h = Image.open('.' + p).size; L = w / h > 1.1
        if cur and (len(cur) == 3 or (L and land >= 1 and len(cur) >= 2) or (L and land == 2)):
            rows.append(cur); cur, land = [], 0
        cur.append((p, alt, cap)); land += L
    if cur: rows.append(cur)
    return rows
P = lambda n, a, c: (n, a, c)
edg = dict(slug='interior-edgewater', title='Edgewater, Miami', anchor='edgewater',
  desc='A bay-front apartment in Edgewater, Miami, designed end to end by AKA Interior Design: living room, kitchen, entry and study with custom millwork in fluted oak.',
  h1='Edgewater, Miami', facts='Full service. Completed 2026.',
  preload='<link rel="preload" as="image" type="image/avif" imagesrcset="/img/v2/edgf-hero-living-800.avif 800w, /img/v2/edgf-hero-living-1600.avif 1600w, /img/v2/edgf-hero-living-2400.avif 2400w" imagesizes="(max-width:700px) 100vw, 60vw" fetchpriority="high">\n',
  paras=['A bay-front apartment designed end to end: living room, kitchen, entry and study. Custom millwork in fluted oak runs from the kitchen to the living room and holds the television, a wine wall and lit niches.',
         'The gradient relief above the sofa set the palette for every room. The work was coordinated with the building and a general contractor; purchasing, deliveries and installation were run by the studio.'],
  rows=[['LEAD', P('edgf-hero-living|eager'.split('|')[0], 'Living room facing the bay: a long pale sectional with a plum throw, a sculptural coffee table and a gradient relief on the wall', 'The gradient relief above the sofa set the palette for the apartment.')],
        [P('edgf-long-view', 'Living room, fluted-oak wall and kitchen in one room, the bay beyond', 'One room from the kitchen to the bay.'), P('edgf-media-wall', 'Media wall in fluted oak with lit niches and a wine wall under a brass and smoked-glass pendant', 'The wall of fluted oak: wine, niches and the television in one piece.')],
        [P('edgf-kitchen', 'Kitchen bar with stools under a globe chandelier and a bouclé armchair', 'The kitchen bar.'), P('edgf-living', 'A pale sectional with a plum throw, a sculptural coffee table and a textured rug', 'Living room.'), P('edgf-sofa-bay', 'The sectional and an oval travertine coffee table', 'Travertine, bouclé and a plum throw.')],
        [P('edgf-entry', 'The entry: a round backlit mirror on fluted oak and a floating shelf', 'The entry.'), P('edgf-niche', 'Two white ceramic vases in a fluted-oak niche', 'A niche in the millwork.'), P('edgf-terrace', 'Terrace dining table in stone with woven chairs over the bay', 'The terrace, over the bay.')]],
  credits='Design: AKA Interior Design, Fabian Ortega. Photographs taken by phone at delivery, corrected only for light and verticals.',
  next='<a class="tl" href="/interior-collector">Next: a collector’s apartment, Miami</a>')
pieces = [('Spaghetti vase','Gaetano Pesce, Fish Design. Red resin, made by hand.','The only object on the pine coffee table, next to two stacked monographs. Its red is the red of the tiger in the painting above.'),
 ('Panthella 160 lamp','Verner Panton, Louis Poulsen. Chrome.','On the amber cart under the painting, with a candle in amber glass. Chrome is the only new metal, next to the cantilever chairs.'),
 ('Bilboquet table lamps','Philippe Malouin, Flos. Linen.','On both sides of the bed, with a head that turns to the page or to the wall.'),
 ('Parentesi','Achille and Pier Giacomo Castiglioni, Flos, 1971.','If the lounge chair becomes a reading corner: a cable from ceiling to floor with a single spot, almost no volume.'),
 ('Loop candleholders','Italian, vintage, silver-plated, in the manner of Lino Sabattini.','Two, on the diagonal, on each side of the bronze: the first thing you see when you walk in.'),
 ('Oxide planters','Ten Thousand Pots. Glazed ceramic, made by hand.','A glaze from chocolate to rust, the colour of the pine table and the leather chair.'),
 ('Picture lights','One family, polished chrome.','The same light for every work that needs one, so the eye goes to the art, not the fixtures.')]
col = dict(slug='interior-collector', title='A collector’s apartment, Miami', anchor='collector',
  desc='Collection styling for an open-plan apartment in Miami with more than twenty works: rearranged, lit, and every new piece chosen for a written reason.',
  h1='A collector’s apartment, Miami', facts='Collection styling. Proposal, 2026.',
  paras=['More than twenty works in one open room. Nothing leaves the collection and nothing is added to it. The proposal rearranges and lights the art, and changes only what sits around it: a few pieces with a signature, warm textures, and one colour taken from the paintings.',
         'The photographs show the apartment as it is today, before the proposal.'],
  rows=[[P('colf-living', 'Open living room: a patterned blue rug, a cognac leather lounge chair and a pine coffee table', 'The living room as it is today.'), P('colf-window', 'Curved window wall with a round work, velvet armchairs and a cognac sofa', 'The window wall and the round work.')],
        [P('colf-dining', 'Dining table with caned chairs and a gold sculpture, framed works on the kitchen wall', 'The dining table.'), P('colf-bronze', 'A gold sculpture on the dining table by the window', 'The bronze.'), P('colf-entry-wall', 'An entry wall with framed works hung close together', 'The entry wall.')],
        ['LEAD', P('colf-wave', 'A large work on paper of a wave in blues, by the door', 'A large work on paper, by the door.')]],
  extra='  <section class="sub-block" aria-labelledby="pcs"><h2 id="pcs">What the proposal adds, and why</h2><dl>' + ''.join(f'<div><dt>{a}<span>{b}</span></dt><dd>{c}</dd></div>' for a, b, c in pieces) + '</dl></section>',
  credits='Design and curation: AKA Interior Design, Fabian Ortega. The artists of the collection are not named.',
  next='<a class="tl" href="/interior-quito">Next: from plan to home, Quito</a>')
dec = [('Six chairs, not eight','The chosen chair, the Klub by Steen Østergaard, is 63.5 cm wide; three a side would overlap by 2.5 cm. Two a side and two at the heads, and four more at the island.'),
 ('A piece made for the dining wall','“Trama Topográfica”: a wool-felt work drawn by the studio for the wall behind the table, in the shyrdak tradition — one continuous line that enters, turns and leaves. In prototype.'),
 ('A work for the only quiet corner','A Kathmandu paper wall work by Jessica Stockholder, in burgundy. It completes the red of a Rosso Levanto marble side table and balances the two greens.'),
 ('A rug that stays quiet','On the terrace, a flat weave under the whole seating area that stops 34 cm short of the fire.')]
qto = dict(slug='interior-quito', title='From plan to home: Quito', anchor='quito',
  desc='A family apartment in Quito designed remotely from Miami: measured plan, furnished plan to scale and renders of the proposal, each labelled.',
  h1='From plan to home: Quito', facts='Designed from Miami. Proposal, 2026.',
  paras=['A family apartment in Quito, designed from Miami and furnished at a distance. We measured the plan from the architect’s files, placed every piece to scale, and rendered the rooms to decide before anything was bought. Purchasing is online, with shipping to Ecuador.',
         'Twenty-four people can sit at once, in four groups that see each other. The renders are proposals, not photographs: the home is not installed yet.'],
  rows=[[P('qto-empty', 'The empty apartment: a long living room opening to the terrace and the kitchen', 'Before: the empty apartment, as it was handed over.'), P('qto-render-living', 'Render of the proposed living room: a cognac sofa, a pale rug and the terrace beyond', 'Render, proposal: the same room, furnished.')],
        ['LEAD', P('qto-plan-measured', 'Measured plan of the apartment in centimetres, drawn from the architect’s files', '1. The plan, measured in centimetres from the architect’s files.')],
        [P('qto-plan-furnished', 'Furnished plan to scale: terrace, living, dining, kitchen and entry, each piece numbered', '2. Every piece placed to scale and numbered to its own sheet.'), P('qto-render-dining', 'Render of the proposed dining room: an oval table in oak and cane, a round mirror and wall lights', '3. Render, proposal: the dining room.'), P('qto-render-entry', 'Render of the proposed entry: a tall carved column and a dark wood door', 'Render, proposal: the entry.')]],
  extra='  <section class="sub-block" aria-labelledby="dec"><h2 id="dec">Four decisions on the plan</h2><dl>' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in dec) + '</dl></section>',
  credits='Design and curation: AKA Interior Design, Fabian Ortega. Plans and renders by the studio; renders are concepts over photographs of the empty apartment and are labelled as such.',
  next='<a class="tl" href="/interior-oceanfront">Next: our own homes in Ecuador</a>')
oce = dict(slug='interior-oceanfront', title='Over the Pacific, Ecuador', anchor='own',
  desc='An apartment over the Pacific in Ecuador, designed and furnished by Fabian Ortega in 2018: linen, red wood, oak blocks under glass, a bed framed by four trunks.',
  h1='Over the Pacific, Ecuador', facts='Our own home. 2018.',
  paras=['An apartment over the Pacific, designed and furnished by Fabian himself, room by room. White linen sofas held in solid red-wood blocks, a marble table on a crowd of oak legs, and a wall of geometric works that spills across the plaster.',
         'Over the dining table, bare bulbs on long black cables; the table is a patchwork of oak blocks under glass, facing the sea. In the bedroom, the bed is framed by four tree trunks. On the roof, a pergola of cane over patterned tiles.'],
  rows=autorows(legacy('/tmp/old-oce.html')),
  credits='Design and furnishing: Fabian Ortega. Our own home, photographed as lived in.',
  next='<a class="tl" href="/interior-antiques">Next: over the river, Samborondón</a>')
ant = dict(slug='interior-antiques', title='Over the river, Samborondón', anchor='own',
  desc='A layered apartment over the river in Samborondón, Ecuador, designed and furnished by Fabian Ortega in 2018: family antiques with modern pieces, a dining room for twelve, a study painted by hand.',
  h1='Over the river, Samborondón', facts='Our own home. 2018.',
  paras=['The opposite of the beach: a layered home over the river where family antiques — a carved sideboard, a bracket clock, crystal candelabra — live with modern pieces. Draped, tufted sofas face each other across a chevron hide, around a table of brass and glass.',
         'A dining room for twelve under a large black-and-blue work, a bar painted black around a portrait, and a study brushed in blue across walls and ceiling like a woven check. Every room is anchored by its rug.'],
  rows=autorows(legacy('/tmp/old-ant.html')),
  credits='Design and furnishing: Fabian Ortega. Our own home, photographed as lived in.',
  next='<a class="tl" href="/interior-edgewater">Next: Edgewater, Miami</a>')
json.dump([edg, col, qto, oce, ant], open('/tmp/sp3.json', 'w'))
print([len(x['rows']) for x in (oce, ant)])
