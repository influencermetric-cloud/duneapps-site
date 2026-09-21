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
      "mileage-log-template", "mileage-log-for-irs-audit", "forgot-to-track-doordash-miles",
      "is-mileiq-free"]),
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
       title="Guides: receipts, mileage and tax records · Dune Apps",
       description="Sourced guides on what the IRS, HMRC, ATO, CRA and UAE FTA require from receipts and mileage logs — rates, retention periods, and what counts as proof.",
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
      <p style="max-width:60ch;margin-top:10px">One page, 22 trips. The columns are the ones the IRS and HMRC ask for: date, where, why, miles, plus odometer readings so the miles are provable. Print it and keep it in the glovebox. There is also an <a href="/downloads/mileage-log-template.xlsx" download>Excel workbook</a>, a <a href="/downloads/mileage-log-template.csv" download>CSV</a> and a <a href="/downloads/mileage-log-template.pdf">ready made PDF</a>.</p></div>
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
  <p style="font-size:.82rem;color:var(--faint);margin-top:14px">IRS 2026 rate: 72.5¢ per business mile to 30 June, 76¢ from 1 July. HMRC 2026/27: 55p for the first 10,000 business miles, then 25p. Rates checked against IRS.gov and GOV.UK on 21 September 2026. Free template and guide at duneapps.com</p>
</div>'''
render(out="templates/mileage-log/index.html", title="Printable mileage log (free) · Dune Apps",
       description="A free printable one page mileage log with the columns the IRS and HMRC require: date, from and to, purpose, odometer, miles, parking. 24 trips a page.",
       canonical=f"{SITE}/templates/mileage-log/", body=tpl_body, priority="0.6")
print("printable template")

# ---------- 5. Real XLSX and PDF, when the libraries are available ----------
# The site build itself is stdlib only, so these are generated when openpyxl
# and reportlab happen to be installed and the committed files in downloads/
# are simply left alone otherwise. Regenerate after a rate change with:
#   python3 -m venv .venv && .venv/bin/pip install openpyxl reportlab
#   .venv/bin/python build_all.py
HEADERS = ["Date", "From", "To", "Business purpose", "Odometer start", "Odometer end",
           "Business miles", "Personal miles", "Rate ($/mile)", "Deduction ($)",
           "Parking & tolls ($)", "Notes"]
EXAMPLE = ["2026-03-14", "Home office", "Acme Corp, 120 Main St", "Client meeting, Q2 contract",
           41230, 41252, 22, 0, 0.725, None, 0, "Rate to 30 Jun 2026: 0.725"]
EXAMPLE2 = ["2026-07-08", "Home office", "Bank, then post office", "Deposit cheques; ship samples",
            42011, 42019, 8, 0, 0.76, None, 4.5, "Rate from 1 Jul 2026: 0.76"]
RATE_NOTE = ("IRS 2026: 72.5¢ a business mile to 30 June, 76¢ from 1 July. "
             "HMRC 2026/27: 55p for the first 10,000 business miles, then 25p. "
             "Checked against IRS.gov and GOV.UK on 21 September 2026.")

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    Workbook = None

if Workbook:
    wb = Workbook()
    ws = wb.active
    ws.title = "2026 mileage log"
    ink, teal = "0E1315", "1A4B44"
    thin = Side(style="thin", color="D5DBDD")
    ws.append(HEADERS)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF", size=11)
        c.fill = PatternFill("solid", fgColor=teal)
        c.alignment = Alignment(vertical="center", wrap_text=True)
        c.border = Border(bottom=thin)
    ROWS = 60
    for n, ex in enumerate(( EXAMPLE, EXAMPLE2 ), start=2):
        ws.append(ex)
        ws.cell(row=n, column=10).value = f"=IF(G{n}=\"\",\"\",G{n}*I{n})"
    for n in range(4, ROWS + 2):
        ws.cell(row=n, column=10).value = f"=IF(G{n}=\"\",\"\",G{n}*I{n})"
    tot = ROWS + 2
    ws.cell(row=tot, column=1).value = "TOTAL"
    for col in (7, 8, 10, 11):
        L = get_column_letter(col)
        ws.cell(row=tot, column=col).value = f"=SUM({L}2:{L}{ROWS + 1})"
    for c in ws[tot]:
        c.font = Font(bold=True, color=ink)
        c.border = Border(top=thin)
    for col, w in zip(range(1, 13), (12, 20, 30, 34, 15, 15, 14, 14, 13, 14, 17, 30)):
        ws.column_dimensions[get_column_letter(col)].width = w
    for n in range(2, tot + 1):
        ws.cell(row=n, column=9).number_format = "0.000"
        for col in (10, 11):
            ws.cell(row=n, column=col).number_format = "#,##0.00"
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:L{ROWS + 1}"

    rm = wb.create_sheet("Read me")
    for row in [
        ["Free mileage log, 2026"],
        [],
        ["What every trip must show"],
        ["Date", "The date of the trip. It also decides which rate applies."],
        ["Destination", "A place a stranger could find. \"Client\" is not a destination."],
        ["Business purpose", "In words. \"Site survey before quoting\", not \"work\"."],
        ["Miles", "Measured, not rounded. 14.3, not 15."],
        [],
        ["Once a year"],
        ["Odometer", "Write the reading down on 1 January and 31 December, with the date."],
        [],
        ["Rates"],
        ["IRS 2026", "72.5 cents a business mile to 30 June, 76 cents from 1 July."],
        ["IRS medical", "20.5 cents to 30 June, 23.5 cents from 1 July."],
        ["IRS charitable", "14 cents all year."],
        ["HMRC 2026/27", "55p for the first 10,000 business miles from 6 April 2026, then 25p."],
        [],
        ["Keeping it so it holds up"],
        ["", "Fill it in the same day, or at the latest the same week. IRS Publication 463 treats"],
        ["", "a log kept weekly that accounts for the week's use as a timely kept record."],
        ["", "A year written up in April is a statement prepared later, and it is worth less."],
        [],
        ["Checked", RATE_NOTE],
        ["Source", "https://www.irs.gov/tax-professionals/standard-mileage-rates"],
        ["Source", "https://www.irs.gov/publications/p463"],
        ["Source", "https://www.gov.uk/expenses-and-benefits-business-travel-mileage/rules-for-tax"],
        ["From", "https://duneapps.com/posts/mileage-log-template.html"],
    ]:
        rm.append(row)
    for r in (1, 3, 9, 12, 18):
        rm.cell(row=r, column=1).font = Font(bold=True, color=teal, size=13 if r == 1 else 11)
    rm.column_dimensions["A"].width = 20
    rm.column_dimensions["B"].width = 96
    wb.save(dl / "mileage-log-template.xlsx")
    print("xlsx template")

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as pdfcanvas
except ImportError:
    pdfcanvas = None

if pdfcanvas:
    W, H = landscape(A4)
    c = pdfcanvas.Canvas(str(dl / "mileage-log-template.pdf"), pagesize=(W, H))
    c.setTitle("Free mileage log 2026")
    c.setAuthor("Dune Apps")
    c.setSubject("Printable mileage log with the fields the IRS and HMRC require")
    TEAL = colors.HexColor("#1A4B44")
    INK = colors.HexColor("#0E1315")
    GREY = colors.HexColor("#59666A")
    LINE = colors.HexColor("#C9D2D4")
    L, R = 12 * mm, W - 12 * mm
    y = H - 14 * mm
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 15)
    c.drawString(L, y, "Mileage log 2026")
    c.setFont("Helvetica", 9); c.setFillColor(GREY)
    c.drawRightString(R, y + 1, "duneapps.com/posts/mileage-log-template.html")
    y -= 7 * mm
    c.setFont("Helvetica", 8.5)
    c.drawString(L, y, "Fill it in the same day. Write the purpose in words. Do not round the miles.")
    y -= 8 * mm
    c.setFont("Helvetica", 9); c.setFillColor(INK)
    x_at = L
    for label, w in (("Vehicle", 74 * mm), ("Year", 30 * mm),
                     ("Odometer at year start", 84 * mm), ("Odometer at year end", 84 * mm)):
        c.drawString(x_at, y, label + ":")
        c.setStrokeColor(LINE); c.setLineWidth(0.6)
        c.line(x_at + c.stringWidth(label + ": ", "Helvetica", 9), y - 1.2, x_at + w - 8 * mm, y - 1.2)
        x_at += w
    y -= 9 * mm

    COLS = [("Date", 20), ("From", 34), ("To", 42), ("Business purpose", 62),
            ("Odo start", 22), ("Odo end", 22), ("Miles", 18), ("Parking / tolls", 26)]
    total = sum(w for _, w in COLS)
    scale = (R - L) / (total * mm)
    xs, x = [], L
    for name, w in COLS:
        xs.append((name, x, w * mm * scale)); x += w * mm * scale

    head_h = 7 * mm
    c.setFillColor(TEAL); c.rect(L, y - head_h, R - L, head_h, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 8.5)
    for name, x0, w in xs:
        c.drawString(x0 + 2 * mm, y - head_h + 2.3 * mm, name)
    y -= head_h

    ROWS_PDF = 24
    row_h = (y - 22 * mm) / ROWS_PDF
    c.setStrokeColor(LINE); c.setLineWidth(0.5)
    top = y
    # One worked example, printed faintly, so the form explains itself.
    c.setFillColor(colors.HexColor("#F3F6F6")); c.rect(L, top - row_h, R - L, row_h, stroke=0, fill=1)
    c.setFillColor(GREY); c.setFont("Helvetica-Oblique", 7.6)
    for (name, x0, w), val in zip(xs, ["14 Mar 2026", "Home office", "Acme Corp, 120 Main St",
                                       "Client meeting, Q2 contract", "41230", "41252", "22", "0.00"]):
        c.drawString(x0 + 2 * mm, top - row_h + 2.2 * mm, val)
    for i in range(ROWS_PDF + 1):
        yy = y - i * row_h
        c.line(L, yy, R, yy)
    for _, x0, w in xs:
        c.line(x0, top, x0, top - ROWS_PDF * row_h)
    c.line(R, top, R, top - ROWS_PDF * row_h)

    y = top - ROWS_PDF * row_h - 6 * mm
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(L, y, "Page total, business miles: ______________")
    c.drawString(L + 78 * mm, y, "Parking and tolls: ______________")
    y -= 5.5 * mm
    c.setFillColor(GREY); c.setFont("Helvetica", 7.4)
    c.drawString(L, y, RATE_NOTE)
    y -= 4 * mm
    c.drawString(L, y, "Every trip needs four things: the date, where you went, why, and the miles. "
                       "Keep odometer readings for 1 January and 31 December so the yearly total can be shown.")
    c.showPage()
    c.save()
    print("pdf template")
