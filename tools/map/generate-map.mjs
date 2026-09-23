// Generates assets/img/world-dots.svg (the dot-matrix world map) and
// tools/map-points.json (where each trade lane starts and ends).
//   cd tools/map && npm install && node generate-map.mjs && python3 ../build.py
// Map data: Natural Earth via the world-atlas package (public domain).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const nm = (p) => path.join(here, 'node_modules', p);
import { feature } from 'topojson-client';
import { geoNaturalEarth1, geoContains } from 'd3-geo';

const land  = JSON.parse(fs.readFileSync(nm('world-atlas/land-50m.json')));
const ctry  = JSON.parse(fs.readFileSync(nm('world-atlas/countries-50m.json')));
const landF = feature(land, land.objects.land);
const countries = feature(ctry, ctry.objects.countries);
const liberia = countries.features.find(f => f.id === '430');
if (!liberia) throw new Error('Liberia not found');

const W = 1600, H = 820;
// Centre the Atlantic so the lanes into West Africa sit mid-frame.
const proj = geoNaturalEarth1().rotate([-8, 0]).fitExtent([[0, 0], [W, H]], { type: 'Sphere' });

const STEP = 8.5;
const rows = [];
const gold = [];
let minY = Infinity, maxY = -Infinity, n = 0;
for (let y = STEP / 2; y < H; y += STEP) {
  const row = [];
  for (let x = STEP / 2; x < W; x += STEP) {
    const ll = proj.invert([x, y]);
    if (!ll || !isFinite(ll[0])) continue;
    if (ll[1] < -57) continue;                    // drop Antarctica
    if (!geoContains(landF, ll)) continue;
    const px = +x.toFixed(1), py = +y.toFixed(1);
    if (geoContains(liberia, ll)) gold.push([px, py]); else row.push(px);
    minY = Math.min(minY, py); maxY = Math.max(maxY, py); n++;
  }
  if (row.length) rows.push([+y.toFixed(1), row]);
}

// Relative path commands: rows of "m8.5 0h0" repeat and gzip to almost nothing.
const dPath = rows.map(([y, xs]) => {
  let s = `M${xs[0]} ${y}h0`;
  for (let i = 1; i < xs.length; i++) s += `m${+(xs[i] - xs[i - 1]).toFixed(1)} 0h0`;
  return s;
}).join('');
const gPath = gold.map(([x, y]) => `M${x} ${y}h0`).join('');

const pad = 12;
const vb = [0, Math.floor(minY - pad), W, Math.ceil(maxY - minY + pad * 2)];

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.join(' ')}" width="${vb[2]}" height="${vb[3]}">` +
  `<path d="${dPath}" fill="none" stroke="#7cc39c" stroke-opacity=".34" stroke-width="3.3" stroke-linecap="round"/>` +
  `<path d="${gPath}" fill="none" stroke="#f0c000" stroke-width="4.6" stroke-linecap="round"/>` +
  `</svg>`;
fs.writeFileSync(path.join(here, '../../assets/img/world-dots.svg'), svg);

// Anchor points for the route overlay, in the same coordinate space.
const P = (lon, lat) => proj([lon, lat]).map(v => +v.toFixed(1));
const points = {
  viewBox: vb,
  monrovia:  P(-10.806, 6.345),
  asia:      P(121.47, 31.23),     // Shanghai
  middleEast:P(55.06, 25.01),      // Jebel Ali
  europe:    P(4.14, 51.95),       // Rotterdam
  americas:  P(-74.0, 40.7),       // New York
  southAm:   P(-46.33, -23.96),    // Santos
  westAfrica:P(3.39, 6.45),        // Lagos
};
fs.writeFileSync(path.join(here, '../map-points.json'), JSON.stringify(points, null, 1));
console.log('dots:', n, 'liberia dots:', gold.length, 'viewBox:', vb.join(' '));
console.log('svg bytes:', svg.length);
console.log(points);
