# AAA Smoke & Vape — Static Marketing Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page static marketing website for AAA Smoke & Vape Shop (Shoreline, WA) that drives foot traffic to the physical store — no e-commerce, no cart.

**Architecture:** Single `index.html` with external `css/style.css` and `js/main.js`. Age gate modal blocks all content on first visit; localStorage remembers the confirmation for 24h. All design tokens defined as CSS custom properties in `:root`.

**Tech Stack:** Plain HTML5, CSS3 (custom properties, flexbox, grid), vanilla JS, Google Fonts (Barlow Condensed + Nunito Sans), deployable to GitHub Pages or Vercel with zero config.

## Global Constraints

- Palette: `#000000` (black), `#1F150C` (espresso), `#412D15` (leather brown), `#E1DCC9` (cream), `#9E9581` (muted)
- Fonts: Barlow Condensed 700/800 (headings), Nunito Sans 400/600/700 (body)
- Border radius: `4px` everywhere — no exceptions
- No e-commerce: zero cart, zero checkout, zero "add to cart"
- Age gate required: blocks all content, uses localStorage `aaa_age_confirmed` with 24h expiry
- Must be responsive: 375px (mobile), 768px (tablet), 1280px (desktop)
- Must pass WCAG AA contrast: cream `#E1DCC9` on black `#000000` = 14.8:1 ✓, cream on espresso `#1F150C` = ~10:1 ✓
- No build step, no npm, no bundler — open `index.html` directly in browser to test
- Placeholder content used throughout (address, phone, hours) — easy to swap

---

### Task 1: Project scaffold + design tokens

**Files:**
- Create: `index.html`
- Create: `css/style.css`
- Create: `js/main.js`

**Interfaces:**
- Produces: HTML shell consumed by all later tasks; CSS token variables consumed by all style tasks

- [ ] **Step 1: Create `index.html` shell**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="AAA Smoke & Vape Shop — Shoreline, Washington. Best prices, knowledgeable staff, huge selection. Open 7 days.">
  <title>AAA Smoke & Vape Shop | Shoreline, WA</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <!-- Age gate injected by JS -->
  <div id="site-content" aria-hidden="true">
    <!-- Nav, main, footer go here in later tasks -->
  </div>
  <script src="js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create `css/style.css` with design tokens + reset**

```css
/* === TOKENS === */
:root {
  --black:    #000000;
  --espresso: #1F150C;
  --leather:  #412D15;
  --cream:    #E1DCC9;
  --muted:    #9E9581;
  --radius:   4px;
  --font-display: 'Barlow Condensed', sans-serif;
  --font-body:    'Nunito Sans', sans-serif;
  --max-w: 1200px;
  --pad-x: clamp(20px, 5vw, 48px);
}

/* === RESET === */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--black);
  color: var(--cream);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
img { display: block; max-width: 100%; }
a { color: inherit; text-decoration: none; }
button { cursor: pointer; font-family: inherit; border: none; background: none; }

/* === UTILITY === */
.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}
.container {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--pad-x);
}
```

- [ ] **Step 3: Create empty `js/main.js`**

```js
// AAA Smoke & Vape — main.js
// Age gate logic added in Task 2
```

- [ ] **Step 4: Open `index.html` in browser — verify blank black page loads with no console errors**

- [ ] **Step 5: Commit**

```bash
cd C:/Users/adyan/Repos/aaa-smoke-vape
git init
git add .
git commit -m "feat: scaffold — HTML shell, CSS tokens, JS entry"
```

---

### Task 2: Age gate modal

**Files:**
- Modify: `index.html` — add modal HTML before `#site-content`
- Modify: `css/style.css` — add modal styles
- Modify: `js/main.js` — add gate logic

**Interfaces:**
- Consumes: `--espresso`, `--leather`, `--cream`, `--muted`, `--radius` tokens from Task 1
- Produces: `aaa_age_confirmed` localStorage key (24h TTL) read by gate check on page load; `#site-content` toggled to `aria-hidden="false"` and `display: block` on confirm

- [ ] **Step 1: Add modal HTML inside `<body>` before `#site-content`**

```html
<div id="age-gate" role="dialog" aria-modal="true" aria-labelledby="age-gate-heading">
  <div class="age-gate__backdrop"></div>
  <div class="age-gate__card">
    <p class="age-gate__eyebrow">Age Verification</p>
    <h1 id="age-gate-heading" class="age-gate__heading">Are you 21<br>or older?</h1>
    <p class="age-gate__body">You must be 21+ to view this site. By entering you confirm you are of legal age in your jurisdiction.</p>
    <button class="btn btn--primary" id="age-confirm">Yes, I'm 21+</button>
    <button class="btn btn--ghost" id="age-deny">No, take me back</button>
  </div>
</div>
```

- [ ] **Step 2: Add modal + shared button styles to `css/style.css`**

```css
/* === AGE GATE === */
#age-gate {
  position: fixed; inset: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: center;
}
.age-gate__backdrop {
  position: absolute; inset: 0;
  background: rgba(0, 0, 0, 0.92);
}
.age-gate__card {
  position: relative; z-index: 1;
  background: var(--espresso);
  border: 1px solid var(--leather);
  border-top: 3px solid var(--cream);
  border-radius: var(--radius);
  padding: 36px 32px;
  text-align: center;
  max-width: 320px;
  width: calc(100% - 40px);
}
.age-gate__eyebrow {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  color: var(--cream);
  opacity: 0.6;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.age-gate__heading {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 800;
  color: var(--cream);
  text-transform: uppercase;
  line-height: 1.05;
  margin-bottom: 12px;
}
.age-gate__body {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 24px;
}

/* === BUTTONS === */
.btn {
  display: block;
  width: 100%;
  border-radius: var(--radius);
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 12px 0;
  transition: opacity 0.15s ease;
}
.btn:hover { opacity: 0.85; }
.btn:focus-visible { outline: 2px solid var(--cream); outline-offset: 2px; }
.btn--primary {
  background: var(--cream);
  color: var(--black);
  margin-bottom: 10px;
}
.btn--ghost {
  background: transparent;
  color: var(--muted);
  border: 1px solid var(--leather);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0;
}

/* Site content hidden until gate cleared */
#site-content { display: none; }
#site-content.visible { display: block; }
```

- [ ] **Step 3: Add age gate logic to `js/main.js`**

```js
const STORAGE_KEY = 'aaa_age_confirmed';
const TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

function isAgeConfirmed() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) return false;
  const { timestamp } = JSON.parse(stored);
  return Date.now() - timestamp < TTL_MS;
}

function showSite() {
  const gate = document.getElementById('age-gate');
  const content = document.getElementById('site-content');
  gate.style.display = 'none';
  content.classList.add('visible');
  content.removeAttribute('aria-hidden');
}

function initAgeGate() {
  if (isAgeConfirmed()) { showSite(); return; }

  document.getElementById('age-confirm').addEventListener('click', () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ timestamp: Date.now() }));
    showSite();
  });

  document.getElementById('age-deny').addEventListener('click', () => {
    window.location.href = 'https://www.google.com';
  });
}

document.addEventListener('DOMContentLoaded', initAgeGate);
```

- [ ] **Step 4: Test in browser**
  - Open `index.html` — age gate modal appears, site content hidden
  - Click "Yes, I'm 21+" — modal disappears, site content visible (currently blank)
  - Refresh — gate does NOT reappear (localStorage TTL active)
  - Open DevTools → Application → LocalStorage → delete `aaa_age_confirmed` → refresh → gate reappears
  - Click "No, take me back" → redirected to google.com

- [ ] **Step 5: Commit**

```bash
git add css/style.css js/main.js index.html
git commit -m "feat: age gate modal with 24h localStorage TTL"
```

---

### Task 3: Navigation

**Files:**
- Modify: `index.html` — add `<nav>` inside `#site-content`
- Modify: `css/style.css` — add nav styles

**Interfaces:**
- Consumes: `.container` utility, token variables
- Produces: sticky nav with logo, links, "Call Us" + "Directions" buttons visible on all sections

- [ ] **Step 1: Add nav HTML inside `#site-content`**

```html
<nav class="nav" aria-label="Main navigation">
  <div class="container nav__inner">
    <a href="#" class="nav__logo" aria-label="AAA Smoke and Vape home">
      AAA Smoke &amp; Vape
    </a>
    <ul class="nav__links" role="list">
      <li><a href="#products" class="nav__link">Products</a></li>
      <li><a href="#about" class="nav__link">About</a></li>
      <li><a href="#hours" class="nav__link">Hours</a></li>
      <li><a href="#contact" class="nav__link">Contact</a></li>
    </ul>
    <div class="nav__actions">
      <a href="tel:+12065550199" class="btn-nav btn-nav--outline">Call Us</a>
      <a href="https://maps.google.com/?q=123+Aurora+Ave+N+Shoreline+WA+98133"
         target="_blank" rel="noopener noreferrer"
         class="btn-nav btn-nav--primary">Directions</a>
    </div>
  </div>
</nav>
```

- [ ] **Step 2: Add nav styles to `css/style.css`**

```css
/* === NAV === */
.nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--espresso);
  border-bottom: 1px solid var(--leather);
}
.nav__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  gap: 24px;
}
.nav__logo {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 800;
  color: var(--cream);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  white-space: nowrap;
  flex-shrink: 0;
}
.nav__links {
  display: flex;
  gap: 24px;
  list-style: none;
}
.nav__link {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: var(--muted);
  transition: color 0.15s ease;
}
.nav__link:hover { color: var(--cream); }
.nav__actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
.btn-nav {
  display: inline-block;
  padding: 7px 14px;
  border-radius: var(--radius);
  font-size: 12px;
  font-weight: 700;
  transition: opacity 0.15s ease;
}
.btn-nav:hover { opacity: 0.8; }
.btn-nav:focus-visible { outline: 2px solid var(--cream); outline-offset: 2px; }
.btn-nav--outline {
  border: 1px solid var(--leather);
  color: var(--muted);
  font-family: var(--font-body);
}
.btn-nav--primary {
  background: var(--cream);
  color: var(--black);
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

/* Mobile: hide nav links, keep actions */
@media (max-width: 640px) {
  .nav__links { display: none; }
  .nav__logo { font-size: 13px; }
}
```

- [ ] **Step 3: Test — sticky nav stays at top on scroll, links are visible, Directions button is cream on black**

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: sticky nav with logo, links, call + directions CTAs"
```

---

### Task 4: Hero section

**Files:**
- Modify: `index.html` — add `<main>` with hero section
- Modify: `css/style.css` — hero styles

**Interfaces:**
- Consumes: `.container`, `.btn--primary`, token variables
- Produces: `<main id="main-content">` landmark used by skip-link (add to nav in this task)

- [ ] **Step 1: Add skip link to `index.html` (before nav, inside `#site-content`)**

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

- [ ] **Step 2: Add hero HTML after nav, inside `#site-content`**

```html
<main id="main-content">
  <section class="hero" aria-labelledby="hero-heading">
    <div class="container hero__inner">
      <div class="hero__content">
        <p class="eyebrow">Shoreline, Washington · Open 7 Days</p>
        <h2 id="hero-heading" class="hero__heading">
          Shoreline's<br>Smoke<br>Shop
        </h2>
        <p class="hero__body">
          The biggest selection in the area, at prices that make sense.
          Staff who actually know what they're talking about.
        </p>
        <div class="hero__actions">
          <a href="https://maps.google.com/?q=123+Aurora+Ave+N+Shoreline+WA+98133"
             target="_blank" rel="noopener noreferrer"
             class="hero-btn hero-btn--primary">Get Directions</a>
          <a href="tel:+12065550199" class="hero-btn hero-btn--outline">(206) 555-0199</a>
        </div>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Step 3: Add hero styles to `css/style.css`**

```css
/* === SKIP LINK === */
.skip-link {
  position: absolute;
  top: -100%;
  left: 16px;
  z-index: 9999;
  background: var(--cream);
  color: var(--black);
  font-weight: 700;
  padding: 8px 16px;
  border-radius: var(--radius);
  transition: top 0.1s;
}
.skip-link:focus { top: 8px; }

/* === HERO === */
.hero {
  background: var(--black);
  padding: 64px 0 56px;
  position: relative;
  overflow: hidden;
}
.hero::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 35%;
  height: 100%;
  background: var(--espresso);
  clip-path: polygon(20% 0, 100% 0, 100% 100%, 0% 100%);
  pointer-events: none;
}
.hero__inner { position: relative; z-index: 1; }
.eyebrow {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-bottom: 16px;
}
.hero__heading {
  font-family: var(--font-display);
  font-size: clamp(52px, 9vw, 88px);
  font-weight: 800;
  color: var(--cream);
  text-transform: uppercase;
  line-height: 0.9;
  margin-bottom: 20px;
  letter-spacing: 0.01em;
}
.hero__body {
  font-size: 14px;
  color: var(--muted);
  line-height: 1.7;
  max-width: 340px;
  margin-bottom: 28px;
}
.hero__actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.hero-btn {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 13px 28px;
  border-radius: var(--radius);
  transition: opacity 0.15s ease;
}
.hero-btn:hover { opacity: 0.85; }
.hero-btn:focus-visible { outline: 2px solid var(--cream); outline-offset: 2px; }
.hero-btn--primary {
  background: var(--cream);
  color: var(--black);
}
.hero-btn--outline {
  border: 2px solid var(--leather);
  color: var(--muted);
}

@media (max-width: 640px) {
  .hero { padding: 40px 0 36px; }
  .hero::after { display: none; }
}
```

- [ ] **Step 4: Test — hero heading displays at large size, diagonal block visible on desktop, hidden on mobile**

- [ ] **Step 5: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: hero section with heading, body, CTA buttons, diagonal block"
```

---

### Task 5: Trust bar

**Files:**
- Modify: `index.html` — add trust bar section after hero, inside `<main>`
- Modify: `css/style.css` — trust bar styles

**Interfaces:**
- Consumes: `.container`, token variables

- [ ] **Step 1: Add trust bar HTML after `.hero` section**

```html
<section class="trust" aria-label="Why shop with us">
  <div class="container trust__grid">
    <div class="trust__item">
      <p class="trust__stat">Lowest<br>Prices</p>
      <p class="trust__sub">We'll beat any local price</p>
    </div>
    <div class="trust__item">
      <p class="trust__stat">Staff Who<br>Know</p>
      <p class="trust__sub">Real answers, no upsell</p>
    </div>
    <div class="trust__item">
      <p class="trust__stat">1000+<br>Products</p>
      <p class="trust__sub">In stock, on the shelf today</p>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add trust bar styles**

```css
/* === TRUST BAR === */
.trust {
  background: var(--espresso);
  border-top: 1px solid var(--leather);
  border-bottom: 1px solid var(--leather);
  padding: 24px 0;
}
.trust__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
}
.trust__item {
  text-align: center;
  padding: 0 20px;
}
.trust__item + .trust__item {
  border-left: 1px solid var(--leather);
}
.trust__stat {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  color: var(--cream);
  line-height: 1.05;
  margin-bottom: 6px;
}
.trust__sub {
  font-size: 11px;
  color: var(--muted);
  line-height: 1.4;
}

@media (max-width: 480px) {
  .trust__grid { grid-template-columns: 1fr; gap: 16px; }
  .trust__item + .trust__item { border-left: none; border-top: 1px solid var(--leather); padding-top: 16px; }
}
```

- [ ] **Step 3: Test — 3 columns on desktop, stacked on mobile under 480px**

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: trust bar — lowest prices, knowledgeable staff, 1000+ products"
```

---

### Task 6: What We Carry + Product Teasers

**Files:**
- Modify: `index.html` — add two sections: categories + product teasers
- Modify: `css/style.css` — category chip + product card styles

**Interfaces:**
- Consumes: `.container`, token variables, `.eyebrow`
- Produces: `id="products"` anchor used by nav link

- [ ] **Step 1: Add categories + product teaser HTML after trust bar**

```html
<section class="categories" id="products" aria-labelledby="categories-heading">
  <div class="container">
    <h2 id="categories-heading" class="section-heading">What We Carry</h2>
    <p class="section-sub">Come in and let our staff walk you through everything.</p>
    <ul class="chip-list" role="list" aria-label="Product categories">
      <li class="chip chip--active">Vapes &amp; Disposables</li>
      <li class="chip">Glass &amp; Pipes</li>
      <li class="chip">Vape Juice / E-Liquid</li>
      <li class="chip">Wraps &amp; Papers</li>
      <li class="chip">CBD Products</li>
      <li class="chip">Kratom</li>
      <li class="chip">Hookah / Shisha</li>
      <li class="chip">Nicotine Pouches</li>
      <li class="chip">Cigarettes &amp; Tobacco</li>
      <li class="chip">Accessories</li>
    </ul>
  </div>
</section>

<section class="products" aria-labelledby="products-heading">
  <div class="container">
    <div class="products__header">
      <h2 id="products-heading" class="section-heading">In Store Now</h2>
      <p class="products__cta-text">Come see it all →</p>
    </div>
    <div class="product-grid">
      <article class="product-card">
        <div class="product-card__img" aria-hidden="true"></div>
        <div class="product-card__body">
          <p class="product-card__cat">Vapes</p>
          <p class="product-card__name">Vape Pod Kit</p>
          <p class="product-card__price">From $24.99</p>
        </div>
      </article>
      <article class="product-card">
        <div class="product-card__img" aria-hidden="true"></div>
        <div class="product-card__body">
          <p class="product-card__cat">Glass</p>
          <p class="product-card__name">Water Pipe</p>
          <p class="product-card__price">From $49.99</p>
        </div>
      </article>
      <article class="product-card">
        <div class="product-card__img" aria-hidden="true"></div>
        <div class="product-card__body">
          <p class="product-card__cat">Wraps</p>
          <p class="product-card__name">Rolling Papers</p>
          <p class="product-card__price">From $3.99</p>
        </div>
      </article>
      <article class="product-card">
        <div class="product-card__img" aria-hidden="true"></div>
        <div class="product-card__body">
          <p class="product-card__cat">CBD</p>
          <p class="product-card__name">CBD Gummies</p>
          <p class="product-card__price">From $29.99</p>
        </div>
      </article>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add section + chip + card styles**

```css
/* === SECTION COMMON === */
.section-heading {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 800;
  color: var(--cream);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.section-sub {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 18px;
}

/* === CATEGORIES === */
.categories {
  background: var(--black);
  padding: 40px 0;
}
.chip-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  list-style: none;
}
.chip {
  background: var(--espresso);
  border: 1.5px solid var(--leather);
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: var(--radius);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.chip--active {
  border-color: var(--cream);
  color: var(--cream);
}

/* === PRODUCTS === */
.products {
  background: var(--espresso);
  padding: 40px 0;
  border-top: 1px solid var(--leather);
}
.products__header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
}
.products__cta-text {
  font-size: 12px;
  color: var(--muted);
  font-weight: 600;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.product-card {
  background: var(--black);
  border: 1px solid var(--leather);
  border-radius: var(--radius);
  overflow: hidden;
}
.product-card__img {
  background: #1A1005;
  height: 120px;
}
.product-card__body { padding: 12px; }
.product-card__cat {
  font-size: 10px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
}
.product-card__name {
  font-size: 13px;
  font-weight: 600;
  color: var(--cream);
  margin-bottom: 6px;
}
.product-card__price {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 800;
  color: var(--cream);
  opacity: 0.55;
}

@media (max-width: 640px) {
  .product-grid { grid-template-columns: repeat(2, 1fr); }
}
```

- [ ] **Step 3: Test — 4-col product grid on desktop, 2-col on mobile, category chips wrap**

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: categories section and product teasers grid"
```

---

### Task 7: Hours & Location + Footer

**Files:**
- Modify: `index.html` — add hours/location section + footer
- Modify: `css/style.css` — hours + footer styles

**Interfaces:**
- Consumes: `.container`, token variables
- Produces: `id="hours"` and `id="contact"` anchors used by nav links

- [ ] **Step 1: Add hours/location and footer HTML after products section**

```html
  <section class="location" id="hours" aria-labelledby="location-heading">
    <div class="container">
      <h2 id="location-heading" class="section-heading">Come Find Us</h2>
      <div class="location__grid">
        <div class="location__hours" id="contact">
          <h3 class="location__label">Hours</h3>
          <ul class="hours-list" role="list">
            <li class="hours-row">
              <span class="hours-day">Mon – Fri</span>
              <span class="hours-time">9 AM – 9 PM</span>
            </li>
            <li class="hours-row">
              <span class="hours-day">Saturday</span>
              <span class="hours-time">10 AM – 8 PM</span>
            </li>
            <li class="hours-row">
              <span class="hours-day">Sunday</span>
              <span class="hours-time">11 AM – 7 PM</span>
            </li>
          </ul>
        </div>
        <div class="location__address">
          <h3 class="location__label">Address</h3>
          <address class="location__addr-text">
            123 Aurora Ave N<br>
            Shoreline, WA 98133
          </address>
          <a href="tel:+12065550199" class="location__phone">(206) 555-0199</a>
          <a href="https://maps.google.com/?q=123+Aurora+Ave+N+Shoreline+WA+98133"
             target="_blank" rel="noopener noreferrer"
             class="location__map-btn">Open in Maps</a>
        </div>
      </div>
    </div>
  </section>
</main>

<footer class="footer" role="contentinfo">
  <div class="container footer__inner">
    <p class="footer__name">AAA Smoke &amp; Vape</p>
    <p class="footer__meta">© 2026 · Shoreline, WA · Must be 21+ to enter</p>
  </div>
</footer>
```

- [ ] **Step 2: Add location + footer styles**

```css
/* === LOCATION === */
.location {
  background: var(--black);
  padding: 48px 0;
  border-top: 1px solid var(--leather);
}
.location__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  margin-top: 24px;
}
.location__label {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 14px;
}
.hours-list { list-style: none; }
.hours-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--muted);
  padding: 8px 0;
  border-bottom: 1px solid var(--espresso);
}
.hours-row:last-child { border-bottom: none; }
.hours-time {
  color: var(--cream);
  font-weight: 600;
}
.location__addr-text {
  font-style: normal;
  font-size: 14px;
  font-weight: 600;
  color: var(--cream);
  line-height: 1.6;
  margin-bottom: 10px;
}
.location__phone {
  display: block;
  font-size: 13px;
  color: var(--muted);
  margin-bottom: 16px;
  transition: color 0.15s;
}
.location__phone:hover { color: var(--cream); }
.location__map-btn {
  display: block;
  background: var(--cream);
  color: var(--black);
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 11px 0;
  border-radius: var(--radius);
  text-align: center;
  transition: opacity 0.15s;
}
.location__map-btn:hover { opacity: 0.85; }
.location__map-btn:focus-visible { outline: 2px solid var(--cream); outline-offset: 2px; }

/* === FOOTER === */
.footer {
  background: var(--espresso);
  border-top: 2px solid var(--leather);
  padding: 18px 0;
}
.footer__inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.footer__name {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 800;
  color: var(--cream);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.footer__meta {
  font-size: 11px;
  color: var(--muted);
}

@media (max-width: 640px) {
  .location__grid { grid-template-columns: 1fr; gap: 32px; }
  .footer__inner { justify-content: center; text-align: center; }
}
```

- [ ] **Step 3: Test — hours display as a clean list, "Open in Maps" button is cream, footer sits at bottom**

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: hours/location section and footer"
```

---

### Task 8: Mobile polish + reduced motion

**Files:**
- Modify: `css/style.css` — add `@media (prefers-reduced-motion)` and final mobile tweaks

**Interfaces:**
- Consumes: all existing CSS classes

- [ ] **Step 1: Add reduced motion + final polish to bottom of `css/style.css`**

```css
/* === REDUCED MOTION === */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
  html { scroll-behavior: auto; }
}

/* === FINAL MOBILE TWEAKS === */
@media (max-width: 375px) {
  .hero__heading { font-size: 44px; }
  .hero__actions { flex-direction: column; }
  .hero-btn { text-align: center; }
  .trust__stat { font-size: 18px; }
}
```

- [ ] **Step 2: Full cross-device test checklist**
  - Resize to 375px — no horizontal scroll, all text readable
  - Resize to 768px — product grid is 2-col, nav links hidden, layout intact
  - Resize to 1280px — full layout, diagonal hero block visible
  - Enable OS "Reduce Motion" — all transitions instant, no jank
  - Tab through the page — focus rings visible on all interactive elements
  - Open in Chrome DevTools → Lighthouse → run Accessibility audit → score should be 90+

- [ ] **Step 3: Commit**

```bash
git add css/style.css
git commit -m "feat: reduced motion support, final mobile tweaks"
```

---

### Task 9: Deploy

**Files:**
- Create: `vercel.json` (optional, for Vercel)
- No changes to `index.html` or CSS

- [ ] **Option A — GitHub Pages:**

```bash
git remote add origin https://github.com/<your-username>/aaa-smoke-vape.git
git push -u origin main
# In GitHub repo Settings → Pages → Source: Deploy from branch → main → / (root)
# Site live at: https://<your-username>.github.io/aaa-smoke-vape/
```

- [ ] **Option B — Vercel (recommended, faster):**

```bash
# Install Vercel CLI if needed:
npm i -g vercel
# From project root:
vercel
# Follow prompts: project name = aaa-smoke-vape, framework = Other, root = ./
# Site live at: https://aaa-smoke-vape.vercel.app
```

- [ ] **Verify live site:**
  - Age gate appears on first load
  - "Yes, I'm 21+" dismisses gate and shows site
  - "Get Directions" / "Open in Maps" link opens Google Maps correctly
  - "Call Us" / phone number links open dialer on mobile
  - Refresh after confirming — gate does NOT reappear

- [ ] **Commit deploy config if added**

```bash
git add vercel.json
git commit -m "chore: add vercel config"
```
