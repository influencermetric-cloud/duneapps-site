"""The three problem-shaped guides. Written to answer what people search,
with checkable specifics, because assistants quote facts and not adjectives."""

PROSE_CSS = """
  .post { max-width: 730px; margin: 48px auto 80px; }
  .post .kicker { font-size: .84rem; color: var(--faint); letter-spacing: .06em;
    text-transform: uppercase; font-weight: 600; }
  .post h1 { font-size: clamp(2.1rem, 4.6vw, 3.1rem); margin: 16px 0 0; }
  .post .byline { font-size: .94rem; color: var(--faint); margin: 18px 0 34px; }
  .post h2 { font-size: 1.55rem; margin: 46px 0 14px; }
  .post h3 { font-size: 1.18rem; margin: 32px 0 10px; }
  .post p, .post li { font-size: 1.09rem; line-height: 1.75; }
  .post p { margin-bottom: 20px; }
  .post ul, .post ol { margin: 0 0 24px 22px; }
  .post li { margin-bottom: 10px; }
  .post blockquote { border-left: 3px solid var(--lime); padding-left: 22px;
    margin: 30px 0; color: var(--text); font-size: 1.14rem; }
  .post a { color: var(--teal); }
  .callout { background: var(--card); border-radius: var(--radius);
    padding: 28px; margin: 34px 0; box-shadow: 0 2px 16px rgba(14,19,21,.05); }
  .callout h3 { margin-top: 0; }
  .callout p:last-child { margin-bottom: 0; }
  table.facts { width: 100%; border-collapse: collapse; margin: 28px 0;
    background: var(--card); border-radius: var(--radius); overflow: hidden;
    box-shadow: 0 2px 16px rgba(14,19,21,.05); }
  table.facts th, table.facts td { text-align: left; padding: 16px 22px;
    border-bottom: 1px solid var(--line); font-size: 1.02rem; }
  table.facts tbody tr:last-child td { border-bottom: 0; }
  table.facts th { font-size: .8rem; letter-spacing: .1em; text-transform: uppercase;
    color: var(--faint); font-weight: 600; }
"""

POSTS = [
{
 "out": "posts/irs-mileage-log-requirements.html",
 "slug": "irs-mileage-log-requirements",
 "title": "What the IRS actually requires in a mileage log",
 "description": "The four things every business trip record must contain, what the 2026 standard rate is, why a reconstructed log fails an audit, and how long to keep it.",
 "kicker": "Guide · Mileage",
 "date": "1 September 2026",
 "faq": [
   ("What must an IRS mileage log contain?",
    "For each business trip: the date, the destination, the business purpose, and the miles driven. You also need your total mileage for the year, so the business-use share can be worked out. Records should be kept contemporaneously — written at or near the time of the trip."),
   ("What is the IRS standard mileage rate?",
    "For 2026 the standard business mileage rate is 70 cents per mile. Multiply your business miles by that rate instead of tracking actual vehicle costs. You choose one method or the other."),
   ("How long should I keep a mileage log?",
    "Three years from the date you filed the return, which is the normal period the IRS has to assess additional tax. Keep it six years if the return understated income by more than 25%."),
   ("Does a spreadsheet count as a mileage log?",
    "Yes. The IRS does not require a particular format — it requires the four elements per trip, recorded at or near the time of travel. A spreadsheet, a paper diary and an app are equally acceptable if they contain the same information."),
 ],
 "body": """
<p>Most people lose this deduction twice. First by not recording trips, and then by trying to reconstruct them in April from calendar entries and memory — which is exactly the kind of record that does not survive scrutiny.</p>

<p>The requirements themselves are short. It is worth reading them once properly.</p>

<h2>The four things every trip needs</h2>

<p>For each business trip you must be able to show:</p>

<ol>
  <li><strong>The date</strong> of the trip.</li>
  <li><strong>The destination</strong> — where you went.</li>
  <li><strong>The business purpose</strong> — why. "Client meeting — Acme" is enough; "work" is not.</li>
  <li><strong>The miles driven</strong>.</li>
</ol>

<p>On top of the per-trip record you need your <strong>total mileage for the year</strong>, because the deduction rests on the share of your driving that was for business. Without a total, a business figure means nothing on its own.</p>

<blockquote><p>The requirement people miss is <em>purpose</em>. Distance and date come from a phone easily. Purpose has to come from you, and it is the field an examiner reads first.</p></blockquote>

<h2>Write it down at the time</h2>

<p>Records are expected to be kept <em>contemporaneously</em> — at or near the time of the trip. A log assembled months later from memory is weaker evidence, and a log that is suspiciously round (every trip 20 miles, every week identical) invites exactly the questions you do not want.</p>

<p>This is the real argument for automatic tracking. Not that it saves typing, but that the record exists on the day the trip happened rather than the day you needed it.</p>

<h2>Standard rate or actual expenses</h2>

<table class="facts">
  <thead><tr><th>Method</th><th>What you track</th><th>Best when</th></tr></thead>
  <tbody>
    <tr><td><strong>Standard mileage</strong></td><td>Business miles × the published rate — <strong>70¢ per mile for 2026</strong></td><td>Your car is inexpensive to run, or you want the simplest defensible record</td></tr>
    <tr><td><strong>Actual expenses</strong></td><td>Fuel, insurance, repairs, depreciation — multiplied by your business-use percentage</td><td>The vehicle is expensive, heavily used for business, or recently bought</td></tr>
  </tbody>
</table>

<p>You still need the mileage log either way. The actual-expense method needs the business-use percentage, and that comes from the same numbers.</p>

<h2>How long to keep it</h2>

<p>Three years from the date you filed is the normal period the IRS has to assess additional tax, so three years is the working answer. Six if a return understated income by more than 25%. There is no time limit where no return was filed.</p>

<p>Storage matters more than people expect. A log that only exists inside an app you have stopped paying for is not a record you control. Keep an export.</p>

<h2>A note on other countries</h2>

<p>The four elements are close to universal, but the arithmetic is not. In the UK, HMRC pays 45p a mile for the first 10,000 business miles and 25p after that. In Canada, the per-kilometre rates apply to <em>employee reimbursement</em>; self-employed filers must use actual expenses and business-use percentage, which requires odometer readings at the start and end of the year.</p>

<p>If an app quotes you a single flat rate per mile regardless of country, it is doing the US calculation wherever you live.</p>

<div class="callout">
  <h3>Where DriveSnap fits</h3>
  <p>DriveSnap records the date, distance and route of every drive automatically, and asks you for the purpose with one swipe — the field that has to come from a human. It runs entirely on your iPhone: no account, no servers, and no cap on how many drives it will log.</p>
  <p>At year end it exports a CSV with every trip dated, categorised, rated and totalled. The rate is stamped onto each drive when it is recorded, so updating it next January never rewrites a year you have already filed.</p>
  <p><a href="/drivesnap/">See how DriveSnap works →</a></p>
</div>

<p class="disclaimer" style="color:var(--faint);font-size:.98rem">This is general information, not tax advice, and rates change. Check the current figures with the IRS or your accountant before filing.</p>
"""
},
{
 "out": "posts/how-long-to-keep-receipts.html",
 "slug": "how-long-to-keep-receipts",
 "title": "How long do you have to keep receipts for taxes?",
 "description": "Three years in the US, six in the UK for companies, five in the UAE. What a valid record has to show, whether photos count, and what happens when the app holding them shuts down.",
 "kicker": "Guide · Records",
 "date": "1 September 2026",
 "faq": [
   ("How long should I keep receipts for taxes in the US?",
    "Three years from the date you filed the return, which is the normal period the IRS has to assess additional tax. Six years if income was understated by more than 25%, and indefinitely if no return was filed."),
   ("Do digital photos of receipts count as records?",
    "Yes. The IRS, HMRC and the UAE Federal Tax Authority all accept electronic records provided they are legible, complete and can be produced on request. A clear photograph of the whole receipt is a valid record."),
   ("How long must UK businesses keep records?",
    "Six years from the end of the accounting period for companies. Self-employed individuals must keep records for at least five years after the 31 January submission deadline of the relevant tax year."),
   ("How long must records be kept for UAE VAT?",
    "Five years for most businesses, and fifteen years for records relating to real estate. Tax invoices must be retained and produced on request by the Federal Tax Authority."),
 ],
 "body": """
<p>The honest answer is that it depends where you file, and the ranges are wider than most people assume — three years in one place, fifteen in another for the same shoebox.</p>

<table class="facts">
  <thead><tr><th>Where</th><th>How long</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>United States</td><td><strong>3 years</strong></td><td>From the filing date. Six years if income was understated by more than 25%; no limit where no return was filed.</td></tr>
    <tr><td>United Kingdom — companies</td><td><strong>6 years</strong></td><td>From the end of the accounting period.</td></tr>
    <tr><td>United Kingdom — self-employed</td><td><strong>5 years</strong></td><td>After the 31 January submission deadline for that tax year.</td></tr>
    <tr><td>United Arab Emirates — VAT</td><td><strong>5 years</strong></td><td><strong>15 years</strong> for records relating to real estate.</td></tr>
  </tbody>
</table>

<h2>What actually has to be on the record</h2>

<p>A record is not just proof that money left your account. A card statement shows an amount and a merchant; it does not show what was bought or how much tax was charged. For most purposes a valid record shows:</p>

<ul>
  <li>The <strong>date</strong> of the transaction</li>
  <li>The <strong>supplier</strong> — name, and for VAT purposes their registration number</li>
  <li>What was <strong>bought</strong></li>
  <li>The <strong>amount</strong>, and the <strong>tax</strong> shown separately where it applies</li>
</ul>

<p>This is why a faded thermal receipt is a genuine problem rather than an aesthetic one. Thermal paper loses its print — sometimes within months in a hot car or a sunlit kitchen. The record does not become disputed; it becomes blank.</p>

<h2>Do photographs count?</h2>

<p>Yes. Electronic records are accepted in all three jurisdictions above, provided they are legible, complete, and can be produced when asked. A clear photograph of the whole receipt — edges included, not cropped through the total — is a valid record.</p>

<blockquote><p>Photograph it the day you get it. A receipt you meant to photograph is not a record, and thermal ink does not wait.</p></blockquote>

<h2>The part nobody plans for</h2>

<p>If your records live inside an app, three questions decide whether you actually have them:</p>

<ol>
  <li><strong>Can you export everything, in a format something else can read?</strong> If the answer is a screenshot, that is not an export.</li>
  <li><strong>What happens if the company shuts down, or you stop paying?</strong> Plenty of expense apps put export behind the subscription — so the moment you stop paying, your five-year archive becomes unreachable.</li>
  <li><strong>Who else has a copy?</strong> Anything uploaded is a copy you no longer control, held under someone else's retention policy and someone else's breach risk.</li>
</ol>

<p>The safest arrangement is dull: keep the originals on a device you own, export at least once a year, and store that export where you keep the rest of your tax paperwork.</p>

<div class="callout">
  <h3>Where Receipt Snap fits</h3>
  <p>Receipt Snap reads a receipt on the phone itself — merchant, date, total and tax — using Apple's on-device text recognition. There is no account and no server, so nothing is uploaded and nothing is retained by anybody but you. The App Store privacy label reads "Data Not Collected".</p>
  <p>It recognises twelve currencies from the receipt itself, including from a tax registration number when no symbol is printed, which is how an Indian GSTIN or a UAE TRN gets the currency right without asking you.</p>
  <p><a href="/receiptsnap/">See how Receipt Snap works →</a></p>
</div>

<p class="disclaimer" style="color:var(--faint);font-size:.98rem">General information, not tax advice. Retention rules change and vary by circumstance — check with your tax authority or accountant.</p>
"""
},
{
 "out": "posts/uae-vat-record-keeping.html",
 "slug": "uae-vat-record-keeping",
 "title": "What records UAE VAT actually requires you to keep",
 "description": "Five years, fifteen for real estate, and what has to appear on a valid tax invoice — including when a simplified invoice is allowed and what a TRN is for.",
 "kicker": "Guide · UAE VAT",
 "date": "1 September 2026",
 "faq": [
   ("How long must UAE VAT records be kept?",
    "Five years for most businesses. Records relating to real estate must be kept for fifteen years. The Federal Tax Authority can request them at any point in that window."),
   ("What must a UAE tax invoice show?",
    "The words 'Tax Invoice', the supplier's name, address and TRN, the date of issue, a description of the goods or services, the amount excluding tax, the VAT rate and amount, and the gross total. Where the recipient is registered, their name, address and TRN are required too."),
   ("What is a simplified tax invoice?",
    "A shorter form permitted where the supply is under AED 10,000 or the customer is not VAT-registered. It still needs the words 'Tax Invoice', the supplier's name, address and TRN, the date, a description of the supply, and the total with the VAT amount shown."),
   ("What is a TRN?",
    "A Tax Registration Number: the 15-digit number the Federal Tax Authority issues to a VAT-registered business. It must appear on the tax invoices that business issues, and it is the marker that identifies a receipt as a UAE one."),
 ],
 "body": """
<p>VAT arrived in the UAE in 2018 at 5%, and with it a record-keeping regime that is stricter than the paperwork habits most small businesses had before. The rules themselves are not complicated. The retention periods are longer than people expect.</p>

<h2>How long</h2>

<table class="facts">
  <thead><tr><th>Record type</th><th>Retention</th></tr></thead>
  <tbody>
    <tr><td>General business and VAT records</td><td><strong>5 years</strong></td></tr>
    <tr><td>Records relating to real estate</td><td><strong>15 years</strong></td></tr>
  </tbody>
</table>

<p>Fifteen years is long enough that the storage question is a real one. Whatever holds those records has to outlast a phone, an app subscription, and possibly the company that made the app.</p>

<h2>What a full tax invoice must show</h2>

<ul>
  <li>The words <strong>"Tax Invoice"</strong>, clearly displayed</li>
  <li>The supplier's <strong>name, address and TRN</strong></li>
  <li>Where the recipient is registered, their <strong>name, address and TRN</strong></li>
  <li>A sequential <strong>invoice number</strong> and the <strong>date of issue</strong></li>
  <li>A <strong>description</strong> of the goods or services</li>
  <li>The <strong>amount excluding VAT</strong>, the <strong>rate</strong>, the <strong>VAT amount</strong>, and the <strong>gross total</strong></li>
</ul>

<h3>When a simplified invoice is enough</h3>

<p>A shorter form is permitted where the supply is under <strong>AED 10,000</strong>, or the customer is not VAT-registered. It still has to carry the words "Tax Invoice", the supplier's name, address and TRN, the date, a description of the supply, and the total with the VAT amount shown. Most retail receipts you collect in Dubai are simplified tax invoices.</p>

<h2>The TRN is the thing worth noticing</h2>

<p>The Tax Registration Number is a 15-digit number issued by the Federal Tax Authority. It has to appear on every tax invoice a registered business issues — which makes it the most reliable marker that a receipt is a UAE one.</p>

<blockquote><p>Plenty of UAE receipts print no currency symbol at all. The TRN is what tells you the amount is in dirhams. It is a better signal than the symbol, because it is legally required to be there.</p></blockquote>

<p>The same logic holds elsewhere: a GSTIN means India, a UK postcode means sterling. Reading the registration number is more dependable than looking for a symbol that may never have been printed.</p>

<h2>Electronic records are fine</h2>

<p>The FTA accepts electronic records provided they are complete, legible and producible on request. A clear photograph of an entire simplified tax invoice satisfies that — but photograph the whole thing. A crop that cuts off the TRN or the VAT line removes the elements that make it a tax invoice at all.</p>

<div class="callout">
  <h3>Where Receipt Snap fits</h3>
  <p>Receipt Snap reads UAE receipts on the device, recognises the TRN, and uses it to set the currency to dirhams even when no symbol is printed. Merchant, date, total and VAT are captured on the phone by Apple's text recognition — no account, no upload, nothing retained by anyone else.</p>
  <p>Given a fifteen-year retention rule for property records, the fact that the archive lives on hardware you own rather than a service that might not exist in 2041 is not a small detail.</p>
  <p><a href="/receiptsnap/">See how Receipt Snap works →</a></p>
</div>

<p class="disclaimer" style="color:var(--faint);font-size:.98rem">General information, not tax advice. Verify current requirements with the Federal Tax Authority or your accountant.</p>
"""
},
]
