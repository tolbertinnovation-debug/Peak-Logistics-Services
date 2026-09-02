/* Peak Logistics Services — site behaviour.
   Everything here is progressive enhancement: the site is fully usable
   with JavaScript disabled. */
(function () {
  'use strict';

  /* ---------------------------------------------------- Mobile navigation */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');

  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    };

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) setOpen(false);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });

    // Reset the panel when we grow past the mobile breakpoint.
    var wide = window.matchMedia('(min-width: 901px)');
    var onChange = function (event) { if (event.matches) setOpen(false); };
    if (wide.addEventListener) wide.addEventListener('change', onChange);
    else if (wide.addListener) wide.addListener(onChange);
  }

  /* --------------------------------------------------- Sticky header cue */
  var header = document.querySelector('.site-header');
  if (header) {
    var syncHeader = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    syncHeader();
    window.addEventListener('scroll', syncHeader, { passive: true });
  }

  /* ------------------------------------------------- Reveal on first view */
  var reveals = document.querySelectorAll('.reveal');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reveals.length && !reduced && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    reveals.forEach(function (el) { observer.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* --------------------------------------------------------- Footer year */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());

  /* -------------------------------------------------------- Enquiry form
     The site is hosted as static files, so there is no server to post to.
     The form hands a fully composed message to the visitor's mail client.
     To collect submissions server-side instead, see README.md. */
  var form = document.getElementById('enquiry-form');
  if (!form) return;

  var status = document.getElementById('form-status');
  var mailbox = form.dataset.mailto || 'peaklogisticsservices@gmail.com';

  var value = function (name) {
    var field = form.elements[name];
    return field && field.value ? field.value.trim() : '';
  };

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    if (!form.reportValidity()) return;

    var name = value('name');
    var service = value('service') || 'General enquiry';

    var body = [
      'Name: ' + name,
      'Company: ' + (value('company') || '—'),
      'Email: ' + value('email'),
      'Phone: ' + (value('phone') || '—'),
      'Service required: ' + service,
      'Origin / destination: ' + (value('route') || '—'),
      '',
      'Shipment details:',
      value('message') || '—',
      '',
      '— Sent from peaklogisticsservices website'
    ].join('\r\n');

    var href = 'mailto:' + mailbox +
      '?subject=' + encodeURIComponent('Quote request: ' + service + ' — ' + name) +
      '&body=' + encodeURIComponent(body);

    // Show the fallback message first, so it is on screen even if the
    // visitor has no mail client registered to handle the hand-off.
    if (status) {
      status.hidden = false;
      status.textContent =
        'Opening your email app with the request ready to send. If nothing happens, ' +
        'email us directly at ' + mailbox + ' or call +231 886 826 289.';
      status.focus();
    }

    window.location.href = href;
  });
})();
