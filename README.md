# Peak Logistics Services — company website

A static marketing website for **Peak Logistics Services**, a full-service logistics
company based opposite the Freeport of Monrovia, Bushrod Island, Monrovia, Liberia.

All copy, services, mission, vision, values and contact details come from the company
profile document; the palette and imagery are taken from the company's own logo, banner
and flyer artwork.

> Your Cargo, Our Commitment. Reaching New Heights in Liberia.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home — hero, service overview, strategic advantage, mission/vision/values, target market |
| `services.html` | The six service lines in detail, the four transport modes, and how a shipment is handled |
| `about.html` | Introduction, mission, vision, core values, target market, strategic advantage, looking ahead |
| `contact.html` | Contact details, enquiry form, and a map of the Bushrod Island area |
| `404.html` | Not-found page |

## Running it locally

There is **no build step and no dependencies** — it is plain HTML, CSS and one small
JavaScript file. Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Layout

```
├── index.html, services.html, about.html, contact.html, 404.html
├── assets/
│   ├── css/style.css        # all styling; brand tokens are the :root block at the top
│   ├── js/main.js           # nav, sticky header, scroll reveals, enquiry form
│   ├── img/                 # logo mark, favicons, photography, brand collateral
│   └── docs/                # company profile PDF, linked from the About page
├── favicon.ico, robots.txt, sitemap.xml
```

## Before it goes live

1. **Point the domain at the site.** The site is set up for
   `https://peaklogisticsservices.com` — that host appears in the canonical URLs, the
   social-share cards, `robots.txt` and `sitemap.xml`. Register the domain if you have
   not already, then follow *Pointing peaklogisticsservices.com at the site* under
   **Publishing** below.

   If the domain ever changes, search and replace `peaklogisticsservices.com` across
   `index.html`, `services.html`, `about.html`, `contact.html`, `404.html`,
   `robots.txt` and `sitemap.xml`. Nothing on the page breaks if it is wrong, but
   search engines and link previews will point at the wrong host.

2. **Decide how enquiries are received.** The contact form is currently *client-side
   only*: it validates the fields and opens the visitor's own email app with everything
   filled in, addressed to `peaklogisticsservices@gmail.com`. Nothing is stored on the
   site, and it needs no server. It also means a visitor with no mail app configured
   will fall back to the phone and WhatsApp links shown beneath the form.

   To collect submissions properly instead, point the form at a form service — for
   example [Formspree](https://formspree.io) or Netlify Forms — by giving
   `#enquiry-form` an `action` and `method="POST"` and deleting the submit handler at
   the bottom of `assets/js/main.js`. The field names (`name`, `company`, `email`,
   `phone`, `service`, `route`, `message`) are already sensible.

3. **Add opening hours.** These were not in the company profile, so none are published.
   If you want them, add another `.contact-item` block to `contact.html`.

4. **Check the map pin.** The embedded map is centred on the Freeport of Monrovia area
   and is labelled as approximate. For an exact pin, replace the `marker=` coordinates
   in the `iframe` on `contact.html` with the office's real latitude and longitude.

5. **Confirm the social links.** The footer links to
   `facebook.com/peaklogisticsservices` and `instagram.com/peaklogisticsservices`, based
   on the `@peaklogisticsservices` handle in the company profile. Correct them if the
   real page URLs differ.

## Publishing

Any static host will serve this folder as-is — GitHub Pages, Netlify, Cloudflare Pages,
or ordinary cPanel hosting via FTP.

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

## Editing content

- **Text and services** live directly in the HTML. The six service cards use the same
  markup on `index.html` and `services.html`, so edit both if a service changes.
- **Navigation and footer** are repeated in each page (this keeps the site dependency
  free). Changing a nav link means changing it in all five files.
- **Colours, spacing and type** are CSS custom properties in the `:root` block at the
  top of `assets/css/style.css`. The greens and golds were sampled from the company
  logo and banner.

## Notes on the build

- **Accessibility** — skip link, one `<h1>` per page with no heading-level jumps,
  labelled form fields, visible focus rings, and colour contrast meeting WCAG AA. Gold
  is used as a decorative fill; gold *text* on light backgrounds uses the darker
  `--gold-ink` so it stays legible.
- **Works without JavaScript** — the scroll-reveal animation is scoped to a `.js` class
  so content is never hidden if scripts fail to load. Motion is disabled for visitors
  who set `prefers-reduced-motion`.
- **Responsive** — verified for horizontal overflow from 320px to 1920px.
- **Manrope** is loaded from Google Fonts with `display=swap` and falls back to the
  system UI font, so text renders immediately on a slow connection. To remove the
  third-party request entirely, delete the two `fonts.` `<link>` tags from each page's
  `<head>`; the fallback stack takes over.
