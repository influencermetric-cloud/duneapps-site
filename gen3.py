#!/usr/bin/env python3
"""The PaidSnap product page and its privacy policy.

The privacy page is not optional decoration. The App Store listing and the app's own
Settings screen both point at https://duneapps.com/paidsnap/privacy/, and Apple rejects a
version whose privacy or support link does not resolve. Both URLs 404'd until this file
existed, which would have been a third rejection.

Every number here is read from the shipping code, not from memory:
  * three free documents a month      -> Core/Sources/PaidSnapCore/FreePlan.swift
  * 49.99 / 39.99 / 29.99 and 89.99   -> Core/Sources/PaidSnapCore/LoyaltyLadder.swift
  * the sixteen tax countries         -> Core/Sources/PaidSnapCore/CountryPack.swift
  * reminders at 9am, due day and +3  -> PaidSnap/Models/Reminders.swift

Run: python3 gen3.py   (or build_all.py, which calls it)
"""

import json

from build import render
from gen2 import FAQ_CSS, PAGE_CSS, faq_block, faq_ld

APP_ID = "6814346014"
STORE = f"https://apps.apple.com/app/id{APP_ID}"
SUPPORT = "https://github.com/influencermetric-cloud/paidsnap-support"

# Flip to True the day Apple approves it; the hero and the closing panel both read this.
LIVE = False

CTA = (f'<a class="btn btn-primary" href="{STORE}" data-app="paidsnap" data-place="hero">Get PaidSnap</a>'
       if LIVE else
       '<span class="btn btn-primary is-soon" aria-disabled="true">Coming to the App Store</span>')

COUNTRIES = [
    ("United States", "USD", "Sales tax", "No national rate, so none is pre-filled"),
    ("United Kingdom", "GBP", "VAT", "20%, 5%, 0%"),
    ("Ireland", "EUR", "VAT", "23%"),
    ("Germany", "EUR", "VAT", "19%, 7%"),
    ("France", "EUR", "VAT", "20%"),
    ("Spain", "EUR", "VAT", "21%"),
    ("Italy", "EUR", "VAT", "22%"),
    ("Netherlands", "EUR", "VAT", "21%, 9%"),
    ("United Arab Emirates", "AED", "VAT", "5%, 0% · headed Tax Invoice"),
    ("Saudi Arabia", "SAR", "VAT", "15% · headed Tax Invoice"),
    ("South Africa", "ZAR", "VAT", "15%, 0% · headed Tax Invoice"),
    ("India", "INR", "GST", "18%, 5%, 40%, 0% · splits into CGST and SGST, or IGST"),
    ("Australia", "AUD", "GST", "10% · headed Tax Invoice"),
    ("New Zealand", "NZD", "GST", "15% · headed Tax Invoice"),
    ("Singapore", "SGD", "GST", "9% · headed Tax Invoice"),
    ("Canada", "CAD", "GST/HST", "By province: 13% Ontario, 14% Nova Scotia, 5% + 9.975% QST Quebec"),
]

FAQ = [
    ("Does PaidSnap take a cut of what I invoice?",
     "No, and it could not. Your client pays you directly, into your own bank account or through "
     "your own payment link printed on the invoice. PaidSnap never touches the money, so there is "
     "nothing to hold, nothing to release and no percentage to take."),
    ("What does the free plan actually include?",
     "Three documents a month, forever, with no watermark on the invoice. Unlimited clients, "
     "unlimited saved items, your logo, your invoice numbers, tax, the real PDF and the email. "
     "Pro removes the three-a-month cap and adds photos, signatures, deposits and part payments, "
     "the tax reports and the widget."),
    ("Why does the price go down instead of up?",
     "Because every other invoicing app does the opposite, and raising the price on the people who "
     "stayed is the thing their reviews complain about most. PaidSnap is $49.99 for the first year, "
     "$39.99 for the second, then $29.99 for every year after that. There is also a one-off $89.99 "
     "if you would rather never think about it again. The lower prices are claimed in one tap in the "
     "month before renewal; Apple cannot change a price for one customer on its own."),
    ("Is my client's data sent anywhere?",
     "No. PaidSnap has no networking code at all — no account, no sign-up, no analytics, no servers. "
     "Invoices, clients, prices and PDFs live in the app's own storage on your iPhone. You can export "
     "a backup file you keep yourself, and you can import one back."),
    ("Does my client have to sign in to see the invoice?",
     "No. The invoice goes out as a real PDF attached to the email, the way an accountant expects it. "
     "It is not a link to a portal, so there is nothing for your client to create an account for and "
     "nothing that stops working if the app disappears."),
    ("Which countries are the tax rates right for?",
     "Sixteen are pre-filled and were checked against the tax authority in September 2026: the United "
     "States, United Kingdom, Ireland, Germany, France, Spain, Italy, the Netherlands, the United Arab "
     "Emirates, Saudi Arabia, South Africa, India, Australia, New Zealand, Singapore and Canada, the "
     "last one province by province. Every other country still gets the right currency and paper size; "
     "you type the rate, because a guessed tax rate on an invoice is worse than a blank one."),
    ("Can I move over from another invoicing app?",
     "Yes, if it can export a CSV. PaidSnap reads the file, shows you which column it thinks is which, "
     "and lets you correct it before anything is saved. Clients and saved items come across in about "
     "two minutes. Nothing is uploaded to do it."),
    ("What happens if I stop paying?",
     "Your invoices stay. Everything you have already made is still there, still openable, still "
     "exportable as a PDF and as a backup file. You drop back to three new documents a month."),
]

BODY = f'''<section class="hero"><div class="wrap split">
  <div>
    <span class="badge">New · <b>iPhone</b></span>
    <h1>Invoices that get you paid.</h1>
    <p class="lede">Send a proper invoice in two minutes, from the job, from your phone. A real PDF
      attached to the email, not a link your client has to sign in to open. No account, and the whole
      thing stays on your iPhone.</p>
    <div class="actions">
      {CTA}
      <a class="btn btn-dark" href="#price">Why the price goes down</a>
    </div>
    <div class="assurances"><span>No account</span><span>Nothing uploaded</span><span>3 free a month</span></div>
  </div>
  <div class="visual"><div class="bubble"></div><div class="phones">
    <img src="/assets/paidsnap-1.png" alt="An invoice ready to email as a PDF" loading="lazy">
    <img src="/assets/paidsnap-2.png" alt="The PaidSnap home screen showing what is outstanding" loading="lazy">
    <img src="/assets/paidsnap-3.png" alt="An invoice marked paid" loading="lazy">
  </div></div>
</div></section>

<section class="section" id="price"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">The part nobody else does</span>
    <h2>The price goes down the longer you stay</h2>
    <p>Invoicing apps raise the price on the people who stayed. It is the complaint that fills their
      reviews. PaidSnap does the opposite, and it is written into the product rather than into a
      promise: three yearly plans, and you step down to the next one in the month before renewal.</p></div>
  <table class="cmp reveal">
    <thead><tr><th>&nbsp;</th><th style="color:var(--teal)">PaidSnap Pro</th><th>What usually happens</th></tr></thead>
    <tbody>
      <tr><td>First year</td><td class="ours">$49.99, after a 7-day free trial</td><td class="them">An introductory price</td></tr>
      <tr><td>Second year</td><td class="ours">$39.99</td><td class="them">Full price</td></tr>
      <tr><td>Third year and every year after</td><td class="ours">$29.99</td><td class="them">Full price, plus the increase</td></tr>
      <tr><td>Pay once instead</td><td class="ours">$89.99, for good</td><td class="them">Usually not offered</td></tr>
      <tr><td>Free plan</td><td class="ours">3 documents a month, forever, no watermark</td><td class="them">A trial that ends</td></tr>
      <tr><td>Cut of what you invoice</td><td class="ours">None. Your client pays you directly</td><td class="them">A percentage, if payments run through them</td></tr>
    </tbody>
  </table>
  <p class="note">Prices are US App Store prices; your own store shows your own currency. The lower
    years are claimed in one tap when the reminder appears, because Apple has no way to lower a price
    for one customer by itself. Cancel and come back later and you start again at the first year.</p>
</div></section>

<section class="section" style="background:var(--bg-2)"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">What it does</span><h2>Everything the job needs, nothing it doesn't</h2></div>
  <div class="features">
    <div class="feat card reveal wide">
      <img src="/assets/paidsnap-1.png" alt="The share sheet for a finished invoice" loading="lazy">
      <div><div class="tag">The document</div>
        <h3>A real PDF, not a portal link</h3>
        <p>Your logo, your colours, your own numbering. The amount due and how to pay sit at the top
          of the page where a client actually looks, with your bank details and a payment QR code
          printed underneath. Email it, message it, print it, or save it to Files.</p></div></div>
    <div class="feat card reveal"><div class="tag">Getting paid</div>
      <h3>It chases for you</h3>
      <p>A reminder at 9am on the day an invoice falls due, and again three days after. Short payment
        terms get paid faster, so PaidSnap suggests seven days rather than thirty.</p></div>
    <div class="feat card reveal"><div class="tag">Tax</div>
      <h3>Right for where you work</h3>
      <p>Pick your country and the currency, tax, paper size and heading are set for you. VAT, GST,
        sales tax, and the words "Tax Invoice" where the law asks for them.</p></div>
    <div class="feat card reveal"><div class="tag">Money</div>
      <h3>Deposits and part payments</h3>
      <p>Take a deposit up front, record what has landed, and the document shows the balance still
        owed. Per-item discounts and whole-invoice discounts both work, before tax.</p></div>
    <div class="feat card reveal wide">
      <img src="/assets/paidsnap-3.png" alt="An invoice marked paid" loading="lazy">
      <div><div class="tag">The record</div>
        <h3>Earnings, tax collected, and a CSV</h3>
        <p>What you invoiced, what landed, what is still owed, by month. Export a CSV your accountant
          can open, and a backup file of everything that you keep yourself. Estimates turn into
          invoices with one tap, so a quote that gets accepted does not get retyped.</p></div></div>
    <div class="feat card reveal"><div class="tag">Proof</div>
      <h3>Photos and signatures</h3>
      <p>Attach photos of the work, sign it yourself, and have the client sign on the phone. Lock the
        app behind Face ID if you would rather not leave client details open.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">How it goes</span><h2>From the job to the invoice</h2></div>
  <div class="stepline reveal"><div class="n">1</div><div><h3>Open it and start</h3>
    <p>No sign-up, no email, no password. Type your business name once and the first invoice is
      already numbered.</p></div></div>
  <div class="stepline reveal"><div class="n">2</div><div><h3>Add the work</h3>
    <p>Items you use often are saved and reused. Tax is applied the way your country applies it, and
      the total updates as you type, so there is no preview step to guess at.</p></div></div>
  <div class="stepline reveal"><div class="n">3</div><div><h3>Send the PDF</h3>
    <p>Email it straight from the app with the invoice attached, or share it anywhere else. Your
      client opens an attachment, which is the one thing every client can do.</p></div></div>
  <div class="stepline reveal"><div class="n">4</div><div><h3>Mark it paid</h3>
    <p>Tap paid and the reminder cancels itself. The PDF stops showing an amount due and stops
      showing the payment QR, so nobody pays the same invoice twice.</p></div></div>
</div></section>

<section class="section" id="countries" style="background:var(--bg-2)"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Tax</span><h2>Sixteen countries checked, the rest left honest</h2>
    <p>These rates were read from the tax authority in September 2026. Anywhere else, PaidSnap still
      sets your currency and paper size and lets you type the rate — because a wrong rate printed on
      an invoice is worse than a blank field.</p></div>
  <table class="cmp reveal">
    <thead><tr><th>Country</th><th>Currency</th><th>Called</th><th>Pre-filled</th></tr></thead>
    <tbody>
      {"".join(f"<tr><td>{c}</td><td>{cur}</td><td>{name}</td><td>{detail}</td></tr>"
               for c, cur, name, detail in COUNTRIES)}
    </tbody>
  </table>
  <p class="note">Rates move. India moved to GST 2.0 in September 2025 and Nova Scotia cut HST to 14%
    in April 2025, which is why these are checked rather than remembered. If one of them is out of
    date, <a href="{SUPPORT}">tell us</a> and it gets fixed in the next build.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Being straight about it</span><h2>What PaidSnap does not do</h2></div>
  <div class="grid g-2" style="margin-top:40px">
    <div class="card reveal"><h3>No web dashboard, no team</h3>
      <p>It is an iPhone app. There is no browser version, no Android version, no shared account for
        an office and no administrator view. If two people need the same books, this is not the
        product, and no amount of privacy makes up for a missing dashboard you actually need.</p></div>
    <div class="card reveal"><h3>No card payments inside the app</h3>
      <p>PaidSnap prints your bank details and your own payment link on the invoice. It does not
        process cards, so it never holds your money — and it also cannot tell you the second a
        payment lands. You mark it paid.</p></div>
    <div class="card reveal"><h3>No automatic sync between devices</h3>
      <p>Records live on the phone that made them. You can export a backup file and import it on
        another device, but there is no account quietly keeping two phones in step.</p></div>
    <div class="card reveal"><h3>No recurring invoices yet</h3>
      <p>Billing the same client every month means duplicating last month's invoice, which takes two
        taps. A proper schedule is on the list, not in the build.</p></div>
  </div>
</div></section>

{faq_block(FAQ)}

<section class="section" id="support"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Support</span><h2>Something wrong? Say so.</h2>
    <p>Open an issue on the <a href="{SUPPORT}">PaidSnap support page</a> and it gets read. Include
      your iOS version and what happened. Please do not post invoices or client details — they
      contain other people's information, and nothing about your invoices is visible to us anyway.</p>
    <p style="margin-top:16px"><a href="/paidsnap/privacy/">Privacy policy</a> ·
      <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Terms of Use (EULA)</a></p></div>
</div></section>

<section class="section"><div class="wrap"><div class="final reveal">
  <h2>Send the invoice.<br>Then forget about it.</h2>
  <div class="actions">
    {CTA}
    <a class="btn btn-dark" href="/">More from Dune Apps</a></div>
  <div class="assurances" style="justify-content:center"><span>3 free a month</span><span>No account</span><span>iOS 17 or later</span></div>
</div></div></section>'''

PRIVACY_CSS = """
  .legal { max-width: 68ch; margin: 0 auto; padding: 64px 0 90px; }
  .legal h1 { font-size: clamp(2rem, 4vw, 2.9rem); margin-bottom: 10px; }
  .legal .when { color: var(--faint); font-size: .92rem; }
  .legal h2 { font-size: 1.32rem; margin: 46px 0 12px; }
  .legal p, .legal li { color: var(--muted); line-height: 1.75; }
  .legal ul { margin: 14px 0 0 20px; }
  .legal li { margin-bottom: 8px; }
  .legal .lead { font-size: 1.14rem; color: var(--text); font-weight: 500; }
"""

PRIVACY = f'''<section class="wrap"><div class="legal">
  <h1>PaidSnap privacy policy</h1>
  <p class="when">Last updated 22 September 2026</p>

  <p class="lead" style="margin-top:28px">PaidSnap does not collect, transmit or share any data.
    It has no accounts, no analytics, no advertising identifiers and no servers, and the app makes
    no network connections of any kind.</p>

  <h2>Where your invoices live</h2>
  <p>Your business details, clients, saved items, invoices, estimates, payments, photos, signatures
    and every PDF PaidSnap produces are stored in the app's own private storage on your iPhone.
    Nothing is sent anywhere to create them, and nothing is sent anywhere afterwards. Deleting the
    app deletes this data.</p>

  <h2>What we can see</h2>
  <p>Nothing. There is no server to receive it, so there is no copy of your invoices, your clients or
    your earnings anywhere but on your own device. That is also why we cannot recover your records if
    you lose the phone — export a backup file from Settings and keep it somewhere you control.</p>

  <h2>When you send an invoice</h2>
  <p>Emailing, messaging, printing or saving an invoice hands the PDF to Apple's own share sheet and
    then to whichever app you pick. From that moment the document is governed by that app and that
    service, not by PaidSnap. We do not see the address you send it to.</p>

  <h2>Photos</h2>
  <p>If you attach a photo, PaidSnap receives only the images you pick through Apple's photo picker.
    It has no access to the rest of your photo library.</p>

  <h2>Payments</h2>
  <p>PaidSnap never processes a payment. Your bank details and your own payment link are printed on
    the invoice you produce, and your client pays you directly. No payment information passes through
    the app.</p>

  <h2>Purchases</h2>
  <p>PaidSnap Pro is bought through Apple's In-App Purchase. Apple handles the transaction and tells
    the app only whether a valid purchase exists. We never receive your name, your card, your address
    or your Apple Account. Apple's own privacy policy covers that transaction.</p>

  <h2>Notifications</h2>
  <p>Reminders about invoices falling due are scheduled by iOS on your device. They are not push
    notifications, nothing is sent from a server, and the text never leaves the phone.</p>

  <h2>Backups</h2>
  <p>The backup file PaidSnap exports goes wherever you choose to put it, and it is yours to look
    after. Separately, your iPhone's own iCloud or computer backup may include this app's data;
    that backup is governed by your Apple Account settings, not by PaidSnap.</p>

  <h2>Children</h2>
  <p>PaidSnap is a tool for running a business and is not directed at children. It collects no data
    from anyone, of any age.</p>

  <h2>Changes</h2>
  <p>If this policy ever changes, the date at the top changes with it. Any release that started
    collecting data would say so here first, and in the App Store privacy label.</p>

  <h2>Questions</h2>
  <p>Open an issue at <a href="{SUPPORT}">the PaidSnap support page</a>.</p>
</div></section>'''


def main():
    render(out="paidsnap/index.html",
           title="PaidSnap — invoices that get you paid",
           description="Send a real PDF invoice from your iPhone in two minutes. No account, nothing "
                       "uploaded, three free a month. And the price goes down the longer you stay: "
                       "$49.99, then $39.99, then $29.99.",
           canonical="https://duneapps.com/paidsnap/", og_type="product",
           body=BODY, style=PAGE_CSS + FAQ_CSS + """
  .btn.is-soon { opacity: .96; cursor: default; }
  .features .feat.card { padding: 26px 28px; }
""",
           og_image="og-paidsnap.png", priority="0.9",
           head=faq_ld(FAQ) + '<script type="application/ld+json">' + json.dumps({
               "@context": "https://schema.org", "@type": "SoftwareApplication", "name": "PaidSnap",
               "applicationCategory": "BusinessApplication", "operatingSystem": "iOS 17.0 or later",
               "description": "Invoice maker for iPhone. Real PDF invoices, no account, nothing "
                              "uploaded. Free plan sends three documents a month.",
               "offers": [{"@type": "Offer", "price": "0", "priceCurrency": "USD",
                           "description": "Free plan, three documents a month"},
                          {"@type": "Offer", "price": "49.99", "priceCurrency": "USD",
                           "description": "PaidSnap Pro, first year"},
                          {"@type": "Offer", "price": "89.99", "priceCurrency": "USD",
                           "description": "PaidSnap Pro lifetime"}]}) + "</script>")
    print("page: paidsnap/index.html")

    render(out="paidsnap/privacy/index.html",
           title="PaidSnap privacy policy — nothing is collected",
           description="PaidSnap has no accounts, no analytics and no servers, and makes no network "
                       "connections. Invoices, clients and PDFs stay on your iPhone.",
           canonical="https://duneapps.com/paidsnap/privacy/",
           body=PRIVACY, style=PRIVACY_CSS, og_image="og-paidsnap.png", priority="0.4")
    print("page: paidsnap/privacy/index.html")


if __name__ == "__main__":
    main()
