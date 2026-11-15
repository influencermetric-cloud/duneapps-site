"""Scheduled guides for duneapps.com (see the note above INDEX in content_posts.py).

Each draft is a dict with the same keys as a post in content_posts.POSTS, plus:
  "publish_on": "YYYY-MM-DD"  date (IST) it goes live; date_iso and updated match it
  "link_from":  [slug, ...]   live posts that should list it in their related cards
Nothing here renders before its date.

A draft may only link to pages that are already live on its publish_on date,
or build_all.py fails its broken link check and nothing publishes that day.
"""

_IRS_RATES = "https://www.irs.gov/tax-professionals/standard-mileage-rates"
_IRS_P463 = "https://www.irs.gov/publications/p463"
_IRS_P334 = "https://www.irs.gov/publications/p334"
_IRS_N2610 = "https://www.irs.gov/pub/irs-drop/n-26-10.pdf"
_IRS_A2611 = "https://www.irs.gov/irb/2026-29_irb"
_IRS_SC2026 = "https://www.irs.gov/pub/irs-pdf/f1040sc.pdf"
_IRS_SC_INSTR_DRAFT = "https://www.irs.gov/pub/irs-dft/i1040sc--dft.pdf"
_IRS_SC_INSTR = "https://www.irs.gov/instructions/i1040sc"
_IRS_RECORDS = "https://www.irs.gov/businesses/small-businesses-self-employed/what-kind-of-records-should-i-keep"
_IRS_1099K = "https://www.irs.gov/businesses/understanding-your-form-1099-k"

# ===========================================================================
# 18 Nov 2026. Standard mileage rate vs actual expenses: the cost per mile test
# ===========================================================================
SVA_CALC_HTML = '''
<div class="calc" id="sva-calc">
  <h3>Standard rate or actual expenses, 2026</h3>
  <p class="hint">Use whole-car figures for the year, business and personal together. Leave out business parking, tolls and car loan interest: you deduct those under either method, so they never change the answer.</p>
  <div class="row">
    <div><label for="sv1">Business miles, 1 Jan to 30 Jun 2026</label><input id="sv1" type="number" inputmode="decimal" min="0" placeholder="e.g. 12000"></div>
    <div><label for="sv2">Business miles, 1 Jul to 31 Dec 2026</label><input id="sv2" type="number" inputmode="decimal" min="0" placeholder="e.g. 12000"></div>
  </div>
  <div class="row" style="margin-top:14px">
    <div><label for="sv3">Total miles driven in 2026, all purposes</label><input id="sv3" type="number" inputmode="decimal" min="0" placeholder="e.g. 30000"></div>
    <div><label for="sv4">Fuel and oil ($)</label><input id="sv4" type="number" inputmode="decimal" min="0" placeholder="e.g. 3600"></div>
  </div>
  <div class="row" style="margin-top:14px">
    <div><label for="sv5">Insurance ($)</label><input id="sv5" type="number" inputmode="decimal" min="0" placeholder="e.g. 1800"></div>
    <div><label for="sv6">Repairs, maintenance and tires ($)</label><input id="sv6" type="number" inputmode="decimal" min="0" placeholder="e.g. 1400"></div>
  </div>
  <div class="row" style="margin-top:14px">
    <div><label for="sv7">Registration, licenses, garage rent ($)</label><input id="sv7" type="number" inputmode="decimal" min="0" placeholder="e.g. 200"></div>
    <div><label for="sv8">Depreciation or lease payments for the year ($)</label><input id="sv8" type="number" inputmode="decimal" min="0" placeholder="e.g. 2500"></div>
  </div>
  <div class="out"><span class="n" id="sv-out">Enter your figures</span><small id="sv-sub">larger deduction for 2026</small></div>
  <p class="lines" id="sv-std"></p>
  <p class="lines" id="sv-act"></p>
  <p class="lines" id="sv-cpm"></p>
  <noscript><p class="lines">The sums, if the calculator does not run. Standard: (January to June business miles × $0.725) + (July to December business miles × $0.76). Actual: total car costs × (business miles ÷ total miles).</p></noscript>
</div>'''
SVA_CALC_JS = '''<script>
(function(){
  var $=function(i){return document.getElementById(i);};
  if(!$('sv1')) return;
  var ids=['sv1','sv2','sv3','sv4','sv5','sv6','sv7','sv8'];
  var f=function(n){return n.toLocaleString('en-US',{style:'currency',currency:'USD'});};
  var v=function(i){return Math.max(0,parseFloat($(i).value)||0);};
  var go=function(){
    var a=v('sv1'), b=v('sv2'), t=v('sv3');
    var c=v('sv4')+v('sv5')+v('sv6')+v('sv7')+v('sv8');
    var biz=a+b, out=$('sv-out'), sub=$('sv-sub');
    $('sv-std').textContent=''; $('sv-act').textContent=''; $('sv-cpm').textContent='';
    if(!biz){ out.textContent='Enter your figures'; sub.textContent='larger deduction for 2026'; return; }
    var std=a*0.725+b*0.76;
    $('sv-std').textContent='Standard rate: '+a.toLocaleString()+' mi × 72.5¢ + '+b.toLocaleString()+' mi × 76¢ = '+f(std);
    if(!t || !c){ out.textContent=f(std); sub.textContent='standard mileage deduction. Add total miles and car costs to compare'; return; }
    if(t<biz){ out.textContent='Check total miles'; sub.textContent='total miles cannot be less than business miles'; return; }
    var pct=biz/t, act=c*pct, rate=std/biz, cpm=c/t;
    $('sv-act').textContent='Actual expenses: '+f(c)+' × '+(pct*100).toFixed(1)+'% business use = '+f(act);
    $('sv-cpm').textContent='Your car costs '+(cpm*100).toFixed(1)+'¢ for every mile you drove. Your average 2026 rate is '+(rate*100).toFixed(1)+'¢. Actual expenses win only when the first number is higher.';
    if(Math.abs(std-act)<0.005){ out.textContent=f(std); sub.textContent='a tie: both methods give the same deduction'; }
    else if(std>act){ out.textContent=f(std); sub.textContent='standard rate wins, by '+f(std-act)+' over actual expenses'; }
    else { out.textContent=f(act); sub.textContent='actual expenses wins, by '+f(act-std)+' over the standard rate. Read the first-year rule below before choosing'; }
  };
  ids.forEach(function(i){$(i).addEventListener('input',go);});
})();
</script>'''


def _cpm_table():
    costs = [6000, 9000, 12000, 15000, 18000]
    miles = [10000, 15000, 20000, 30000, 40000]
    head = "".join(f"<th>{m:,} mi</th>" for m in miles)
    rows = ""
    for c in costs:
        cells = ""
        for m in miles:
            cents = c / m * 100
            txt = f"{cents:.1f}".rstrip("0").rstrip(".") + "¢"
            if cents >= 76:
                cells += f"<td><strong>{txt}</strong></td>"
            elif cents > 72.5:
                cells += f"<td><em>{txt}</em></td>"
            else:
                cells += f"<td>{txt}</td>"
        rows += f"<tr><td><strong>${c:,}</strong></td>{cells}</tr>"
    return ('<table class="facts">\n  <thead><tr><th>Costs a year, by total miles</th>' + head + '</tr></thead>\n'
            '  <tbody>' + rows + '</tbody>\n</table>')


DRAFTS = [

{
 "publish_on": "2026-11-18",
 "link_from": ["irs-mileage-rate-2026", "delivery-driver-mileage-deduction", "irs-mileage-log-requirements"],
 "out": "posts/standard-mileage-rate-vs-actual-expenses.html",
 "slug": "standard-mileage-rate-vs-actual-expenses",
 "seo_title": "Standard Mileage Rate vs Actual Expenses: 2026 Calculator",
 "meta": "Standard mileage rate vs actual expenses for 2026: a calculator with both IRS rates, the cost per mile where actual wins, and the first-year lock-in rule.",
 "title": "Standard mileage rate vs actual expenses: which one wins for 2026",
 "description": "A calculator that compares the two IRS car deduction methods with both 2026 rates, a cost per mile table that shows which wins, two worked examples, and the first-year rule that decides what you can use later.",
 "dek": "One number settles it: what your car costs for every mile you drive, against the IRS rate. Here is how to work that out, a calculator that does it for you, and the rules that stop you changing your mind later.",
 "topic": "Mileage",
 "date_iso": "2026-11-18", "updated": "2026-11-18",
 "og": "og-standard-mileage-rate-vs-actual-expenses.png",
 "cta": "drivesnap",
 "cta_title": "Both methods start with the same log.",
 "cta_text": "DriveSnap detects drives on its own and you mark each one business or personal with a swipe, so the business miles and the split are in one dated record. It does not read your odometer, so note that on 1 January and 31 December. Tracking is free and has no drive cap.",
 "checked": (f'Checked against the <a href="{_IRS_RATES}">IRS standard mileage rates page</a>, '
             f'<a href="{_IRS_N2610}">Notice 2026-10</a>, <a href="{_IRS_P463}">Publication 463</a> and the '
             f'<a href="{_IRS_SC_INSTR_DRAFT}">draft 2026 Schedule C instructions</a> on 16 November 2026.'),
 "takeaways": [
   "<strong>The test:</strong> divide what the car cost you for the year by every mile you drove. If that beats the IRS rate, actual expenses wins. If not, the standard rate wins.",
   "The 2026 rate is <strong>72.5¢</strong> a mile to 30 June and <strong>76¢</strong> from 1 July, so compare against your own average of the two.",
   "A modest car driven a lot, the usual delivery or rideshare setup, does better on the standard rate. An expensive car driven fewer miles can do better on actual expenses.",
   "Choose with care in the car's first year. Standard first keeps both options open. Actual first, with accelerated depreciation, generally closes the standard rate for that car for good. A leased car stays on whichever method you start with.",
   "Business parking, tolls and the business share of car loan interest are deductible under either method. On the 2026 Schedule C the interest has its own line, <strong>16b</strong>.",
 ],
 "faq": [
   ("Which is better, the standard mileage rate or actual expenses?",
    "Whichever gives the larger figure for your car, and one division tells you. Add up what the car cost for the year (fuel, insurance, repairs, tires, registration, and depreciation or lease payments) and divide by the total miles you drove, business and personal. If the result is more than the IRS rate, 72.5 cents to 30 June 2026 and 76 cents from 1 July, actual expenses gives the bigger deduction. If it is less, the standard rate does."),
   ("Can I switch from actual expenses to the standard mileage rate?",
    "Usually not for the same car. Publication 463 says you cannot use the standard rate on a car if you have claimed depreciation on it under MACRS, a section 179 deduction, or the special depreciation allowance. For a leased car, the standard rate must be used for the whole lease if you want it at all. Going the other way, from the standard rate to actual expenses, is allowed in a later year, with straight line depreciation from then on."),
   ("Can I deduct my car payments?",
    "Not as payments. Under either method you can deduct the business share of the interest on a car loan, which goes on line 16b of the 2026 Schedule C. The cost of the car itself comes back through depreciation, which is built into the standard rate, or claimed on line 13 under actual expenses. Lease payments are different: under actual expenses the business share goes on line 20a."),
   ("Do I need a mileage log if I use actual expenses?",
    "Yes. Actual expenses are deductible only in proportion to business use, and Publication 463 divides them by miles: a car driven 20,000 miles with 12,000 for business can claim 60% of its costs. That percentage comes from a log of business miles and the total miles for the year. Schedule C, Part IV, or Form 4562 when you claim depreciation, asks for both."),
   ("What is the depreciation part of the 2026 standard mileage rate?",
    "35 cents a mile, set in IRS Notice 2026-10, and the July rate change did not alter it. Every business mile you claim at the standard rate reduces the car's basis by that amount. It matters when you sell the car, or if you switch to actual expenses later and start depreciating what is left."),
 ],
 "sources": [
   ("IRS: Standard mileage rates (72.5¢ to 30 June 2026, 76¢ from 1 July)", _IRS_RATES),
   ("IRS Notice 2026-10: 2026 standard mileage rates and the 35¢ depreciation component", _IRS_N2610),
   ("IRS Bulletin 2026-29, Announcement 2026-11: the 1 July 2026 rate change", _IRS_A2611),
   ("IRS Publication 463 (2025): choosing a method, actual car expenses, business use", _IRS_P463),
   ("IRS: Instructions for Schedule C (2026), early release draft of 8 October 2026", _IRS_SC_INSTR_DRAFT),
   ("IRS: Schedule C (Form 1040) 2026", _IRS_SC2026),
 ],
 "related": ["irs-mileage-rate-2026", "delivery-driver-mileage-deduction", "irs-mileage-log-requirements"],
 "script": SVA_CALC_JS,
 "body": """
<h2>The one division that decides it</h2>

<p>The two methods look like different worlds. One is a flat rate per business mile. The other is a stack of fuel, insurance and repair receipts. Underneath, they compare the same two numbers.</p>

<p>With actual expenses you deduct your car costs multiplied by your business use. Publication 463 works out business use from miles: <em>"You are a contractor and drive your car 20,000 miles during the year: 12,000 miles for business use and 8,000 miles for personal use. You can claim only 60% (12,000 ÷ 20,000) of the cost of operating your car as a business expense."</em></p>

<p>So actual expenses equals your business miles multiplied by <strong>what the car costs for every mile you drive</strong>. The standard method equals your business miles multiplied by <strong>the IRS rate</strong>. The business miles are the same on both sides. The method that wins is the one with the bigger number per mile.</p>

<blockquote><p>Total car costs for the year ÷ total miles driven, business and personal. If that is above the IRS rate, actual expenses wins. If it is below, the standard rate wins.</p></blockquote>

<p>For 2026 the IRS rate is two numbers, because it changed on 1 July: 72.5 cents a mile to 30 June and 76 cents from 1 July. Your own rate is somewhere between the two, depending on when you drove. The calculator works it out.</p>

<h2>Calculator: both methods side by side</h2>
""" + SVA_CALC_HTML + """

<p>Two things are left out on purpose. Business parking and tolls are deductible in full under either method, and so is the business share of car loan interest. Adding them to both sides changes the totals but never the winner.</p>

<h2>Cost per mile: where actual expenses starts to win</h2>

<p>Each cell is a year of car costs divided by the total miles driven. <strong>Bold</strong> beats the 76 cent rate, so actual expenses wins for the whole year. <em>Italic</em> sits between 72.5 and 76 cents, so it depends on how your miles split across the year. Plain is below 72.5 cents, so the standard rate wins.</p>

""" + _cpm_table() + """

<p>Read down the right-hand columns and the pattern is plain. A car that does 30,000 or 40,000 miles a year has to cost a great deal to beat the rate. That is the delivery and rideshare car: lots of miles, a modest car, so the standard rate wins by thousands, as <a href="/posts/delivery-driver-mileage-deduction.html">the delivery mileage calculator</a> shows in dollars. Actual expenses comes into its own on the left: an expensive car, or a new one with heavy depreciation, driven fewer miles.</p>

<h2>Two worked examples</h2>

<h3>A delivery driver with a paid-off sedan</h3>

<p>She drives 30,000 miles in 2026, of which 24,000 are for deliveries: 12,000 before 30 June and 12,000 after. The car costs $3,600 in fuel, $1,800 in insurance, $1,400 in repairs and tires and $200 in registration. Say depreciation comes to $2,500 for the year; the real figure would come from Form 4562.</p>

<ul>
  <li>Standard rate: 12,000 × $0.725 + 12,000 × $0.76 = <strong>$17,820</strong></li>
  <li>Actual expenses: $9,500 of costs × 80% business use = <strong>$7,600</strong></li>
  <li>Cost per mile: $9,500 ÷ 30,000 = 31.7 cents, less than half the rate</li>
</ul>

<p>The standard rate wins by $10,220. Fuel is the cost people think of, and fuel was only $3,600 of a $17,820 deduction. The rate pays for a car's whole running cost at a national figure, and a cheap car driven hard costs less per mile than that figure.</p>

<h3>A realtor with a leased SUV</h3>

<p>He drives 12,000 miles in 2026, of which 9,000 are showing homes and meeting clients, split evenly across the year. The lease costs $9,600, fuel $2,400, insurance $2,400, maintenance $300 and registration $600.</p>

<ul>
  <li>Standard rate: 4,500 × $0.725 + 4,500 × $0.76 = <strong>$6,682.50</strong></li>
  <li>Actual expenses: $15,300 of costs × 75% business use = <strong>$11,475</strong></li>
  <li>Cost per mile: $15,300 ÷ 12,000 = $1.275, well above the rate</li>
</ul>

<p>Actual expenses wins by about $4,800 before one adjustment: a car leased for 30 days or more may carry an <em>inclusion amount</em> that reduces the lease deduction, worked out from a table in Publication 463. And because it is a lease, the choice he makes in the first year holds for the whole lease, which is the next section.</p>

<!--cta-->

<h2>What each method lets you deduct, line by line</h2>

<p>The 2026 Schedule C has a new line for car loan interest. The draft instructions, dated 8 October 2026: <em>"Report the business-use portion of vehicle loan interest on line 16b, regardless of whether you use the business standard mileage rate or the actual costs of operating your vehicle."</em></p>

<table class="facts">
  <thead><tr><th>Cost</th><th>Standard rate</th><th>Actual expenses</th><th>2026 Schedule C</th></tr></thead>
  <tbody>
    <tr><td>Fuel and oil</td><td>Inside the rate</td><td>Business share</td><td>Line 9</td></tr>
    <tr><td>Repairs, maintenance, tires</td><td>Inside the rate</td><td>Business share</td><td>Line 9</td></tr>
    <tr><td>Insurance</td><td>Inside the rate</td><td>Business share</td><td>Line 9</td></tr>
    <tr><td>Registration, license plates, garage rent</td><td>Inside the rate</td><td>Business share</td><td>Line 9</td></tr>
    <tr><td>Depreciation</td><td>Inside the rate, 35¢ a mile</td><td>Business share, within the car limits</td><td>Line 13, with Form 4562</td></tr>
    <tr><td>Lease payments</td><td>Inside the rate</td><td>Business share, less any inclusion amount</td><td>Line 20a</td></tr>
    <tr><td>Car loan interest</td><td>Business share</td><td>Business share</td><td>Line 16b, new for 2026</td></tr>
    <tr><td>Personal property tax on the car</td><td>Business share</td><td>Business share</td><td>Line 23</td></tr>
    <tr><td>Business parking and tolls</td><td>In full, on top of the rate</td><td>In full</td><td>Line 9</td></tr>
  </tbody>
</table>

<p>The standard rate is not just fuel. Publication 463 is blunt about it: if you use the standard rate, <em>"You can't deduct depreciation, lease payments, maintenance and repairs, gasoline (including gasoline taxes), oil, insurance, or vehicle registration fees."</em> So fuel receipts do not go on top of the rate. <a href="/posts/do-you-need-receipts-for-tax-deductions.html">Which receipts you actually need</a> covers what to keep under each method.</p>

<h2>The first-year rule, and the other ways to get locked in</h2>

<p>This is the part that matters more than any single year's numbers. Publication 463: <em>"If you want to use the standard mileage rate for a car you own, you must choose to use it in the first year the car is available for use in your business. Then, in later years, you can choose to use either the standard mileage rate or actual expenses."</em></p>

<table class="facts">
  <thead><tr><th>Situation</th><th>What the rules allow</th></tr></thead>
  <tbody>
    <tr><td><strong>Owned car, standard rate in year one</strong></td><td>Either method in later years. A switch to actual expenses uses straight line depreciation over the car's remaining estimated life.</td></tr>
    <tr><td><strong>Owned car, actual expenses in year one</strong></td><td>No standard rate later if you claimed MACRS, a section 179 deduction or bonus depreciation on it.</td></tr>
    <tr><td><strong>Leased car</strong></td><td>The standard rate must be used for the entire lease period. The instructions add that you cannot use actual expenses for a leased vehicle once you have used the standard rate on it.</td></tr>
    <tr><td><strong>Five or more cars used at the same time</strong></td><td>No standard rate for any of them. Fleets use actual expenses.</td></tr>
    <tr><td><strong>Business use 50% or less</strong></td><td>Actual expenses still work, but MACRS is out: Publication 463 requires more than 50% business use for it, so depreciation is straight line.</td></tr>
  </tbody>
</table>

<p>The choice is made on the return itself, by its due date including extensions, and Publication 463 says <em>"You can't revoke the choice."</em> If you started using a car for work in 2026, the return you file in early 2027 is where it gets made.</p>

<p>When the numbers are close in year one, the standard rate is the choice that keeps both doors open. When actual expenses wins by a wide margin, as with the leased SUV above, it can be worth closing the door. Run both before you file, every year the choice is still yours.</p>

<h2>The depreciation inside the rate</h2>

<p>The standard rate is not free of depreciation. Part of every mile is treated as wear on the car, and Notice 2026-10 sets that part: <em>"the portion of the business standard mileage rate treated as depreciation is 26 cents per mile for 2022, 28 cents per mile for 2023, 30 cents per mile for 2024, 33 cents per mile for 2025, and 35 cents per mile for 2026."</em> The 1 July announcement raised the rate itself and left every other provision of the notice in effect, so 35 cents applies to the whole of 2026.</p>

<p>Each business mile you claim at the standard rate lowers the car's basis by that amount. 15,000 business miles in 2026 is a $5,250 reduction. You feel it in two places: when you sell or trade in the car, because the gain or loss is worked out from the lower basis, and if you move to actual expenses later, because depreciation starts from what is left.</p>

<h2>The records each method needs</h2>

<p>Neither method excuses you from a mileage log. Whichever you use, the IRS asks for your total miles for the year split into business, commuting and other: on Schedule C, Part IV, or on Form 4562 if you are claiming depreciation. Both ask whether your evidence is written.</p>

<table class="facts">
  <thead><tr><th>Record</th><th>Standard rate</th><th>Actual expenses</th></tr></thead>
  <tbody>
    <tr><td>Log of each business trip: date, place, purpose, miles</td><td>Yes</td><td>Yes</td></tr>
    <tr><td>Odometer on 1 January and 31 December</td><td>Yes, for total miles</td><td>Yes, it sets the business share</td></tr>
    <tr><td>Parking and toll receipts</td><td>Yes</td><td>Yes</td></tr>
    <tr><td>Fuel, repair, insurance and registration receipts</td><td>No</td><td>Yes, every one</td></tr>
    <tr><td>Purchase or lease papers, date first used for business</td><td>Useful for basis</td><td>Yes, for depreciation or the lease</td></tr>
  </tbody>
</table>

<p>The log has to be made at the time, or close to it. <a href="/posts/irs-mileage-log-requirements.html">What the IRS requires in a mileage log</a> sets out each element with the rule behind it, and the <a href="/posts/mileage-log-template.html">free mileage log template</a> has the columns, including odometer readings, as a PDF and a spreadsheet with both 2026 rates built in. If the two-rate split is new to you, <a href="/posts/irs-mileage-rate-2026.html">the 2026 rate page</a> covers it, and <a href="/posts/mileage-log-for-irs-audit.html">what an auditor rejects in a mileage log</a> is the check to run before you file.</p>
""",
},

# ===========================================================================
# 21 Nov 2026. Schedule C expense categories: the 2026 form, line by line
# ===========================================================================
{
 "publish_on": "2026-11-21",
 "link_from": ["do-you-need-receipts-for-tax-deductions", "how-long-to-keep-receipts", "expense-tracker-apps-that-dont-sell-your-data"],
 "out": "posts/schedule-c-expense-categories.html",
 "slug": "schedule-c-expense-categories",
 "seo_title": "Schedule C Expense Categories: The 2026 Line-by-Line List",
 "meta": "Schedule C expense categories for 2026, line by line: lines 8 to 27b, the new car loan interest line, where phones and software go, and what to keep.",
 "title": "Schedule C expense categories: every line on the 2026 form, and what goes on it",
 "description": "Every expense line on the 2026 Schedule C with what belongs on it and the record to keep, the new vehicle loan interest line, where awkward costs like phones, software and platform fees go, and worked examples for a driver, a freelancer and a seller.",
 "dek": "Many lists online still show last year's form. The 2026 Schedule C splits the interest line in three. Here is every category on it, what goes where, and how to sort a year of receipts so the totals drop straight onto the form.",
 "topic": "Receipts",
 "date_iso": "2026-11-21", "updated": "2026-11-21",
 "og": "og-schedule-c-expense-categories.png",
 "cta": "receiptsnap",
 "cta_title": "Keep the receipt the day you get it.",
 "cta_text": "Point the camera at it and Receipt Snap reads the merchant, date, total and tax on your iPhone, then finds it again by word or month when you add up the year. Its categories are everyday ones, not Schedule C lines, so the table above does the mapping. Nothing is uploaded.",
 "checked": (f'Checked against the <a href="{_IRS_SC2026}">2026 Schedule C</a>, the '
             f'<a href="{_IRS_SC_INSTR_DRAFT}">draft 2026 instructions</a>, the '
             f'<a href="{_IRS_SC_INSTR}">2025 instructions</a> and <a href="{_IRS_P334}">Publication 334</a> on 16 November 2026.'),
 "takeaways": [
   "Schedule C has <strong>25 expense lines</strong> in Part II, numbered 8 to 27b, plus line 30 for a home office and Part III for the cost of stock you sell.",
   "New for 2026: interest is split into <strong>16a</strong> mortgage, <strong>16b</strong> vehicle loan and <strong>16c</strong> other. Many lists online still show the old 16a and 16b.",
   "Anything with no line of its own goes in Part V by name and totals to <strong>line 27b</strong>. Software and bank fees go here. A mobile phone goes here or on line 25.",
   "Your own health insurance and retirement contributions do not go on Schedule C. They go on Schedule 1, lines 17 and 16.",
   "For each receipt the IRS wants the payee, the amount, proof of payment, the date and what it was for. Sort them by line as they come in and the totals are done by January.",
 ],
 "faq": [
   ("What are the expense categories on Schedule C?",
    "Part II of the 2026 Schedule C lists them as lines 8 to 27b: advertising, car and truck expenses, commissions and fees, contract labor, depletion, depreciation, employee benefit programs, insurance, interest (mortgage, vehicle loan, other), legal and professional services, office expense, pension and profit-sharing plans, rent or lease (vehicles and equipment, other property), repairs and maintenance, supplies, taxes and licenses, travel, deductible meals, utilities, wages, the energy efficient commercial buildings deduction, and other expenses. Business use of your home goes on line 30, and the cost of goods you sell is worked out in Part III."),
   ("Where do I put my phone bill on Schedule C?",
    "There is no phone line. The line 25 instructions deal only with a home landline: the base rate of the first line into your home is not deductible, but extra business costs and a second line are. For a mobile phone, deduct the business share of the bill either on line 25 or as a named item in Part V, Other expenses, and put it in the same place every year."),
   ("Where do software subscriptions go on Schedule C?",
    "The form has no software line. The instructions for Part V say to include all ordinary and necessary business expenses not deducted elsewhere and to list the type and amount of each separately, so list each subscription by name there. The Part V total goes on line 27b."),
   ("What changed on Schedule C for 2026?",
    "The interest line now has three parts: 16a for mortgage interest paid to banks, 16b for vehicle loan interest, and 16c for other interest. The draft instructions say the business share of car loan interest goes on 16b whether you use the standard mileage rate or actual expenses. The standard mileage rate is 72.5 cents a mile to 30 June 2026 and 76 cents from 1 July, and the threshold for sending a 1099-NEC to a contractor rose from $600 to $2,000."),
   ("Does my own health insurance go on Schedule C?",
    "No. Line 14 is for benefit programs for your employees. The draft 2026 instructions say not to include on line 14 what you paid for yourself as a self-employed person, and point you to Schedule 1, line 17, which can cover health insurance for you, your spouse and dependents even if you do not itemize."),
 ],
 "sources": [
   ("IRS: Schedule C (Form 1040) 2026, the form", _IRS_SC2026),
   ("IRS: Instructions for Schedule C (2026), early release draft of 8 October 2026", _IRS_SC_INSTR_DRAFT),
   ("IRS: Instructions for Schedule C (2025), final", _IRS_SC_INSTR),
   ("IRS Publication 334: Tax Guide for Small Business (ordinary and necessary, de minimis safe harbor)", _IRS_P334),
   ("IRS: What kind of records should I keep", _IRS_RECORDS),
   ("IRS: Understanding your Form 1099-K ($20,000 and 200 transactions)", _IRS_1099K),
   ("IRS: Standard mileage rates", _IRS_RATES),
 ],
 "related": ["standard-mileage-rate-vs-actual-expenses", "do-you-need-receipts-for-tax-deductions", "how-long-to-keep-receipts"],
 "body": """
<h2>The test every line shares</h2>

<p>Before the lines, the rule they all sit under. Publication 334: <em>"To be deductible, a business expense must be both ordinary and necessary. An ordinary expense is one that is common and accepted in your field of business. A necessary expense is one that is helpful and appropriate for your business."</em> It adds that an expense <em>"does not have to be indispensable to be considered necessary,"</em> and that when something is partly personal, you separate the two and deduct only the business part.</p>

<p>The categories below decide where a deduction goes, not whether you get it. Put a legitimate expense on the wrong line and the profit at the bottom is the same. Put a personal expense on any line and it is wrong everywhere.</p>

<h2>Every 2026 expense line, and what goes on it</h2>

<p>The 2026 Schedule C is already posted on irs.gov. Its instructions are an early release draft dated 8 October 2026; the rules in this table come from that draft, or from the final 2025 instructions where a line has not changed.</p>

<table class="facts">
  <thead><tr><th>Line</th><th>Category</th><th>What goes here</th><th>Keep</th></tr></thead>
  <tbody>
    <tr><td><strong>8</strong></td><td>Advertising</td><td>Paid ads, promoted listings, flyers, business cards</td><td>Invoice or receipt</td></tr>
    <tr><td><strong>9</strong></td><td>Car and truck expenses</td><td>Standard mileage (72.5¢ a mile to 30 June 2026, 76¢ from 1 July) plus business parking and tolls, or the business share of actual car costs</td><td>Mileage log; parking and toll receipts</td></tr>
    <tr><td><strong>10</strong></td><td>Commissions and fees</td><td>Commissions and fees you paid to get or do the work</td><td>Statement or invoice</td></tr>
    <tr><td><strong>11</strong></td><td>Contract labor</td><td>Independent contractors, not employees. A 1099-NEC is due for payments of $2,000 or more in 2026</td><td>Invoice; payment record</td></tr>
    <tr><td><strong>12</strong></td><td>Depletion</td><td>Oil, gas, minerals, timber. Blank for almost everyone else</td><td>n/a</td></tr>
    <tr><td><strong>13</strong></td><td>Depreciation and section 179</td><td>Equipment that lasts well beyond a year: a computer, a camera, the car under actual expenses. Often needs Form 4562</td><td>Purchase receipt; date first used</td></tr>
    <tr><td><strong>14</strong></td><td>Employee benefit programs</td><td>Health, life and dependent care plans for employees. Not your own health insurance</td><td>Plan statements</td></tr>
    <tr><td><strong>15</strong></td><td>Insurance (other than health)</td><td>Business liability, professional and business property cover. Car insurance goes on line 9</td><td>Policy and premium notice</td></tr>
    <tr><td><strong>16a</strong></td><td>Mortgage interest</td><td>Interest paid to banks on business property</td><td>Lender statement</td></tr>
    <tr><td><strong>16b</strong></td><td>Vehicle loan interest</td><td>New for 2026. The business share of car loan interest, under either car method</td><td>Loan statement</td></tr>
    <tr><td><strong>16c</strong></td><td>Other interest</td><td>Business interest not on 16a or 16b, such as a business credit card or loan</td><td>Statements</td></tr>
    <tr><td><strong>17</strong></td><td>Legal and professional services</td><td>Accountants and attorneys for the business, including preparing the business part of your return</td><td>Invoice</td></tr>
    <tr><td><strong>18</strong></td><td>Office expense</td><td>In the instructions' words, <em>"office supplies and postage"</em></td><td>Receipt</td></tr>
    <tr><td><strong>19</strong></td><td>Pension and profit-sharing plans</td><td>Contributions for employees. Your own go on Schedule 1, line 16</td><td>Plan records</td></tr>
    <tr><td><strong>20a</strong></td><td>Rent or lease: vehicles, machinery, equipment</td><td>The business share of rented equipment, or of a leased car under actual expenses</td><td>Lease or rental agreement</td></tr>
    <tr><td><strong>20b</strong></td><td>Rent or lease: other business property</td><td>Office space or other property you rent for the business</td><td>Lease; rent receipts</td></tr>
    <tr><td><strong>21</strong></td><td>Repairs and maintenance</td><td>Repairs that keep something working without adding value or extending its life. Not your own labor</td><td>Invoice</td></tr>
    <tr><td><strong>22</strong></td><td>Supplies</td><td>Materials used up in the year: packaging, cleaning supplies, and books or tools you normally use within a year. Not stock you resell</td><td>Receipt</td></tr>
    <tr><td><strong>23</strong></td><td>Taxes and licenses</td><td>Business licenses, sales tax you owe as the seller, property tax on business assets. Not income tax or self-employment tax</td><td>Tax bill; license</td></tr>
    <tr><td><strong>24a</strong></td><td>Travel</td><td>Lodging and transport on overnight business trips away from your tax home</td><td>Hotel folio; tickets</td></tr>
    <tr><td><strong>24b</strong></td><td>Deductible meals</td><td>Business meals, usually at 50%, including meals on overnight trips</td><td>Receipt; who was there and why</td></tr>
    <tr><td><strong>25</strong></td><td>Utilities</td><td>Utilities for the business. Not the base rate of the first phone line into your home</td><td>Bills</td></tr>
    <tr><td><strong>26</strong></td><td>Wages</td><td>Employees' pay, less certain employment credits</td><td>Payroll records</td></tr>
    <tr><td><strong>27a</strong></td><td>Energy efficient commercial buildings</td><td>Form 7205, for construction that began before 1 July 2026</td><td>Form 7205</td></tr>
    <tr><td><strong>27b</strong></td><td>Other expenses</td><td>Everything with no line of its own, listed by name in Part V</td><td>Receipt for each</td></tr>
    <tr><td><strong>30</strong></td><td>Business use of home</td><td>Form 8829, or the simplified method: $5 a square foot, up to 300 square feet</td><td>Measurements; home costs</td></tr>
    <tr><td><strong>Part III</strong></td><td>Cost of goods sold</td><td>Stock bought to resell and materials in what you make. Flows to line 4</td><td>Supplier invoices; inventory counts</td></tr>
  </tbody>
</table>

<p>The income side is line 1, gross receipts, and it takes everything the business earned whether or not a form reports it. A payment app or marketplace has to send a 1099-K only when payments <em>"total over $20,000 in more than 200 transactions,"</em> and a client has to send a 1099-NEC only from $2,000 in 2026. Below those, the income is still yours to report.</p>

<h2>What changed on the 2026 form</h2>

<p>The 2025 form had two interest lines: 16a for mortgage and 16b for everything else. The 2026 form has three, and the draft instructions list them under What's New: <em>"New Line 16b, Vehicle loan interest. Use line 16b to report the business-use portion of your vehicle loan interest."</em> Other business interest that used to go on the old 16b now goes on 16c.</p>

<p>Line 16b applies under either car method. If you take the standard mileage rate, the interest is not inside the rate; you claim the business share of it on 16b on top. The personal share may be deductible on Schedule 1-A instead, but the same dollar cannot go on both. Which car method suits you is its own question, worked through with a calculator in <a href="/posts/standard-mileage-rate-vs-actual-expenses.html">standard mileage rate vs actual expenses</a>.</p>

<p>Two other changes touch line 9 and line 11. The mileage rate changed on 1 July, so the draft instructions tell you to multiply January to June miles by 72.5 cents and July to December miles by 76 cents, as covered in <a href="/posts/irs-mileage-rate-2026.html">the 2026 rate guide</a>. And the threshold for sending a 1099-NEC to a contractor rose from $600 to $2,000.</p>

<h2>Where the awkward expenses go</h2>

<p>Most costs fit a line without thought. These are the ones people get stuck on.</p>

<table class="facts">
  <thead><tr><th>Expense</th><th>Where it goes</th><th>Why</th></tr></thead>
  <tbody>
    <tr><td>Mobile phone</td><td>Line 25 or Part V, business share only</td><td>The form has no phone line. Line 25's instructions cover a home landline only. Choose one place and keep to it every year</td></tr>
    <tr><td>Software and subscriptions</td><td>Part V, by name, to line 27b</td><td>No line of its own. Part V takes <em>"all ordinary and necessary business expenses not deducted elsewhere"</em></td></tr>
    <tr><td>Bank fees</td><td>Part V, to line 27b</td><td>Publication 334 lists bank fees among other expenses you can deduct</td></tr>
    <tr><td>Platform or marketplace fees</td><td>Line 10, or Part V by name</td><td>They are fees you paid. Check whether the income figure on your 1099 is before or after them; if before, the fees are a deduction you have to claim</td></tr>
    <tr><td>A laptop or tool under $2,500</td><td>Part V, if you elect the de minimis safe harbor</td><td>Publication 334: amounts under the safe harbor <em>"should be included as other expenses in Part V"</em>. Otherwise depreciate it on line 13</td></tr>
    <tr><td>Your own health insurance</td><td>Schedule 1, line 17</td><td>Not line 14, which is for employees</td></tr>
    <tr><td>Your own retirement contributions</td><td>Schedule 1, line 16</td><td>Not line 19, which is for employees</td></tr>
    <tr><td>Sales tax you collected</td><td>In line 1, then line 23</td><td>The instructions say collected sales tax goes into gross receipts too, then out again as a tax you paid</td></tr>
  </tbody>
</table>

<p>Some costs have no line because they are not deductible at all. Publication 334 lists among them charitable contributions, club dues, entertainment, fines and penalties paid to a government for breaking the law, political contributions, and personal, living and family expenses.</p>

<h2>Three examples: a driver, a freelancer, a seller</h2>

<h3>A delivery driver</h3>

<p>Most of the deduction is line 9: business miles at the two 2026 rates, plus business parking and tolls. The business share of the car loan interest goes on 16b. The business share of the phone bill goes on line 25 or in Part V. If an app takes a fee from each payout and the income figure on its tax form is before that fee, the fee is a deduction too. That is four or five lines out of twenty-five, and <a href="/posts/delivery-driver-mileage-deduction.html">the delivery mileage calculator</a> does the biggest one.</p>

<h3>A freelance designer working from home</h3>

<p>Line 8 for a portfolio ad, line 17 for the accountant, line 18 for postage and office supplies, line 30 for the home office under the simplified method, and Part V for each software subscription by name. A new laptop goes on line 13, or in Part V under the de minimis safe harbor if it cost $2,500 or less and the election is made.</p>

<h3>An online seller</h3>

<p>The stock is not a supply: it goes through Part III, cost of goods sold, which reaches line 4. Packaging goes on line 22 and postage on line 18. Marketplace fees go on line 10 or in Part V. Every sale goes in line 1, 1099-K or not, and any sales tax the seller collected goes in line 1 and back out on line 23.</p>

<h2>How to sort receipts so the totals are done</h2>

<p>The IRS describes what each expense record has to show: <em>"Your supporting documents should identify the payee, the amount paid, proof of payment, the date incurred, and include a description of the item purchased or service received that shows the amount was for a business expense."</em> On organizing them, its advice is one line: <em>"organize them by year and type of income or expense."</em></p>

<p>The Schedule C lines are the types. So the routine is short:</p>

<ul>
  <li><strong>One folder a year</strong>, and inside it one folder for each line you actually use.</li>
  <li><strong>File each receipt on the day</strong>, with the line number and a few words on what it was for. A receipt shows the payee, the amount and the date; the purpose is the part only you know.</li>
  <li><strong>Once a month</strong>, check the card statement against the folders. The statement proves payment; the receipt proves what was bought.</li>
  <li><strong>At year end</strong>, total each folder. Each total is a line on the form.</li>
</ul>

<p>Thermal receipts fade, so photograph them while they can still be read. <a href="/posts/do-you-need-receipts-for-tax-deductions.html">Do you need receipts for tax deductions</a> covers when a bank statement is enough and the $75 rule, and <a href="/posts/how-long-to-keep-receipts.html">how long to keep receipts</a> covers when you can throw the folders away.</p>

<!--cta-->

<p>If you invoice clients, the invoices are the line 1 record. The <a href="/invoice-templates/us-invoice.html">free US invoice template</a> has the fields a client's accounts team expects, and <a href="/paidsnap/">PaidSnap</a> makes the same invoice on your iPhone and keeps a copy there.</p>
""",
},

]
