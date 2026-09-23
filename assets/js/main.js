/* Peak Logistics Services — site behaviour.
   Progressive enhancement throughout: every page is complete and usable with
   JavaScript off. Nothing here is required to read the site or to get in touch. */
(function () {
  'use strict';

  var doc = document;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var io = 'IntersectionObserver' in window;

  function onView(els, cb, opts) {
    if (!els.length) return;
    if (!io) { els.forEach(cb); return; }
    var ob = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { cb(e.target); ob.unobserve(e.target); } });
    }, opts || { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    els.forEach(function (el) { ob.observe(el); });
  }

  /* ------------------------------------------------------------- Menu */
  var burger = $('.burger');
  var nav = $('#nav');
  var menuOpen = false;
  if (burger && nav) {
    // Everything outside the header is made inert while the menu is open, so keyboard
    // and screen-reader focus stays inside the menu.
    var behind = $$('.util, main, .ftr, .wa-fab');
    var setMenu = function (open) {
      menuOpen = open;
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.classList.toggle('is-open', open);
      doc.body.classList.toggle('nav-open', open);
      behind.forEach(function (el) { el.inert = open; });
      syncHeader();
    };
    burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') { setMenu(false); burger.focus(); }
    });
    var wide = window.matchMedia('(min-width: 901px)');
    var reset = function (m) { if (m.matches) setMenu(false); };
    wide.addEventListener ? wide.addEventListener('change', reset) : wide.addListener(reset);
  }

  /* ------------------------------------------------- Header & WA button */
  var hdr = $('.hdr');
  var fab = $('.wa-fab');
  var top = $('.hero, .phero');
  var ftr = $('.ftr');
  var heroOut = !top, ftrIn = false;

  // The header stays dark while the menu is open so the two read as one panel.
  function syncHeader() {
    if (hdr) hdr.classList.toggle('is-solid', window.scrollY > 24 && !menuOpen);
  }
  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  if (fab && io) {
    var fabSync = function () { fab.classList.toggle('is-hidden', !heroOut || ftrIn); };
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.target === top) heroOut = !e.isIntersecting;
        if (e.target === ftr) ftrIn = e.isIntersecting;
      });
      fabSync();
    }, { threshold: 0 }).observe(top || ftr);
    if (top && ftr) new IntersectionObserver(function (es) {
      ftrIn = es[0].isIntersecting; fabSync();
    }).observe(ftr);
    fabSync();
  }

  /* --------------------------------------------------------- Reveals */
  var rv = $$('.rv');
  if (reduced) rv.forEach(function (el) { el.classList.add('in'); });
  else onView(rv, function (el) { el.classList.add('in'); });

  /* ------------------------------------------ Hero: shipment walkthrough */
  var jc = $$('.jc-steps li');
  if (jc.length) {
    var paint = function (n) {
      jc.forEach(function (li, i) {
        li.classList.toggle('is-done', i < n);
        li.classList.toggle('is-now', i === n);
      });
    };
    if (reduced) paint(jc.length);
    else {
      var step = 0;
      paint(0);
      setInterval(function () {
        step = (step + 1) % (jc.length + 2);   // pause briefly on "all done"
        paint(Math.min(step, jc.length));
      }, 1500);
    }
  }

  /* ------------------------------------------------ Services explorer */
  $$('.svx').forEach(function (svx) {
    var tabs = $$('.svx__tab', svx);
    var panels = $$('.svp', svx);
    var list = $('.svx__tabs', svx);
    if (!tabs.length || tabs.length !== panels.length) return;
    var mq = window.matchMedia('(min-width: 960px)');
    var current = 0;

    function select(i, focus) {
      current = i;
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      if (focus) tabs[i].focus();
    }

    function mode() {
      if (mq.matches) {
        svx.classList.add('is-tabbed');
        list.setAttribute('role', 'tablist');
        list.setAttribute('aria-orientation', 'vertical');
        tabs.forEach(function (t, j) {
          t.setAttribute('role', 'tab');
          t.setAttribute('aria-controls', panels[j].id);
          panels[j].setAttribute('role', 'tabpanel');
          panels[j].setAttribute('aria-labelledby', t.id);
          panels[j].tabIndex = 0;
        });
        select(current);
      } else {
        svx.classList.remove('is-tabbed');
        list.removeAttribute('role');
        tabs.forEach(function (t, j) {
          t.removeAttribute('role');
          panels[j].removeAttribute('role');
          panels[j].removeAttribute('tabindex');
          panels[j].hidden = false;
        });
      }
    }

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = tabs.length, to = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') to = (i + 1) % n;
        else if (k === 'ArrowUp' || k === 'ArrowLeft') to = (i - 1 + n) % n;
        else if (k === 'Home') to = 0;
        else if (k === 'End') to = n - 1;
        if (to !== null) { e.preventDefault(); select(to, true); }
      });
    });
    mq.addEventListener ? mq.addEventListener('change', mode) : mq.addListener(mode);
    mode();
  });

  /* -------------------------------------------------------- Route map */
  $$('.netmap').forEach(function (map) {
    $$('.arc', map).forEach(function (p, i) {
      var len = Math.ceil(p.getTotalLength());
      p.style.setProperty('--len', len);
      p.style.setProperty('--d', (i * 0.22) + 's');
    });
    var go = function () {
      map.classList.add('is-live');
      if (reduced) return;
      $$('animateMotion', map).forEach(function (a, i) {
        setTimeout(function () { try { a.beginElement(); } catch (e) {} }, 2200 + i * 350);
      });
    };
    onView([map], go, { threshold: 0.25 });
  });

  /* ----------------------------------------------------- Journey road */
  $$('.jr').forEach(function (jr) {
    var stops = $$('.stop', jr);
    var pins = $$('.jr__pins li', jr);
    var n = stops.length;
    function set(p) {
      jr.style.setProperty('--p', p.toFixed(4));
      stops.forEach(function (s, i) {
        var on = p >= (i + 0.5) / n - 0.14;
        s.classList.toggle('is-on', on);
        if (pins[i]) pins[i].classList.toggle('is-on', on);
      });
    }
    if (reduced) { set(1); return; }
    var ticking = false;
    function update() {
      ticking = false;
      var r = jr.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = (vh * 0.78 - r.top) / (r.height + vh * 0.28);
      set(Math.max(0, Math.min(1, p)));
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  /* ---------------------------------------------------- Document stack */
  onView($$('.docs'), function (el) { el.classList.add('is-live'); }, { threshold: 0.4 });

  /* -------------------------------------------------------------- Year */
  $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ----------------------------------------------------- Quote wizard
     The site is static, so there is no server to post to. The finished
     request is handed to WhatsApp or the visitor's email app, already
     written. Without JavaScript the form falls back to a plain mailto post. */
  var form = $('#quote-form');
  if (!form) return;

  var PHONE = form.dataset.wa;          // international format, digits only
  var EMAIL = form.dataset.email;
  var steps = $$('fieldset[data-step]', form);
  var marks = $$('.wiz__steps li');
  var status = $('#wiz-status');
  var at = 0;

  form.setAttribute('novalidate', '');
  form.removeAttribute('action');

  // Prefill from ?service=<slug>, used by the "Request a quote" links on each service.
  var want = new URLSearchParams(window.location.search).get('service');
  if (want) {
    var match = $('input[name="service"][data-slug="' + want.replace(/[^a-z-]/g, '') + '"]', form);
    if (match) match.checked = true;
  }

  function show(i, focus) {
    at = i;
    steps.forEach(function (fs, j) { fs.hidden = j !== i; });
    marks.forEach(function (m, j) {
      m.classList.toggle('is-on', j === i);
      m.classList.toggle('is-done', j < i);
      if (j === i) m.setAttribute('aria-current', 'step'); else m.removeAttribute('aria-current');
    });
    if (steps[i].dataset.step === 'review') fillReview();
    if (focus) {
      var lg = $('legend', steps[i]);
      lg.setAttribute('tabindex', '-1');
      lg.focus({ preventScroll: true });
      var box = form.closest('.wiz').getBoundingClientRect();
      if (box.top < 0 || box.top > window.innerHeight * 0.4) {
        window.scrollTo({ top: window.scrollY + box.top - 110, behavior: reduced ? 'auto' : 'smooth' });
      }
    }
  }

  function valid(fs) {
    var phone = form.elements.phone, email = form.elements.email;
    if (fs.contains(phone)) {
      var none = !phone.value.trim() && !email.value.trim();
      phone.setCustomValidity(none ? 'Enter a phone number or an email address so we can reply.' : '');
    }
    var fields = $$('input, select, textarea', fs);
    for (var i = 0; i < fields.length; i++) {
      if (!fields[i].checkValidity()) { fields[i].reportValidity(); return false; }
    }
    return true;
  }

  function val(name) {
    var el = form.elements[name];
    if (!el) return '';
    if (el instanceof RadioNodeList || (el.length && el[0] && el[0].type)) {
      var out = [];
      Array.prototype.forEach.call(el, function (x) { if (x.checked) out.push(x.value); });
      return out.join(', ');
    }
    return (el.value || '').trim();
  }

  function rows() {
    return [
      ['Service', val('service')],
      ['Transport', val('mode') || 'Not specified'],
      ['From', val('origin')],
      ['To', val('destination')],
      ['Cargo', val('cargo')],
      ['Weight / volume', val('size')],
      ['Ready date', val('ready')],
      ['Name', val('name')],
      ['Company', val('company')],
      ['Phone', val('phone')],
      ['Email', val('email')],
      ['Reply by', val('reply')]
    ].filter(function (r) { return r[1]; });
  }

  function fillReview() {
    var dl = $('#review');
    dl.textContent = '';
    rows().forEach(function (r) {
      var d = doc.createElement('div');
      var dt = doc.createElement('dt'); dt.textContent = r[0];
      var dd = doc.createElement('dd'); dd.textContent = r[1];
      d.appendChild(dt); d.appendChild(dd); dl.appendChild(d);
    });
  }

  function message() {
    return 'Quote request — Peak Logistics Services\n\n' +
      rows().map(function (r) { return r[0] + ': ' + r[1]; }).join('\n');
  }

  function done(how) {
    status.hidden = false;
    status.textContent = how === 'wa'
      ? 'WhatsApp should now be open with your request written out — just press send. If it did not open, message us on +231 886 826 289.'
      : 'Your email app should now be open with the request filled in — just press send. If nothing opened, email ' + EMAIL + '.';
    status.focus();
  }

  form.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-go]');
    if (!b) return;
    e.preventDefault();
    var go = b.dataset.go;
    if (go === 'next') { if (valid(steps[at])) show(at + 1, true); }
    else if (go === 'back') show(at - 1, true);
    else if (go === 'edit') show(0, true);
    else if (go === 'wa') {
      window.open('https://wa.me/' + PHONE + '?text=' + encodeURIComponent(message()), '_blank', 'noopener');
      done('wa');
    } else if (go === 'email') {
      done('email');
      window.location.href = 'mailto:' + EMAIL +
        '?subject=' + encodeURIComponent('Quote request: ' + val('service') + ' — ' + val('name')) +
        '&body=' + encodeURIComponent(message());
    }
  });

  // Enter in a text field moves forward rather than submitting a half-filled form.
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (steps[at].dataset.step !== 'review' && valid(steps[at])) show(at + 1, true);
  });

  show(0, false);
})();
