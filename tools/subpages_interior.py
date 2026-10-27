import json, sys
sys.path.insert(0, 'tools'); import subpage
def f(cls, ph, cap=''):
    return f'<figure class="{cls}">{ph}' + (f'<figcaption class="cap">{cap}</figcaption>' if cap else '') + '</figure>'
S6, S3, S2 = '(max-width:900px) 100vw, 1180px', '(max-width:900px) 100vw, 590px', '(max-width:900px) 50vw, 390px'
edg = dict(slug='interior-edgewater', title='Edgewater Residence, Miami', anchor='edgewater',
  desc='A bay-front apartment in Edgewater, Miami, designed end to end by AKA Interior Design: living room, kitchen, entry and study with custom millwork.',
  no='Project 01', h1='Edgewater Residence, Miami.', mline='Miami · 2026 · Residential · Full service',
  paras=['A bay-front apartment in Edgewater, designed end to end: living room, kitchen, entry and study, with custom millwork throughout. A gradient relief above the sofa sets the palette for the whole home; fluted oak, lit niches and a wine wall turn the media wall into one piece of furniture joined to the kitchen.',
         'Coordinated with the building’s requirements and a general contractor; purchasing, deliveries and installation run by the studio.'],
  body=['<div class="grid">',
    f('w6', '{{pic:edg-hero-living|Living room facing the bay: a long pale sectional, a sculptural coffee table and a gradient relief on the wall|'+S6+'|eager}}', 'The living room. A gradient relief above the sofa sets the palette for the whole home.'),
    f('w3', '{{pic:edg-media-wall|Media wall in fluted oak with lit niches and a wine wall, a brass and smoked-glass pendant|'+S3+'}}', 'The media wall: one piece of custom millwork, joined to the kitchen.'),
    f('w3', '{{pic:edg-long-view|One continuous room: living room, fluted oak column and kitchen|'+S3+'}}', 'One continuous room, read from end to end.'),
    f('w2 t', '{{pic:edg-kitchen|Kitchen island with stools under a globe chandelier and a bouclé armchair|'+S2+'}}', 'Kitchen and bar.'),
    f('w2 t', '{{pic:edg-living|A pale sectional with a plum throw, a sculptural coffee table and a textured rug|'+S2+'}}', 'Living room.'),
    f('w2 t', '{{pic:edg-sofa-bay|The sectional and the coffee table, the bay through the glass|'+S2+'}}', 'Toward the bay.'),
    f('w2 t', '{{pic:edg-entry|The entry: a round backlit mirror on fluted oak and a shelf|'+S2+'}}', 'The entry.'),
    f('w2 t', '{{pic:edg-niche|Two white ceramic vases in a fluted oak niche|'+S2+'}}', 'A niche in the millwork.'),
    f('w2 t', '{{pic:edg-terrace|Terrace dining table in stone with woven chairs over the bay|'+S2+'}}', 'Terrace.'),
    '</div>'],
  credits='Design: AKA Interior Design — Fabian Ortega · Custom millwork, purchasing and installation coordinated by the studio · Photographs: phone, edited for light and verticals only.',
  next='<a class="alt" href="/interior-collector">Collector’s Apartment, Miami →</a>')
pieces = [('Spaghetti vase','Gaetano Pesce · Fish Design · red resin, made by hand','The only object on the pine coffee table, next to two stacked monographs. <em>Its red is the red of the tiger.</em>'),
 ('Panthella 160, chrome','Verner Panton · Louis Poulsen','On the amber cart under the tiger, with a candle in amber glass: a warm altar beneath the painting. Chrome and silver are the only new metal, in conversation with the cantilever chairs.'),
 ('Bilboquet table lamps','Philippe Malouin · Flos · linen','At both sides of the bed, with a head that turns to the page or to the wall.'),
 ('Parentesi','Castiglioni · Flos · 1971','If the lounge chair becomes a reading corner: a cable from ceiling to floor with a single spot, almost no volume.'),
 ('Loop candleholders','Italian, vintage, silver-plated · in the manner of Lino Sabattini','Two, on the diagonal, flanking the bronze — the first thing you see when you walk in.'),
 ('Oxide planters','Ten Thousand Pots · glazed ceramic, made by hand','A glaze that runs from chocolate to rust, in the colour of the pine table and the leather of the lounge chair: it reads as studio ceramics, not as a nursery pot.'),
 ('Picture lights','one family, polished chrome','A single family of lights for the works that need them, so the collection — not the fixtures — is what you see.')]
col = dict(slug='interior-collector', title='Collector’s Apartment, Miami', anchor='collector',
  desc='Collection styling for an open-plan apartment in Miami with more than twenty works: rearranged, lit, and every new piece with a written reason.',
  no='Project 02', h1='Collector’s Apartment, Miami.', mline='Miami · 2026 · Collection styling · Proposal',
  paras=['More than twenty works in an open-plan apartment. The brief: nothing leaves, nothing is added to the collection. It is rearranged and lit, and the layer around it is rewritten — few pieces with a signature, warm textures, and a single thread of colour taken from the art.',
         'The photographs show the apartment as it lives today, before the proposal.'],
  body=['<div class="grid">',
    f('w3 t', '{{pic:col-living|Open living room: a patterned blue rug, a cognac leather lounge chair and a pine coffee table|'+S3+'|eager}}', 'The collection as it lives today.'),
    f('w3 t', '{{pic:col-window|Curved window wall with a round work, velvet armchairs and a cognac sofa|'+S3+'}}', 'The round work and the window wall.'),
    f('w2 t', '{{pic:col-dining|Dining table with caned chairs and a gold sculpture, framed works on the kitchen wall|'+S2+'}}', 'The dining table, where the proposal puts the bronze alone at the centre.'),
    f('w2 t', '{{pic:col-bronze|A gold sculpture on the dining table by the window|'+S2+'}}', 'The bronze.'),
    f('w2 t', '{{pic:col-entry-wall|An entry wall with framed works hung close together|'+S2+'}}', 'The entry wall.'),
    f('w6', '{{pic:col-wave|A large work on paper of a wave in blues, above the floor by the door|'+S6+'}}', 'A large work on paper.'),
    '</div>',
    '<section class="block" aria-labelledby="pcs"><div><span class="k" style="display:block;margin-bottom:14px">The proposal</span><h2 class="serif" id="pcs">The pieces, and why they are there.</h2></div><div class="rows">' +
    ''.join(f'<div class="rowi"><div><b>{a}</b><span>{b}</span></div><p>{c}</p></div>' for a,b,c in pieces) + '</div></section>'],
  credits='Design and curation: AKA Interior Design — Fabian Ortega · Photographs show the apartment before the proposal · The artists of the collection are not named.',
  next='<a class="alt" href="/interior-quito">Quito Residence →</a>')
dec = [('Six chairs, not eight: comfort rules.','The Klub chair by Steen Østergaard is 63.5 cm wide; three a side would overlap by 2.5 cm. Two a side plus two heads at the table, and four more at the island.'),
 ('A piece made for the dining wall.','“Trama Topográfica”: a wool-felt work drawn by the studio for the wall behind the table, in the shyrdak felt tradition — one continuous line that enters, turns and leaves. In prototype.'),
 ('A work over the only quiet corner.','A Kathmandu paper wall work by Jessica Stockholder, in burgundy, chosen against the palette: it completes the red thread of a Rosso Levanto marble side table and balances the two greens.'),
 ('A rug that stays quiet.','On the terrace, a flat weave that takes the whole seating area and stops 34 cm short of the fire — the fire is never over a rug.')]
qto = dict(slug='interior-quito', title='Quito Residence: from plan to home', anchor='quito',
  desc='A family apartment in Quito designed remotely from Miami: measured plan, furnished plan to scale and renders of the proposal, each labelled.',
  no='Project 05', h1='Quito Residence: from plan to home.', mline='Quito, Ecuador · 2026 · Remote design · Plan and proposal',
  paras=['A family apartment in Quito, designed from Miami and furnished at a distance. The plan was rebuilt from the architect’s drawings and measured in centimetres; every piece has its own sheet and a line that says why it is there; purchasing is online, with shipping to Ecuador.',
         'Twenty-four people can sit at once, in four groups that see each other. Renders are proposals, not photographs: the home is not installed yet.'],
  body=['<div class="grid">',
    f('w6', '{{pic:qto-empty|The empty apartment: a long living room opening to the terrace and the kitchen|'+S6+'|eager}}', '<span class="lab">Before</span> The empty apartment, as it was handed over.'),
    f('w6 paper', '{{pic:qto-plan-measured|Measured plan of the apartment in centimetres, drawn from the architect’s files|'+S6+'}}', '<span class="lab">Plan</span> Measured from the architect’s files, in centimetres.'),
    f('w3 paper', '{{pic:qto-plan-furnished|Furnished plan to scale: terrace, living, dining, kitchen and entry, each piece numbered|'+S3+'}}', '<span class="lab">Plan · furnished</span> Every piece to scale, numbered to its own sheet.'),
    f('w3', '{{pic:qto-render-entry|Render of the proposed entry: a tall carved column and a dark wood door|'+S3+'}}', '<span class="lab">Render · proposal</span> The entry.'),
    f('w3', '{{pic:qto-render-living|Render of the proposed living room: a cognac sofa, a pale rug and the terrace beyond|'+S3+'}}', '<span class="lab">Render · proposal</span> The living room.'),
    f('w3', '{{pic:qto-render-dining|Render of the proposed dining room: an oval table in oak and cane, a round mirror and wall lights|'+S3+'}}', '<span class="lab">Render · proposal</span> The dining room.'),
    '</div>',
    '<section class="block" aria-labelledby="dec"><div><span class="k" style="display:block;margin-bottom:14px">Decisions on the plan</span><h2 class="serif" id="dec">Four decisions, and why.</h2></div><div class="rows">' +
    ''.join(f'<div class="rowi"><div><b>{a}</b></div><p>{b}</p></div>' for a,b in dec) + '</div></section>'],
  credits='Design and curation: AKA Interior Design — Fabian Ortega · Plans and renders by the studio; renders are concepts over photographs of the empty apartment and are labelled as such.',
  next='<a class="alt" href="/interior-oceanfront">Oceanfront Apartment, Ecuador →</a>')
json.dump([edg, col, qto], open('/tmp/sp.json', 'w'))
