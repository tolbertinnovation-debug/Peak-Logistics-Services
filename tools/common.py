# -*- coding: utf-8 -*-
"""Content and shared page chrome for the Peak Logistics Services site.

Edit the contact details, services, FAQ and other copy here, then run
`python3 tools/build.py` from the repository root to regenerate the HTML.
"""
import json, html, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + os.sep
SITE = 'https://peaklogisticsservices.com'
TEL, TEL_H = '+231886826289', '+231 886 826 289'
WA_NUM = '231886826289'
WA = 'https://wa.me/' + WA_NUM
EMAIL = 'peaklogisticsservices@gmail.com'
EMAIL_WBR = 'peaklogisticsservices<wbr>@gmail.com'   # display only: breaks cleanly before the @
FB = 'https://www.facebook.com/peaklogisticsservices'
IG = 'https://www.instagram.com/peaklogisticsservices'
TAGLINE = 'Your Cargo, Our Commitment. Reaching New Heights in Liberia.'
ADDR_LINES = ['Opposite Freeport of Monrovia', 'Behind CONEX Gas Station',
              'Bushrod Island, Monrovia, Liberia']
ADDR_HTML = '<br>'.join(ADDR_LINES)
PDF = 'assets/docs/Peak-Logistics-Services-Company-Profile.pdf'

PHOTOS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos.json')))

def pic(name, alt, sizes, cls='', eager=False):
    """<picture> with WebP and a JPEG fallback at every width in tools/photos.json."""
    v = PHOTOS[name]
    src = lambda ext: ', '.join(f'assets/img/photos/{name}-{w}.{ext} {w}w' for w, h in v)
    w, h = v[-1]
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return (f'<picture{c}><source type="image/webp" srcset="{src("webp")}" sizes="{sizes}">'
            f'<img src="assets/img/photos/{name}-{v[0][0]}.jpg" srcset="{src("jpg")}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{html.escape(alt, quote=True)}"{load} decoding="async"></picture>')

def ico(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} aria-hidden="true"><use href="#i-{name}"></use></svg>'

S = 'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
SPRITE = f'''<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true" focusable="false">
<symbol id="i-ship" viewBox="0 0 24 24" {S}><path d="M2 20.5c1.2 0 1.9-.5 2.6-1.2a2.8 2.8 0 0 1 4.3 0c.7.7 1.4 1.2 2.6 1.2s1.9-.5 2.6-1.2a2.8 2.8 0 0 1 4.3 0c.7.7 1.4 1.2 2.6 1.2"/><path d="M4.5 17.5 3 12.5h18l-2 5"/><path d="M6 12.5V8h7v4.5"/><path d="M13 9.5h4v3"/><path d="M8.5 8V5h3v3"/></symbol>
<symbol id="i-plane" viewBox="0 0 24 24" {S}><path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3L13 8 4.8 6.2a.5.5 0 0 0-.5.8l4 4.6-2.3 2.3-2.4-.5a.5.5 0 0 0-.5.8L5 16.5 6.3 19a.5.5 0 0 0 .8-.1l-.5-2.4 2.3-2.3 4.6 4a.5.5 0 0 0 .8-.5Z"/></symbol>
<symbol id="i-truck" viewBox="0 0 24 24" {S}><path d="M14 17V6a1 1 0 0 0-1-1H2.5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1H4"/><path d="M14 8.5h4.2a1 1 0 0 1 .85.47l2.3 3.7a1 1 0 0 1 .15.53V16a1 1 0 0 1-1 1h-1.2"/><circle cx="6.8" cy="17.3" r="2.2"/><circle cx="16.8" cy="17.3" r="2.2"/><path d="M9 17.3h5.6"/></symbol>
<symbol id="i-train" viewBox="0 0 24 24" {S}><rect x="5" y="3" width="14" height="13" rx="3"/><path d="M5 10h14"/><path d="M8.5 13.2h.01M15.5 13.2h.01"/><path d="m8 19.5-2 2M16 19.5l2 2"/><path d="M9 3v7M15 3v7"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24" {S}><path d="M12 21.5s7.5-3.4 7.5-9.6V5.6L12 2.5 4.5 5.6v6.3c0 6.2 7.5 9.6 7.5 9.6Z"/><path d="m8.8 12 2.2 2.2 4.4-4.4"/></symbol>
<symbol id="i-doc" viewBox="0 0 24 24" {S}><path d="M14 2.5H7a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-12Z"/><path d="M14 2.5v5h5"/><path d="M8.5 12.5h7M8.5 16h7"/></symbol>
<symbol id="i-chain" viewBox="0 0 24 24" {S}><path d="M3.5 7.5 12 3l8.5 4.5L12 12Z"/><path d="M3.5 7.5v9L12 21v-9"/><path d="M20.5 7.5v9L12 21"/><path d="m7.8 5.3 8.4 4.5"/></symbol>
<symbol id="i-warehouse" viewBox="0 0 24 24" {S}><path d="M2.5 20.5V9L12 4l9.5 5v11.5"/><path d="M6.5 20.5V13h11v7.5"/><path d="M6.5 16.7h11"/><path d="M1.5 20.5h21"/></symbol>
<symbol id="i-route" viewBox="0 0 24 24" {S}><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="5.5" r="2.5"/><path d="M16 5.5H9a3.5 3.5 0 0 0 0 7h6a3.5 3.5 0 0 1 0 7H8"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m4.5 12.5 4.8 4.8L19.5 7"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15.5"/><path d="m13.5 6 6 6-6 6"/></symbol>
<symbol id="i-back" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12H4.5"/><path d="m10.5 6-6 6 6 6"/></symbol>
<symbol id="i-ne" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24" {S}><path d="M15.5 21A13.5 13.5 0 0 1 3 8.5 3.5 3.5 0 0 1 6.5 5h1.2a1 1 0 0 1 1 .8l.7 3a1 1 0 0 1-.3.95l-1.4 1.3a12 12 0 0 0 5.25 5.25l1.3-1.4a1 1 0 0 1 .95-.3l3 .7a1 1 0 0 1 .8 1v1.2A3.5 3.5 0 0 1 15.5 21Z"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24" {S}><rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3 7 8.1 5.4a1.6 1.6 0 0 0 1.8 0L21 7"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24" {S}><path d="M12 22s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11Z"/><circle cx="12" cy="11" r="2.6"/></symbol>
<symbol id="i-target" viewBox="0 0 24 24" {S}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/></symbol>
<symbol id="i-eye" viewBox="0 0 24 24" {S}><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24" {S}><path d="m12 3 2.7 5.7 6.3.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.3-.9Z"/></symbol>
<symbol id="i-handshake" viewBox="0 0 24 24" {S}><path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2l-3.9-3.9a2 2 0 0 0-2.8 0l-.9.9a1.4 1.4 0 0 1-2-2l2.8-2.8a4 4 0 0 1 4.8-.6l.5.3a3 3 0 0 0 2 .4H21"/><path d="m21 5.5.5 9-2 .5"/><path d="M3 5.5 2.5 14.5 9 21a1.4 1.4 0 0 0 2-2"/><path d="M3 5.5h7"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24" {S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-rocket" viewBox="0 0 24 24" {S}><path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1Z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2Z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/></symbol>
<symbol id="i-building" viewBox="0 0 24 24" {S}><rect x="4" y="2.5" width="16" height="19" rx="1.5"/><path d="M9 21.5v-4h6v4"/><path d="M8.5 6.5h.01M12 6.5h.01M15.5 6.5h.01M8.5 10h.01M12 10h.01M15.5 10h.01M8.5 13.5h.01M12 13.5h.01M15.5 13.5h.01"/></symbol>
<symbol id="i-swap" viewBox="0 0 24 24" {S}><path d="M4 8h14.5"/><path d="m15 4.5 3.5 3.5-3.5 3.5"/><path d="M20 16H5.5"/><path d="m9 12.5-3.5 3.5L9 19.5"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24" {S}><circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19"/><path d="M12 2.5a14.5 14.5 0 0 1 0 19 14.5 14.5 0 0 1 0-19Z"/></symbol>
<symbol id="i-download" viewBox="0 0 24 24" {S}><path d="M12 3.5v12"/><path d="m7 10.5 5 5 5-5"/><path d="M4 20.5h16"/></symbol>
<symbol id="i-box" viewBox="0 0 24 24" {S}><path d="M21 8 12 3 3 8v8l9 5 9-5Z"/><path d="m3 8 9 5 9-5M12 13v8"/></symbol>
<symbol id="i-question" viewBox="0 0 24 24" {S}><circle cx="12" cy="12" r="9.5"/><path d="M9.3 9a2.8 2.8 0 0 1 5.4 1c0 1.9-2.7 2.5-2.7 4"/><path d="M12 17.5h.01"/></symbol>
<symbol id="i-sparkle" viewBox="0 0 24 24" {S}><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-whatsapp" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.05L2 22l5.1-1.33A10 10 0 1 0 12 2Zm0 1.8a8.2 8.2 0 1 1-4.28 15.2l-.3-.18-3.03.79.8-2.95-.2-.31A8.2 8.2 0 0 1 12 3.8Zm-3.5 4c-.18 0-.47.07-.72.34-.25.27-.95.93-.95 2.26s.98 2.62 1.11 2.8c.14.18 1.9 3.02 4.7 4.1 2.32.9 2.8.72 3.3.68.5-.05 1.62-.66 1.85-1.3.23-.64.23-1.19.16-1.3-.07-.12-.25-.19-.52-.32-.27-.14-1.62-.8-1.87-.89-.25-.09-.43-.13-.61.14-.18.27-.7.88-.86 1.06-.16.18-.32.2-.59.07-.27-.14-1.15-.42-2.19-1.35-.81-.72-1.35-1.61-1.51-1.88-.16-.27-.02-.42.12-.55.12-.12.27-.32.4-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.13-.6-1.48-.83-2.03-.22-.53-.44-.46-.61-.47l-.52-.01Z"/></symbol>
<symbol id="i-facebook" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5.02 3.66 9.18 8.44 9.94v-7.03H7.9v-2.9h2.54V9.85c0-2.52 1.5-3.91 3.77-3.91 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.45 2.9h-2.33V22c4.78-.76 8.44-4.92 8.44-9.94Z"/></symbol>
<symbol id="i-instagram" viewBox="0 0 24 24" {S}><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></symbol>
</svg>'''

# ------------------------------------------------------------------ content

SERVICES = [
    dict(slug='freight-forwarding', photo='reach-stacker', alt='A reach stacker lifts a red container from a ship onto a waiting truck at the quay.', icon='ship', title='Freight Forwarding', short='Freight forwarding',
         blurb='We coordinate the movement of your cargo across every mode of transport, choosing the route and carrier that fit your budget and your deadline.',
         detail='Whether it is a single air consignment or a regular container flow, we compare routes and carriers across modes, book the space, and keep you informed until the cargo arrives.',
         bullets=['Air, sea, road and rail transportation', 'Route optimisation and carrier coordination',
                  'Shipment tracking and global shipping support'],
         tags=['Air', 'Sea', 'Road', 'Rail']),
    dict(slug='customs-brokerage', photo='customs-counter', alt='A clearing agent hands a stack of documents to a customs officer across the counter.', icon='shield', title='Customs Brokerage', short='Customs clearing',
         blurb='Customs is where shipments stall. We prepare, file and follow through on your entries so cargo clears without avoidable delay or penalty.',
         detail='We prepare and file your import and export entries, work out and process the duties and taxes due, and make sure each consignment meets local and international requirements.',
         bullets=['Import and export documentation', 'Duty and tax processing',
                  'Regulatory compliance with local and international laws'],
         tags=['Import', 'Export', 'Duties & taxes']),
    dict(slug='documentation', photo='gate-check', alt='An inspector with a clipboard checks a container truck’s papers at a terminal gate.', icon='doc', title='Documentation Services', short='Documentation',
         blurb='Every shipment carries a paper trail. We prepare it correctly the first time and manage it from booking through to final delivery.',
         detail='Commercial invoices, bills of lading, certificates of origin and packing lists — prepared, checked against one another and managed end to end, so the paperwork never holds up the cargo.',
         bullets=['Commercial invoices and bills of lading', 'Certificates of origin and packing lists',
                  'End-to-end documentation management'],
         tags=['B/L', 'Invoice', 'COO', 'Packing list']),
    dict(slug='supply-chain', photo='warehouse-aisle', alt='Two staff review stock on a tablet in a racked warehouse aisle as a forklift moves a pallet.', icon='chain', title='Supply Chain Management', short='Supply chain',
         blurb='Beyond single shipments, we help you plan the flow of goods — how much to hold, where to hold it and how it reaches your customers.',
         detail='For clients moving goods regularly, we look past the individual shipment: planning flows, advising on stock and coordinating warehousing and distribution so goods are where you need them.',
         bullets=['Logistics planning and advisory', 'Inventory control and coordination',
                  'Warehousing and distribution solutions'],
         tags=['Planning', 'Inventory', 'Warehousing']),
    dict(slug='specialised', photo='sealed-container', alt='A forklift loads wrapped pallets beside a container door closed with a yellow security seal.', icon='warehouse', title='Specialised Logistics', short='Specialised logistics',
         blurb='For cargo that needs more than a standard lane — goods held under bond, trades between third countries, and delivery to the final address.',
         detail='Some consignments need particular handling. We manage bonded storage while duties are pending, cross-trade movements that never touch Liberia, and the last mile to your door.',
         bullets=['Bonded warehousing', 'Cross-trade operations', 'Last-mile delivery solutions'],
         tags=['Bonded', 'Cross-trade', 'Last mile']),
    dict(slug='transportation', photo='highway-truck', alt='A white truck carrying an orange container on an open road lined with palm trees.', icon='truck', title='Transportation Services', short='Transportation',
         blurb='Reliable, flexible cargo delivery across Liberia and beyond, shaped around what you are carrying and when it needs to arrive.',
         detail='We arrange transport around your cargo, your route and your timetable — from a single delivery across Monrovia to regular movements inland and beyond the border.',
         bullets=['Reliable and flexible cargo delivery', 'Customised transport solutions based on client needs',
                  'Deliveries across Liberia and beyond'],
         tags=['Liberia', 'Regional', 'Door to door']),
]

MODES = [
    ('plane', 'Air freight', 'AIR', 'For urgent, high-value or time-critical consignments that cannot wait on a vessel.'),
    ('ship', 'Sea freight', 'SEA', 'Container cargo through the Freeport of Monrovia — the workhorse for volume.'),
    ('truck', 'Road transport', 'ROAD', 'Cargo delivery across Liberia and beyond, including the last mile to your door.'),
    ('train', 'Rail freight', 'RAIL', 'Heavy and bulk movements coordinated wherever the rail corridor supports them.'),
]

STEPS = [
    ('Enquiry & planning', 'Tell us what is moving, from where and by when. We weigh air, sea, road and rail and confirm the route, the carrier and the cost.'),
    ('Booking & documents', 'We book the space and prepare the paperwork — invoice, bill of lading, certificate of origin, packing list — before the cargo moves.'),
    ('Customs clearance', 'We file the entry, process duties and taxes and work through the regulatory requirements until your cargo is released.'),
    ('Delivery & handover', 'Warehousing where you need it, transport to the final address, and confirmation that everything arrived as expected.'),
]

ADVANTAGE = [
    ('Local market knowledge', 'A deep understanding of Liberia’s logistics landscape — its port, its routes and how things actually get done.'),
    ('Customs expertise', 'Real experience navigating customs procedures, duties and the documentation each entry demands.'),
    ('Integrated across modes', 'Air, sea, road and rail planned together, so a shipment never falls between two providers.'),
    ('Complex operations, handled', 'Efficient handling of complicated logistics — bonded storage, cross-trade and multi-leg moves included.'),
]

SEGMENTS = [
    ('rocket', 'Startups & growing enterprises', 'Professional logistics from your very first shipment, without building an in-house team.'),
    ('building', 'Established companies', 'A dependable partner for regular volumes, recurring routes and complex operations.'),
    ('swap', 'Importers & exporters', 'Clearing, duties and documentation handled in both directions, on every consignment.'),
    ('globe', 'NGOs & international organisations', 'Careful, compliant handling of programme supplies into and across Liberia.'),
]

VALUES = [
    ('star', 'Excellence', 'Delivering high-quality services consistently, on every shipment we handle.'),
    ('handshake', 'Integrity', 'Operating with transparency and professionalism — in our pricing and our paperwork alike.'),
    ('clock', 'Reliability', 'Ensuring dependable and timely service delivery, so your plans hold.'),
]

MISSION = 'To ensure the smooth, efficient and timely transportation of goods and services, delivering consistent value and reliability to our clients.'
VISION = 'To become a leading logistics provider in Liberia and beyond, recognised for transforming logistics operations through innovation, efficiency and excellence in service delivery.'

FAQ = [
    ('What does Peak Logistics Services do?',
     'We are a full-service logistics company based in Monrovia. We handle freight forwarding by air, sea, road and rail, customs brokerage, shipping documentation, supply chain management, specialised logistics such as bonded warehousing and cross-trade, and transportation across Liberia and beyond.'),
    ('Can you clear my goods through customs in Liberia?',
     'Yes. Our customs brokerage service covers import and export documentation, duty and tax processing, and compliance with local and international regulations — we prepare and file the entry and follow it through until your cargo is released.'),
    ('Which documents will I need to ship?',
     'Most shipments need a commercial invoice, a bill of lading (or air waybill), a certificate of origin and a packing list, though the exact set depends on the cargo and the route. We prepare, check and manage these for you as part of our documentation service.'),
    ('Do you offer warehousing?',
     'Yes — warehousing and distribution solutions as part of supply chain management, including inventory control, and bonded warehousing for goods held while duties are pending.'),
    ('Do you deliver outside Monrovia?',
     'Yes. Our transportation services deliver cargo across Liberia and beyond, including last-mile delivery to the final address.'),
    ('Who do you work with?',
     'Businesses of all sizes: startups and growing enterprises, established companies, importers and exporters, and NGOs and international organisations.'),
    ('How do I get a quote?',
     'Use the quote form on our <a href="contact.html">contact page</a>, message us on WhatsApp, or call +231 886 826 289. Tell us what you are shipping, where it is coming from and going to, and when it needs to arrive.'),
    ('Where is your office?',
     'Opposite the Freeport of Monrovia, behind the CONEX gas station, on Bushrod Island, Monrovia.'),
]

NAV = [('index.html', 'Home'), ('services.html', 'Services'), ('about.html', 'About'), ('contact.html', 'Contact')]

# ------------------------------------------------------------------ chrome

def head(title, desc, path, jsonld=(), noindex=False):
    canon = SITE + '/' if path == 'index.html' else f'{SITE}/{path}'
    ld = ''.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>\n' for x in jsonld)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    return f'''<!DOCTYPE html>
<html lang="en-LR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
{robots}<meta name="theme-color" content="#061c13">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Peak Logistics Services">
<meta property="og:locale" content="en_LR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add('js');</script>
{ld}</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
{SPRITE}
'''

def header(cur):
    CUR = ' aria-current="page"'
    links = '\n'.join(f'      <a href="{h}"{CUR if h == cur else ""}>{l}</a>' for h, l in NAV)
    return f'''<div class="util">
  <div class="wrap">
    <ul>
      <li><a href="tel:{TEL}">{ico("phone")}{TEL_H}</a></li>
      <li><a href="mailto:{EMAIL}">{ico("mail")}{EMAIL}</a></li>
    </ul>
    <ul>
      <li><a href="contact.html#map">{ico("pin")}Bushrod Island, Monrovia</a></li>
      <li><a href="{FB}" rel="noopener" aria-label="Facebook">{ico("facebook")}</a></li>
      <li><a href="{IG}" rel="noopener" aria-label="Instagram">{ico("instagram")}</a></li>
    </ul>
  </div>
</div>
<header class="hdr">
  <div class="wrap hdr__bar">
    <a class="brand" href="index.html" aria-label="Peak Logistics Services, home">
      <img src="assets/img/logo-mark.png" width="280" height="141" alt="" decoding="async">
      <span class="brand__txt">
        <span class="brand__name"><b>PEAK</b> LOGISTICS</span>
        <span class="brand__sub">Services · Liberia</span>
      </span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
{links}
      <div class="nav__extra">
        <a class="btn btn--gold" href="contact.html#quote">Get a quote {ico("arrow", "arr")}</a>
        <a class="btn btn--line-dark" href="{WA}" rel="noopener">{ico("whatsapp")} WhatsApp {TEL_H}</a>
      </div>
    </nav>
    <a class="hdr__tel" href="tel:{TEL}"><span>{ico("phone")}</span><span>{TEL_H}</span></a>
    <a class="btn btn--gold hdr__cta" href="contact.html#quote">Get a quote {ico("arrow", "arr")}</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu">
      {ico("menu", "i-m")}{ico("close", "i-x")}
    </button>
  </div>
</header>
'''

def footer():
    svc = '\n'.join(f'          <li><a href="services.html#{s["slug"]}">{s["title"]}</a></li>' for s in SERVICES)
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__about">
        <a class="ftr__brand" href="index.html">
          <img src="assets/img/logo-mark.png" width="280" height="141" alt="" loading="lazy" decoding="async">
          <span class="brand__txt"><span class="brand__name"><b>PEAK</b> LOGISTICS</span><span class="brand__sub">Services · Liberia</span></span>
        </a>
        <p>A full-service logistics company moving cargo by air, sea, road and rail — with customs and documentation handled end to end.</p>
        <ul class="socials">
          <li><a href="{FB}" rel="noopener" aria-label="Peak Logistics Services on Facebook">{ico("facebook")}</a></li>
          <li><a href="{IG}" rel="noopener" aria-label="Peak Logistics Services on Instagram">{ico("instagram")}</a></li>
          <li><a href="{WA}" rel="noopener" aria-label="Message Peak Logistics Services on WhatsApp">{ico("whatsapp")}</a></li>
        </ul>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
{svc}
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="about.html#mission">Mission &amp; vision</a></li>
          <li><a href="about.html#values">Core values</a></li>
          <li><a href="index.html#faq">FAQ</a></li>
          <li><a href="contact.html#quote">Request a quote</a></li>
          <li><a href="{PDF}">Company profile (PDF)</a></li>
        </ul>
      </div>
      <div>
        <h2>Office</h2>
        <address>{ADDR_HTML}</address>
        <ul style="margin-top:1.1rem">
          <li><a href="tel:{TEL}">{TEL_H}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{IG}" rel="noopener">@peaklogisticsservices</a></li>
        </ul>
      </div>
    </div>
    <svg class="ftr__big" viewBox="0 0 1200 128" aria-hidden="true" focusable="false"><text x="2" y="122" textLength="1196" lengthAdjust="spacingAndGlyphs"><tspan>PEAK</tspan> LOGISTICS</text></svg>
    <div class="ftr__bottom">
      <p>&copy; <span data-year>2026</span> Peak Logistics Services. All rights reserved. <span class="ftr__credit">Powered by <a href="https://tolbertinnovationhub.org" rel="noopener">Tolbert Innovation Hub</a>.</span></p>
      <p class="tagline">{TAGLINE}</p>
    </div>
  </div>
</footer>
<a class="wa-fab is-hidden" href="{WA}" rel="noopener" aria-label="Chat with Peak Logistics Services on WhatsApp">{ico("whatsapp")}<span>WhatsApp us</span></a>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''

def tag(n, label):
    return f'<p class="tag"><b>[{n}]</b> {label}</p>' if n else f'<p class="tag">{label}</p>'

def phero(crumb, t, title, lead, extra='', photo=None, pos='70% 50%'):
    bg = (f'\n    <div class="phero__bg" style="--pos:{pos}" aria-hidden="true">{pic(photo, "", "100vw", eager=True)}</div>'
          if photo else '')
    cls = 'phero phero--photo' if photo else 'phero'
    return f'''  <section class="{cls}">{bg}
    <div class="wrap">
      <ol class="crumbs"><li><a href="index.html">Home</a></li><li aria-current="page">{crumb}</li></ol>
      <h1 class="h1">{title}</h1>
      <p class="lead">{lead}</p>{extra}
    </div>
  </section>
'''

def cta_block():
    return f'''  <section class="sec sec--paper">
    <div class="wrap">
      <div class="cta on-dark rv">
        <div>
          {tag("", "Get in touch")}
          <h2 class="h2">Ready when your cargo is.</h2>
          <p class="lead">Tell us what you are moving and where it needs to go. We will come back with the route, the documents required and a quote.</p>
        </div>
        <div class="channels">
          <a class="channel channel--wa" href="{WA}" rel="noopener"><span class="channel__i">{ico("whatsapp")}</span><span><b>WhatsApp</b><small>{TEL_H}</small></span>{ico("ne")}</a>
          <a class="channel" href="tel:{TEL}"><span class="channel__i">{ico("phone")}</span><span><b>Call us</b><small>{TEL_H}</small></span>{ico("ne")}</a>
          <a class="channel" href="mailto:{EMAIL}"><span class="channel__i">{ico("mail")}</span><span><b>Email</b><small>{EMAIL}</small></span>{ico("ne")}</a>
          <a class="channel" href="contact.html#quote"><span class="channel__i">{ico("box")}</span><span><b>Request a quote</b><small>Four quick steps</small></span>{ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>
'''

def business_ld():
    return {
        '@context': 'https://schema.org', '@type': 'LocalBusiness',
        '@id': SITE + '/#business',
        'name': 'Peak Logistics Services', 'slogan': TAGLINE,
        'description': 'Full-service logistics company in Monrovia, Liberia: freight forwarding by air, sea, road and rail, customs brokerage, documentation, supply chain management, specialised logistics and transportation.',
        'url': SITE + '/', 'logo': SITE + '/assets/img/logo-mark.png', 'image': SITE + '/assets/img/og-card.jpg',
        'telephone': TEL, 'email': EMAIL,
        'address': {'@type': 'PostalAddress',
                    'streetAddress': 'Opposite Freeport of Monrovia, Behind CONEX Gas Station, Bushrod Island',
                    'addressLocality': 'Monrovia', 'addressCountry': 'LR'},
        'areaServed': {'@type': 'Country', 'name': 'Liberia'},
        'sameAs': [FB, IG],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Logistics services',
            'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['title'], 'description': s['blurb']}} for s in SERVICES]},
    }

def crumbs_ld(name, path):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': name, 'item': f'{SITE}/{path}'}]}

def write(path, text):
    with open(ROOT + path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'wrote {path:14} {len(text):>7,} bytes')
