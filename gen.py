"""Guides, the guides hub, the printable mileage log and the CSV template.

Everything here goes through build.render / build.render_article, so the
chrome is byte-identical to every other page.
"""
import csv
import io
import pathlib

from build import render, render_article, nice_date, reading_minutes, ROOT, SITE, APP_STORE
from content_posts import POSTS, INDEX

# ---------- 1. Every guide ----------
for post in POSTS:
    render_article(post, INDEX)
    print("guide:", post["out"])

# ---------- 2. The hub ----------
GROUPS = [
    ("Mileage and the deduction",
     "The rates, the log, and what the IRS and HMRC actually ask to see.",
     ["irs-mileage-rate-2026", "hmrc-mileage-rates-2026", "irs-mileage-log-requirements",
      "mileage-log-template", "forgot-to-track-doordash-miles"]),
    ("Receipts and records",
     "What counts as proof, how long to keep it, and what a valid invoice shows.",
     ["do-you-need-receipts-for-tax-deductions", "how-long-to-keep-receipts", "uae-vat-record-keeping"]),
    ("Privacy",
     "Where your data goes, how to check, and why receipt apps pay you.",
     ["expense-tracker-apps-that-dont-sell-your-data", "receipt-apps-pay-you-pennies"]),
    ("Building in public",
     "Notes from the workbench.",
     ["the-bug-that-would-have-shipped"]),
]
FEATURED = "irs-mileage-rate-2026"


def card(p, featured=False):
    cls = "post-card featured reveal" if featured else "post-card reveal"
    return (f'<a class="{cls}" href="/{p["out"]}"><span class="topic">{p["topic"]}</span>'
            f'<h3>{p["title"]}</h3><p>{p["description"]}</p>'
            f'<span class="when">Updated {nice_date(p["updated"])} · {reading_minutes(p["body"])} min read</span></a>')


groups_html = ""
for name, blurb, slugs in GROUPS:
    cards = "".join(card(INDEX[s]) for s in slugs if s in INDEX)
    groups_html += f'''<section class="hub-group"><div class="wrap">
  <div class="gh"><h2>{name}</h2><p>{blurb}</p></div>
  <div class="grid g-3">{cards}</div>
</div></section>'''

hub_body = f'''<section class="hub-head"><div class="wrap">
  <span class="eyebrow">Guides</span>
  <h1>What the tax authority actually requires — with the rule quoted</h1>
  <p>Practical answers on receipts, mileage and the records behind a deduction, for the US, UK, UAE, Canada and Australia. Every figure is checked against the primary source and dated. Written by the person building the apps.</p>
</div></section>
<section style="padding:0 0 10px"><div class="wrap">
  <div class="grid" style="grid-template-columns:1fr">{card(INDEX[FEATURED], featured=True)}</div>
</div></section>
{groups_html}
<section class="section" style="padding-top:60px"><div class="wrap"><div class="final reveal" style="background:var(--card);border-radius:40px;padding:64px 32px;text-align:center;box-shadow:var(--e2)">
  <h2 style="font-size:clamp(1.8rem,4vw,2.6rem)">The apps do the record-keeping these guides describe.</h2>
  <p style="max-width:56ch;margin:16px auto 0">Receipt Snap reads receipts on your iPhone. DriveSnap logs every business drive automatically. Neither has a server, an account, or anywhere to send your data.</p>
  <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:30px">
    <a class="btn btn-primary" href="{APP_STORE}" data-app="receiptsnap" data-place="hub-footer">Get Receipt Snap — free</a>
    <a class="btn btn-dark" href="/drivesnap/">See DriveSnap</a>
  </div>
</div></div></section>'''

render(out="writing/index.html",
       title="Guides — receipts, mileage and the records tax authorities actually require · Dune Apps",
       description="Practical, sourced guides on what the IRS, HMRC, ATO, CRA and the UAE FTA require from your receipts and mileage logs — rates, retention periods, what counts as proof — from the people building Receipt Snap and DriveSnap.",
       canonical=f"{SITE}/writing/", body=hub_body, og_image="og-writing.png", priority="0.9")
print("guides hub")

# ---------- 3. CSV template ----------
buf = io.StringIO()
w = csv.writer(buf)
w.writerow(["Date", "From", "To", "Business purpose", "Odometer start", "Odometer end",
            "Business miles", "Personal miles", "Rate ($ per mile)", "Deduction ($)", "Parking & tolls ($)", "Notes"])
examples = [
    ["2026-03-14", "Home office", "Acme Corp, 120 Main St", "Client meeting — Q2 contract", 41230, 41252, 22, 0, 0.725, "=G2*I2", 0, "Rate to 30 Jun 2026: 0.725"],
    ["2026-07-08", "Home office", "Bank, then post office", "Deposit cheques; ship samples", 42011, 42019, 8, 0, 0.76, "=G3*I3", 4.5, "Rate from 1 Jul 2026: 0.76"],
]
for r in examples:
    w.writerow(r)
for i in range(4, 30):
    w.writerow(["", "", "", "", "", "", "", "", "", f"=G{i}*I{i}", "", ""])
w.writerow(["TOTAL", "", "", "", "", "", "=SUM(G2:G29)", "=SUM(H2:H29)", "", "=SUM(J2:J29)", "=SUM(K2:K29)",
            "Year-start odometer: ____   Year-end odometer: ____"])
dl = ROOT / "downloads"
dl.mkdir(exist_ok=True)
(dl / "mileage-log-template.csv").write_text(buf.getvalue())
print("csv template")

# ---------- 4. Printable mileage log ----------
rows = "".join("<tr>" + "<td></td>" * 7 + "</tr>" for _ in range(22))
tpl_body = f'''<div class="wrap tpl" style="max-width:1000px;margin:36px auto 80px">
  <div class="no-print" style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;margin-bottom:8px">
    <div><span class="eyebrow">Free template</span><h1 style="font-size:2rem;margin-top:12px">Printable mileage log</h1>
      <p style="max-width:60ch;margin-top:10px">One page, 22 trips. The columns are the ones the IRS and HMRC ask for — date, where, why, miles — plus odometer readings so the miles are provable. Print it and keep it in the glovebox; there is also a <a href="/downloads/mileage-log-template.csv" download>spreadsheet version</a>.</p></div>
    <button class="btn btn-primary" onclick="window.print()">Print this page</button>
  </div>
  <p style="font-size:.9rem;color:var(--faint)" class="no-print">Tip: fill it in the same day, never round the miles, and write the purpose in words a stranger would understand.</p>
  <div style="display:flex;justify-content:space-between;gap:20px;margin-top:22px;font-size:.95rem">
    <span>Vehicle: ______________________</span><span>Year: ________</span>
    <span>Odometer at year start: __________</span><span>Odometer at year end: __________</span>
  </div>
  <table>
    <thead><tr><th style="width:11%">Date</th><th style="width:22%">From → To</th><th style="width:27%">Business purpose</th><th style="width:10%">Odo start</th><th style="width:10%">Odo end</th><th style="width:9%">Miles</th><th style="width:11%">Parking / tolls</th></tr></thead>
    <tbody>{rows}
      <tr><td colspan="5" style="text-align:right;font-weight:600">Page totals</td><td></td><td></td></tr>
    </tbody>
  </table>
  <p style="font-size:.82rem;color:var(--faint);margin-top:14px">IRS 2026 rate: 72.5¢ per business mile to 30 June, 76¢ from 1 July. HMRC 2026/27: 55p for the first 10,000 business miles, then 25p. duneapps.com/posts/mileage-log-template.html</p>
</div>'''
render(out="templates/mileage-log/index.html", title="Printable mileage log (free) — Dune Apps",
       description="A free, printable one-page mileage log with the columns the IRS and HMRC require: date, from/to, business purpose, odometer readings, miles and parking. 22 trips per page.",
       canonical=f"{SITE}/templates/mileage-log/", body=tpl_body, priority="0.6")
print("printable template")
