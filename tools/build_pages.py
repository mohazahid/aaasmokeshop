"""Builds one page per brand or category (flum/index.html and so on), the sitemap and llms.txt.
Edit PAGES below and run: python tools/build_pages.py"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.aaasmokeandvape.com"
MAPS = "https://maps.google.com/?q=14610+15th+Ave+NE+Shoreline+WA+98155"
GOOGLE = "https://share.google/Qu0QS6vpapjurIIUR"

PAGES = [
    {
        "slug": "flum", "name": "FLUM", "kind": "disposable vapes",
        "title": "FLUM Vapes in Shoreline WA | AAA Smoke & Vape",
        "desc": "FLUM disposable vapes at AAA Smoke & Vape in Shoreline, WA. FLUM Mello and Float X in store. Open Monday to Saturday 10:30 AM to 7 PM.",
        "intro": "We carry FLUM disposables at our Shoreline store, including FLUM Mello and FLUM Float X. Flavors change pretty often, so ask at the counter what just came in.",
        "items": ["FLUM Mello", "FLUM Float X", "New FLUM flavors as they come in"],
        "faq": [("Do you have FLUM Mello?", "Yes, we carry FLUM Mello and FLUM Float X. Which flavors we have depends on the week, so ask at the counter."),
                ("Can I order FLUM online?", "No, we only sell vapes in the store. You have to be 21 or older and we check ID.")],
    },
    {
        "slug": "geek-bar", "name": "Geek Bar", "kind": "disposable vapes",
        "title": "Geek Bar Vapes in Shoreline WA | AAA Smoke & Vape",
        "desc": "Geek Bar Pulse 2 and Meloso Max at AAA Smoke & Vape in Shoreline, WA. In store Monday to Saturday 10:30 AM to 7 PM at 14610 15th Ave NE.",
        "intro": "We have Geek Bar Pulse 2 and Geek Bar Meloso Max at our Shoreline store. New flavors come in pretty often so it is worth asking what we have that week.",
        "items": ["Geek Bar Pulse 2", "Geek Bar Meloso Max", "New Geek Bar flavors as they come in"],
        "faq": [("Do you carry Geek Bar Pulse 2?", "Yes, we carry Geek Bar Pulse 2 and Meloso Max in the store."),
                ("Do you ship Geek Bar?", "No, we only sell in the store and you have to be 21 or older.")],
    },
    {
        "slug": "zyn", "name": "ZYN", "kind": "nicotine pouches",
        "title": "ZYN Nicotine Pouches in Shoreline WA | AAA Smoke & Vape",
        "desc": "ZYN nicotine pouches in 3mg and 6mg at AAA Smoke & Vape in Shoreline, WA. Cool Mint, Wintergreen, Coffee and more. Open Monday to Saturday.",
        "intro": "We carry ZYN in 3mg and 6mg. We usually have Cool Mint, Wintergreen, Coffee, Cinnamon and Citrus, but it depends on what is in stock that week. We also carry On! and Zone pouches.",
        "items": ["ZYN Cool Mint", "ZYN Wintergreen", "ZYN Coffee", "ZYN Cinnamon", "ZYN Citrus", "On! and Zone pouches"],
        "faq": [("Do you have ZYN 6mg?", "Yes, we carry ZYN in 3mg and 6mg."),
                ("What other pouches do you carry?", "We also carry On! and Zone nicotine pouches.")],
    },
    {
        "slug": "kratom", "name": "Kratom", "kind": "kratom",
        "title": "Kratom in Shoreline WA, MIT45 | AAA Smoke & Vape",
        "desc": "Kratom at AAA Smoke & Vape in Shoreline, WA. MIT45 Gold, MIT45 Boost and Super K as extracts, powders, capsules and shots. 21+ only.",
        "intro": "We carry MIT45 Gold, MIT45 Boost and Super K as extracts, powders, capsules and shots. If it is your first time buying kratom just ask at the counter and we will go over the differences between the brands and the formats.",
        "items": ["MIT45 Gold", "MIT45 Boost", "Super K Extra Strong", "Kratom capsules", "Kratom powder", "Kratom shots"],
        "faq": [("Do you carry MIT45?", "Yes, we have MIT45 Gold and MIT45 Boost, plus Super K."),
                ("Do I need to be 21 to buy kratom?", "Yes, you have to be 21 or older and we check ID.")],
    },
    {
        "slug": "cigars", "name": "Cigars and cigarillos", "kind": "cigars",
        "title": "Cigars and Cigarillos in Shoreline WA | AAA Smoke & Vape",
        "desc": "Black & Mild, Swisher Sweets, Garcia y Vega and Backwoods at AAA Smoke & Vape in Shoreline, WA. Open Monday to Saturday 10:30 AM to 7 PM.",
        "intro": "We carry Black & Mild, Swisher Sweets, Garcia y Vega and Backwoods, in singles and packs. We also have cigarettes, wraps and papers.",
        "items": ["Black & Mild", "Swisher Sweets", "Garcia y Vega", "Backwoods", "Cigarettes", "Wraps and papers"],
        "faq": [("Do you carry Black & Mild Wine?", "Yes, we carry Black & Mild including Wine and Wood Tip."),
                ("Do you sell single cigarillos?", "Yes, some brands come as singles and two packs, so ask at the counter.")],
    },
    {
        "slug": "glass", "name": "Glass and pipes", "kind": "glass",
        "title": "Glass, Pipes and Hookah in Shoreline WA | AAA Smoke & Vape",
        "desc": "Glass pipes, hookah, shisha and accessories at AAA Smoke & Vape in Shoreline, WA. Open Monday to Saturday 10:30 AM to 7 PM at 14610 15th Ave NE.",
        "intro": "We have glass pipes, hookahs, shisha and accessories in the store. The glass changes a lot so it is best to come see what is on the shelf.",
        "items": ["Glass pipes", "Hookah", "Shisha", "Lighters and accessories", "CBD products"],
        "faq": [("Do you sell hookah?", "Yes, we carry hookahs and shisha."),
                ("Do you have CBD?", "Yes, we have CBD products in the store.")],
    },
]

e = html.escape


def nav_links(current: str) -> str:
    cur = ' aria-current="page"'
    return "".join(
        f'<li><a href="/{p["slug"]}/" class="nav__link"{cur if p["slug"] == current else ""}>{e(p["name"].split(" and ")[0])}</a></li>'
        for p in PAGES)


def footer() -> str:
    links = "".join(f'<li><a href="/{p["slug"]}/">{e(p["name"])}</a></li>' for p in PAGES)
    return f'''    <footer class="footer" role="contentinfo">
      <div class="container">
        <nav class="footer__links" aria-label="Brands we carry"><ul role="list"><li><a href="/">Home</a></li>{links}</ul></nav>
        <div class="footer__inner">
          <p class="footer__name">AAA Smoke &amp; Vape</p>
          <p class="footer__meta">&copy; 2026 &middot; 14610 15th Ave NE, Shoreline, WA 98155 &middot; 21+ only</p>
        </div>
      </div>
    </footer>'''


def page(p: dict) -> str:
    url = f"{SITE}/{p['slug']}/"
    schema = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": p["name"], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]
    items = "".join(f"<li>{e(i)}</li>" for i in p["items"])
    faq = "".join(f'<div class="faq-item"><dt class="faq-q">{e(q)}</dt><dd class="faq-a">{e(a)}</dd></div>' for q, a in p["faq"])
    others = "".join(f'<li><a href="/{o["slug"]}/">{e(o["name"])}</a></li>' for o in PAGES if o is not p)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(p["title"])}</title>
  <meta name="description" content="{e(p["desc"])}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(p["title"])}">
  <meta property="og:description" content="{e(p["desc"])}">
  <meta property="og:image" content="{SITE}/images/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/images/og.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="/css/style.css">
  <script defer src="/_vercel/insights/script.js"></script>
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
  <div id="age-gate" role="dialog" aria-modal="true" aria-labelledby="age-gate-heading">
    <div class="age-gate__backdrop"></div>
    <div class="age-gate__card">
      <p class="age-gate__eyebrow">Age Verification</p>
      <p id="age-gate-heading" class="age-gate__heading">Are you 21<br>or older?</p>
      <p class="age-gate__body">You have to be 21 or older to use this site.</p>
      <button class="btn btn--primary" id="age-confirm">Yes, I'm 21+</button>
      <button class="btn btn--ghost" id="age-deny">No, take me back</button>
    </div>
  </div>
  <div id="site-content" aria-hidden="true">
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <nav class="nav" aria-label="Main navigation">
      <div class="container nav__inner">
        <a href="/" class="nav__logo" aria-label="AAA Smoke and Vape home">AAA Smoke &amp; Vape</a>
        <ul class="nav__links" role="list">{nav_links(p["slug"])}</ul>
        <div class="nav__actions">
          <a href="{MAPS}" target="_blank" rel="noopener noreferrer" class="btn-nav btn-nav--primary">Directions</a>
        </div>
      </div>
    </nav>
    <main id="main-content" tabindex="-1">
      <section class="hero">
        <div class="container hero__inner">
          <div class="hero__content">
            <p class="crumbs"><a href="/">Home</a> / {e(p["name"])}</p>
            <p class="status" id="open-status">Open Monday to Saturday, 10:30 AM to 7 PM</p>
            <h1 class="hero__heading">{e(p["name"])} in Shoreline, WA</h1>
            <p class="hero__body">{e(p["intro"])}</p>
            <div class="hero__actions">
              <a href="{MAPS}" target="_blank" rel="noopener noreferrer" class="hero-btn hero-btn--primary">Get directions</a>
              <a href="/#contact-form" class="hero-btn hero-btn--outline">Ask if we have it</a>
            </div>
          </div>
          <aside class="hero__card" aria-label="Store info">
            <p class="hero__card-label">Visit us</p>
            <p class="hero__card-big">14610 15th Ave NE</p>
            <p class="hero__card-text">Shoreline, WA 98155</p>
            <div class="hero__card-row"><span>Mon to Sat</span><span>10:30 AM to 7 PM</span></div>
            <div class="hero__card-row"><span>Sunday</span><span>Closed</span></div>
            <p class="hero__card-text">21+ only, bring a valid ID</p>
            <a class="hero__card-link" href="{GOOGLE}" target="_blank" rel="noopener noreferrer">See our Google reviews &rarr;</a>
          </aside>
        </div>
      </section>
      <section class="categories">
        <div class="container">
          <h2 class="section-heading">{e(p["name"])} we carry</h2>
          <p class="section-sub">What is on the shelf changes week to week, these are what we usually have. We do not sell {e(p["kind"])} online, only in the store.</p>
          <ul class="cat-list" role="list">{items}</ul>
        </div>
      </section>
      <section class="categories">
        <div class="container">
          <h2 class="section-heading">How to find us</h2>
          <p class="section-sub">We are at 14610 15th Ave NE in Shoreline, a short drive from Lake Forest Park, Kenmore and north Seattle. We are open Monday through Saturday from 10:30 AM to 7 PM and closed on Sunday. Bring a valid ID, you have to be 21 or older to come in.</p>
          <a href="{MAPS}" target="_blank" rel="noopener noreferrer" class="hero-btn hero-btn--primary">Open in Maps</a>
        </div>
      </section>
      <section class="faq-section">
        <div class="container">
          <h2 class="section-heading">Common questions</h2>
          <dl class="faq-list">{faq}</dl>
        </div>
      </section>
      <section class="categories">
        <div class="container">
          <h2 class="section-heading">We also carry</h2>
          <ul class="cat-list cat-list--links" role="list">{others}</ul>
        </div>
      </section>
    </main>
{footer()}
    <div class="mobile-bar" aria-label="Quick actions">
      <a href="{MAPS}" target="_blank" rel="noopener noreferrer" class="mobile-bar__btn mobile-bar__btn--primary">Directions</a>
      <a href="/#contact-form" class="mobile-bar__btn">Contact</a>
    </div>
  </div>
  <script src="/js/main.js"></script>
</body>
</html>
'''


def main():
    for p in PAGES:
        out = ROOT / p["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(p), encoding="utf-8", newline="\r\n")
    urls = [f"{SITE}/"] + [f"{SITE}/{p['slug']}/" for p in PAGES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url>\n    <loc>{u}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8", newline="\r\n")
    llms = ["# AAA Smoke & Vape", "",
            "> Smoke and vape shop at 14610 15th Ave NE, Shoreline, WA 98155. Open Monday to Saturday 10:30 AM to 7 PM, closed Sunday. 21+ only. In store sales only, no online orders.", "",
            "## Pages", f"- [Home]({SITE}/): store info, hours, what we carry, FAQ"]
    llms += [f"- [{p['name']}]({SITE}/{p['slug']}/): {p['desc']}" for p in PAGES]
    llms += ["", "## Links", f"- [Google reviews]({GOOGLE})", f"- [Directions]({MAPS})"]
    (ROOT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8", newline="\r\n")
    print(f"built {len(PAGES)} pages")


if __name__ == "__main__":
    main()
