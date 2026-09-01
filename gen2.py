import json
from build import render

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
PAGE_CSS = """
  .hero { position: relative; padding: 56px 0 92px; overflow: hidden; }
  .hero .split { display: grid; grid-template-columns: 1.05fr .95fr; gap: 48px; align-items: center; }
  .badge { display: inline-flex; align-items: center; gap: 9px; background: var(--card);
    border-radius: 999px; padding: 8px 16px; font-size: .9rem; color: var(--muted);
    box-shadow: 0 2px 12px rgba(14,19,21,.06); }
  .badge b { color: var(--teal); }
  .hero h1 { font-size: clamp(2.4rem, 5vw, 3.9rem); margin: 26px 0 0; }
  .hero .lede { font-size: 1.13rem; max-width: 50ch; margin-top: 22px; }
  .hero .actions { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 34px; }
  .hero .assurances { justify-content: flex-start; }
  .visual { position: relative; min-height: 520px; }
  .bubble { position: absolute; right: -22%; top: 50%; transform: translateY(-50%);
    width: 740px; height: 740px; border-radius: 50%;
    background:
      radial-gradient(circle at 30% 28%, #FFE9A8 0%, transparent 42%),
      radial-gradient(circle at 68% 22%, #A8E4FF 0%, transparent 46%),
      radial-gradient(circle at 74% 74%, #D8B4FE 0%, transparent 48%),
      radial-gradient(circle at 26% 76%, #9BF6D2 0%, transparent 46%),
      conic-gradient(from 210deg, #FDE2E4, #CDE7FF, #E0D4FF, #D6F5E3, #FFF3C4, #FDE2E4);
    filter: blur(2px) saturate(1.12); opacity: .95; }
  .phones { position: relative; z-index: 2; display: flex; gap: 18px;
    align-items: flex-end; justify-content: center; padding: 30px 0; }
  .phones img { width: 200px; border-radius: 22px; box-shadow: 0 24px 54px rgba(14,19,21,.22); }
  .phones img:nth-child(2) { width: 228px; margin-bottom: 28px; }
  @media (max-width: 980px) { .hero .split { grid-template-columns: 1fr; }
    .bubble { right: -30%; width: 600px; height: 600px; } }
  .features { display: grid; gap: 22px; grid-template-columns: repeat(3, 1fr);
    align-items: start; margin-top: 48px; }
  .feat.wide { grid-column: span 2; display: flex; gap: 28px; align-items: center; }
  .feat.wide img { width: 172px; border-radius: 18px; flex: 0 0 auto;
    box-shadow: 0 12px 30px rgba(14,19,21,.14); }
  @media (max-width: 900px) { .features { grid-template-columns: 1fr; }
    .feat.wide { grid-column: auto; flex-direction: column; align-items: flex-start; } }
  .tag { font-size: .82rem; letter-spacing: .08em; text-transform: uppercase;
    color: var(--teal); font-weight: 600; margin-bottom: 10px; }
  .stepline { display: grid; grid-template-columns: 92px 1fr; gap: 26px;
    padding: 32px 0; border-bottom: 1px solid var(--line); align-items: start; }
  .stepline .n { font-size: 2.5rem; font-weight: 600; color: var(--line-2); line-height: 1; }
  .stepline h3 { font-size: 1.28rem; margin-bottom: 8px; }
  table.cmp { width: 100%; border-collapse: collapse; margin-top: 40px;
    background: var(--card); border-radius: var(--radius); overflow: hidden;
    box-shadow: 0 2px 16px rgba(14,19,21,.05); }
  table.cmp th, table.cmp td { text-align: left; padding: 20px 24px; border-bottom: 1px solid var(--line); }
  table.cmp tbody tr:last-child td { border-bottom: 0; }
  table.cmp thead th { font-size: .8rem; letter-spacing: .1em; text-transform: uppercase;
    color: var(--faint); font-weight: 600; }
  table.cmp td.ours { color: var(--teal); font-weight: 600; }
  table.cmp td.them { color: var(--faint); }
  .note { font-size: .88rem; color: var(--faint); margin-top: 16px; }
  .final { background: var(--card); border-radius: 40px; padding: 84px 40px; text-align: center;
    box-shadow: 0 4px 30px rgba(14,19,21,.06); }
  .final h2 { font-size: clamp(2rem, 4.4vw, 3rem); }
  .final .actions { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; margin-top: 32px; }
"""

def faq_block(pairs):
    items = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)
    return f'''<section class="section" style="background:var(--bg-2)"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Questions</span><h2>Straight answers</h2></div>
  <div style="margin-top:30px">{items}</div></div></section>'''

def faq_ld(pairs):
    return ('<script type="application/ld+json">' + json.dumps({
      "@context":"https://schema.org","@type":"FAQPage",
      "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pairs]}) + "</script>")

# ---------------- Receipt Snap ----------------
RS_FAQ = [
 ("Does Receipt Snap upload my receipts?","No. The photo is read on your iPhone using Apple's on-device text recognition, and the result is stored on the device. There is no account and no Receipt Snap server — the App Store privacy label reads Data Not Collected."),
 ("Which currencies does it recognise?","Twelve, detected from the receipt itself. Where no symbol is printed it reads the tax registration number instead — a UAE TRN means dirhams, an Indian GSTIN means rupees, a UK postcode means sterling."),
 ("Do photographs of receipts count as tax records?","Yes. The IRS, HMRC and the UAE Federal Tax Authority all accept electronic records provided they are legible, complete and producible on request. Photograph the whole receipt, including the tax line."),
 ("What does it cost?","Receipt Snap is free. A Pro tier is planned for a later version; scanning and searching your receipts will stay free."),
 ("What happens if the scan gets something wrong?","Every field is editable before you save, and you can re-crop the photo by dragging the corners if the automatic crop misses. Nothing is filed without you seeing it."),
]
RS_BODY = f'''<section class="hero"><div class="wrap split">
  <div>
    <span class="badge">Free · <b>Data Not Collected</b></span>
    <h1>Your receipts, read on your phone and kept there</h1>
    <p class="lede">Point the camera at a receipt. Receipt Snap reads the merchant, date, total and tax in about two seconds, files it, and never sends it anywhere.</p>
    <div class="actions">
      <a class="btn btn-primary" href="#how">How it works</a>
      <a class="btn btn-dark" href="/posts/how-long-to-keep-receipts.html">How long to keep receipts</a>
    </div>
    <div class="assurances"><span>No account</span><span>0 servers</span><span>12 currencies</span></div>
  </div>
  <div class="visual"><div class="bubble"></div><div class="phones">
    <img src="/assets/receiptsnap-2.png" alt="Searching receipts" loading="lazy">
    <img src="/assets/receiptsnap-1.png" alt="Receipt Snap home screen" loading="lazy">
    <img src="/assets/receiptsnap-3.png" alt="Monthly spending summary" loading="lazy">
  </div></div>
</div></section>

<div class="wrap marquee-wrap" style="margin-top:60px"><div class="marquee">
  <span>Vision OCR</span><span>·</span><span>Apple Foundation Models</span><span>·</span><span>GSTIN</span><span>·</span>
  <span>UAE TRN</span><span>·</span><span>VAT</span><span>·</span><span>CSV export</span><span>·</span><span>Works offline</span><span>·</span>
  <span>Vision OCR</span><span>·</span><span>Apple Foundation Models</span><span>·</span><span>GSTIN</span><span>·</span>
  <span>UAE TRN</span><span>·</span><span>VAT</span><span>·</span><span>CSV export</span><span>·</span><span>Works offline</span><span>·</span>
</div></div>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Built for the actual job</span>
    <h2>Reads the receipt.<br>Keeps it to itself.</h2></div>
  <div class="features">
    <div class="card feat wide reveal">
      <img src="/assets/receiptsnap-1.png" alt="Receipt Snap home" loading="lazy">
      <div><p class="tag">01 · On device</p><h3>Two seconds, no upload</h3>
      <p>Apple's Vision framework reads the text on the phone, and on newer iPhones an on-device model pulls structure out of it. The receipt never has to leave the device to be understood.</p></div>
    </div>
    <div class="card feat reveal"><p class="tag">02 · Currency</p><h3>Reads the tax number</h3>
      <p>Where no symbol is printed, it recognises a UAE TRN, an Indian GSTIN or a UK postcode and sets the currency from that.</p></div>
    <div class="card feat reveal"><p class="tag">03 · Search</p><h3>Find it in words</h3>
      <p>Search naturally — "coffee in July" — and filter any month or date range.</p></div>
    <div class="card feat wide reveal">
      <img src="/assets/receiptsnap-3.png" alt="Monthly summary" loading="lazy">
      <div><p class="tag">04 · At year end</p><h3>A summary you can hand over</h3>
      <p>Browse any month, tap a category to see everything spent on it, and share a summary card. Deleted receipts stay recoverable for 30 days.</p></div>
    </div>
  </div>
</div></section>

<section class="section" id="how" style="background:var(--bg-2)"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">From paper to filed</span><h2>Three steps</h2></div>
  <div style="margin-top:34px">
    <div class="stepline reveal"><div class="n">01</div><div><h3>Photograph it the day you get it</h3><p>Thermal paper fades — sometimes within months in a hot car. The shutter fires immediately; there is no waiting for the app to find the edges.</p></div></div>
    <div class="stepline reveal"><div class="n">02</div><div><h3>Check what it read</h3><p>Merchant, date, total and tax come back filled in. Every field is editable, and you can drag the corners to re-crop if the automatic crop misses.</p></div></div>
    <div class="stepline reveal"><div class="n">03</div><div><h3>Find it years later</h3><p>Search by word, month or category. Records need keeping for three years in the US, five in the UAE, fifteen for UAE property.</p></div></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Why it matters</span>
    <h2>Most receipt apps are not expense trackers</h2>
    <p>They are purchase-data companies. You photograph a receipt, they sell what you bought, to whom, at what price and how often. The points you earn are the price they pay for it.</p></div>
  <table class="cmp reveal">
    <thead><tr><th>&nbsp;</th><th style="color:var(--teal)">Receipt Snap</th><th>Points-and-rewards receipt apps</th></tr></thead>
    <tbody>
      <tr><td>Where the photo goes</td><td class="ours">Nowhere — it stays on the phone</td><td class="them">Their servers</td></tr>
      <tr><td>Account required</td><td class="ours">Never</td><td class="them">Yes</td></tr>
      <tr><td>Purchase data sold</td><td class="ours">Never</td><td class="them">That is the business model</td></tr>
      <tr><td>App Store privacy label</td><td class="ours">Data Not Collected</td><td class="them">Linked to you</td></tr>
    </tbody>
  </table>
  <p class="note"><a href="/posts/receipt-apps-pay-you-pennies.html">The long version, with the numbers →</a></p>
</div></section>

{faq_block(RS_FAQ)}

<section class="section"><div class="wrap"><div class="final reveal">
  <h2>A receipt vault that has nowhere<br>to send your receipts.</h2>
  <div class="actions">
    <a class="btn btn-primary" href="/posts/how-long-to-keep-receipts.html">How long to keep receipts</a>
    <a class="btn btn-dark" href="/">More from Dune Apps</a></div>
  <div class="assurances" style="justify-content:center"><span>Free</span><span>No account</span><span>iOS 17 or later</span></div>
</div></div></section>'''

render(out="receiptsnap/index.html",
  title="Receipt Snap — receipts read on your phone and kept there",
  description="Receipt Snap reads the merchant, date, total and tax from a receipt on your iPhone in about two seconds. No account, no servers, nothing uploaded. Twelve currencies, recognised from the receipt.",
  canonical="https://duneapps.com/receiptsnap/",
  body=RS_BODY, style=PAGE_CSS + FAQ_CSS, og_image="og-receiptsnap.png",
  head=faq_ld(RS_FAQ) + '<script type="application/ld+json">' + json.dumps({
    "@context":"https://schema.org","@type":"SoftwareApplication","name":"Receipt Snap",
    "applicationCategory":"FinanceApplication","operatingSystem":"iOS 17.0 or later",
    "description":"On-device receipt scanner. Reads merchant, date, total and tax on the iPhone; nothing is uploaded.",
    "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}) + "</script>")
print("receiptsnap page")

# ---------------- DriveSnap vs MileIQ ----------------
CMP_FAQ = [
 ("Is DriveSnap a good MileIQ alternative?","If you want automatic drive detection without a monthly drive cap and without your location history leaving the phone, yes. If you need a web dashboard, team administration or multi-user reporting, MileIQ does those and DriveSnap does not."),
 ("Does MileIQ have a free drive limit?","MileIQ's free tier is limited to 40 drives per month. Once you pass it, drives stop being logged until the next month or until you subscribe. DriveSnap has no cap on the free tier."),
 ("How much does each cost?","MileIQ Unlimited is listed at $59.99 a year, with a premium tier at $119.99. DriveSnap Pro is $29.99 a year with the first month free, or $79.99 once for life. DriveSnap's tracking is free and uncapped either way."),
 ("Can I move my MileIQ history into DriveSnap?","Not automatically. DriveSnap can import its own backup file, but there is no MileIQ importer. Drives already filed for a past tax year are usually best left where they are, with an export kept for your records."),
 ("Which one should I choose?","Choose MileIQ if you need a team product with a web dashboard. Choose DriveSnap if you are self-employed or a sole trader, you want an uncapped free tier, and you would rather your location history stayed on your own device."),
]
CMP_BODY = f'''<section class="hero"><div class="wrap split">
  <div>
    <span class="badge">Comparison · <b>Updated Sep 2026</b></span>
    <h1>DriveSnap vs MileIQ</h1>
    <p class="lede">Both detect drives automatically and both produce a tax report. They differ on three things that matter: whether the free tier stops logging, where your location history lives, and what a year costs.</p>
    <div class="actions">
      <a class="btn btn-primary" href="#table">See the comparison</a>
      <a class="btn btn-dark" href="/drivesnap/">About DriveSnap</a>
    </div>
    <div class="assurances"><span>No drive caps</span><span>Nothing uploaded</span><span>$29.99/yr</span></div>
  </div>
  <div class="visual"><div class="bubble"></div><div class="phones">
    <img src="/assets/drivesnap-2.png" alt="Classifying a drive" loading="lazy">
    <img src="/assets/drivesnap-1.png" alt="DriveSnap home screen" loading="lazy">
    <img src="/assets/drivesnap-3.png" alt="Tax report" loading="lazy">
  </div></div>
</div></section>

<section class="section" id="table"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Side by side</span><h2>The differences that decide it</h2></div>
  <table class="cmp reveal">
    <thead><tr><th>&nbsp;</th><th style="color:var(--teal)">DriveSnap</th><th>MileIQ</th></tr></thead>
    <tbody>
      <tr><td>Free drives per month</td><td class="ours">Unlimited</td><td class="them">40, then logging stops</td></tr>
      <tr><td>Where location history lives</td><td class="ours">Only on your iPhone</td><td class="them">Their servers</td></tr>
      <tr><td>Account required</td><td class="ours">No</td><td class="them">Yes</td></tr>
      <tr><td>Yearly price</td><td class="ours">$29.99 · first month free</td><td class="them">$59.99 · $119.99 premium</td></tr>
      <tr><td>Lifetime option</td><td class="ours">$79.99</td><td class="them">None</td></tr>
      <tr><td>Automatic drive detection</td><td class="ours">Yes</td><td class="them">Yes</td></tr>
      <tr><td>Swipe to classify</td><td class="ours">Yes</td><td class="them">Yes</td></tr>
      <tr><td>Work-hours auto-classification</td><td class="ours">Yes</td><td class="them">Yes</td></tr>
      <tr><td>Web dashboard</td><td class="them">No</td><td class="ours" style="color:var(--faint);font-weight:400">Yes</td></tr>
      <tr><td>Teams and admin reporting</td><td class="them">No</td><td class="ours" style="color:var(--faint);font-weight:400">Yes</td></tr>
      <tr><td>Platforms</td><td class="them">iPhone only</td><td class="ours" style="color:var(--faint);font-weight:400">iPhone, Android, web</td></tr>
    </tbody>
  </table>
  <p class="note">MileIQ figures are US App Store list prices and published tier limits, September 2026. Rows where MileIQ is stronger are shown plainly rather than left out.</p>
</div></section>

<section class="section" style="background:var(--bg-2)"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">The honest summary</span><h2>Which one you should pick</h2></div>
  <div class="grid g-2" style="margin-top:40px">
    <div class="card reveal"><h3>Choose MileIQ if…</h3>
      <p>You run a team and need a web dashboard, administrator reporting or per-employee reimbursement. You use Android, or you need the same account across a phone and a desktop. Those are real products DriveSnap does not have, and no amount of privacy makes up for a missing dashboard you actually need.</p></div>
    <div class="card reveal"><h3>Choose DriveSnap if…</h3>
      <p>You are self-employed or a sole trader logging your own driving. You want a free tier that never stops recording mid-month, a cheaper subscription, and your location history to stay on your own device. And you would rather pay once, for life, than subscribe forever.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">The cap</span><h2>Why 40 drives a month is the real issue</h2>
    <p>It is not that the free tier ends. It is <em>where</em> it ends. Pass the cap on the 18th and the rest of the month is simply missing from your log — and a mileage record with a hole in it is not a partial record, it is an unusable one. That is the complaint that appears most often in reviews of capped trackers, and it is why DriveSnap gates the export instead of the logging.</p>
    <p style="margin-top:18px"><a href="/posts/irs-mileage-log-requirements.html">What the IRS actually requires in a mileage log →</a></p></div>
</div></section>

{faq_block(CMP_FAQ)}

<section class="section"><div class="wrap"><div class="final reveal">
  <h2>Uncapped tracking.<br>Nothing uploaded.</h2>
  <div class="actions">
    <a class="btn btn-primary" href="/drivesnap/">See DriveSnap</a>
    <a class="btn btn-dark" href="/writing/">Read the guides</a></div>
  <div class="assurances" style="justify-content:center"><span>Free to track</span><span>No account</span><span>$29.99/yr for export</span></div>
</div></div></section>'''

render(out="compare/drivesnap-vs-mileiq/index.html",
  title="DriveSnap vs MileIQ — an honest comparison (2026)",
  description="MileIQ caps free users at 40 drives a month and stores your location history on its servers. DriveSnap has no cap and keeps drives on your phone. Full side-by-side, including where MileIQ is better.",
  canonical="https://duneapps.com/compare/drivesnap-vs-mileiq/",
  body=CMP_BODY, style=PAGE_CSS + FAQ_CSS, og_image="og-compare.png", head=faq_ld(CMP_FAQ))
print("comparison page")
