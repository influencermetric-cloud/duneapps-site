#!/usr/bin/env python3
"""Renders every page from one shared shell.

The pages drifted apart before because each carried its own copy of the
header, footer, fonts and meta. Now there is exactly one definition of the
chrome and each page supplies only its own body.

This file also owns:
  - render_article(): the editorial template every guide is rendered through
  - App Store links with campaign tokens, and the /go/<creator>/ redirects
  - GA4 click events for every App Store link, so a creator's traffic can be
    measured without a server
  - the sitemap, robots and llms.txt, generated from the pages actually rendered
"""
import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://duneapps.com"
GA = "G-BTY3LVJMBB"
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------------------
# Apps and links
# ---------------------------------------------------------------------------
# Apple campaign links need a provider token (pt). It is generated ONCE in
# App Store Connect -> App Analytics -> Campaigns -> "Generate campaign link",
# and it never changes. Until it is pasted here, links carry no pt/ct and
# attribution relies on our own GA4 click events instead.
PROVIDER_TOKEN = None

APPS = {
    "receiptsnap": {"name": "Receipt Snap", "id": "6806519870",
                    "store": "https://apps.apple.com/app/id6806519870", "page": "/receiptsnap/"},
    # DriveSnap is not on the App Store yet; its link goes to the product page.
    "drivesnap":   {"name": "DriveSnap", "id": "6807116273", "store": None, "page": "/drivesnap/"},
}
APP_STORE = APPS["receiptsnap"]["store"]

# /go/<name>/ pages. One per creator or channel. Add a name, rebuild, hand
# out duneapps.com/go/<name>/ — clicks are counted by GA4 (creator_click) and,
# once PROVIDER_TOKEN is set, by App Store Connect under the same name.
CREATORS = ["x", "linkedin", "tiktok", "youtube", "reddit", "email"]


def app_link(app="receiptsnap", ct=None):
    a = APPS[app]
    if not a["store"]:
        return a["page"]
    if PROVIDER_TOKEN and ct:
        return f"https://apps.apple.com/app/apple-store/id{a['id']}?pt={PROVIDER_TOKEN}&ct={ct}&mt=8"
    return a["store"]


# ---------------------------------------------------------------------------
# Chrome
# ---------------------------------------------------------------------------
FAVICON = ('data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20'
  'viewBox%3D%270%200%2040%2040%27%3E%3Cdefs%3E%3CclipPath%20id%3D%27d%27%3E%3Ccircle%20cx%3D%2720%27%20'
  'cy%3D%2720%27%20r%3D%2719%27%2F%3E%3C%2FclipPath%3E%3C%2Fdefs%3E%3Ccircle%20cx%3D%2720%27%20cy%3D%2720%27%20'
  'r%3D%2719%27%20fill%3D%27%23EFF3F1%27%2F%3E%3Cg%20clip-path%3D%27url%28%23d%29%27%3E%3Ccircle%20cx%3D%2713%27%20'
  'cy%3D%2713%27%20r%3D%275%27%20fill%3D%27%23C3F04C%27%2F%3E%3Cpath%20d%3D%27M13%2041%20L41%2041%20L41%2025%20'
  'C%2034%2025.8%2027.5%2028.8%2022%2033.8%20L13%2041%20Z%27%20fill%3D%27%239DB8B2%27%2F%3E%3Cpath%20d%3D%27'
  'M-1%2041%20L-1%2029.4%20C%208%2028.6%2015.2%2025.8%2020.4%2021%20C%2021.6%2019.9%2022.9%2019.9%2024%2021.1%20'
  'C%2028%2025.4%2033.4%2029%2041%2030.8%20L41%2041%20Z%27%20fill%3D%27%231A4B44%27%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E')

HEADER = f'''<a class="skip" href="#main">Skip to content</a>
<div class="progress" id="progress" aria-hidden="true"></div>
<header id="hdr"><div class="wrap bar">
  <a class="brand" href="/"><span class="mark" aria-hidden="true"></span><span>Dune Apps</span></a>
  <nav class="site-nav">
    <a href="/writing/">Guides</a>
    <a href="/receiptsnap/">Receipt Snap</a>
    <a href="/drivesnap/">DriveSnap</a>
    <a class="btn btn-primary btn-sm" href="{APP_STORE}" data-app="receiptsnap" data-place="header">Get the app</a>
  </nav>
</div></header>'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="/"><span class="mark" aria-hidden="true"></span><span>Dune Apps</span></a>
        <p style="margin-top:18px;max-width:34ch;color:rgba(255,255,255,.72)">iPhone tools for the money you can claim back: your receipts and your business miles, with every record kept on your own phone.</p>
      </div>
      <div><h4>Apps</h4>
        <a href="/receiptsnap/">Receipt Snap</a>
        <a href="/drivesnap/">DriveSnap</a>
        <a href="/compare/drivesnap-vs-mileiq/">DriveSnap vs MileIQ</a>
        <a href="{APP_STORE}" data-app="receiptsnap" data-place="footer">Receipt Snap on the App Store</a></div>
      <div><h4>Guides</h4>
        <a href="/posts/irs-mileage-rate-2026.html">IRS mileage rate 2026</a>
        <a href="/posts/hmrc-mileage-rates-2026.html">HMRC mileage rates 2026/27</a>
        <a href="/posts/do-you-need-receipts-for-tax-deductions.html">Do you need receipts for deductions?</a>
        <a href="/posts/how-long-to-keep-receipts.html">How long to keep receipts</a>
        <a href="/posts/irs-mileage-log-requirements.html">IRS mileage log rules</a>
        <a href="/writing/">All guides</a></div>
      <div><h4>Tools &amp; help</h4>
        <a href="/posts/mileage-log-template.html">Free mileage log template</a>
        <a href="/templates/mileage-log/">Printable mileage log</a>
        <a href="https://github.com/influencermetric-cloud/receiptsnap-support">Receipt Snap support</a>
        <a href="https://github.com/influencermetric-cloud/drivesnap-support">DriveSnap support</a>
        <a href="https://github.com/influencermetric-cloud/receiptsnap-support/blob/main/PRIVACY.md">Privacy policy</a></div>
    </div>
    <p class="disclosure">© Dune Apps. This website uses Google Analytics to see which pages help people. The apps themselves collect nothing at all.</p>
  </div>
</footer>
<script>
  const hdr = document.getElementById('hdr');
  addEventListener('scroll', () => hdr.classList.toggle('stuck', scrollY > 8), {{ passive: true }});
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {{
    const io = new IntersectionObserver(es => es.forEach(e => {{
      if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }}
    }}), {{ rootMargin: '0px 0px -8% 0px' }});
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  }} else document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));

  // Every App Store click becomes a GA4 event with the app and where on the
  // page it was clicked, so "which guide sends people to the store" is answerable.
  document.addEventListener('click', e => {{
    const a = e.target.closest('a[href]'); if (!a || typeof gtag !== 'function') return;
    const h = a.getAttribute('href') || '';
    if (h.includes('apps.apple.com')) {{
      gtag('event', 'app_store_click', {{
        app: a.dataset.app || (h.includes('6806519870') ? 'receiptsnap' : 'other'),
        placement: a.dataset.place || (a.closest('[id]') || {{}}).id || 'body',
        page_path: location.pathname }});
    }} else if (a.classList.contains('btn')) {{
      gtag('event', 'cta_click', {{ label: a.textContent.trim().slice(0, 40), page_path: location.pathname }});
    }}
  }}, {{ capture: true }});

  // Reading progress + table-of-contents highlight, only where an article exists.
  const art = document.querySelector('.art-main');
  if (art) {{
    const bar = document.getElementById('progress');
    const tick = () => {{
      const r = art.getBoundingClientRect(); const total = r.height - innerHeight;
      bar.style.width = Math.max(0, Math.min(1, -r.top / Math.max(total, 1))) * 100 + '%';
    }};
    addEventListener('scroll', tick, {{ passive: true }}); tick();
    const links = [...document.querySelectorAll('.toc a')];
    const heads = links.map(l => document.getElementById(l.getAttribute('href').slice(1))).filter(Boolean);
    if (heads.length) {{
      const spy = new IntersectionObserver(es => es.forEach(en => {{
        if (en.isIntersecting) {{
          links.forEach(l => l.classList.toggle('on', l.getAttribute('href') === '#' + en.target.id));
        }}
      }}), {{ rootMargin: '-100px 0px -70% 0px' }});
      heads.forEach(h => spy.observe(h));
    }}
  }}
</script>'''

ORG_LD = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": SITE + "/#org", "name": "Dune Apps", "url": SITE + "/",
         "logo": {"@type": "ImageObject", "url": SITE + "/brand/dune-mark-512.png"},
         "sameAs": ["https://github.com/influencermetric-cloud",
                    "https://apps.apple.com/us/developer/nahid-saleem/id6792166765"]},
        {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Dune Apps",
         "publisher": {"@id": SITE + "/#org"}},
        {"@type": "Person", "@id": SITE + "/#nahid", "name": "Nahid Saleem",
         "jobTitle": "Founder, Dune Apps",
         "description": "Builds Receipt Snap and DriveSnap — iPhone tools that keep tax records on the device. Writes the guides from the research done to build them.",
         "url": SITE + "/"},
    ]})

PAGES = []  # (out, lastmod, priority) — everything rendered, for the sitemap


def render(*, out, title, description, canonical, body, style="", head="",
           og_image="og.png", og_type="website", noindex=False, lastmod=None, priority="0.7"):
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA}', {{ anonymize_ip: true }});
</script>
<script>document.documentElement.classList.add('js')</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
{"<meta name='robots' content='noindex,follow'>" if noindex else ""}
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="/brand/dune-mark-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Dune Apps">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ORG_LD}</script>
{head}
<link rel="stylesheet" href="/style.css">
{f"<style>{style}</style>" if style else ""}
</head>
<body>
{HEADER}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    path = ROOT / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page)
    if not noindex:
        PAGES.append((out, lastmod or TODAY, priority))
    return path


# ---------------------------------------------------------------------------
# Article template
# ---------------------------------------------------------------------------
def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60] or "section"


def reading_minutes(body_html):
    words = len(re.sub(r"<[^>]+>", " ", body_html).split())
    return max(1, round(words / 220))


def add_heading_ids(body_html):
    """Give every h2 an id and an anchor link; return (html, [(id, text)])."""
    heads = []
    def repl(m):
        text = m.group(2)
        hid = slugify(text)
        base, n = hid, 2
        while any(h[0] == hid for h in heads):
            hid = f"{base}-{n}"; n += 1
        heads.append((hid, re.sub(r"<[^>]+>", "", text)))
        return f'<h2 id="{hid}"{m.group(1)}><a class="anchor" href="#{hid}" aria-hidden="true">#</a>{text}</h2>'
    out = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body_html, flags=re.S)
    return out, heads


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def cta_card(app, title=None, text=None, place="article"):
    a = APPS[app]
    href = app_link(app)
    label = f"Get {a['name']} — free" if a["store"] else f"See {a['name']}"
    defaults = {
        "receiptsnap": ("Every receipt, read and filed in two seconds.",
                        "Point the camera at it. Receipt Snap reads the merchant, date, total and tax on your iPhone and keeps the record there — nothing is uploaded, and there is no account to make."),
        "drivesnap":   ("Every business mile, logged on the day it happens.",
                        "DriveSnap detects drives automatically, asks for the purpose with one swipe, and exports a log an examiner can read. No drive caps; your location history never leaves the phone."),
    }
    t, x = defaults[app]
    return f'''<aside class="cta-card">
  <div><span class="k">{a['name']}</span><h3>{title or t}</h3><p>{text or x}</p>
    <p class="fine">{"App Store · Free · Data Not Collected" if a["store"] else "iPhone · No drive caps · Free to track"}</p></div>
  <a class="btn btn-primary" href="{href}" data-app="{app}" data-place="{place}">{label}</a>
</aside>'''


def rail_card(app):
    a = APPS[app]
    href = app_link(app)
    copy = {"receiptsnap": "Reads a receipt on your iPhone in two seconds and keeps it there. Free, no account.",
            "drivesnap": "Logs every business drive automatically. No caps, nothing uploaded."}[app]
    return f'''<div class="rail-card"><span class="k">From Dune Apps</span><h4>{a['name']}</h4><p>{copy}</p>
  <a class="btn btn-primary btn-sm" href="{href}" data-app="{app}" data-place="rail">{"Get it free" if a["store"] else "See the app"}</a></div>'''


def faq_html(pairs):
    items = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)
    return f'<section class="faqs" style="margin-top:54px"><h2 id="questions">Questions people ask</h2><div style="margin-top:18px">{items}</div></section>'


def faq_ld(pairs):
    return {"@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q),
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                           for q, a in pairs]}


FAQ_CSS = """
  details.faq { background: var(--card); border-radius: var(--radius-sm); padding: 18px 22px;
    margin-bottom: 10px; box-shadow: var(--e1); }
  details.faq summary { font-size: 1.04rem; font-weight: 600; color: var(--text); cursor: pointer;
    list-style: none; display: flex; justify-content: space-between; gap: 20px; }
  details.faq summary::-webkit-details-marker { display: none; }
  details.faq summary::after { content: '+'; color: var(--teal); font-size: 1.3rem; line-height: 1; }
  details.faq[open] summary::after { content: '\\2013'; }
  details.faq p { margin-top: 12px; color: var(--muted); line-height: 1.6; }
"""


def render_article(post, index):
    """post: dict from content_posts.POSTS. index: slug -> post, for related cards."""
    body, heads = add_heading_ids(post["body"])
    mins = reading_minutes(post["body"])
    app = post.get("cta")
    card = cta_card(app, post.get("cta_title"), post.get("cta_text")) if app else ""
    if "<!--cta-->" in body:
        body = body.replace("<!--cta-->", card, 1)
    else:
        body += card

    toc_links = "".join(f'<a href="#{hid}">{html.escape(t)}</a>' for hid, t in heads)
    if post.get("faq"):
        toc_links += '<a href="#questions">Questions people ask</a>'
    toc = f'<nav class="toc" aria-label="On this page"><div class="label">On this page</div>{toc_links}</nav>'

    takeaways = ""
    if post.get("takeaways"):
        takeaways = ('<div class="takeaways"><div class="label">Key takeaways</div><ul>'
                     + "".join(f"<li>{t}</li>" for t in post["takeaways"]) + "</ul></div>")

    checked = f'<p class="checked">{post["checked"]}</p>' if post.get("checked") else ""

    sources = ""
    if post.get("sources"):
        sources = ('<section class="sources"><div class="label">Sources</div><ol>'
                   + "".join(f'<li><a href="{u}" rel="noopener">{html.escape(l)}</a></li>' for l, u in post["sources"])
                   + "</ol></section>")

    related = ""
    rel = [index[s] for s in post.get("related", []) if s in index]
    if rel:
        cards = "".join(
            f'<a class="post-card" href="/{r["out"]}"><span class="topic">{r["topic"]}</span><h3>{r["title"]}</h3>'
            f'<span class="when">{nice_date(r["updated"])} · {reading_minutes(r["body"])} min</span></a>' for r in rel)
        related = f'<section class="related"><div class="label">Keep reading</div><div class="grid">{cards}</div></section>'

    author = '''<div class="author"><span class="mark" aria-hidden="true"></span><div>
  <h4>Written by Nahid Saleem</h4>
  <p>Founder of Dune Apps. These guides come out of the research done to build Receipt Snap and DriveSnap. Every rule quoted here is one the apps had to get right. Not tax advice; check your own position with your tax authority or accountant.</p></div></div>'''

    dek = post.get("dek") or post["description"]
    updated = post["updated"]
    published = post["date_iso"]
    meta = (f'<div class="meta"><span>By <b>Nahid Saleem</b></span><span class="dot"></span>'
            f'<span>Updated <b>{nice_date(updated)}</b></span><span class="dot"></span><span>{mins} min read</span></div>')

    article = f'''<div class="wrap"><div class="article-page">
<article class="art-main">
  <nav class="crumbs" aria-label="Breadcrumb"><span><a href="/">Home</a></span><span><a href="/writing/">Guides</a></span><span>{post["topic"]}</span></nav>
  <header class="art-head">
    <span class="topic">{post["topic"]}</span>
    <h1>{post["title"]}</h1>
    <p class="dek">{dek}</p>
    {meta}
    {checked}
  </header>
  {takeaways}
  <details class="toc-m"><summary>On this page</summary>{toc}</details>
  <div class="prose">
{body}
  </div>
  {faq_html(post["faq"]) if post.get("faq") else ""}
  {sources}
  <p class="disclaimer">{post.get("disclaimer", "General information, not tax advice. Rules and rates change; check the current position with your tax authority or an accountant before filing.")}</p>
  {author}
  {related}
</article>
<aside class="art-rail">
  {toc}
  {rail_card(app) if app else ""}
</aside>
</div></div>
{post.get("script", "")}'''

    url = f"{SITE}/{post['out']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": post["title"],
         "description": post["description"], "datePublished": published, "dateModified": updated,
         "author": {"@id": SITE + "/#nahid"}, "publisher": {"@id": SITE + "/#org"},
         "mainEntityOfPage": url, "image": f"{SITE}/{post.get('og', 'og-writing.png')}",
         "articleSection": post["topic"], "inLanguage": "en"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/writing/"},
            {"@type": "ListItem", "position": 3, "name": post["title"], "item": url}]},
    ]}
    if post.get("faq"):
        ld["@graph"].append(faq_ld(post["faq"]))
    head = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"
    head += f'<meta property="article:published_time" content="{published}"><meta property="article:modified_time" content="{updated}">'

    # <title> stays inside Google's ~60-character display; the suffix is added
    # only when it fits. The long, descriptive title remains the on-page h1.
    seo_t = post.get("seo_title") or post["title"]
    page_title = f"{seo_t} · Dune Apps" if len(seo_t) + 12 <= 62 else seo_t
    return render(out=post["out"], title=page_title, description=post.get("meta") or post["description"],
                  canonical=url, body=article, style=FAQ_CSS + post.get("style", ""), head=head,
                  og_image=post.get("og", "og-writing.png"), og_type="article", lastmod=updated, priority="0.8")


# ---------------------------------------------------------------------------
# Creator / channel redirect pages
# ---------------------------------------------------------------------------
def render_go_pages():
    for name in CREATORS:
        for app, path in (("receiptsnap", f"go/{name}/index.html"), ("drivesnap", f"go/{name}/drivesnap/index.html")):
            target = app_link(app, ct=name)
            if not APPS[app]["store"]:
                target = SITE + APPS[app]["page"]
            body = f'''<div class="wrap go"><div>
  <p class="eyebrow">Dune Apps</p>
  <h1 style="font-size:2rem;margin:14px 0 10px">Taking you to {APPS[app]["name"]}…</h1>
  <p>If nothing happens, <a href="{target}" data-app="{app}" data-place="go-{name}">tap here</a>.</p>
</div></div>
<script>
  try {{ gtag('event', 'creator_click', {{ creator: '{name}', app: '{app}', transport_type: 'beacon' }}); }} catch (e) {{}}
  setTimeout(function () {{ location.replace('{target}'); }}, 350);
</script>'''
            render(out=path, title=f"{APPS[app]['name']} — Dune Apps", description=f"Get {APPS[app]['name']}.",
                   canonical=f"{SITE}/{path.rsplit('/index.html', 1)[0]}/", body=body, noindex=True,
                   head=f'<meta http-equiv="refresh" content="2;url={target}">')


# ---------------------------------------------------------------------------
# Sitemap, robots, llms.txt
# ---------------------------------------------------------------------------
def write_sitemap():
    seen, rows = set(), []
    for out, lastmod, prio in PAGES:
        loc = SITE + "/" + out
        loc = loc[:-len("index.html")] if loc.endswith("index.html") else loc
        if loc in seen:
            continue
        seen.add(loc)
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><priority>{prio}</priority></url>")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"sitemap: {len(rows)} urls")


def write_llms(posts):
    lines = ["# Dune Apps", "",
             "> iPhone tools that keep tax records on the device — Receipt Snap (receipt scanner, on-device OCR, no account) and DriveSnap (automatic mileage log, no drive caps). Both run without servers; the App Store privacy label reads Data Not Collected. The guides answer what tax authorities actually require from receipts and mileage logs, with the rule quoted and the source linked.",
             "", "## Apps",
             f"- [Receipt Snap]({SITE}/receiptsnap/): reads merchant, date, total and tax from a receipt on the iPhone in about two seconds. Free; Pro removes the 15-scan monthly cap. App Store: {APP_STORE}",
             f"- [DriveSnap]({SITE}/drivesnap/): detects drives automatically, one-swipe classification, CSV export and year-end report. No drive caps on the free tier.",
             f"- [DriveSnap vs MileIQ]({SITE}/compare/drivesnap-vs-mileiq/): side-by-side, including where MileIQ is better.",
             "", "## Guides"]
    for p in posts:
        lines.append(f"- [{p['title']}]({SITE}/{p['out']}): {p['description']}")
    lines += ["", "## Tools",
              f"- [Free mileage log template]({SITE}/posts/mileage-log-template.html) — CSV download and a printable sheet.",
              f"- [Printable mileage log]({SITE}/templates/mileage-log/)",
              "", "## Facts the guides are built on (verified September 2026)",
              "- IRS standard mileage rate 2026: 72.5 cents/mile 1 Jan–30 Jun; 76 cents/mile 1 Jul–31 Dec. 2025 was 70 cents.",
              "- IRS: receipts not required for expenses under $75 except lodging (Publication 463); keep records 3 years, 6 if income understated by more than 25%.",
              "- HMRC approved mileage rate: 55p/mile for the first 10,000 business miles from 6 April 2026 (45p before), 25p after; self-employed keep records 5 years after the 31 January deadline; VAT records 6 years.",
              "- ATO: written evidence required when total work-related claims exceed $300; records kept 5 years.",
              "- CRA: records kept 6 years from the end of the tax year they relate to.",
              "- UAE FTA: VAT records kept 5 years; 15 years for real estate."]
    (ROOT / "llms.txt").write_text("\n".join(lines) + "\n")
    print("llms.txt")
