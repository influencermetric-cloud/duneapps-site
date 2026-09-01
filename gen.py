import json, pathlib
from build import render
from content_posts import POSTS, PROSE_CSS

def faq_ld(pairs):
    return ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
    }) + "</script>")

def faq_html(pairs):
    items = "".join(
        f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)
    return f'''<section class="section" style="background:var(--bg-2)"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Questions</span>
  <h2>Straight answers</h2></div>
  <div style="margin-top:30px">{items}</div></div></section>'''

FAQ_CSS = """
  details.faq { background: var(--card); border-radius: var(--radius-sm); padding: 22px 26px;
    margin-bottom: 12px; box-shadow: 0 2px 12px rgba(14,19,21,.04); }
  details.faq summary { font-size: 1.1rem; font-weight: 600; color: var(--text); cursor: pointer;
    list-style: none; display: flex; justify-content: space-between; gap: 20px; }
  details.faq summary::-webkit-details-marker { display: none; }
  details.faq summary::after { content: '+'; color: var(--teal); font-size: 1.4rem; line-height: 1; }
  details.faq[open] summary::after { content: '\\2013'; }
  details.faq p { margin-top: 14px; max-width: 66ch; }
"""

# ---------- 1. The three guides ----------
for post in POSTS:
    article = f'''<article class="post wrap">
  <p class="kicker">{post["kicker"]}</p>
  <h1>{post["title"]}</h1>
  <p class="byline">{post["date"]} · Dune Apps</p>
  {post["body"]}
  <p style="margin-top:44px"><a href="/writing/">← All writing</a></p>
</article>
{faq_html(post["faq"])}'''
    ld = ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": post["title"], "description": post["description"],
        "datePublished": "2026-09-01",
        "author": {"@type": "Organization", "name": "Dune Apps"},
        "publisher": {"@type": "Organization", "name": "Dune Apps"},
        "mainEntityOfPage": f'https://duneapps.com/{post["out"]}'}) + "</script>") + faq_ld(post["faq"])
    render(out=post["out"], title=f'{post["title"]} — Dune Apps',
           description=post["description"],
           canonical=f'https://duneapps.com/{post["out"]}',
           body=article, style=PROSE_CSS + FAQ_CSS, head=ld)
    print("guide:", post["out"])

# ---------- 2. Writing index ----------
ENTRIES = [
    ("1 Sep 2026", "Guide", "What the IRS actually requires in a mileage log",
     "The four things every trip record must contain, the 2026 rate, and why a reconstructed log fails.",
     "/posts/irs-mileage-log-requirements.html"),
    ("1 Sep 2026", "Guide", "How long do you have to keep receipts for taxes?",
     "Three years in the US, six in the UK, five in the UAE — and what happens when the app holding them shuts down.",
     "/posts/how-long-to-keep-receipts.html"),
    ("1 Sep 2026", "Guide", "What records UAE VAT actually requires you to keep",
     "Five years, fifteen for real estate, and what has to appear on a valid tax invoice.",
     "/posts/uae-vat-record-keeping.html"),
    ("31 Aug 2026", "Building", "The bug that would have shipped",
     "A mileage tracker that silently recorded zero distance for city driving, and four ways it could have put a wrong number on a tax return.",
     "/posts/the-bug-that-would-have-shipped.html"),
    ("30 Aug 2026", "Privacy", "Why receipt apps pay you pennies",
     "The biggest receipt apps are not expense trackers. They are purchase-data companies.",
     "/posts/receipt-apps-pay-you-pennies.html"),
]
rows = "".join(f'''<a class="row reveal" href="{u}">
  <span class="date">{d}<br><span class="cat">{c}</span></span>
  <span><h3>{t}</h3><p>{s}</p></span><span class="arrow">&rarr;</span></a>''' for d, c, t, s, u in ENTRIES)
render(out="writing/index.html", title="Writing — guides on receipts, mileage and private software · Dune Apps",
  description="Practical guides on what tax authorities actually require from your records, plus notes from building software that keeps your data on your phone.",
  canonical="https://duneapps.com/writing/",
  style="""
  .row { display: grid; grid-template-columns: 150px 1fr auto; gap: 26px; align-items: baseline;
    padding: 30px 0; border-bottom: 1px solid var(--line); text-decoration: none; }
  .row:hover h3 { color: var(--teal); }
  .row .date { font-size: .9rem; color: var(--faint); }
  .row .cat { color: var(--teal); font-weight: 600; font-size: .82rem; }
  .row h3 { font-size: 1.32rem; margin-bottom: 7px; transition: color .18s ease; }
  .row .arrow { color: var(--faint); font-size: 1.2rem; }
  @media (max-width: 700px) { .row { grid-template-columns: 1fr; gap: 8px; } .row .arrow { display: none; } }
  """,
  body=f'''<section class="section" style="padding-bottom:40px"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Writing</span>
    <h2 style="font-size:clamp(2.2rem,4.6vw,3.4rem)">Guides, and notes from the workbench</h2>
    <p>What tax authorities actually require from your records — and what building software that keeps your data on your phone really looks like.</p>
  </div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">{rows}</div></section>''')
print("writing index")
