# -*- coding: utf-8 -*-
"""Builds every page of the site into the repository root.

    python3 tools/build.py

Needs only the Python 3 standard library. Content lives in tools/common.py;
page layouts and section components live here. The generated HTML is
committed, so the published site itself has no build step.
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *   # noqa: F401,F403

# Projected anchor points for the route map, written by tools/map/generate-map.mjs.
PTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map-points.json')))

# ------------------------------------------------------------- components

def svc_explorer():
    tabs = '\n'.join(
        f'''        <li><button class="svx__tab" id="tab-{s["slug"]}" type="button"><span>{i+1:02d}</span>{s["title"]}{ico("arrow")}</button></li>'''
        for i, s in enumerate(SERVICES))
    panels = []
    for i, s in enumerate(SERVICES):
        checks = ''.join(f'<li>{ico("check")}<span>{b}</span></li>' for b in s['bullets'])
        tags = ''.join(f'<li>{t}</li>' for t in s['tags'])
        panels.append(f'''        <article class="svp" id="svc-{s["slug"]}">
          <div class="svp__photo">{pic(s["photo"], s["alt"], "(min-width: 960px) 44vw, 100vw")}</div>
          <div class="svp__top"><span class="svp__icon">{ico(s["icon"])}</span></div>
          <h3>{s["title"]}</h3>
          <p class="svp__desc">{s["blurb"]}</p>
          <p class="svp__desc">{s["detail"]}</p>
          <ul class="checks">{checks}</ul>
          <div class="svp__foot">
            <ul class="svp__modes" aria-label="Covers">{tags}</ul>
            <a class="link-arrow" href="contact.html?service={s["slug"]}#quote">Request a quote {ico("arrow")}</a>
          </div>
        </article>''')
    return f'''    <div class="svx">
      <ul class="svx__tabs">
{tabs}
      </ul>
      <div class="svx__panels">
{chr(10).join(panels)}
      </div>
    </div>'''


def netmap(hero=False):
    vb = PTS['viewBox']
    mx, my = PTS['monrovia']
    hubs = [('asia', 'Asia', 'end', 0, -16), ('middleEast', 'Middle East', 'middle', 0, -16),
            ('europe', 'Europe', 'middle', 0, -16), ('americas', 'Americas', 'middle', 0, -16),
            ('southAm', 'South America', 'middle', 0, 30), ('westAfrica', 'West Africa', 'start', 14, 5)]
    arcs, trails, marks, runners = [], [], [], []
    for i, (k, label, anchor, dx, dy) in enumerate(hubs):
        x, y = PTS[k]
        d = math.hypot(mx - x, my - y)
        cx, cy = (x + mx) / 2, (y + my) / 2 - max(40, d * 0.32)
        path = f'M{x} {y}Q{cx:.1f} {cy:.1f} {mx} {my}'
        trails.append(f'<path class="arc-trail" d="{path}"/>')
        arcs.append(f'<path class="arc" id="arc-{k}" d="{path}"/>')
        marks.append(f'<circle class="hub" cx="{x}" cy="{y}" r="6"/>'
                     f'<text class="hub-label" x="{x+dx}" y="{y+dy}" text-anchor="{anchor}">{label}</text>')
        runners.append(f'<circle class="runner" r="4" visibility="hidden">'
                       f'<set attributeName="visibility" to="visible" begin="m{i}.begin"/>'
                       f'<animateMotion id="m{i}" dur="{2.6 + i * 0.35:.2f}s" repeatCount="indefinite" begin="indefinite">'
                       f'<mpath href="#arc-{k}"/></animateMotion></circle>')
    cls = 'netmap netmap--hero' if hero else 'netmap rv'
    return f'''      <figure class="{cls}" style="margin:0">
        <svg viewBox="{' '.join(map(str, vb))}" role="img" aria-labelledby="map-t">
          <title id="map-t">World map with freight lanes from Asia, the Middle East, Europe, the Americas and West Africa converging on Monrovia, Liberia</title>
          <image href="assets/img/world-dots.svg" x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}"/>
          <g>{''.join(trails)}</g>
          <g>{''.join(arcs)}</g>
          <g>{''.join(marks)}</g>
          <g>{''.join(runners)}</g>
          <circle class="home-ring" cx="{mx}" cy="{my}" r="14"/><circle class="home-ring r2" cx="{mx}" cy="{my}" r="14"/>
          <circle class="home-dot" cx="{mx}" cy="{my}" r="7"/>
          <text class="home-label" x="{mx-18}" y="{my+34}" text-anchor="end">Monrovia</text>
          <text class="home-sub" x="{mx-18}" y="{my+54}" text-anchor="end">Freeport · Bushrod Island</text>
        </svg>
      </figure>'''


def modegrid():
    return '<div class="modegrid rv">' + ''.join(
        f'<div class="mode">{ico(i)}<span class="mode__code">{c}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, t, c, d in MODES) + '</div>'


def journey():
    n = len(STEPS)
    pins = ''.join(f'<li style="left:{(i+0.5)/n*100:.1f}%"></li>' for i in range(n))
    stops = ''.join(f'<li class="stop"><p class="stop__n">STAGE {i+1:02d}</p><h3>{t}</h3><p>{d}</p></li>'
                    for i, (t, d) in enumerate(STEPS))
    return f'''      <div class="jr">
        <div class="jr__road" aria-hidden="true">
          <div class="jr__fill"></div>
          <ul class="jr__pins">{pins}</ul>
          <div class="jr__truck">{ico("truck")}</div>
        </div>
        <ol class="jr__stops">{stops}</ol>
      </div>'''


def docs_visual():
    docs = [('Commercial Invoice', 'INV'), ('Bill of Lading', 'B/L'),
            ('Certificate of Origin', 'COO'), ('Packing List', 'P/L')]
    cards = ''.join(
        f'<div class="doc" style="--i:{i}"><div class="doc__h"><span class="doc__t">{t}</span><span class="doc__c">{c}</span></div>'
        f'<div class="doc__lines">{"<i></i>" * 7}</div><div class="doc__row"><i></i><i></i></div></div>'
        for i, (t, c) in enumerate(docs))
    return f'''        <div class="docs rv" aria-hidden="true">{cards}<div class="stamp">CLEARED<small>CUSTOMS</small></div></div>'''


def doclist():
    items = [('Commercial invoice', 'Invoice'), ('Bill of lading', 'B/L'), ('Certificate of origin', 'COO'),
             ('Packing list', 'P/L'), ('Import & export declarations', 'Customs')]
    return '<ul class="doclist">' + ''.join(
        f'<li>{ico("doc")}<b>{t}</b><span>{c}</span></li>' for t, c in items) + '</ul>'


def adv_list():
    return '<ul class="adv">' + ''.join(
        f'<li><span class="adv__n">{i+1:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>'
        for i, (t, d) in enumerate(ADVANTAGE)) + '</ul>'


def segs():
    return '<div class="segs">' + ''.join(
        f'<article class="seg rv" style="--rd:{i*.08:.2f}s"><span class="seg__i">{ico(ic)}</span><h3>{t}</h3><p>{d}</p></article>'
        for i, (ic, t, d) in enumerate(SEGMENTS)) + '</div>'


def values():
    return '<div class="values">' + ''.join(
        f'<div class="value rv" style="--rd:{i*.08:.2f}s"><span class="value__i">{ico(ic)}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, (ic, t, d) in enumerate(VALUES)) + '</div>'


def mv():
    return f'''      <div class="mv rv">
        <div><p class="mv__k">Our mission</p><p class="mv__q">{MISSION}</p></div>
        <div><p class="mv__k">Our vision</p><p class="mv__q">{VISION}</p></div>
      </div>'''


def faq_list():
    return '<div class="faq">' + ''.join(
        f'<details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>'
        for q, a in FAQ) + '</div>'


def faq_ld():
    import re
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}}
        for q, a in FAQ]}


TICKER = ['Freight forwarding', 'Customs brokerage', 'Documentation', 'Supply chain management',
          'Bonded warehousing', 'Cross-trade', 'Last-mile delivery', 'Air · Sea · Road · Rail']

def ticker():
    items = ''.join(f'<li>{t}</li>' for t in TICKER)
    return f'''  <div class="ticker">
    <div class="ticker__track"><ul>{items}</ul><ul aria-hidden="true">{items}</ul></div>
  </div>
'''

# ------------------------------------------------------------------- home

def home():
    modes = ''.join(f'<li>{ico(i)}{c}</li>' for i, t, c, d in MODES)
    body = f'''{header('index.html')}
<main id="main">

  <section class="hero hero--map">
    <div class="wrap hero__inner">
      <div class="hero__copy">
        <p class="pill"><span class="pulse"></span>Opposite the Freeport of Monrovia</p>
        <h1 class="h-display">Your cargo. <span class="gold">Our commitment.</span></h1>
        <p class="hero__lead">Freight forwarding, customs clearing and supply chain management for businesses in Liberia — by air, sea, road and rail, with every document handled end to end.</p>
        <div class="btns">
          <a class="btn btn--gold" href="contact.html#quote">Get a quote {ico("arrow", "arr")}</a>
          <a class="btn btn--line-dark" href="{WA}" rel="noopener">{ico("whatsapp")} Chat on WhatsApp</a>
        </div>
        <ul class="modes" aria-label="Transport modes">{modes}</ul>
      </div>
    </div>
    <div class="hero__map">
{netmap(hero=True)}
    </div>
  </section>

{ticker()}
  <section class="sec sec--paper" aria-labelledby="intro-h">
    <div class="wrap">
      {tag("01", "Who we are")}
      <h2 class="statement rv" id="intro-h">A full-service logistics company for Liberia. We move goods by <em>air, sea, road and rail</em> — and handle the <span class="u">customs and paperwork</span> in between.</h2>
      <div class="pillars">
        <div class="pillar rv"><p class="pillar__n">01 — EFFICIENCY</p><h3>The right route, first time</h3><p>We plan the mode, route and carrier around your budget and deadline, then coordinate every hand-off along the way.</p></div>
        <div class="pillar rv" style="--rd:.08s"><p class="pillar__n">02 — COMPLIANCE</p><h3>Cleared, not held</h3><p>Customs regulations and documentation requirements met in full, so shipments clear without avoidable delays or penalties.</p></div>
        <div class="pillar rv" style="--rd:.16s"><p class="pillar__n">03 — TIMELINESS</p><h3>One team, start to finish</h3><p>Cargo followed from origin to destination, with a single team accountable for getting it there on time.</p></div>
      </div>
      <div class="figures rv">
        <div class="figure"><p class="figure__v">04</p><p class="figure__l">Transport modes</p><p class="figure__s">Air, sea, road and rail</p></div>
        <div class="figure"><p class="figure__v">06</p><p class="figure__l">Service lines</p><p class="figure__s">From forwarding to the last mile</p></div>
        <div class="figure"><p class="figure__v">01</p><p class="figure__l">Point of contact</p><p class="figure__s">For the whole journey</p></div>
        <div class="figure"><p class="figure__v">LR</p><p class="figure__l">Rooted in Liberia</p><p class="figure__s">Based on Bushrod Island, Monrovia</p></div>
      </div>
    </div>
  </section>

  <section class="sec sec--white" id="services" aria-labelledby="svc-h">
    <div class="wrap">
      <div class="head head--split">
        <div>{tag("02", "Services")}<h2 class="h2" id="svc-h">Everything between origin and your door.</h2></div>
        <div><p class="lead">Six service lines covering the whole logistics value chain. Use one, or hand us the entire shipment.</p>
          <p style="margin-top:1.1rem"><a class="link-arrow" href="services.html">All service details {ico("arrow")}</a></p></div>
      </div>
{svc_explorer()}
    </div>
  </section>

  <section class="sec sec--dark sec--clip" aria-labelledby="reach-h">
    <div class="wrap split reach">
      <div>
        {tag("03", "Reach")}
        <h2 class="h2" id="reach-h">From the world’s trade hubs to <span class="gold">Liberia.</span></h2>
        <p class="lead" style="margin-top:1.25rem">Global shipping support and shipment tracking until your cargo lands in Liberia — then onward delivery across Liberia and beyond.</p>
      </div>
      <div class="hero__vis rv">
        <span class="hero__corner" aria-hidden="true"></span>
        <div class="hero__photo">
          {pic("port-crane-tall", "A gantry crane lifts a blue container from a berthed ship while a port worker in a hard hat watches from the quay.", "(min-width: 960px) 44vw, 100vw")}
          <p class="hero__badge"><b>●</b> Air · Sea · Road · Rail</p>
        </div>
        <div class="journey-card" aria-label="How a shipment moves with us">
          <p class="journey-card__h"><span>How your cargo moves</span><span>Origin → Door</span></p>
          <ol class="jc-steps">
            <li><span class="jc-dot">{ico("check")}</span>Freight booked<small>AIR · SEA · ROAD</small></li>
            <li><span class="jc-dot">{ico("check")}</span>Documents prepared<small>B/L · INV · COO</small></li>
            <li><span class="jc-dot">{ico("check")}</span>Customs cleared<small>DUTIES · TAX</small></li>
            <li><span class="jc-dot">{ico("check")}</span>Delivered<small>TO YOUR DOOR</small></li>
          </ol>
        </div>
      </div>
    </div>
    <div class="wrap">
      {modegrid()}
    </div>
  </section>

  <section class="sec sec--paper" aria-labelledby="proc-h">
    <div class="wrap">
      <div class="head head--split">
        <div>{tag("04", "How it works")}<h2 class="h2" id="proc-h">One team, from enquiry to handover.</h2></div>
        <p class="lead">Our operations cover the entire value chain, so the people who plan your shipment are the people who deliver it.</p>
      </div>
{journey()}
    </div>
  </section>

  <section class="sec sec--white" aria-labelledby="docs-h">
    <div class="wrap split">
      <div>
        {tag("05", "Customs &amp; documentation")}
        <h2 class="h2" id="docs-h">Paperwork is where shipments stall. We make sure yours don’t.</h2>
        <p class="lead" style="margin-top:1.25rem">Import and export documentation, duty and tax processing, and compliance with local and international law — prepared correctly the first time.</p>
        {doclist()}
      </div>
{docs_visual()}
    </div>
  </section>

  <section class="sec sec--dark" aria-labelledby="why-h">
    <div class="wrap split split--rev">
      <div class="frame frame--tall rv">
        {pic("fleet-tall", "A crew in high-visibility vests talks beside a white truck carrying a container, palm trees behind.", "(min-width: 960px) 44vw, 100vw")}
        <p class="frame__cap">One partner, every mode <span>Sea · Air · Road · Rail</span></p>
      </div>
      <div>
        {tag("06", "Why Peak")}
        <h2 class="h2" id="why-h">One partner instead of four.</h2>
        <p class="lead" style="margin-top:1.25rem">As a one-stop logistics provider we manage the complexity — so you can focus on your core business.</p>
        {adv_list()}
      </div>
    </div>
  </section>

  <section class="sec sec--paper" aria-labelledby="seg-h">
    <div class="wrap">
      <div class="head head--split">
        <div>{tag("07", "Who we serve")}<h2 class="h2" id="seg-h">Built for businesses of every size.</h2></div>
        <p class="lead">Our solutions are tailored to diverse logistics needs across industries — whether you import a container a year or run a continuous supply line.</p>
      </div>
      {segs()}
    </div>
  </section>

  <section class="sec sec--forest ribs" aria-labelledby="mv-h">
    <div class="wrap">
      <h2 class="visually-hidden" id="mv-h">Mission and vision</h2>
{mv()}
      <p class="words rv" style="margin-top:clamp(2.5rem,5vw,4rem)" aria-label="Trusted, reliable, professional"><span>Trusted</span><span></span><span class="o">Reliable</span><span></span><span>Professional</span></p>
    </div>
  </section>

  <section class="sec sec--white" id="faq" aria-labelledby="faq-h">
    <div class="wrap faq-grid">
      <div>
        {tag("08", "FAQ")}
        <h2 class="h2" id="faq-h">Questions we hear often.</h2>
        <p class="lead" style="margin-top:1.25rem">Something else on your mind? Ask us directly — we are happy to talk it through.</p>
        <div class="btns" style="margin-top:1.75rem">
          <a class="btn btn--green" href="{WA}" rel="noopener">{ico("whatsapp")} Ask on WhatsApp</a>
          <a class="btn btn--line" href="tel:{TEL}">{ico("phone")} Call us</a>
        </div>
      </div>
      {faq_list()}
    </div>
  </section>

{cta_block()}
</main>
{footer()}'''
    return head('Peak Logistics Services | Freight Forwarding &amp; Customs Clearing in Liberia',
                'Freight forwarding by air, sea, road and rail, customs clearing, documentation, warehousing and transportation — a full-service logistics company opposite the Freeport of Monrovia, Liberia.',
                'index.html', jsonld=[business_ld(), faq_ld()]) + body

# --------------------------------------------------------------- services

def services():
    jump = '<ul class="jump">' + ''.join(
        f'<li><a href="#{s["slug"]}"><span>{i+1:02d}</span>{s["short"]}</a></li>' for i, s in enumerate(SERVICES)) + '</ul>'
    rows = []
    for i, s in enumerate(SERVICES):
        tags = ''.join(f'<li>{t}</li>' for t in s['tags'])
        checks = ''.join(f'<li>{ico("check")}<span>{b}</span></li>' for b in s['bullets'])
        rows.append(f'''      <article class="svc-row" id="{s["slug"]}" aria-labelledby="h-{s["slug"]}">
        <div class="svc-row__side">
          <span class="svc-row__icon">{ico(s["icon"])}</span>
          <span class="svc-row__n">SERVICE {i+1:02d} / 06</span>
          <h2 id="h-{s["slug"]}">{s["title"]}</h2>
          <ul class="svp__modes" aria-label="Covers">{tags}</ul>
          <div class="svc-row__photo">{pic(s["photo"], s["alt"], "(min-width: 960px) 38vw, 100vw")}</div>
        </div>
        <div class="svc-row__body rv">
          <p class="lead">{s["blurb"]}</p>
          <p>{s["detail"]}</p>
          <div class="svc-row__box">
            <h3>What’s included</h3>
            <ul class="checks">{checks}</ul>
          </div>
          <div class="btns">
            <a class="btn btn--green" href="contact.html?service={s["slug"]}#quote">Request a quote {ico("arrow", "arr")}</a>
            <a class="btn btn--line" href="{WA}" rel="noopener">{ico("whatsapp")} Ask on WhatsApp</a>
          </div>
        </div>
      </article>''')
    body = f'''{header('services.html')}
<main id="main">
{phero('Services', 'Services', 'Logistics for the whole value chain.',
       'Six service lines, four transport modes and one point of contact — from the first enquiry, through customs clearance, to the final delivery address.', jump,
       photo='fleet', pos='62% 60%')}
  <section class="sec sec--white" aria-label="Service lines">
    <div class="wrap">
{chr(10).join(rows)}
    </div>
  </section>

  <section class="sec sec--paper" aria-labelledby="docs-h">
    <div class="wrap split">
      <div>
        {tag("", "Documentation")}
        <h2 class="h2" id="docs-h">The paperwork, prepared once and prepared right.</h2>
        <p class="lead" style="margin-top:1.25rem">Every consignment carries a paper trail. We prepare each document, check them against one another and manage them from booking to delivery.</p>
        {doclist()}
      </div>
{docs_visual()}
    </div>
  </section>

  <section class="sec sec--dark" aria-labelledby="modes-h">
    <div class="wrap">
      <div class="head head--split">
        <div>{tag("", "Transport modes")}<h2 class="h2" id="modes-h">Air, sea, road and rail — planned together.</h2></div>
        <p class="lead">We choose the combination that fits your cargo, your budget and your deadline, and coordinate every leg in between.</p>
      </div>
      {modegrid()}
    </div>
  </section>

  <section class="sec sec--white" aria-labelledby="proc-h">
    <div class="wrap">
      <div class="head head--split">
        <div>{tag("", "How it works")}<h2 class="h2" id="proc-h">From enquiry to handover.</h2></div>
        <p class="lead">The same team stays with your shipment the whole way through.</p>
      </div>
{journey()}
    </div>
  </section>

{cta_block()}
</main>
{footer()}'''
    return head('Services | Freight Forwarding, Customs Brokerage &amp; Transport — Peak Logistics Services',
                'Freight forwarding, customs brokerage, documentation, supply chain management, bonded warehousing, cross-trade and transportation across Liberia by air, sea, road and rail.',
                'services.html', jsonld=[crumbs_ld('Services', 'services.html')]) + body

# ------------------------------------------------------------------ about

def about():
    body = f'''{header('about.html')}
<main id="main">
{phero('About', 'About us', 'Reaching new heights in Liberia.',
       'Peak Logistics Services is a full-service logistics company committed to delivering efficient, reliable and client-focused solutions across Liberia.',
       photo='highway-truck', pos='70% 55%')}
  <section class="sec sec--white" aria-labelledby="intro-h">
    <div class="wrap split">
      <div>
        {tag("01", "Introduction")}
        <h2 class="h2" id="intro-h">Cargo moves. Paperwork follows. We handle both.</h2>
        <p class="lead" style="margin-top:1.25rem">We specialise in the seamless movement of goods by air, sea, road and rail, while ensuring full compliance with customs regulations and documentation requirements.</p>
        <p style="margin-top:1rem;color:var(--muted)">Our operations cover the entire logistics value chain — from freight coordination and customs clearance to warehousing and final delivery. By combining industry expertise with local market knowledge, we keep cargo flowing smoothly from origin to destination, prioritising efficiency, compliance and timeliness.</p>
        <div class="btns" style="margin-top:2rem">
          <a class="btn btn--green" href="{PDF}">{ico("download")} Company profile (PDF)</a>
          <a class="btn btn--line" href="services.html">Our services {ico("arrow", "arr")}</a>
        </div>
      </div>
      <div class="frame frame--tall rv">
        {pic("warehouse-team-tall", "Three warehouse staff in hard hats review a consignment on a tablet and clipboard beside racked pallets.", "(min-width: 960px) 44vw, 100vw")}
        <p class="frame__cap">Freight · Customs · Warehousing <span>Monrovia</span></p>
      </div>
    </div>
  </section>

  <section class="sec sec--forest ribs" id="mission" aria-labelledby="mv-h">
    <div class="wrap">
      <div class="head">{tag("02", "Mission &amp; vision")}<h2 class="h2" id="mv-h">Where we are going.</h2></div>
{mv()}
      <div class="head" id="values" style="margin-top:clamp(4rem,8vw,6rem)">{tag("03", "Core values")}<h2 class="h2">What we hold ourselves to.</h2></div>
      {values()}
      <p class="words rv" style="margin-top:clamp(3rem,6vw,4.5rem)" aria-label="Trusted, reliable, professional"><span>Trusted</span><span></span><span class="o">Reliable</span><span></span><span>Professional</span></p>
    </div>
  </section>

  <section class="sec sec--paper" aria-labelledby="adv-h">
    <div class="wrap split">
      <div>
        {tag("04", "Strategic advantage")}
        <h2 class="h2" id="adv-h">Why clients consolidate with us.</h2>
        <p class="lead" style="margin-top:1.25rem">As a one-stop logistics provider, our approach lets clients focus on their core business while we manage the logistics complexities.</p>
      </div>
      {adv_list()}
    </div>
  </section>

  <section class="sec sec--paper" id="market" aria-labelledby="seg-h" style="padding-top:0">
    <div class="wrap">
      <div class="head head--split">
        <div>{tag("05", "Target market")}<h2 class="h2" id="seg-h">Who we serve.</h2></div>
        <p class="lead">We serve businesses of all sizes, with solutions tailored to diverse logistics needs across industries.</p>
      </div>
      {segs()}
    </div>
  </section>

  <section class="sec sec--white" aria-labelledby="ahead-h">
    <div class="wrap">
      <div class="head">{tag("06", "Looking ahead")}<h2 class="h2" id="ahead-h">Expanding what we can carry for you.</h2>
        <p class="lead">We are focused on expanding our service offerings and entering new markets — continuously innovating to deliver logistics that improve efficiency, reduce costs and raise client satisfaction.</p></div>
      <div class="ahead">
        <div class="rv"><h3>New services</h3><p>Broadening what we offer, so more of your supply chain can sit with one trusted partner.</p></div>
        <div class="rv" style="--rd:.08s"><h3>New markets</h3><p>Taking the standards we hold in Liberia further afield, alongside the clients who grow with us.</p></div>
        <div class="rv" style="--rd:.16s"><h3>Continuous improvement</h3><p>Finding better ways to move cargo — faster, at lower cost and with fewer surprises.</p></div>
      </div>
      <div class="profile-card rv" style="margin-top:clamp(3rem,6vw,4.5rem)">
        <img class="profile-card__thumb" src="assets/img/company-flyer.jpg" width="820" height="1160" alt="" loading="lazy" decoding="async">
        <div><h3>Company profile</h3><p>Services, mission, values and contact details in one document — ready to share with your team.</p></div>
        <a class="btn btn--green" href="{PDF}">{ico("download")} Download</a>
      </div>
    </div>
  </section>

{cta_block()}
</main>
{footer()}'''
    return head('About Us | Peak Logistics Services, Monrovia, Liberia',
                'Our mission, vision, core values and the strategic advantage behind Peak Logistics Services — a full-service logistics company on Bushrod Island, Monrovia.',
                'about.html', jsonld=[crumbs_ld('About', 'about.html')]) + body

# ---------------------------------------------------------------- contact

def contact():
    svc = ''.join(
        f'<label class="choice"><input type="radio" name="service" value="{s["title"]}" data-slug="{s["slug"]}"{" required" if i == 0 else ""}>'
        f'<span>{ico(s["icon"])}{s["title"]}</span></label>' for i, s in enumerate(SERVICES))
    svc += f'<label class="choice"><input type="radio" name="service" value="Not sure yet — please advise"><span>{ico("question")}Not sure yet</span></label>'
    modes = ''.join(f'<label class="choice"><input type="checkbox" name="mode" value="{t.split()[0]}"><span>{ico(i)}{t.split()[0]}</span></label>'
                    for i, t, c, d in MODES)
    reply = ''.join(f'<label class="choice"><input type="radio" name="reply" value="{v}"{" checked" if n == 0 else ""}><span>{ico(ic)}{v}</span></label>'
                    for n, (ic, v) in enumerate([('whatsapp', 'WhatsApp'), ('phone', 'Phone call'), ('mail', 'Email')]))
    nextb = f'<button class="btn btn--green jsonly" type="button" data-go="next">Continue {ico("arrow", "arr")}</button>'
    backb = f'<button class="btn btn--line jsonly" type="button" data-go="back">{ico("back")} Back</button>'
    R = '<span class="req" aria-hidden="true"> *</span>'
    O = ' <span class="opt">(optional)</span>'

    body = f'''{header('contact.html')}
<main id="main">
{phero('Contact', 'Contact', 'Let’s move your cargo.',
       'Send the details through the quote form, or reach us directly on WhatsApp, by phone or by email. Our office is opposite the Freeport of Monrovia.',
       photo='gate-check', pos='64% 50%')}
  <section class="sec sec--paper">
    <div class="wrap contact-grid">

      <div class="wiz" id="quote">
        <div class="wiz__head">
          {tag("", "Request a quote")}
          <h2 class="h2" style="font-size:clamp(1.7rem,3vw,2.4rem)">Tell us about your shipment.</h2>
          <p class="muted" style="margin-top:.75rem">Four short steps. Nothing is stored on this website — your request comes straight to us by WhatsApp or email.</p>
          <ol class="wiz__steps" aria-label="Progress"><li>Service</li><li>Cargo</li><li>Contact</li><li>Send</li></ol>
        </div>
        <form id="quote-form" action="mailto:{EMAIL}?subject=Quote%20request" method="post" enctype="text/plain"
              data-wa="{WA_NUM}" data-email="{EMAIL}">

          <fieldset data-step="1">
            <legend>What do you need?<small>Pick the closest match — you can explain the details later.</small></legend>
            <fieldset class="grp"><legend>Service{R}</legend><div class="choices">{svc}</div></fieldset>
            <fieldset class="grp"><legend>Transport mode{O}</legend><div class="chips">{modes}</div></fieldset>
            <div class="wiz__nav"><div class="right">{nextb}</div></div>
          </fieldset>

          <fieldset data-step="2">
            <legend>About the cargo<small>Rough figures are fine.</small></legend>
            <div class="fields fields--2">
              <div class="fld"><label class="lbl" for="origin">Collecting from{R}</label><input id="origin" name="origin" required placeholder="e.g. Shanghai, China" autocomplete="off"></div>
              <div class="fld"><label class="lbl" for="destination">Delivering to{R}</label><input id="destination" name="destination" required placeholder="e.g. Monrovia, Liberia" autocomplete="off"></div>
            </div>
            <div class="fields" style="margin-top:1.1rem">
              <div class="fld"><label class="lbl" for="cargo">What are you shipping?{R}</label><textarea id="cargo" name="cargo" required placeholder="e.g. Two 40ft containers of building materials"></textarea></div>
            </div>
            <div class="fields fields--2" style="margin-top:1.1rem">
              <div class="fld"><label class="lbl" for="size">Weight or volume{O}</label><input id="size" name="size" placeholder="e.g. 18 tonnes, or 2 × 40ft"></div>
              <div class="fld"><label class="lbl" for="ready">Ready to ship{O}</label><input id="ready" name="ready" type="date"></div>
            </div>
            <div class="wiz__nav">{backb}<div class="right">{nextb}</div></div>
          </fieldset>

          <fieldset data-step="3">
            <legend>Your details<small>Give us a phone number, an email address, or both.</small></legend>
            <div class="fields fields--2">
              <div class="fld"><label class="lbl" for="name">Full name{R}</label><input id="name" name="name" required autocomplete="name"></div>
              <div class="fld"><label class="lbl" for="company">Company{O}</label><input id="company" name="company" autocomplete="organization"></div>
              <div class="fld"><label class="lbl" for="phone">Phone / WhatsApp</label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+231 …"></div>
              <div class="fld"><label class="lbl" for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
            </div>
            <fieldset class="grp" style="margin-top:1.6rem"><legend>Reply by</legend><div class="chips">{reply}</div></fieldset>
            <div class="wiz__nav">{backb}<div class="right"><button class="btn btn--green jsonly" type="button" data-go="next">Review request {ico("arrow", "arr")}</button></div></div>
            <div class="nojs-only" style="margin-top:2rem">
              <button class="btn btn--green" type="submit">{ico("mail")} Send by email</button>
              <p class="wiz__note">Opens your email app. You can also <a href="{WA}" rel="noopener">message us on WhatsApp</a> or call {TEL_H}.</p>
            </div>
          </fieldset>

          <fieldset data-step="review" hidden>
            <legend>Check and send<small>Both options open with your request already written — just press send.</small></legend>
            <dl class="review" id="review"></dl>
            <div class="send">
              <button class="btn btn--wa btn--block" type="button" data-go="wa">{ico("whatsapp")} Send via WhatsApp</button>
              <button class="btn btn--green btn--block" type="button" data-go="email">{ico("mail")} Send via email</button>
            </div>
            <p class="wiz__status" id="wiz-status" role="status" tabindex="-1" hidden></p>
            <div class="wiz__nav">{backb}<div class="right"><button class="btn btn--line jsonly" type="button" data-go="edit">Start over</button></div></div>
          </fieldset>
        </form>
      </div>

      <aside class="aside" aria-label="Contact details">
        <div class="card-dark">
          <h2>Talk to us directly</h2>
          <ul class="cinfo">
            <li><span>{ico("whatsapp")}</span><div><small>WhatsApp</small><a href="{WA}" rel="noopener">{TEL_H}</a></div></li>
            <li><span>{ico("phone")}</span><div><small>Phone</small><a href="tel:{TEL}">{TEL_H}</a></div></li>
            <li><span>{ico("mail")}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL_WBR}</a></div></li>
            <li><span>{ico("pin")}</span><div><small>Office</small><address>{ADDR_HTML}</address></div></li>
            <li><span>{ico("instagram")}</span><div><small>Social</small><a href="{IG}" rel="noopener">@peaklogisticsservices</a></div></li>
          </ul>
        </div>
        <div class="card-light">
          <h2>Have these to hand</h2>
          <p>A quote comes back faster when we know:</p>
          <ul class="checks" style="margin-top:1rem;font-size:.95rem">
            <li>{ico("check")}<span>What the goods are, and roughly how much</span></li>
            <li>{ico("check")}<span>Where they are collected and delivered</span></li>
            <li>{ico("check")}<span>When they need to arrive</span></li>
            <li>{ico("check")}<span>Any documents you already hold — invoice, packing list</span></li>
          </ul>
        </div>
      </aside>

    </div>
  </section>

  <section class="sec sec--white" id="map" aria-labelledby="map-h">
    <div class="wrap">
      <div class="head head--split">
        <div>{tag("", "Find us")}<h2 class="h2" id="map-h">Opposite the Freeport of Monrovia.</h2></div>
        <p class="lead">Behind the CONEX gas station on Bushrod Island — minutes from where your containers land.</p>
      </div>
      <div class="mapbox">
        <div class="mapbox__card">
          <b>Peak Logistics Services</b>
          <p class="muted" style="margin-top:.35rem">{ADDR_HTML}</p>
          <p style="margin-top:.75rem"><a class="link-arrow" href="https://www.google.com/maps/search/?api=1&amp;query=Freeport+of+Monrovia%2C+Bushrod+Island%2C+Monrovia%2C+Liberia" rel="noopener">Get directions {ico("ne")}</a></p>
        </div>
        <iframe title="Map of the Freeport of Monrovia area, Bushrod Island" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
                src="https://www.openstreetmap.org/export/embed.html?bbox=-10.8400%2C6.3150%2C-10.7550%2C6.3700&amp;layer=mapnik&amp;marker=6.3450%2C-10.8060"></iframe>
      </div>
      <p class="muted" style="margin-top:1rem;font-size:.88rem">Map data &copy; <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a> contributors. The marker shows the Freeport; call us for exact directions to the office.</p>
    </div>
  </section>
</main>
{footer()}'''
    return head('Contact &amp; Quotes | Peak Logistics Services, Monrovia, Liberia',
                'Request a logistics quote or contact Peak Logistics Services on +231 886 826 289, WhatsApp or peaklogisticsservices@gmail.com. Office opposite the Freeport of Monrovia, Bushrod Island.',
                'contact.html', jsonld=[business_ld(), crumbs_ld('Contact', 'contact.html')]) + body

# -------------------------------------------------------------------- 404

def notfound():
    body = f'''{header('')}
<main id="main">
  <section class="sec sec--dark">
    <div class="wrap nf">
      <div>
        <p class="nf__code" aria-hidden="true">404</p>
        <h1 class="h1">Wrong turn.</h1>
        <p class="lead">This page has gone off route — it does not exist or has moved. Let us get you back on the road.</p>
        <div class="btns">
          <a class="btn btn--gold" href="index.html">Back to home {ico("arrow", "arr")}</a>
          <a class="btn btn--line-dark" href="contact.html#quote">Request a quote</a>
        </div>
      </div>
    </div>
  </section>
</main>
{footer()}'''
    return head('Page not found | Peak Logistics Services',
                'The page you were looking for could not be found. Return to Peak Logistics Services — freight forwarding and customs clearing in Monrovia, Liberia.',
                '404.html', noindex=True) + body


def build_all():
    write('index.html', home())
    write('services.html', services())
    write('about.html', about())
    write('contact.html', contact())
    write('404.html', notfound())

if __name__ == '__main__':
    build_all()
