# Peak Logistics Services — website

The website for **Peak Logistics Services**, a full-service logistics company based
opposite the Freeport of Monrovia, Bushrod Island, Monrovia, Liberia.

> Your Cargo, Our Commitment. Reaching New Heights in Liberia.

All copy comes from the company profile, and the greens and golds are sampled from the
company's own logo and banner. The figures on the homepage (years of experience,
on-time rate, shipments and so on) were supplied by the company.

## Pages

| Page | What's on it |
| --- | --- |
| `index.html` | Hero with a shipment walkthrough, interactive services explorer, world route map converging on Monrovia, the scroll-driven journey road, customs & documentation, why Peak, who we serve, mission & vision, FAQ |
| `services.html` | Each of the six service lines in full, documentation, transport modes, how a shipment is handled |
| `about.html` | Introduction, mission, vision, core values, strategic advantage, target market, looking ahead, company profile download |
| `contact.html` | Four-step quote request (sent by WhatsApp or email), direct contact details, map |
| `404.html` | Not-found page |

## Previewing it

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000     # then visit http://localhost:8000
```

## Changing the content

The pages are **generated** — edit the source, not the HTML:

| To change… | Edit |
| --- | --- |
| Phone, email, address, social links | the constants at the top of `tools/common.py` |
| Services, FAQ, values, mission, segments | the lists in `tools/common.py` |
| Homepage figures (10+ years, 98% on time…) | `STATS` in `tools/common.py` — keep them current |
| Header, footer, calls to action | the functions in `tools/common.py` |
| Page layouts and sections | `tools/build.py` |
| Colours, type, spacing | the `:root` block at the top of `assets/css/style.css` |
| Photographs | see *Photos* below |

Then rebuild:

```sh
python3 tools/build.py
```

It needs only Python 3 — no packages. Commit the regenerated `.html` files along with
your change. **Edits made directly to the HTML are overwritten on the next build.**

### Photos

Originals live in `tools/images/masters/`. `tools/images/process.py` crops each one
and writes WebP and JPEG copies at phone and desktop sizes into `assets/img/photos/` —
the JPEGs are for older phones and feature phones that cannot show WebP. It also draws
`assets/img/og-card.jpg`, the preview shown when the site is shared on WhatsApp or
Facebook. To swap a photo, save the new one over the master with the same name (or add
one and reference it in `tools/common.py`), then:

```sh
pip install Pillow
python3 tools/images/process.py && python3 tools/build.py
```

The dot-matrix world map is generated separately and rarely needs touching. To change
the trade lanes shown on it: `cd tools/map && npm install && node generate-map.mjs`,
then run the build.

## Before it goes live

1. **Point the domain at the site.** The site is set up for
   `https://peaklogisticsservices.com` — see *Pointing peaklogisticsservices.com at the
   site* below. To use a different domain, change `SITE` in `tools/common.py`, the URLs
   in `robots.txt` and `sitemap.xml`, and rebuild.

2. **Switch email over once the company mailboxes work.** The site lists
   Info@, CEO@ and Jallabah.JamesK@peaklogisticsservices.com, but those addresses can
   only receive mail after the domain is registered and email hosting is set up for it
   (for example Google Workspace, Zoho Mail or your registrar's email). Until then the
   quote form, the email buttons and the top bar send to the Gmail address, which is
   also still listed. When the new mailboxes are working, set
   `EMAIL = 'Info@peaklogisticsservices.com'` in `tools/common.py` and rebuild; the Gmail
   address then drops off the lists automatically. Test by sending an email to each
   address first.

3. **Decide how quote requests arrive.** The site has no server, so the quote form
   writes the request out and hands it to the visitor's **WhatsApp** or **email app**,
   addressed to the company — the visitor just presses send. Nothing is stored on the
   site. With JavaScript switched off it falls back to a plain email form.
   To capture submissions on a server instead, point `#quote-form` at a form service
   such as [Formspree](https://formspree.io) and remove the send buttons' handler at
   the end of `assets/js/main.js`.

4. **Swap in your own photographs over time.** The current set is illustrative; the
   captions describe what is shown rather than calling it "our team" or "our
   warehouse". Genuine photos of your own
   trucks, yard, staff and office will still build the most trust — replace the
   masters one at a time as you take them (landscape, at least 1400px wide).

5. **Keep the figures true, and add more proof as you gather it.** The homepage
   figures are in `STATS` in `tools/common.py`; update them as they change (for example,
   500+ shipments). Client testimonials, partner logos and licences would strengthen the
   site further.

6. **Opening hours** were not in the profile either, so none are published.

7. **Map pin.** The contact-page map marks the Freeport of Monrovia and is labelled
   as approximate. For the exact office, change the `marker=` coordinates in
   `tools/build.py` and rebuild.

8. **Social links** point to `facebook.com/peaklogisticsservices` and
   `instagram.com/peaklogisticsservices`, based on the `@peaklogisticsservices` handle.
   Correct `FB` and `IG` in `tools/common.py` if the real pages differ.

## Publishing

Any static host serves this folder as-is — GitHub Pages, Netlify, Cloudflare Pages, or
ordinary cPanel hosting over FTP.

For **GitHub Pages**: repository *Settings → Pages*, set the source to this branch and
the folder to `/ (root)`. No workflow or configuration file is needed.

### Pointing peaklogisticsservices.com at the site

The site's canonical URLs, share cards and sitemap are all set to
`https://peaklogisticsservices.com` (no `www`), so serve it from that exact host — if
you also want `www.peaklogisticsservices.com` to work, redirect it to the bare domain
rather than serving both, or search engines will treat them as two competing copies.

On **GitHub Pages** a custom domain needs two things:

1. At your domain registrar, create these DNS records for the bare domain:

   ```
   A     @   185.199.108.153
   A     @   185.199.109.153
   A     @   185.199.110.153
   A     @   185.199.111.153
   CNAME www tolbertinnovation-debug.github.io.
   ```

2. In the repository, *Settings → Pages → Custom domain*, enter
   `peaklogisticsservices.com` and save. GitHub commits a `CNAME` file to the branch
   for you — do not add one by hand. Once DNS resolves, tick **Enforce HTTPS**; the
   certificate can take up to an hour to issue.

On **Netlify, Cloudflare Pages or cPanel** hosting, add the domain in that host's own
dashboard instead — the `CNAME` file is a GitHub Pages mechanism and is ignored
elsewhere.

## Layout

```
├── index.html, services.html, about.html, contact.html, 404.html   (generated)
├── assets/
│   ├── css/style.css       design system — tokens at the top
│   ├── js/main.js          menu, services explorer, route map, journey road, quote form
│   ├── fonts/              Archivo and JetBrains Mono, self-hosted (SIL OFL)
│   ├── img/                logo, world map, share card, icons
│   │   └── photos/         generated photo sizes (WebP + JPEG)
│   └── docs/               company profile PDF
├── tools/
│   ├── common.py           content and shared page parts
│   ├── build.py            page layouts; run this to rebuild
│   ├── photos.json         sizes of each generated photo
│   ├── images/             photo masters and the script that processes them
│   ├── map-points.json     where each trade lane starts and ends
│   └── map/                optional world-map generator (Node)
├── favicon.ico, robots.txt, sitemap.xml
```

## How it's built

- **Fast on mobile data.** The first screen of the homepage is about 415 KB, and the
  whole page, with nine photos, about 770 KB. Photos load only as they scroll into
  view, at a size matched to the screen. Fonts are self-hosted, so there are no third-party requests
  except the map on the contact page.
- **Works without JavaScript.** Every page reads completely with scripts off: the
  services explorer shows all six services, and the quote form becomes a single email
  form. Animations are disabled for visitors who ask for reduced motion.
- **Accessible.** One `<h1>` per page with no skipped heading levels, labelled form
  fields, keyboard-operable services tabs and menu, visible focus, a skip link, and
  colour contrast meeting WCAG AA throughout.
- **Responsive** from 320px to wide desktop, checked for horizontal overflow at eleven
  widths. On phones the route map zooms into the Atlantic so its labels stay readable.
- **Search-ready.** Structured data for the business, its services, the FAQ and
  breadcrumbs; canonical URLs; sitemap; social share card.

## Credits

- Typefaces: [Archivo](https://github.com/Omnibus-Type/Archivo) and
  [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono), SIL Open Font License —
  see `assets/fonts/`.
- World map: [Natural Earth](https://www.naturalearthdata.com/) data (public domain) via
  `world-atlas`.
- Contact-page map tiles © [OpenStreetMap](https://www.openstreetmap.org/copyright)
  contributors.
