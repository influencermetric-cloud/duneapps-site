"""Every guide on the site, in one place.

Written to answer what people actually type into Google — the queries came
from Google's own autocomplete across the US, UK, UAE and India — with the
rule quoted and the source linked, because assistants and examiners both
quote facts, not adjectives.

Each post carries: what the reader searched (title), the answer in the first
screen (takeaways), the depth, the questions people ask (faq, also emitted as
FAQPage schema), the sources, and ONE product card placed where <!--cta--> sits.
"""
import pathlib

_PORTED = pathlib.Path(__file__).resolve().parent / "_ported"
_IRS_RATES = "https://www.irs.gov/tax-professionals/standard-mileage-rates"
_IRS_P463 = "https://www.irs.gov/publications/p463"
_IRS_KEEP = "https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records"
_HMRC_AMAP = "https://www.gov.uk/expenses-and-benefits-business-travel-mileage/rules-for-tax"
_HMRC_SIMPLE = "https://www.gov.uk/simpler-income-tax-simplified-expenses/vehicles"
_HMRC_KEEP = "https://www.gov.uk/self-employed-records/how-long-to-keep-your-records"
_HMRC_VAT = "https://www.gov.uk/charge-reclaim-record-vat/keeping-vat-records"
_HMRC_VAT700 = "https://www.gov.uk/guidance/vat-guide-notice-700"
_ATO_RECORDS = "https://www.ato.gov.au/individuals-and-families/income-deductions-offsets-and-records/records-you-need-to-keep"
_CRA_KEEP = "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/keeping-records/where-keep-your-records-long-request-permission-destroy-them-early.html"
_UAE_VAT_LAW = "https://uaelegislation.gov.ae/en/legislations/1227"
_UAE_TPL = "https://uaelegislation.gov.ae/en/legislations/1625"

CHECKED_IRS = (f'Checked against the <a href="{_IRS_RATES}">IRS standard mileage rates page</a> and '
               f'<a href="{_IRS_P463}">Publication 463</a> on 21 September 2026.')
CHECKED_HMRC = (f'Checked against <a href="{_HMRC_AMAP}">HMRC approved mileage rates</a> and '
                f'<a href="{_HMRC_SIMPLE}">simplified expenses for vehicles</a> on 21 September 2026.')

# ---------------------------------------------------------------------------
# Calculators (plain JS, no dependencies)
# ---------------------------------------------------------------------------
IRS_CALC_HTML = '''
<div class="calc" id="irs-calc">
  <h3>2026 mileage deduction calculator</h3>
  <p class="hint">Split your business miles at 30 June, because the rate changed on 1 July. Parking and tolls are deducted on top.</p>
  <div class="row">
    <div><label for="m1">Business miles, 1 Jan to 30 Jun 2026</label><input id="m1" type="number" inputmode="decimal" min="0" placeholder="e.g. 4200"></div>
    <div><label for="m2">Business miles, 1 Jul to 31 Dec 2026</label><input id="m2" type="number" inputmode="decimal" min="0" placeholder="e.g. 3800"></div>
  </div>
  <div class="out"><span class="n" id="irs-out">$0.00</span><small>standard mileage deduction, 2026</small></div>
  <p class="lines" id="irs-lines">Enter your miles to see the two halves worked out.</p>
</div>'''
IRS_CALC_JS = '''<script>
(function(){
  var m1=document.getElementById('m1'), m2=document.getElementById('m2'),
      out=document.getElementById('irs-out'), lines=document.getElementById('irs-lines');
  if(!m1) return;
  var f=function(n){return n.toLocaleString('en-US',{style:'currency',currency:'USD'});};
  var go=function(){
    var a=Math.max(0,parseFloat(m1.value)||0), b=Math.max(0,parseFloat(m2.value)||0);
    var x=a*0.725, y=b*0.76;
    out.textContent=f(x+y);
    lines.textContent=(a||b)? (a.toLocaleString()+' mi × 72.5¢ = '+f(x)+'   ·   '+b.toLocaleString()+' mi × 76¢ = '+f(y)) : 'Enter your miles to see the two halves worked out.';
  };
  m1.addEventListener('input',go); m2.addEventListener('input',go);
})();
</script>'''

HMRC_CALC_HTML = '''
<div class="calc" id="hmrc-calc">
  <h3>2026/27 mileage allowance calculator</h3>
  <p class="hint">Business miles in a car or van, tax year 6 April 2026 to 5 April 2027. The first 10,000 miles are at 55p, everything after at 25p.</p>
  <div class="row">
    <div><label for="hm">Business miles this tax year</label><input id="hm" type="number" inputmode="decimal" min="0" placeholder="e.g. 12400"></div>
    <div><label for="hp">Already paid by your employer (£, optional)</label><input id="hp" type="number" inputmode="decimal" min="0" placeholder="0"></div>
  </div>
  <div class="out"><span class="n" id="hmrc-out">£0.00</span><small>approved amount for the year</small></div>
  <p class="lines" id="hmrc-lines">Enter your miles to see the two bands worked out.</p>
</div>'''
HMRC_CALC_JS = '''<script>
(function(){
  var hm=document.getElementById('hm'), hp=document.getElementById('hp'),
      out=document.getElementById('hmrc-out'), lines=document.getElementById('hmrc-lines');
  if(!hm) return;
  var f=function(n){return n.toLocaleString('en-GB',{style:'currency',currency:'GBP'});};
  var go=function(){
    var m=Math.max(0,parseFloat(hm.value)||0), paid=Math.max(0,parseFloat(hp.value)||0);
    var a=Math.min(m,10000), b=Math.max(0,m-10000), amt=a*0.55+b*0.25;
    out.textContent=f(amt);
    var t=m? (a.toLocaleString()+' mi × 55p = '+f(a*0.55)+'   ·   '+b.toLocaleString()+' mi × 25p = '+f(b*0.25)) : 'Enter your miles to see the two bands worked out.';
    if(m && paid>0){ var d=amt-paid; t+= d>=0 ? ('   ·   Mileage Allowance Relief you can claim: '+f(d)) : ('   ·   Paid above the approved amount by '+f(-d)+' — that excess is taxable'); }
    lines.textContent=t;
  };
  hm.addEventListener('input',go); hp.addEventListener('input',go);
})();
</script>'''

# ---------------------------------------------------------------------------
POSTS = [

# ===========================================================================
# 1. IRS mileage rate 2026 — the timely, high-volume page
# ===========================================================================
{
 "out": "posts/irs-mileage-rate-2026.html",
 "slug": "irs-mileage-rate-2026",
 "seo_title": 'IRS Mileage Rate 2026: 72.5¢ Then 76¢ From July',
 "meta": 'IRS mileage rate 2026: 72.5¢ a mile to 30 June, 76¢ from 1 July. How to split your miles, what the rate covers, and every rate since 2019, plus a calculator.',
 "title": "IRS mileage rate 2026: 72.5¢, then 76¢ from 1 July",
 "description": "The IRS raised the standard mileage rate midyear. 72.5 cents a mile applies from January to June 2026 and 76 cents from July. How to split your miles, what the rate includes, and a calculator.",
 "dek": "Two rates in one year is unusual, and getting it wrong is the first thing an examiner sees. Here is the 2026 rate, the midyear change, what the rate actually covers, and a calculator that does the split.",
 "topic": "Mileage",
 "date_iso": "2026-09-20", "updated": "2026-09-20",
 "og": "og-irs-mileage-rate-2026.png",
 "cta": "drivesnap",
 "cta_title": "Log the miles on the day, at the right rate.",
 "cta_text": "DriveSnap detects your drives, stamps the correct 2026 rate onto each one as it happens, and totals both halves of the year for you. No drive caps, and nothing leaves your phone.",
 "checked": CHECKED_IRS,
 "takeaways": [
   "<strong>Business: 72.5¢ a mile</strong> from 1 January to 30 June 2026, and <strong>76¢</strong> from 1 July to 31 December.",
   "Medical and military moving: 20.5¢ then 23.5¢. Charity: 14¢ all year (that one is set by statute).",
   "Split your miles at the date of the trip, not at the date you file. One rate across the whole year is wrong twice.",
   "The rate already covers fuel, maintenance, insurance and depreciation. Parking and tolls are deducted separately, on top.",
   "The 70¢ figure still quoted on a lot of pages is the 2025 rate.",
 ],
 "faq": [
   ("What is the IRS mileage rate for 2026?",
    "72.5 cents per business mile for trips from 1 January to 30 June 2026, and 76 cents per mile for trips from 1 July to 31 December 2026. Medical and military moving mileage is 20.5 cents then 23.5 cents; charitable mileage stays at 14 cents."),
   ("Does the standard mileage rate include gas?",
    "Yes. The rate is a single figure standing in for the whole cost of running the car: fuel, oil, maintenance, tires, insurance, registration and depreciation. You do not add fuel receipts on top. Parking fees and tolls for business trips are the exception: they are deductible in addition to the rate."),
   ("How do I calculate my 2026 deduction with two rates?",
    "Add up the business miles you drove from January to June and multiply by $0.725. Add up July to December and multiply by $0.76. Add the two figures. A driver with 4,000 miles in each half has 4,000 × 0.725 = $2,900 plus 4,000 × 0.76 = $3,040, a deduction of $5,940."),
   ("Can I switch between the standard mileage rate and actual expenses?",
    "Publication 463 sets the rule: if you want to use the standard rate for a car you own, you must choose it in the first year the car is used in your business. In later years you can switch to actual expenses. If you start with actual expenses, you generally cannot go back to the standard rate for that car."),
   ("When will the 2027 rate be announced?",
    "The IRS normally publishes the next year's rate in the middle of December. Check the IRS standard mileage rates page rather than a site that copies it, because the 2026 midyear change shows why."),
 ],
 "sources": [
   ("IRS standard mileage rates (every year from 2011, including the 1 July 2026 change)", _IRS_RATES),
   ("IRS Publication 463, Travel, Gift, and Car Expenses (recordkeeping, choosing a method)", _IRS_P463),
 ],
 "related": ["mileage-log-for-irs-audit", "irs-mileage-log-requirements", "mileage-log-template"],
 "script": IRS_CALC_JS,
 "body": f"""
<h2>The 2026 rates</h2>

<table class="facts">
  <thead><tr><th>Purpose</th><th>1 Jan to 30 Jun 2026</th><th>1 Jul to 31 Dec 2026</th><th>2025, for comparison</th></tr></thead>
  <tbody>
    <tr><td><strong>Business</strong></td><td><strong>72.5¢</strong> per mile</td><td><strong>76¢</strong> per mile</td><td>70¢</td></tr>
    <tr><td>Medical or military moving</td><td>20.5¢</td><td>23.5¢</td><td>21¢</td></tr>
    <tr><td>Charitable</td><td>14¢</td><td>14¢</td><td>14¢</td></tr>
  </tbody>
</table>

<p>The business rate is the one most people mean. It applies to a car, van, pickup or panel truck you own or lease, when you choose the standard mileage method instead of adding up actual costs.</p>

<h2>Every rate since 2019</h2>

<table class="facts">
  <thead><tr><th>Tax year</th><th>Business</th><th>Medical or military moving</th><th>Charitable</th><th>IRS release</th></tr></thead>
  <tbody>
    <tr><td><strong>2026, 1 Jul to 31 Dec</strong></td><td><strong>76¢</strong></td><td>23.5¢</td><td>14¢</td><td>IR&#8239;2026&#8239;29</td></tr>
    <tr><td><strong>2026, 1 Jan to 30 Jun</strong></td><td><strong>72.5¢</strong></td><td>20.5¢</td><td>14¢</td><td>IR&#8239;2025&#8239;128</td></tr>
    <tr><td>2025</td><td>70¢</td><td>21¢</td><td>14¢</td><td>IR&#8239;2024&#8239;312</td></tr>
    <tr><td>2024</td><td>67¢</td><td>21¢</td><td>14¢</td><td>IR&#8239;2023&#8239;239</td></tr>
    <tr><td>2023</td><td>65.5¢</td><td>22¢</td><td>14¢</td><td>IR&#8239;2022&#8239;234</td></tr>
    <tr><td>2022, 1 Jul to 31 Dec</td><td>62.5¢</td><td>22¢</td><td>14¢</td><td>IR&#8239;2022&#8239;124</td></tr>
    <tr><td>2022, 1 Jan to 30 Jun</td><td>58.5¢</td><td>18¢</td><td>14¢</td><td>IR&#8239;2021&#8239;251</td></tr>
    <tr><td>2021</td><td>56¢</td><td>16¢</td><td>14¢</td><td>IR&#8239;2020&#8239;279</td></tr>
    <tr><td>2020</td><td>57.5¢</td><td>17¢</td><td>14¢</td><td>IR&#8239;2019&#8239;215</td></tr>
    <tr><td>2019</td><td>58¢</td><td>20¢</td><td>14¢</td><td>IR&#8239;2018&#8239;251</td></tr>
  </tbody>
</table>

<p>Two things stand out. The charitable rate has not moved once, because it is set by statute rather than by the annual cost study. And the IRS table, which runs back to 2011, contains only three years where the business rate changed inside the year: 2011, 2022 and 2026.</p>

<p>If you are filing a late return or amending one, use the row for that year rather than the current figure. Plenty of apps and spreadsheets still carry an old rate; one popular tracker's App Store listing still tells people to deduct 57.5 cents a mile, which was correct in 2020.</p>

<h2>Why there are two rates this year</h2>

<p>The IRS sets the business rate from a study of the fixed and variable costs of running a car. Normally it publishes one figure in December and leaves it alone for twelve months. When costs move sharply inside a year it can issue a midyear adjustment. It did so in 2022, and it has done so again in 2026, raising the business rate by 3.5 cents from 1 July.</p>

<p>The practical consequence is simple and easy to get wrong: <strong>the rate that applies is the one in force on the day of the trip.</strong> A drive on 28 June is worth 72.5 cents a mile. The same drive on 2 July is worth 76. When you file in 2027, you split the year at 30 June and apply each rate to its own half.</p>

<blockquote><p>Applying one rate across the whole year is wrong in both directions. You either shortchange yourself on the second half, or overclaim on the first. Either way it is the first number an examiner checks.</p></blockquote>

<h2>Calculator: your 2026 deduction</h2>

{IRS_CALC_HTML}

<p>Parking and tolls paid on business trips are not in the rate. Add them separately, with the receipt.</p>

<h2>What the rate includes, and what it does not</h2>

<p>The standard rate is designed to stand in for the whole cost of operating the vehicle. That means it already covers:</p>

<ul>
  <li>Fuel and oil</li>
  <li>Maintenance, repairs and tires</li>
  <li>Insurance and registration</li>
  <li>Depreciation (a fixed portion of each mile is treated as depreciation)</li>
</ul>

<p>So there is no adding fuel receipts on top of the rate. People do, and it is one of the more common errors on a Schedule C. What you <em>can</em> add is parking and tolls paid on business trips, which Publication 463 treats as separate deductible expenses.</p>

<h2>What counts as a business mile</h2>

<p>Driving between two places of work, from your office to a client, to the bank or the post office on business, between job sites, and, for a delivery or rideshare driver, the miles between accepting jobs, all count. Commuting does not: the trip from home to your regular place of work is personal, whatever you are carrying and whatever you are thinking about on the way.</p>

<p>If your home is your principal place of business, trips from home to a client or supplier are business miles. That single rule is worth more to most freelancers than any app.</p>

<!--cta-->

<h2>Standard rate or actual expenses</h2>

<table class="facts">
  <thead><tr><th>Method</th><th>What you track</th><th>Tends to win when</th></tr></thead>
  <tbody>
    <tr><td><strong>Standard mileage</strong></td><td>Business miles × the rate for the period, plus parking and tolls</td><td>The car is inexpensive to run, or you want the simplest record that stands up</td></tr>
    <tr><td><strong>Actual expenses</strong></td><td>Fuel, insurance, repairs, lease or depreciation, multiplied by your business use percentage</td><td>The car is expensive, heavily used for business, or newly bought</td></tr>
  </tbody>
</table>

<p>There is a sequencing rule. If you want the standard rate for a car you own, you must choose it in the first year that car is used in your business; you can move to actual expenses later. Start with actual expenses and you generally cannot go back to the standard rate for that vehicle. Choose deliberately in year one.</p>

<p>Whichever method you use, the mileage log is not optional. Actual expenses needs the business use percentage, and that comes from the same miles.</p>

<h2>If you have already filed using one rate</h2>

<p>This will be a common mistake for the 2026 year, because most software, most spreadsheets and most memories carry a single annual figure.</p>

<p>The fix is an amended return, filed on Form 1040X. Whether it is worth filing depends on which way the error went. If you applied 72.5 cents to the whole year you underclaimed on every trip after 30 June, and the amendment puts money back. If you applied 76 cents to the whole year you overclaimed on the first half, and correcting it voluntarily is a great deal cheaper than having it found.</p>

<p>Either way the arithmetic is the same: go back to the log, split the trips at 30 June, and apply each rate to its own half. If the log does not carry dates precise enough to split on, that is the real problem, and it is the one worth solving before next year.</p>

<h2>The record that makes the number real</h2>

<p>A rate is worthless without the miles behind it, and the IRS is specific about what the record must show for each trip: the <strong>date</strong>, the <strong>destination</strong>, the <strong>business purpose</strong>, and the <strong>miles</strong>, kept at or near the time of the trip rather than rebuilt in April. The full rules are in <a href="/posts/irs-mileage-log-requirements.html">what the IRS requires in a mileage log</a>, and there is a <a href="/posts/mileage-log-template.html">free template</a> with the right columns if you would rather keep it by hand.</p>

<p>If you want to know how that record is judged when someone actually reads it, <a href="/posts/mileage-log-for-irs-audit.html">what an auditor rejects in a mileage log</a> goes through the six things that get one thrown out, with the rule behind each. And if the app you use caps how much it will log, read <a href="/posts/is-mileiq-free.html">what a free tier cap does to a tax record</a> first, because a missing fortnight is a bigger problem than a subscription.</p>
""",
},

# ===========================================================================
# 2. HMRC mileage rates 2026/27 — the rate just changed, few pages have it
# ===========================================================================
{
 "out": "posts/hmrc-mileage-rates-2026.html",
 "slug": "hmrc-mileage-rates-2026",
 "seo_title": 'HMRC Mileage Rates 2026/27: 55p a Mile From 6 April',
 "meta": "HMRC’s approved mileage rate rose from 45p to 55p for the first 10,000 business miles from 6 April 2026. The 2026/27 rates, who can claim, and a calculator.",
 "title": "HMRC mileage rates 2026/27: 55p a mile, and what changed on 6 April",
 "description": "HMRC's approved mileage rate rose from 45p to 55p per mile for the first 10,000 business miles from 6 April 2026. The full 2026/27 rates for cars, motorcycles and bicycles, who can claim, and a calculator.",
 "dek": "The first rise in the approved rate in well over a decade. Here are the 2026/27 figures for employees and the self-employed, what to do if your employer pays less than the approved amount, and the records HMRC expects behind the claim.",
 "topic": "Mileage",
 "date_iso": "2026-09-20", "updated": "2026-09-20",
 "og": "og-hmrc-mileage-rates-2026.png",
 "cta": "drivesnap",
 "cta_title": "A log HMRC can read, kept automatically.",
 "cta_text": "DriveSnap records every business journey — date, distance, route — and asks for the purpose with one swipe. No drive caps on the free tier, and the record stays on your iPhone for the five years HMRC can ask for it.",
 "checked": CHECKED_HMRC,
 "takeaways": [
   "<strong>Cars and vans: 55p a mile for the first 10,000 business miles</strong> in the tax year from 6 April 2026, then <strong>25p</strong>. Before 6 April it was 45p.",
   "Motorcycles: 24p a mile. Bicycles: 20p. Neither has a 10,000-mile step.",
   "Employees: if your employer pays you less than the approved amount, you can claim the difference as Mileage Allowance Relief. If they pay more, the excess is taxable.",
   "Self-employed: the same flat rates apply under simplified expenses, instead of tracking the car's actual costs.",
   "Keep the journey record — date, where, why, miles — for at least 5 years after the 31 January filing deadline.",
 ],
 "faq": [
   ("What is the HMRC mileage rate for 2026/27?",
    "55p per mile for the first 10,000 business miles in a car or van, and 25p per mile after that, for the tax year beginning 6 April 2026. Motorcycles are 24p a mile and bicycles 20p, with no 10,000-mile threshold."),
   ("When did the HMRC mileage rate change from 45p to 55p?",
    "On 6 April 2026, the start of the 2026/27 tax year. Journeys before that date use the old 45p rate, so a claim for the 2025/26 tax year is still at 45p."),
   ("My employer pays me 45p a mile. Can I claim the difference?",
    "Yes. If your employer pays less than the approved amount, you can claim Mileage Allowance Relief on the difference — 10p a mile on the first 10,000 miles in 2026/27 if they are still paying 45p. You claim it through Self Assessment or by contacting HMRC, and you need a record of the business journeys to support it."),
   ("Do the mileage rates apply to electric cars?",
    "The approved mileage allowance for a privately owned car does not depend on what fuels it — an electric car owner uses the same 55p and 25p rates. (The separate advisory electricity rate applies to company cars, which is a different scheme.)"),
   ("Can I claim mileage and fuel receipts?",
    "Not both. The approved rate is meant to cover the whole cost of running the vehicle, fuel included. Under simplified expenses the self-employed choose either the flat rate per mile or the actual costs of the vehicle, and stick with that choice for as long as they use that vehicle."),
 ],
 "sources": [
   ("GOV.UK — Expenses and benefits: business travel mileage, rules for tax (approved rates from 6 April 2026)", _HMRC_AMAP),
   ("GOV.UK — Simplified expenses if you're self-employed: vehicles", _HMRC_SIMPLE),
   ("GOV.UK — Business records if you're self-employed: how long to keep your records", _HMRC_KEEP),
 ],
 "related": ["mileage-log-template", "irs-mileage-log-requirements", "how-long-to-keep-receipts"],
 "script": HMRC_CALC_JS,
 "body": f"""
<h2>The 2026/27 rates</h2>

<table class="facts">
  <thead><tr><th>Vehicle</th><th>First 10,000 business miles</th><th>After 10,000 miles</th><th>Before 6 April 2026</th></tr></thead>
  <tbody>
    <tr><td><strong>Cars and vans</strong></td><td><strong>55p</strong> per mile</td><td><strong>25p</strong> per mile</td><td>45p / 25p</td></tr>
    <tr><td>Motorcycles</td><td>24p</td><td>24p</td><td>24p</td></tr>
    <tr><td>Bicycles</td><td>20p</td><td>20p</td><td>20p</td></tr>
  </tbody>
</table>

<p>The 10,000-mile threshold resets each tax year, on 6 April. It applies per employment for employees and per business for the self-employed, and it is counted in business miles only — commuting to your normal workplace does not count towards it, because commuting is not claimable at all.</p>

<h2>What changed on 6 April</h2>

<p>The 45p rate had been in place since 2011. Fuel, insurance and servicing all rose considerably in the fifteen years since, and the approved amount did not move with them, which is why "45p doesn't cover it" was such a common complaint. From the start of the 2026/27 tax year the first-band rate is 55p. The second band, motorcycles and bicycles are unchanged.</p>

<p>Because the rate is set per tax year rather than per calendar year, there is no midyear split to worry about in the way there is <a href="/posts/irs-mileage-rate-2026.html">with the IRS rate in 2026</a>. Journeys on or after 6 April 2026 are at 55p. Journeys before it — including everything in the 2025/26 return you file by 31 January 2027 — stay at 45p.</p>

<h2>Calculator: your approved amount for 2026/27</h2>

{HMRC_CALC_HTML}

<h2>If you are an employee</h2>

<p>Your employer can pay you up to the approved amount for business journeys in your own car tax-free — these are Mileage Allowance Payments. Three situations follow from that:</p>

<ul>
  <li><strong>They pay the approved rate.</strong> Nothing to claim, nothing to declare.</li>
  <li><strong>They pay less</strong> — plenty of employers are still on 45p, or lower. You can claim <strong>Mileage Allowance Relief</strong> on the shortfall. On 8,000 business miles at 45p against an approved 55p, that is 8,000 × 10p = £800 of relief for the year.</li>
  <li><strong>They pay more.</strong> The amount above the approved rate is taxable and goes on your P11D.</li>
</ul>

<p>You claim the relief through Self Assessment if you already file one, or by writing to HMRC if you do not. Either way it rests on a record of the journeys.</p>

<h2>If you are self-employed</h2>

<p>Under <strong>simplified expenses</strong> you can use the same flat rates — 55p, then 25p — instead of working out the actual running costs of the vehicle and apportioning them to business use. The flat rate covers fuel, insurance, servicing and depreciation, so nothing is added on top for those. Parking and tolls on business journeys are claimed separately.</p>

<p>One rule catches people: once you use the flat rate for a vehicle, you keep using it for as long as that vehicle is in the business. You cannot flip to actual costs in a year when the car needed an expensive repair.</p>

<!--cta-->

<h2>The record HMRC expects</h2>

<p>HMRC does not prescribe a form, but a claim has to be supportable, and what supports it is the same four things every tax authority asks for: the <strong>date</strong> of each journey, <strong>where</strong> it went, <strong>why</strong> it was business, and the <strong>miles</strong>. A total figure with nothing behind it is the claim most likely to be reduced on enquiry.</p>

<p>The self-employed must keep business records for <strong>at least five years after the 31 January submission deadline</strong> of the relevant tax year. A journey record kept on paper, in a spreadsheet, or in an app that lets you export it all satisfy that, provided you can still produce it in year five. There is a <a href="/posts/mileage-log-template.html">free template with the right columns</a> if you keep it by hand.</p>

<h2>Common mistakes on mileage claims</h2>

<ul>
  <li><strong>Claiming the commute.</strong> Home to your usual workplace is not a business journey, however far it is.</li>
  <li><strong>Forgetting the 10,000-mile step.</strong> Miles above the threshold are at 25p, and the threshold resets on 6 April.</li>
  <li><strong>Mixing tax years.</strong> The 55p rate starts on 6 April 2026, not 1 January.</li>
  <li><strong>Round numbers.</strong> A log that says 20 miles every Tuesday reads as an estimate, and estimates are what enquiries are made of.</li>
  <li><strong>Claiming fuel on top of the rate.</strong> The rate already includes it.</li>
</ul>
""",
},

# ===========================================================================
# 3. Do you need receipts for tax deductions — the big question cluster
# ===========================================================================
{
 "out": "posts/do-you-need-receipts-for-tax-deductions.html",
 "slug": "do-you-need-receipts-for-tax-deductions",
 "seo_title": 'Do You Need Receipts for Tax Deductions? The $75 Rule',
 "meta": "The IRS doesn't require a receipt for most expenses under $75 — but always requires a record. What counts as proof in the US, UK, Australia and Canada.",
 "title": "Do you need receipts for tax deductions? The $75 rule and what actually counts as proof",
 "description": "The IRS does not require a receipt for most expenses under $75 — but it always requires a record of the amount, date, place and business purpose. What counts as proof in the US, UK, Australia and Canada, and what to do when a receipt is lost.",
 "dek": "The honest answer is 'not always a receipt, but always a record'. Here is the actual threshold, the one expense that always needs documentation, what a bank statement does and does not prove, and the rules in the UK, Australia and Canada.",
 "topic": "Receipts",
 "date_iso": "2026-09-20", "updated": "2026-09-20",
 "og": "og-do-you-need-receipts-for-tax-deductions.png",
 "cta": "receiptsnap",
 "cta_title": "The receipt, photographed the day you get it.",
 "cta_text": "Receipt Snap reads the merchant, date, total and tax off the paper on your iPhone in about two seconds and files it — so the record exists before the thermal print fades. No account, nothing uploaded.",
 "checked": (f'Checked against <a href="{_IRS_P463}">IRS Publication 463</a>, <a href="{_HMRC_VAT700}">HMRC VAT Notice 700</a>, '
             f'the <a href="{_ATO_RECORDS}">ATO records page</a> and <a href="{_CRA_KEEP}">CRA record-keeping guidance</a> on 20 September 2026.'),
 "takeaways": [
   "<strong>US:</strong> a receipt is not required for an expense under <strong>$75</strong> — except lodging, which always needs one. You still need a record of the amount, date, place and business purpose.",
   "A card statement proves you paid; it does not prove what for or why. Pair it with a note of the purpose.",
   "Lost a receipt? The IRS incomplete-records rule lets you use your own written statement plus other evidence. Estimating is not allowed.",
   "<strong>UK:</strong> keep receipts for expenses; to reclaim VAT you need a VAT invoice (a simplified one is fine up to £250).",
   "<strong>Australia:</strong> written evidence is required once total work-related claims exceed <strong>$300</strong>. <strong>Canada:</strong> keep supporting documents 6 years.",
 ],
 "faq": [
   ("Do I need receipts for tax deductions under $75?",
    "In the US, generally no. Publication 463 says documentary evidence is not needed for an expense under $75, with one exception: lodging always requires it. What you always need — whatever the amount — is a record showing the amount, the date, the place and the business purpose. Without those four, the receipt would not have helped anyway."),
   ("Can I use bank or credit card statements instead of receipts?",
    "Partly. A statement establishes that you paid a certain amount to a certain merchant on a certain date. It does not show what you bought, whether tax was charged, or why the expense was for business. For a small expense that is often enough when combined with a note of the purpose; for anything larger, or anything an examiner might question, keep the receipt too."),
   ("What if I lost a receipt?",
    "Do not estimate — Publication 463 says plainly that you cannot deduct amounts you approximate. Instead, use the incomplete-records rule: your own written statement giving the specific details, plus other supporting evidence such as a card statement, a calendar entry, an email confirming the meeting, or an invoice from the other party. The more of those you have, the stronger the claim."),
   ("Do I need gas receipts for taxes?",
    "Only if you deduct actual car expenses. If you use the standard mileage rate — most self-employed drivers do — the rate already includes fuel, so fuel receipts are irrelevant; what you need instead is a mileage log. Keep the receipts if you use, or might switch to, the actual-expense method."),
   ("Do I need receipts for expenses in the UK?",
    "HMRC expects you to keep records that support what you put on your return, including receipts for business expenses, for at least 5 years after the 31 January deadline. To reclaim VAT you need a VAT invoice from the supplier; for purchases of £250 or less a simplified VAT invoice — which is what most till receipts from VAT-registered retailers are — is sufficient."),
   ("Do I need receipts for work-related deductions in Australia?",
    "If your total claim for work-related expenses is $300 or less, the ATO does not require receipts, but you must be able to show how you worked out the claim. Above $300 you need written evidence for the expenses. Records are kept for five years."),
 ],
 "sources": [
   ("IRS Publication 463 — Chapter 5, Recordkeeping (the $75 rule, adequate records, incomplete records)", _IRS_P463),
   ("IRS — How long should I keep records?", _IRS_KEEP),
   ("GOV.UK — Keeping VAT records (VAT invoices, the £250 simplified invoice, 6-year retention)", _HMRC_VAT),
   ("GOV.UK — Business records if you're self-employed: how long to keep your records", _HMRC_KEEP),
   ("ATO — Records you need to keep (the $300 threshold)", _ATO_RECORDS),
   ("Canada Revenue Agency — Where to keep your records, for how long", _CRA_KEEP),
 ],
 "related": ["how-long-to-keep-receipts", "expense-tracker-apps-that-dont-sell-your-data", "irs-mileage-rate-2026"],
 "body": """
<h2>The short answer</h2>

<p>You do not always need a receipt. You always need a record. Those are different things, and most of the confusion on this question comes from treating them as the same.</p>

<p>A receipt is one kind of evidence — usually the best kind, because it shows what was bought, from whom, for how much, and how much tax was charged. But the tax rules in every country covered here are written around <em>proving</em> an expense, and they allow other evidence to do that when a receipt is small, lost, or was never issued.</p>

<h2>United States: the $75 rule</h2>

<p>IRS Publication 463 draws the line in one sentence. Documentary evidence — a receipt, cancelled cheque or bill — is ordinarily not needed if the expense, <strong>other than lodging</strong>, is <strong>less than $75</strong>. Lodging is the exception: a hotel bill is required whatever it cost.</p>

<p>What the rule does not remove is the requirement for <strong>adequate records</strong>. For every business expense, receipt or not, you must be able to show:</p>

<table class="facts">
  <thead><tr><th>Element</th><th>What it means</th><th>Where it usually comes from</th></tr></thead>
  <tbody>
    <tr><td><strong>Amount</strong></td><td>What it cost</td><td>Receipt, statement</td></tr>
    <tr><td><strong>Time</strong></td><td>The date</td><td>Receipt, statement</td></tr>
    <tr><td><strong>Place</strong></td><td>Where, or from whom</td><td>Receipt, statement</td></tr>
    <tr><td><strong>Business purpose</strong></td><td>Why it was for the business</td><td><strong>You.</strong> No document supplies this.</td></tr>
  </tbody>
</table>

<p>That last row is the one that decides audits. A $40 lunch is under the threshold, so no receipt is required — but "lunch, 14 March, $40, Café Roma" is still not a deductible record until you add "with J. Ortiz, discussed the Q2 contract". Publication 463 also asks that records be kept <em>timely</em>: written down at or near the time of the expense, not reconstructed months later.</p>

<h2>What a bank statement proves</h2>

<p>A card or bank statement is documentary evidence of three of the four elements: amount, date and payee. It is silent on the fourth — purpose — and it says nothing about what was actually purchased or how much of the total was tax.</p>

<p>For a small, routine expense that is often acceptable, combined with a note of the purpose. For anything larger, anything mixed (a shop where you bought both office supplies and groceries), or anything that involves sales tax you want to reclaim, the statement is not a substitute for the receipt.</p>

<blockquote><p>The statement says you spent $212 at an office supply store. The receipt says which $212. If an examiner asks, only one of those answers the question.</p></blockquote>

<h2>When the receipt is lost</h2>

<p>Two things to know. First, you cannot guess: Publication 463 states that you cannot deduct amounts you approximate or estimate. Second, a lost receipt is not a lost deduction, because the same publication has a rule for <strong>incomplete records</strong>. Where you lack complete documentation for an element of an expense, you can establish it with:</p>

<ul>
  <li><strong>your own written statement</strong> containing specific information about that element, and</li>
  <li><strong>other supporting evidence</strong> sufficient to establish it — a card charge, a calendar entry, an email confirming the meeting, an invoice from the other side.</li>
</ul>

<p>The standard is evidence, not paper. A card charge for $84 at a restaurant, a calendar entry for a client lunch at that restaurant on that day, and a note of who was there and why is a defensible record without the receipt. Reconstruction from memory alone, months later, is not — Publication 463 reserves genuine reconstruction for records lost through fire, flood or other casualty.</p>

<!--cta-->

<h2>Gas receipts, medical receipts, and other special cases</h2>

<p><strong>Gas receipts.</strong> If you deduct car costs using the standard mileage rate, fuel is already inside the rate and the receipts are irrelevant; what you need is a <a href="/posts/irs-mileage-log-requirements.html">mileage log</a>. If you use actual expenses, or think you might switch to them for this car, keep them.</p>

<p><strong>Medical expenses.</strong> The $75 rule is written for business travel, meals and car expenses. For itemised medical deductions, keep the provider's bill or receipt and proof of payment; there is no small-amount exemption to lean on, and the amounts add up over a year.</p>

<p><strong>Charitable gifts.</strong> Cash gifts of any amount need a bank record or a written acknowledgment from the charity; gifts of $250 or more need the written acknowledgment specifically. Different rule, different chapter, same principle — the record has to exist.</p>

<h2>United Kingdom</h2>

<p>HMRC's position for the self-employed is direct: keep records of all business expenses, including the receipts, and keep them for <strong>at least 5 years after the 31 January submission deadline</strong> of the tax year they belong to. There is no formal small-amount exemption; a claim you cannot support is a claim that can be disallowed.</p>

<p>VAT adds a second layer. To reclaim input VAT you need a <strong>VAT invoice</strong> from the supplier, not just proof of payment. For supplies of <strong>£250 or less</strong> a <em>simplified</em> VAT invoice is enough — the retailer's name, address and VAT number, the date, a description, the total including VAT, and the VAT rate. Most till receipts from VAT-registered shops already are simplified invoices. Without a valid invoice HMRC can refuse the input tax, and a card statement will not rescue it. VAT records are kept for <strong>6 years</strong>.</p>

<h2>Australia</h2>

<p>The ATO uses a threshold in the other direction. If your <strong>total</strong> claim for work-related expenses is <strong>$300 or less</strong>, you do not need receipts — but you must still be able to show how you worked out the amount. Once the total goes above $300, you need <strong>written evidence</strong> for the expenses (a receipt, invoice or similar document showing the supplier, amount, nature of the goods, date paid and date of the document). Records are kept for <strong>five years</strong>, and a clear photograph of a receipt is acceptable evidence.</p>

<h2>Canada</h2>

<p>The CRA expects supporting documents for the expenses you claim and requires records to be kept for <strong>six years from the end of the tax year they relate to</strong>. Electronic records must be kept in an electronically readable form for that period — a scanned or photographed receipt counts, but the file has to still open in year six.</p>

<h2>The record that survives all four</h2>

<p>Across the IRS, HMRC, ATO and CRA the same four facts keep appearing: what it cost, when, where or from whom, and why. A receipt supplies three of them. The fourth is yours to add, on the day, while you still remember. Do that consistently and the question of whether you needed the receipt stops mattering — you have the record, and the receipt is a bonus.</p>
""",
},

# ===========================================================================
# 4. Expense trackers that don't sell your data — the privacy wedge
# ===========================================================================
{
 "out": "posts/expense-tracker-apps-that-dont-sell-your-data.html",
 "slug": "expense-tracker-apps-that-dont-sell-your-data",
 "seo_title": "Expense Tracker Apps That Don’t Sell Your Data",
 "meta": "Most receipt apps make money from your purchase data. A 30-second App Store check shows which don't, plus five questions to ask before you trust one.",
 "title": "How to find an expense tracker that doesn't sell your data",
 "description": "Most receipt and budgeting apps make money from your purchase data. A 30-second check on the App Store tells you which ones don't, plus five questions to ask before you trust an app with a year of receipts.",
 "dek": "The App Store already tells you whether an app collects your data — most people never look. Here is where the label is, what 'Data Linked to You' actually means for a receipt app, and the five questions that separate a tool from a data business.",
 "topic": "Privacy",
 "date_iso": "2026-09-20", "updated": "2026-09-20",
 "og": "og-expense-tracker-apps-that-dont-sell-your-data.png",
 "cta": "receiptsnap",
 "cta_title": "The privacy label reads Data Not Collected. Because there is nothing to collect.",
 "cta_text": "Receipt Snap has no account and no server. The receipt is read on your iPhone and stays there — which is not a promise, it is how the app is built.",
 "checked": None,
 "takeaways": [
   "Open any app's App Store page and scroll to <strong>App Privacy</strong>. <strong>Data Not Collected</strong> means what it says. <strong>Data Linked to You</strong> with 'Purchases' listed means your receipts are the product.",
   "Points-for-receipts apps are purchase-data businesses. The points are what they pay for the inventory.",
   "Five questions decide it: Is an account required? Does it work in airplane mode? Can you export without paying? What happens if the company shuts down? Where is the text recognition done?",
   "On-device apps have real limits — no web dashboard, sync only through your own iCloud. Decide whether you need those before you decide on privacy.",
 ],
 "faq": [
   ("How can I tell if an app sells my data?",
    "Look at the App Privacy section of its App Store page. Developers must declare what they collect and whether it is linked to your identity or used to track you across other apps. 'Data Not Collected' is the cleanest answer. An expense app that lists 'Purchases' or 'Financial Info' under 'Data Used to Track You' or 'Data Linked to You' is telling you, in Apple's words, what its business is."),
   ("Are receipt scanning apps that pay you safe?",
    "They are safe in the sense that they do what they say. What they say, in their privacy policies, is that your purchase data is shared with partners — consumer goods companies and market research firms. You are paid in points worth a few dollars a month. Whether that trade is worth it is your call; it is not a hidden one."),
   ("Is an offline expense tracker really private?",
    "Working offline is a strong signal, because an app that never needs a connection has no way to send anything anywhere. Check two more things: that there is no account (an account is a server, somewhere), and that export is available so the data is genuinely yours to move."),
   ("What does Receipt Snap collect?",
    "Nothing. The App Store privacy label reads Data Not Collected. There is no account, no analytics inside the app, and no Receipt Snap server to receive anything. Text recognition runs on the iPhone using Apple's own frameworks. This website uses Google Analytics; the app does not."),
 ],
 "sources": [
   ("Apple — App privacy details on the App Store", "https://developer.apple.com/app-store/app-privacy-details/"),
   ("Why receipt apps pay you pennies (the business model, with numbers)", "/posts/receipt-apps-pay-you-pennies.html"),
 ],
 "related": ["receipt-apps-pay-you-pennies", "how-long-to-keep-receipts", "do-you-need-receipts-for-tax-deductions"],
 "body": """
<h2>The 30-second check</h2>

<p>Every app on the App Store carries a privacy label the developer is required to fill in. Open the app's page, scroll past the screenshots and reviews, and find the section headed <strong>App Privacy</strong>. There are three possible headings, and for an expense app they mean very different things:</p>

<table class="facts">
  <thead><tr><th>Label</th><th>What it means</th><th>For a receipt app</th></tr></thead>
  <tbody>
    <tr><td><strong>Data Not Collected</strong></td><td>The developer collects nothing from the app</td><td>Your receipts stay with you</td></tr>
    <tr><td><strong>Data Not Linked to You</strong></td><td>Collected, but not tied to your identity</td><td>Usually crash reports and usage stats; read the detail</td></tr>
    <tr><td><strong>Data Linked to You</strong></td><td>Collected and tied to your account or device</td><td>If 'Purchases' or 'Financial Info' is listed here, your spending is the product</td></tr>
    <tr><td><strong>Data Used to Track You</strong></td><td>Shared with other companies for advertising or data brokerage</td><td>The clearest signal that data leaves the app</td></tr>
  </tbody>
</table>

<p>Tap into the detail and it lists categories: Purchases, Financial Info, Contact Info, Location, Identifiers. An expense tracker that collects 'Purchases' and links it to you has told you, in Apple's standard wording, that it keeps a record of what you buy attached to who you are. That is not necessarily sinister — a cloud sync service has to store your data somewhere. But it is the question answered.</p>

<h2>Why receipt apps became data businesses</h2>

<p>Search the App Store for "receipt" and the top results offer to pay you. Scan a grocery receipt, earn points, redeem a gift card. The mechanics are covered in <a href="/posts/receipt-apps-pay-you-pennies.html">why receipt apps pay you pennies</a>; the short version is that a photograph of a receipt is a line of purchase-panel data — what you bought, which brand, at what price, how often — and consumer goods companies pay for that at a rate far above the points you receive.</p>

<p>None of that is hidden. It is in the privacy policy and, since Apple introduced the labels, on the store page. It is simply that nobody reads either while standing in a car park trying to empty a wallet.</p>

<h2>Five questions that decide it</h2>

<h3>1. Is an account required?</h3>
<p>An account means a server, and a server means a copy of your data that you do not control, held under someone else's retention policy and someone else's breach. Some apps need one for a legitimate reason — multi-device sync, a web dashboard, a team. If you do not need those things, an account is a cost with no benefit.</p>

<h3>2. Does it work in airplane mode?</h3>
<p>The most honest test there is. Put the phone in airplane mode and scan a receipt. If the app reads it, the text recognition is happening on the device. If it spins, the photograph is going to a server to be read, and whatever happens to it there is governed by the privacy policy, not by you.</p>

<h3>3. Can you export everything without paying?</h3>
<p>Your records are yours. Plenty of expense apps put export behind the subscription, which means the day you stop paying is the day your five-year archive becomes a set of screenshots. Look for a CSV or PDF export on the free tier, and use it at least once a year regardless.</p>

<h3>4. What happens if the company shuts down?</h3>
<p>Apps do. If your receipts exist only on their servers, they go with it. If they exist on your phone, in a format you have already exported, the app's fate is irrelevant to your tax records — which, depending on where you live, you may need to keep for <a href="/posts/how-long-to-keep-receipts.html">three to fifteen years</a>.</p>

<h3>5. Where is the text recognition done?</h3>
<p>Apple ships on-device text recognition in iOS, and on recent iPhones an on-device language model that can pull structure — merchant, total, tax — out of that text. An app built on those frameworks never has to send the image anywhere to understand it. An app that sends it to a cloud service may do a good job too; it just has your receipt, and the question is what it does next.</p>

<!--cta-->

<h2>The honest trade-offs of on-device</h2>

<p>Private is not free. An app with no server cannot give you a web dashboard, cannot email you a weekly summary, and cannot let an accountant log in. Sync between your own devices is possible only through your own iCloud account, if the app supports it. Parsing is harder too: a cloud service can throw a large model at every receipt and learn from everyone's data; an on-device app gets one phone, offline.</p>

<p>If you run a team, or you live in a web browser, a cloud product may genuinely be the better tool, and it is worth knowing that before choosing on principle. If you are one person with a wallet full of paper and a tax return to file, the trade-offs mostly run the other way.</p>

<h2>A note on this site</h2>

<p>We make Receipt Snap, so we are not a neutral reviewer and will not rank ourselves against other apps here. What we will say is how to check: the label on our App Store page reads Data Not Collected, the app works in airplane mode, there is no account, and export is on the free tier. Run the same five questions on anything else you are considering, including ours.</p>
""",
},

# ===========================================================================
# 5. Mileage log template — the lead magnet
# ===========================================================================
{
 "out": "posts/mileage-log-template.html",
 "slug": "mileage-log-template",
 "seo_title": 'Free Mileage Log Template: Excel, PDF, CSV',
 "meta": 'Free mileage log template with the columns the IRS and HMRC expect: date, destination, business purpose, miles, odometer. Excel workbook, PDF or a CSV.',
 "title": "Free mileage log template with the columns the IRS and HMRC expect",
 "description": "A free mileage log template with the four columns every tax authority requires: date, destination, purpose, miles, plus odometer readings and totals. Excel, PDF or CSV.",
 "dek": "The template is simple because the rule is simple: four facts per trip, written down on the day. Take the Excel workbook, the PDF or the CSV. No email address, no sign up, no watermark.",
 "topic": "Mileage",
 "date_iso": "2026-09-20", "updated": "2026-09-20",
 "og": "og-mileage-log-template.png",
 "cta": "drivesnap",
 "cta_title": "Or let the phone fill the template in.",
 "cta_text": "DriveSnap records the date, distance and route of every drive automatically and asks for the purpose with one swipe. At the end of the year it exports exactly these columns as a CSV. No drive caps, nothing uploaded.",
 "checked": (f'Columns checked against <a href="{_IRS_P463}">IRS Publication 463</a> (what an adequate record must show) and '
             f'<a href="{_HMRC_AMAP}">HMRC mileage guidance</a> on 21 September 2026. '
             f'The 2026 rates written into the files were checked against the '
             f'<a href="{_IRS_RATES}">IRS standard mileage rates page</a> and '
             f'<a href="{_HMRC_AMAP}">GOV.UK</a> the same day.'),
 "takeaways": [
   "Every trip needs four facts: <strong>date, destination, business purpose, miles</strong>. The template has a column for each, plus start and end odometer so the miles are provable.",
   "Three real files, no sign up: an <strong><a href='/downloads/mileage-log-template.xlsx'>Excel workbook</a></strong> with the totals already formulated, a <strong><a href='/downloads/mileage-log-template.pdf'>print ready PDF</a></strong>, and a <strong><a href='/downloads/mileage-log-template.csv'>CSV</a></strong> for Google Sheets or Numbers.",
   "Fill it in weekly at the latest. Publication 463 treats a log kept weekly as timely. A log rebuilt in April is not.",
   "Record the odometer on 1 January and 31 December (or 6 April and 5 April in the UK). Total miles is what the business share is measured against.",
 ],
 "faq": [
   ("What should a mileage log include?",
    "For each business trip: the date, where you went (or from and to), the business purpose, and the miles driven. Keep your odometer reading at the start and end of the year as well, so total mileage, and therefore the business use percentage, can be shown. Those are the IRS's four elements; HMRC and the CRA ask for the same information."),
   ("Does a spreadsheet count as a mileage log?",
    "Yes. No tax authority requires a particular format. A spreadsheet, a paper diary and an app are equally acceptable if they contain the required facts and were kept at or near the time of the trips."),
   ("How often do I need to update a mileage log?",
    "As close to the trip as practical. IRS Publication 463 says a log maintained weekly that accounts for the week's use is a timely kept record, so a Friday evening habit is enough. Monthly reconstruction from memory is not."),
   ("Do I need to record odometer readings for every trip?",
    "Not for every trip if you record the miles for each one, but you do need odometer readings at the start and end of the year to establish total mileage. Many people also note the odometer on each trip because it makes the miles for each trip self evidently real rather than estimated."),
   ("Is the template free?",
    "Yes. The Excel workbook, the PDF and the CSV are free, with no sign up and no email address. They are made by the people who build DriveSnap, which does the same job automatically, but nothing here requires the app."),
 ],
 "sources": [
   ("IRS Publication 463, Chapter 5, Recordkeeping (adequate records; weekly logs are timely)", _IRS_P463),
   ("GOV.UK: Expenses and benefits, business travel mileage", _HMRC_AMAP),
 ],
 "related": ["mileage-log-for-irs-audit", "irs-mileage-log-requirements", "irs-mileage-rate-2026"],
 "body": """
<h2>Get the template</h2>

<div class="callout">
  <h3>Four files, all free</h3>
  <p><strong><a href="/downloads/mileage-log-template.xlsx">Excel workbook (.xlsx)</a></strong>. A real spreadsheet, not a CSV renamed. Sixty trip rows, the deduction column already formulated, a totals row, and a second sheet holding the 2026 rates and the rules they come from. Opens in Excel, Numbers, LibreOffice and Google Sheets.</p>
  <p><strong><a href="/downloads/mileage-log-template.pdf">Printable PDF</a></strong>. One landscape page, 24 trips, with a worked example printed faintly in the first row so the form explains itself. Made for the glovebox.</p>
  <p><strong><a href="/downloads/mileage-log-template.csv" download>CSV</a></strong>. The plainest possible version, for importing anywhere.</p>
  <p><strong><a href="/templates/mileage-log/">Printable page</a></strong>. The same log as a web page, if you would rather press print than download anything. It strips the site chrome automatically.</p>
  <p style="color:var(--faint);font-size:.92rem">No email address, no sign up, no watermark, nothing to unsubscribe from.</p>
</div>

<p>The honest caveat, stated before you download anything: <strong>a template only works if you fill it in on the day</strong>. That is not a sales line, it is the rule. IRS Publication 463 says a record kept at or near the time of the trip <em>has more value than a statement prepared later when there is generally a lack of accurate recall</em>. A blank template in a drawer and no template at all produce exactly the same deduction. If you know you will not keep it up, skip to the part about letting the phone do it.</p>

<h2>What the columns are, and why each one is there</h2>

<table class="facts">
  <thead><tr><th>Column</th><th>Why</th></tr></thead>
  <tbody>
    <tr><td><strong>Date</strong></td><td>Required everywhere. It also decides which rate applies: in 2026 the IRS rate changed on 1 July, and the HMRC rate on 6 April.</td></tr>
    <tr><td><strong>From and To</strong></td><td>The IRS asks for the destination; recording both ends makes the distance checkable.</td></tr>
    <tr><td><strong>Business purpose</strong></td><td>The field no device can fill in. "Client meeting, Acme" is enough. "Work" is not.</td></tr>
    <tr><td><strong>Odometer start and end</strong></td><td>Makes the miles evidence rather than assertion. Optional per trip, essential at year start and end.</td></tr>
    <tr><td><strong>Business miles</strong></td><td>What the deduction is calculated from.</td></tr>
    <tr><td><strong>Personal miles</strong></td><td>Optional, but it lets the log show total use, which is what business use percentage needs.</td></tr>
    <tr><td><strong>Rate</strong></td><td>Prefilled with the 2026 IRS rates so each trip is valued at the rate in force on its date.</td></tr>
    <tr><td><strong>Parking and tolls</strong></td><td>Deductible on top of the mileage rate, with the receipt.</td></tr>
  </tbody>
</table>

<h2>Which file to take, and how to open it</h2>

<p><strong>Excel, Numbers or LibreOffice:</strong> take the xlsx. It is a real workbook, so the deduction column and the totals row already calculate. Open it, type into the first empty row, and the numbers at the bottom move on their own.</p>

<p><strong>Google Sheets:</strong> take the xlsx too, then File, Import, Upload, and choose Replace spreadsheet. Sheets converts the formulas intact. The CSV also imports, but a CSV cannot carry formulas, so you would be retyping the sums yourself. If you want the log on your phone as well as your laptop, this is the version to use, because Sheets syncs and a downloaded workbook does not.</p>

<p><strong>Paper:</strong> take the PDF. It is one landscape page, so it prints correctly from a phone, a library printer or anything else, and the example row is printed faintly enough not to be confused with your own entries. Keep it in the vehicle rather than on a desk, because the whole point is writing the trip down before you have driven somewhere else.</p>

<p><strong>Something else entirely:</strong> take the CSV. Every accounting package, every spreadsheet and every import wizard in the world reads it. It carries the same columns in the same order as the workbook, so the two are interchangeable.</p>

<p>None of them ask for an email address, and none of them expire.</p>

<h2>What a filled in week looks like</h2>

<p>This is the part most templates leave out, so here is a real week from a small trades business, written the way it should be written.</p>

<table class="facts">
  <thead><tr><th>Date</th><th>From and to</th><th>Business purpose</th><th>Odo start</th><th>Odo end</th><th>Miles</th></tr></thead>
  <tbody>
    <tr><td>2 Mar</td><td>Home office to 14 Bridge St</td><td>Boiler service, Mrs Okafor</td><td>41,230</td><td>41,241</td><td>11.4</td></tr>
    <tr><td>2 Mar</td><td>14 Bridge St to Plumbase, Fenton</td><td>Collect parts for the Bridge St job</td><td>41,241</td><td>41,247</td><td>6.2</td></tr>
    <tr><td>3 Mar</td><td>Home office to Acme Ltd, Reading</td><td>Site survey before quoting</td><td>41,251</td><td>41,289</td><td>38.1</td></tr>
    <tr><td>5 Mar</td><td>Home office to 2 Larch Close and back</td><td>Leak callout, emergency</td><td>41,302</td><td>41,325</td><td>22.8</td></tr>
    <tr><td>6 Mar</td><td>Home office to bank, then post office</td><td>Pay in cheques; ship warranty claim</td><td>41,330</td><td>41,338</td><td>7.9</td></tr>
  </tbody>
</table>

<p>Look at what makes it credible. Every purpose names a person, a place or a job. Not one distance is a round number. The odometer runs continuously, so the second trip on 2 March starts where the first one ended. And the gap between 41,247 on the 2nd and 41,251 on the 3rd is four miles of personal driving, left visible rather than quietly absorbed into the business total. A log that shows its own personal miles reads as a record. A log where every mile is business reads as a claim.</p>

<p>One trip is deliberately absent. The van also went to the supermarket on the 4th, and that is not in the log because it is not deductible. Neither is a trip from home to a single regular workplace, which is commuting whatever is in the back.</p>

<h2>How to keep it so it stands up</h2>

<ol>
  <li><strong>Write the odometer down on the first day of the year.</strong> A photo of the dashboard with the date is fine. Do the same on the last day. Without a total, the business share is unsupported.</li>
  <li><strong>Log trips the same day, or at least the same week.</strong> Publication 463 says a weekly log that accounts for the week's use is timely. Longer than that and you are reconstructing, which the IRS reserves for records lost to fire, flood or casualty, not for forgetting.</li>
  <li><strong>Write the purpose in words a stranger would understand.</strong> An examiner reads that column first. Name the client, the site, the errand. <a href="/posts/mileage-log-for-irs-audit.html">What gets a log rejected</a> goes through this in detail.</li>
  <li><strong>Do not round.</strong> 14.3 miles, not 15. A column of identical round numbers is the surest sign of an estimate, and estimates are not deductible.</li>
  <li><strong>Leave commuting out.</strong> Home to your regular workplace is personal, however far.</li>
  <li><strong>Total monthly.</strong> The CSV has the formula; on paper, add it up at the bottom of each sheet. Split at 30 June if you are in the US this year.</li>
</ol>

<!--cta-->

<h2>Working out the deduction</h2>

<p><strong>US:</strong> business miles in each half of 2026 × the rate for that half, so 72.5¢ to 30 June and 76¢ from 1 July. The <a href="/posts/irs-mileage-rate-2026.html">2026 rate page has a calculator</a>. <strong>UK:</strong> 55p for the first 10,000 business miles in the tax year from 6 April 2026, then 25p, with a <a href="/posts/hmrc-mileage-rates-2026.html">calculator here</a>. <strong>Canada, if you work for yourself:</strong> a different model altogether. Actual vehicle costs multiplied by business kilometres ÷ total kilometres, which is why the odometer columns matter more there than anywhere.</p>

<h2>Common mistakes the template is designed to prevent</h2>

<ul>
  <li>A log with distances but no purposes. It is half a record.</li>
  <li>A log started in March and backfilled to January. The dates say one thing; the handwriting says another.</li>
  <li>A single annual rate applied to a year that had two.</li>
  <li>No odometer reading for the first day of the year and the last, so total miles, and therefore the business percentage, cannot be shown.</li>
  <li>The only copy inside an app you have stopped paying for. Export it, and keep the export with your tax paperwork.</li>
</ul>
""",
},

# ===========================================================================
# 6. IRS mileage log requirements (upgraded)
# ===========================================================================
{
 "out": "posts/irs-mileage-log-requirements.html",
 "slug": "irs-mileage-log-requirements",
 "seo_title": 'What the IRS Requires in a Mileage Log (2026)',
 "meta": 'The four things every business trip record must show, the 2026 rate, why a reconstructed log fails an audit, and how long to keep it.',
 "title": "What the IRS actually requires in a mileage log",
 "description": "The four things every business trip record must contain, what the 2026 standard rate is, why a reconstructed log fails an audit, and how long to keep it.",
 "dek": "Most people lose this deduction twice — first by not recording trips, then by trying to rebuild them in April. The requirements are short. They are worth reading once, properly.",
 "topic": "Mileage",
 "date_iso": "2026-09-01", "updated": "2026-09-20",
 "og": "og-irs-mileage-log-requirements.png",
 "cta": "drivesnap",
 "cta_title": "The record exists on the day the trip happened.",
 "cta_text": "DriveSnap records the date, distance and route of every drive automatically, asks for the purpose with one swipe, and stamps the rate onto each drive as it is recorded — so a filed year never quietly changes.",
 "checked": CHECKED_IRS,
 "takeaways": [
   "Every business trip record must show <strong>the date, the destination, the business purpose, and the miles</strong>. Plus your total mileage for the year.",
   "Records must be kept <strong>contemporaneously</strong> — at or near the time of the trip. A weekly log is timely; an April reconstruction is not.",
   "2026 has two rates: <strong>72.5¢</strong> to 30 June and <strong>76¢</strong> from 1 July. Split your miles at the date.",
   "Keep the log at least <strong>3 years</strong> from the filing date; 6 if income was understated by more than 25%.",
   "Purpose is the field examiners read first, and the only one a phone cannot supply.",
 ],
 "faq": [
   ("What must an IRS mileage log contain?",
    "For each business trip: the date, the destination, the business purpose, and the miles driven. You also need your total mileage for the year, so the business-use share can be worked out. Records should be kept contemporaneously — written at or near the time of the trip."),
   ("What is the IRS standard mileage rate?",
    "2026 has two rates, because the IRS raised it midyear: 72.5 cents a mile for 1 January to 30 June, and 76 cents for 1 July to 31 December. Multiply the business miles driven in each half by the rate for that half. The 70 cents figure still quoted in a lot of places is the 2025 rate. You choose the standard rate or actual expenses, not both."),
   ("How long should I keep a mileage log?",
    "Three years from the date you filed the return, which is the normal period the IRS has to assess additional tax. Keep it six years if the return understated income by more than 25%."),
   ("Does a spreadsheet count as a mileage log?",
    "Yes. The IRS does not require a particular format — it requires the four elements per trip, recorded at or near the time of travel. A spreadsheet, a paper diary and an app are equally acceptable if they contain the same information."),
 ],
 "sources": [
   ("IRS Publication 463 — Travel, Gift, and Car Expenses", _IRS_P463),
   ("IRS — Standard mileage rates", _IRS_RATES),
   ("IRS — How long should I keep records?", _IRS_KEEP),
   ("GOV.UK — HMRC approved mileage rates (55p from 6 April 2026)", _HMRC_AMAP),
 ],
 "related": ["mileage-log-for-irs-audit", "irs-mileage-rate-2026", "mileage-log-template"],
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

<p>Records are expected to be kept <em>contemporaneously</em> — at or near the time of the trip. Publication 463 accepts a log maintained weekly that accounts for the week's use as timely. A log assembled months later from memory is weaker evidence, and a log that is suspiciously round (every trip 20 miles, every week identical) invites exactly the questions you do not want.</p>

<p>This is the real argument for automatic tracking. Not that it saves typing, but that the record exists on the day the trip happened rather than the day you needed it.</p>

<h2>Standard rate or actual expenses</h2>

<table class="facts">
  <thead><tr><th>Method</th><th>What you track</th><th>Best when</th></tr></thead>
  <tbody>
    <tr><td><strong>Standard mileage</strong></td><td>Business miles × the published rate — <strong>72.5¢ before 1 July 2026, 76¢ after</strong></td><td>Your car is inexpensive to run, or you want the simplest defensible record</td></tr>
    <tr><td><strong>Actual expenses</strong></td><td>Fuel, insurance, repairs, depreciation — multiplied by your business use percentage</td><td>The vehicle is expensive, heavily used for business, or recently bought</td></tr>
  </tbody>
</table>

<p>You still need the mileage log either way. The actual-expense method needs the business use percentage, and that comes from the same numbers. The rate, the midyear change and a calculator are on the <a href="/posts/irs-mileage-rate-2026.html">2026 mileage rate page</a>.</p>

<p>Knowing what a log must contain is one half of it. Knowing how it is judged when somebody reads it is the other: <a href="/posts/mileage-log-for-irs-audit.html">what an auditor rejects in a mileage log</a> lists the six failures, quotes the rule behind each, and ends with a checklist you can score your own log against.</p>

<!--cta-->

<h2>How long to keep it</h2>

<p>Three years from the date you filed is the normal period the IRS has to assess additional tax, so three years is the working answer. Six if a return understated income by more than 25%. There is no time limit where no return was filed.</p>

<p>Storage matters more than people expect. A log that only exists inside an app you have stopped paying for is not a record you control. Keep an export.</p>

<h2>If your app stops logging halfway through the month</h2>

<p>This is worth naming, because it is the most common way an otherwise careful record ends up with a hole in it. Several popular trackers cap their free tier by number of drives. MileIQ allows 40 a month, Everlance 30 automatic trips, Driversnote reporting of up to 15, all checked on 21 September 2026. Pass the cap and the app simply stops recording until the month turns over.</p>

<p>The miles you drove after the cap are still deductible. They just are not written down anywhere, and writing them in afterwards is the statement prepared later that this page has been warning about. <a href="/posts/is-mileiq-free.html">What a free tier cap does to a tax record</a> works through the arithmetic and compares what each free plan actually allows.</p>

<h2>A note on other countries</h2>

<p>The four elements are close to universal, but the arithmetic is not. In the UK, HMRC's approved rate is <strong>55p a mile for the first 10,000 business miles from 6 April 2026</strong> (45p before that) and 25p after — see the <a href="/posts/hmrc-mileage-rates-2026.html">2026/27 HMRC rates</a>. In Canada, the per-kilometre rates apply to <em>employee reimbursement</em>; self-employed filers must use actual expenses and business use percentage, which requires odometer readings at the start and end of the year.</p>

<p>If an app quotes you a single flat rate per mile regardless of country, it is doing the US calculation wherever you live.</p>
""",
},

# ===========================================================================
# 7. How long to keep receipts (upgraded: +Canada, +Australia)
# ===========================================================================
{
 "out": "posts/how-long-to-keep-receipts.html",
 "slug": "how-long-to-keep-receipts",
 "seo_title": 'How Long to Keep Receipts for Taxes (US, UK, UAE, CA, AU)',
 "meta": '3 years in the US, 5 for the UK self-employed, 6 in Canada, 5 in Australia and the UAE (15 for property). What a valid record shows and whether photos count.',
 "title": "How long do you have to keep receipts for taxes?",
 "description": "Three years in the US, five for the UK self-employed, six for UK companies and Canada, five in Australia and the UAE (fifteen for UAE property). What a valid record must show, whether photos count, and what happens when the app holding them shuts down.",
 "dek": "It depends where you file, and the range is wider than most people assume — three years in one place, fifteen in another for the same shoebox. The retention periods for six jurisdictions, with the rule each comes from.",
 "topic": "Records",
 "date_iso": "2026-09-01", "updated": "2026-09-20",
 "og": "og-how-long-to-keep-receipts.png",
 "cta": "receiptsnap",
 "cta_title": "Kept on hardware you own, for as long as the rule says.",
 "cta_text": "Receipt Snap reads the receipt on your iPhone and keeps it there — no account, no server, nothing retained by anyone but you. Export any time, without paying.",
 "checked": (f'Checked against <a href="{_IRS_KEEP}">IRS record retention guidance</a>, <a href="{_HMRC_KEEP}">HMRC self-employed records</a>, '
             f'<a href="{_HMRC_VAT}">HMRC VAT records</a>, the <a href="{_ATO_RECORDS}">ATO</a>, the <a href="{_CRA_KEEP}">CRA</a> and UAE tax legislation on 20 September 2026.'),
 "takeaways": [
   "<strong>US: 3 years</strong> from filing. 6 if income was understated by more than 25%; indefinitely if no return was filed.",
   "<strong>UK: 5 years</strong> after the 31 January deadline for the self-employed; <strong>6 years</strong> for companies and for VAT records.",
   "<strong>Canada: 6 years</strong> from the end of the tax year. <strong>Australia: 5 years.</strong>",
   "<strong>UAE: 5 years</strong> for VAT records, <strong>15 years</strong> for anything relating to real estate.",
   "Photographs count everywhere, if they are legible, complete and can be produced on request. Thermal paper fades; the photo does not.",
 ],
 "faq": [
   ("How long should I keep receipts for taxes in the US?",
    "Three years from the date you filed the return, which is the normal period the IRS has to assess additional tax. Six years if income was understated by more than 25%, seven for a claim for worthless securities or a bad-debt deduction, and indefinitely if no return was filed. Employment tax records: four years."),
   ("Do digital photos of receipts count as records?",
    "Yes. The IRS, HMRC, the ATO, the CRA and the UAE Federal Tax Authority all accept electronic records provided they are legible, complete and can be produced on request. Canada adds that electronic records must stay electronically readable for the whole six years. Photograph the whole receipt, including the tax line."),
   ("How long must UK businesses keep records?",
    "Self-employed individuals must keep records for at least five years after the 31 January submission deadline of the relevant tax year. Companies keep records for six years from the end of the accounting period. VAT records are kept for six years."),
   ("How long must records be kept for UAE VAT?",
    "Five years for most businesses, and fifteen years for records relating to real estate. Tax invoices must be retained and produced on request by the Federal Tax Authority."),
   ("How long do I keep receipts in Australia and Canada?",
    "Australia: five years from the date you lodge the return. Canada: six years from the end of the last tax year the records relate to, unless the CRA gives written permission to destroy them earlier."),
 ],
 "sources": [
   ("IRS — How long should I keep records?", _IRS_KEEP),
   ("GOV.UK — Business records if you're self-employed: how long to keep your records", _HMRC_KEEP),
   ("GOV.UK — Keeping VAT records", _HMRC_VAT),
   ("ATO — Records you need to keep", _ATO_RECORDS),
   ("Canada Revenue Agency — Where to keep your records, for how long", _CRA_KEEP),
   ("UAE Federal Decree-Law on Tax Procedures (record retention)", _UAE_TPL),
 ],
 "related": ["do-you-need-receipts-for-tax-deductions", "uae-vat-record-keeping", "expense-tracker-apps-that-dont-sell-your-data"],
 "body": """
<p>The honest answer is that it depends where you file, and the ranges are wider than most people assume — three years in one place, fifteen in another for the same shoebox.</p>

<table class="facts">
  <thead><tr><th>Where</th><th>How long</th><th>Counted from, and notes</th></tr></thead>
  <tbody>
    <tr><td>United States</td><td><strong>3 years</strong></td><td>The filing date. 6 years if income was understated by more than 25%; 7 for worthless-securities or bad-debt claims; no limit where no return was filed.</td></tr>
    <tr><td>United Kingdom — self-employed</td><td><strong>5 years</strong></td><td>After the 31 January submission deadline for that tax year.</td></tr>
    <tr><td>United Kingdom — companies, and VAT</td><td><strong>6 years</strong></td><td>From the end of the accounting period; VAT records 6 years (10 under the One Stop Shop schemes).</td></tr>
    <tr><td>Canada</td><td><strong>6 years</strong></td><td>From the end of the last tax year they relate to. Electronic records must remain electronically readable.</td></tr>
    <tr><td>Australia</td><td><strong>5 years</strong></td><td>From when you lodge the return.</td></tr>
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

<p>This is why a faded thermal receipt is a genuine problem rather than an aesthetic one. Thermal paper loses its print — sometimes within months in a hot car or a sunlit kitchen. The record does not become disputed; it becomes blank. Whether you needed the receipt in the first place is covered in <a href="/posts/do-you-need-receipts-for-tax-deductions.html">do you need receipts for tax deductions</a>.</p>

<h2>Do photographs count?</h2>

<p>Yes. Electronic records are accepted in every jurisdiction above, provided they are legible, complete, and can be produced when asked. A clear photograph of the whole receipt — edges included, not cropped through the total — is a valid record. Canada goes one step further: electronic records must be kept in an electronically readable format for the full six years, so a photo in a format that still opens in year six is what counts.</p>

<blockquote><p>Photograph it the day you get it. A receipt you meant to photograph is not a record, and thermal ink does not wait.</p></blockquote>

<!--cta-->

<h2>The part nobody plans for</h2>

<p>If your records live inside an app, three questions decide whether you actually have them:</p>

<ol>
  <li><strong>Can you export everything, in a format something else can read?</strong> If the answer is a screenshot, that is not an export.</li>
  <li><strong>What happens if the company shuts down, or you stop paying?</strong> Plenty of expense apps put export behind the subscription — so the moment you stop paying, your five-year archive becomes unreachable.</li>
  <li><strong>Who else has a copy?</strong> Anything uploaded is a copy you no longer control, held under someone else's retention policy and someone else's breach risk.</li>
</ol>

<p>The safest arrangement is dull: keep the originals on a device you own, export at least once a year, and store that export where you keep the rest of your tax paperwork. Fifteen years — the UAE property rule — is longer than most apps, and some companies, will exist.</p>
""",
},

# ===========================================================================
# 8. UAE VAT records (upgraded)
# ===========================================================================
{
 "out": "posts/uae-vat-record-keeping.html",
 "slug": "uae-vat-record-keeping",
 "seo_title": 'UAE VAT Record Keeping: 5 Years, 15 for Real Estate',
 "meta": 'What the UAE FTA requires you to keep and for how long, what a valid tax invoice shows, when a simplified invoice is allowed, and what a TRN is.',
 "title": "What records UAE VAT actually requires you to keep",
 "description": "Five years, fifteen for real estate, and what has to appear on a valid tax invoice — including when a simplified invoice is allowed and what a TRN is for.",
 "dek": "VAT arrived in the UAE in 2018 at 5%, with a record-keeping regime stricter than most small businesses were used to. The rules are not complicated. The retention periods are longer than people expect.",
 "topic": "UAE VAT",
 "date_iso": "2026-09-01", "updated": "2026-09-20",
 "og": "og-uae-vat-record-keeping.png",
 "cta": "receiptsnap",
 "cta_title": "Reads the TRN. Sets the currency to dirhams. Keeps it for fifteen years if it has to.",
 "cta_text": "Receipt Snap reads UAE receipts on the device, recognises the TRN and captures merchant, date, total and VAT — on hardware you own, not a service that may not exist in 2041.",
 "checked": (f'Checked against the <a href="{_UAE_VAT_LAW}">UAE Federal Decree-Law on VAT</a> and the '
             f'<a href="{_UAE_TPL}">Federal Decree-Law on Tax Procedures</a> on 20 September 2026.'),
 "takeaways": [
   "Keep VAT records for <strong>5 years</strong>; <strong>15 years</strong> for anything relating to real estate.",
   "A full tax invoice needs the words 'Tax Invoice', the supplier's name, address and <strong>TRN</strong>, a sequential number and date, a description, the net, the VAT rate and amount, and the gross.",
   "A <strong>simplified tax invoice</strong> is allowed for supplies under AED 10,000 or to unregistered customers — most retail receipts are one.",
   "The 15-digit TRN is the surest sign a receipt is a UAE one, and the reason an amount with no symbol is in dirhams.",
   "Electronic records are accepted if complete, legible and producible on request. Photograph the whole receipt — a crop that loses the TRN loses the invoice.",
 ],
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
 "sources": [
   ("UAE Federal Decree-Law on Value Added Tax", _UAE_VAT_LAW),
   ("UAE Federal Decree-Law on Tax Procedures", _UAE_TPL),
   ("Federal Tax Authority — VAT", "https://tax.gov.ae/en/taxes/vat/"),
 ],
 "related": ["how-long-to-keep-receipts", "do-you-need-receipts-for-tax-deductions", "receipt-apps-pay-you-pennies"],
 "body": """
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

<p>A shorter form is permitted where the supply is under <strong>AED 10,000</strong>, or the customer is not VAT-registered. It still has to carry the words "Tax Invoice", the supplier's name, address and TRN, the date, a description of the supply, and the total with the VAT amount shown. Most retail receipts you collect in the UAE are simplified tax invoices.</p>

<h2>The TRN is the thing worth noticing</h2>

<p>The Tax Registration Number is a 15-digit number issued by the Federal Tax Authority. It has to appear on every tax invoice a registered business issues — which makes it the most reliable marker that a receipt is a UAE one.</p>

<blockquote><p>Plenty of UAE receipts print no currency symbol at all. The TRN is what tells you the amount is in dirhams. It is a better signal than the symbol, because it is legally required to be there.</p></blockquote>

<p>The same logic holds elsewhere: a GSTIN means India, a UK postcode means sterling. Reading the registration number is more dependable than looking for a symbol that may never have been printed.</p>

<!--cta-->

<h2>Electronic records are fine</h2>

<p>The FTA accepts electronic records provided they are complete, legible and producible on request. A clear photograph of an entire simplified tax invoice satisfies that — but photograph the whole thing. A crop that cuts off the TRN or the VAT line removes the elements that make it a tax invoice at all.</p>

<p>For how the UAE periods compare with the US, UK, Canada and Australia, see <a href="/posts/how-long-to-keep-receipts.html">how long to keep receipts for taxes</a>.</p>
""",
},

# ===========================================================================
# 9. Forgot to track DoorDash miles (upgraded)
# ===========================================================================
{
 "out": "posts/forgot-to-track-doordash-miles.html",
 "slug": "forgot-to-track-doordash-miles",
 "seo_title": 'Forgot to Track DoorDash Miles? What the IRS Allows',
 "meta": "Months of gig driving with no log: the IRS incomplete-records rule, sampling, the 2026 rates, and why DoorDash’s own mileage number is not your deduction.",
 "title": "You forgot to track your DoorDash miles. Now what?",
 "description": "What the IRS allows when months of gig driving went unlogged: the incomplete-records rule, sampling, and why DoorDash's own number is not your deduction.",
 "dek": "You are four months in. The deliveries happened, the fuel was real, and there is no log. The rules allow less than most advice admits, and more than the panic suggests.",
 "topic": "Mileage",
 "date_iso": "2026-09-19", "updated": "2026-09-20",
 "og": "og-forgot-to-track-doordash-miles.png",
 "cta": "drivesnap",
 "cta_title": "Never do this again — which is the only easy part.",
 "cta_text": "DriveSnap logs the date, distance and route of every drive automatically, and asks for the purpose with one swipe. Tracking is free and uncapped on purpose: a log with a hole in it is worth nothing for tax.",
 "checked": CHECKED_IRS,
 "takeaways": [
   "You <strong>cannot estimate</strong>. Publication 463: you can't deduct amounts you approximate or estimate.",
   "You <strong>can</strong> use the incomplete-records rule: your own written statement plus other evidence — and the IRS names delivery invoices as exactly that evidence.",
   "<strong>Sampling</strong> is allowed: keep a proper log for a representative period and show the rest of the year matched it.",
   "DoorDash's mileage figure covers active deliveries only. The miles between orders are yours too, and the commute is not.",
   "2026 has two rates — 72.5¢ to 30 June, 76¢ from 1 July. Split at the date.",
 ],
 "faq": [
   ("Can I estimate my DoorDash miles for taxes?",
    "No. Publication 463 says plainly that you can't deduct amounts you approximate or estimate. What you can do is different: where records are incomplete, the IRS lets you prove the deduction with your own written statement plus other supporting evidence. For delivery work that evidence already exists — your order history, with a date, a pickup and a drop-off for every trip."),
   ("Does DoorDash track my miles for taxes?",
    "Not in the way you need. DoorDash gives an estimate of distance on active deliveries. It does not count the driving between finishing one order and being sent the next, or the repositioning you do while online and waiting. Those miles are deductible and the platform's figure leaves them out, so treat the number as corroboration, not as your log."),
   ("What is the IRS mileage rate for 2026?",
    "Two rates, because it changed midyear: 72.5 cents a mile from 1 January to 30 June 2026, and 76 cents from 1 July. Split your miles at the date and apply each rate to its own half. The 70 cents figure still quoted in plenty of places is the 2025 rate."),
   ("Can I reconstruct a mileage log after the fact?",
    "Partly, and the distinction matters. The IRS allows reconstruction where records were lost for reasons beyond your control — fire, flood, casualty. Forgetting is not one of those. What is available to you is the incomplete-records rule and sampling: keep an adequate record from today, then show the logged period is representative of the rest of the year."),
 ],
 "sources": [
   ("IRS Publication 463 — Chapter 5 (incomplete records, sampling, timely-kept records)", _IRS_P463),
   ("IRS — Standard mileage rates", _IRS_RATES),
 ],
 "related": ["mileage-log-for-irs-audit", "is-mileiq-free", "irs-mileage-log-requirements"],
 "body": """
<h2>What you cannot do</h2>

<p>You cannot pick a number. IRS <a href="https://www.irs.gov/pub/irs-pdf/p463.pdf">Publication 463</a> puts it in one line, under How To Prove Expenses:</p>

<blockquote><p>You can't deduct amounts that you approximate or estimate.</p></blockquote>

<p>"About 12,000 miles" is an estimate. So is a round 200 miles every week for 26 weeks. Even numbers repeating down a spreadsheet are the first thing that reads as invented, and vehicle expenses are held to a stricter standard than most deductions.</p>

<p>The other thing people reach for — rebuilding the whole year from memory and calling it a log — has a specific place in the rules, and it is not this one. Reconstruction is for records lost <em>because of reasons beyond your control</em>: the publication names fire, flood and other casualties. Forgetting to log is not a casualty.</p>

<h2>What you can do</h2>

<p>Publication 463 has a section headed <strong>What if I Have Incomplete Records?</strong>, and it is the one that applies to you. Where you lack complete records for an element of an expense, you prove it with:</p>

<ul>
  <li><strong>your own written or oral statement</strong> containing specific information about that element, and</li>
  <li><strong>other supporting evidence</strong> sufficient to establish it.</li>
</ul>

<p>Then comes the sentence that matters for anyone who drives for a delivery app. On whether supporting evidence has to be direct:</p>

<blockquote><p>For example, the nature of your work, such as making deliveries, provides circumstantial evidence of the use of your car for business purposes. Invoices of deliveries establish when you used the car for business.</p></blockquote>

<p>Read that again with your own year in mind. Every completed order in your app history is dated, timed, and has a pickup and a drop-off attached to it. That is not memory. It is a record of when the car was used for business, and the IRS names your line of work as the example.</p>

<h2>The evidence a Dasher already has</h2>

<table class="facts">
  <thead><tr><th>Source</th><th>What it establishes</th></tr></thead>
  <tbody>
    <tr><td>Delivery history export from the app</td><td>The date and time of every trip, with pickup and drop-off addresses</td></tr>
    <tr><td>Weekly earnings statements and bank deposits</td><td>Which weeks you actually worked, and how hard</td></tr>
    <tr><td>Oil-change and service invoices, inspection reports</td><td>Odometer readings on real dates — the bookends for total miles</td></tr>
    <tr><td>Phone location history, if you have it switched on</td><td>Routes on specific days, including the miles between orders</td></tr>
    <tr><td>Your own written statement</td><td>The business purpose, which no device can supply for you</td></tr>
  </tbody>
</table>

<p>Distance still has to be worked out trip by trip from the addresses, not waved at. It is tedious. It is also the difference between a deduction that stands up and one that does not.</p>

<h2>Sampling: the part almost nobody uses</h2>

<p>There is a legitimate shortcut in the rules, and it is worth more to you than any app:</p>

<blockquote><p>You can keep an adequate record for parts of a tax year and use that record to prove the amount of business or investment use for the entire year. You must demonstrate by other evidence that the periods for which an adequate record is kept are representative of the use throughout the tax year.</p></blockquote>

<p>The publication's own example is someone who keeps proper records for the first week of each month, shows 75% business use, and uses invoices and bills to demonstrate the other weeks ran at the same rate.</p>

<p>For a delivery driver that translates cleanly. Start an honest log today. Keep it for a full, ordinary month. Then use your platform statements — orders completed and hours online, week by week — to show the logged month was typical of the months before it. The stronger the match between the sampled weeks and the unlogged ones, the stronger the claim.</p>

<p>Two cautions. A sample taken in a freak week proves the wrong thing, in both directions. And a weekly log counts as timely: Publication 463 says a log maintained weekly that accounts for use during the week is a timely kept record, so you do not have to write it up at every red light.</p>

<!--cta-->

<h2>DoorDash's number is not your log</h2>

<p>DoorDash provides an annual mileage estimate. It is an estimate of distance on <em>active deliveries</em> — broadly, from accepting an order to completing it.</p>

<p>What it leaves out is the rest of the working day: driving back out of a suburb after a drop-off, repositioning to a busier area, waiting somewhere hot with the app on. Those miles are business miles. The platform's figure does not know about them.</p>

<p>The other direction matters too. The drive from your home to the zone where you start, and home again at the end, is commuting, and commuting is not deductible. Use the platform number as a sanity check against your own figure. If yours is lower, you have missed something.</p>

<h2>What the miles are worth this year</h2>

<p>2026 has two rates, because the IRS raised it midyear.</p>

<table class="facts">
  <thead><tr><th>Period</th><th>Business rate per mile</th></tr></thead>
  <tbody>
    <tr><td>1 January – 30 June 2026</td><td>72.5¢</td></tr>
    <tr><td>1 July – 31 December 2026</td><td>76¢</td></tr>
  </tbody>
</table>

<p>So a driver with 8,000 business miles in the first half and 6,000 in the second has 8,000 × 72.5¢ = $5,800, plus 6,000 × 76¢ = $4,560. A $10,360 deduction, from a spreadsheet nobody wanted to keep. There is a <a href="/posts/irs-mileage-rate-2026.html">calculator on the 2026 rate page</a>.</p>

<p>Split your year at 30 June. One rate applied across the whole year is wrong twice over, and it is wrong on the page an examiner reads first.</p>

<h2>What to do this week</h2>

<ol>
  <li><strong>Export your delivery history</strong> for the whole period, before the app ages it out.</li>
  <li><strong>Find two odometer readings</strong> with dates on them — a service invoice, an inspection, a photo of the dash. They bracket your total miles, and the total is what the business share is measured against.</li>
  <li><strong>Start a real log today.</strong> Date, destination, purpose, miles. Keep it for a full month without editing it to look tidy. The <a href="/posts/mileage-log-template.html">free template</a> has the right columns.</li>
  <li><strong>Reconstruct trip by trip</strong> for the unlogged months from the order history, and write the statement that goes with it: what the work was, which days you drove, why the car was in use.</li>
  <li><strong>Keep it all together</strong> — export, statements, invoices, log — in one place you control, not inside an app subscription you might cancel. If the tracker you pick caps its free tier, read <a href="/posts/is-mileiq-free.html">what a drive cap does to a tax record</a> first: a log that stops on the 23rd puts you straight back here.</li>
</ol>

<p>Then never do this again, which is the only part that is easy.</p>

<p>Before you file, run the finished log past <a href="/posts/mileage-log-for-irs-audit.html">the checklist an examiner would use</a>. A reconstructed log gets read more carefully than a contemporaneous one, so it is worth knowing in advance which six things get one rejected.</p>
""",
},

# ===========================================================================
# 10. The bug that would have shipped (ported, unchanged text)
# ===========================================================================
{
 "out": "posts/the-bug-that-would-have-shipped.html",
 "slug": "the-bug-that-would-have-shipped",
 "seo_title": 'The Bug That Would Have Shipped',
 "meta": 'A mileage tracker that silently recorded zero distance for city driving, and four ways the same app could have put a wrong number on a tax return.',
 "title": "The bug that would have shipped",
 "description": "A mileage tracker that silently recorded zero distance for city driving — and four separate ways the same app could have put a wrong number on someone's tax return.",
 "dek": "I spent a week building a mileage tracker. It is the kind of app that looks finished long before it works.",
 "topic": "Building",
 "date_iso": "2026-08-31", "updated": "2026-08-31",
 "og": "og-the-bug-that-would-have-shipped.png",
 "cta": "drivesnap",
 "cta_title": "The app this was about.",
 "cta_text": "DriveSnap shipped with every one of these bugs fixed and a named test for each. It logs city drives correctly, stamps the rate onto each drive, and never shows you two numbers that disagree.",
 "checked": None,
 "takeaways": None,
 "faq": None,
 "sources": None,
 "related": ["receipt-apps-pay-you-pennies", "irs-mileage-log-requirements"],
 "disclaimer": "Notes from building the app. Nothing here is tax advice.",
 "body": (_PORTED / "bug.html").read_text(),
},

# ===========================================================================
# 11. Receipt apps pay you pennies (ported, unchanged text)
# ===========================================================================
{
 "out": "posts/receipt-apps-pay-you-pennies.html",
 "slug": "receipt-apps-pay-you-pennies",
 "seo_title": 'Why Receipt Apps Pay You Pennies for Your Data',
 "meta": 'The biggest receipt apps in the App Store are purchase-data companies. What they actually sell, what it costs you, and what I built instead.',
 "title": "Receipt apps pay you pennies because your data is worth dollars",
 "description": "The biggest receipt apps in the App Store are not expense trackers. They are purchase-data companies. What they actually sell, what it costs you, and what I built instead.",
 "dek": "Search the App Store for \"receipt\" and the top results look like games. I spent a week working out why an app that helps you organise paper would need a leaderboard.",
 "topic": "Privacy",
 "date_iso": "2026-08-30", "updated": "2026-08-30",
 "og": "og-receipt-apps-pay-you-pennies.png",
 "cta": "receiptsnap",
 "cta_title": "The opposite, built.",
 "cta_text": "Receipt Snap reads your receipt on the phone in about two seconds. No account. No servers. Nothing uploaded — the privacy label reads Data Not Collected.",
 "checked": None,
 "takeaways": None,
 "faq": None,
 "sources": None,
 "related": ["expense-tracker-apps-that-dont-sell-your-data", "how-long-to-keep-receipts"],
 "disclaimer": "An essay from the founder. Nothing here is tax advice.",
 "body": (_PORTED / "pennies.html").read_text(),
},
# ===========================================================================
# 12. Is MileIQ free? — the free-tier comparison
# ===========================================================================
{
 "out": "posts/is-mileiq-free.html",
 "slug": "is-mileiq-free",
 "seo_title": 'Is MileIQ Free? The 40 Drive Limit, Explained',
 "meta": 'MileIQ is free for 40 drives a month, then logging stops. What that cap does to a tax record, what the paid plan costs now, and the free alternatives.',
 "title": "Is MileIQ free? Yes, for 40 drives a month",
 "description": "MileIQ is free for 40 drives a month, then logging stops. What the cap does to a tax record, what the paid plan costs now, and how the free tiers compare.",
 "dek": "The free tier is real, and it has a hard edge. Forty drives, then the app stops logging until next month. Here is what that costs you, what the paid plan now charges, and what the other free tiers actually allow.",
 "topic": "Mileage",
 "date_iso": "2026-09-21", "updated": "2026-09-21",
 "og": "og-is-mileiq-free.png",
 "cta": "drivesnap",
 "cta_title": "Tracking should never be the thing you pay for.",
 "cta_text": "DriveSnap records every drive automatically with no monthly cap, because a log with a hole in it is worth nothing at tax time. Your location history never leaves the phone, and there is no account to make.",
 "checked": ('Prices and limits read from <a href="https://mileiq.com/pricing" rel="noopener">mileiq.com/pricing</a>, '
             'the App Store listings for each app via the public iTunes lookup API, and '
             '<a href="https://www.driversnote.com/pricing" rel="noopener">driversnote.com/pricing</a> on 21 September 2026. '
             'Past MileIQ prices read from Internet Archive captures of the same pricing page.'),
 "takeaways": [
   "Free means <strong>40 drives a month</strong>. MileIQ's pricing page says so and its App Store listing repeats it.",
   "Paid is <strong>$11.66 a month billed annually</strong>, or $13.99 a month billed monthly. Twelve months at the annual rate is $139.92.",
   "That price has moved twice. The annual plan was $4.99 a month in May 2024 and $7.50 a month in December 2025.",
   "<strong>The cap is the real cost, not the price.</strong> Hit 40 drives on the 23rd and the rest of the month is missing from your log, and the IRS does not let you fill a gap like that from memory.",
   "Other free tiers: Everlance allows 30 automatic trips a month, Driversnote allows reporting of up to 15 trips, Stride states no trip cap at all.",
 ],
 "faq": [
   ("Is MileIQ really free?",
    "Yes, up to a point. The free plan costs nothing and tracks drives automatically, but it is limited to 40 drives every month. That wording is on MileIQ's own pricing page and in its App Store description, which reads 'Unlimited mileage tracking with 40 free drives every month'. Once you pass 40 in a calendar month, further drives are not logged until the month rolls over or you subscribe."),
   ("How much does MileIQ cost in 2026?",
    "The Unlimited plan is listed at $11.66 a month billed annually, or $13.99 a month billed monthly, checked on mileiq.com/pricing on 21 September 2026. Twelve months at the annual rate comes to $139.92. Internet Archive captures of the same page show $4.99 a month billed annually in May 2024 and $7.50 in December 2025, so the annual plan has risen roughly 134 percent in about two and a half years."),
   ("What happens when you hit 40 drives on MileIQ?",
    "Tracking stops for the rest of that month unless you upgrade. The drives you already recorded stay. The problem is the ones after it: they are simply not in the log. For tax that matters more than the money, because IRS Publication 463 expects records kept at or near the time of the trip, and a month with a missing second half cannot be rebuilt from recollection."),
   ("What is the best free mileage tracker instead of MileIQ?",
    "It depends on how much you drive. If you take fewer than 15 business trips a month, almost any free tier covers you. Above that the caps start to bite: Everlance allows 30 automatic trips a month on its free plan, Driversnote allows reporting of up to 15 trips, and Stride's App Store listing names no trip cap. DriveSnap does not cap tracking at all, though it is not on the App Store yet."),
 ],
 "sources": [
   ("MileIQ pricing page (free plan and Unlimited plan prices)", "https://mileiq.com/pricing"),
   ("Internet Archive capture of mileiq.com/pricing, 21 May 2024", "https://web.archive.org/web/20240521164128/https://mileiq.com/pricing"),
   ("Internet Archive capture of mileiq.com/pricing, 17 December 2025", "https://web.archive.org/web/20251217173256/https://mileiq.com/pricing"),
   ("MileIQ on the App Store", "https://apps.apple.com/us/app/id578830929"),
   ("Everlance on the App Store (free plan: 30 automatic trips a month)", "https://apps.apple.com/us/app/id985378916"),
   ("Driversnote pricing page (free plan: reporting of up to 15 trips)", "https://www.driversnote.com/pricing"),
   ("IRS Publication 463, Chapter 5 (timely kept records)", _IRS_P463),
 ],
 "related": ["mileage-log-for-irs-audit", "irs-mileage-log-requirements", "forgot-to-track-doordash-miles"],
 "body": """
<h2>The short answer</h2>

<p>MileIQ is free for <strong>40 drives a month</strong>. After that the app stops logging until the calendar month turns over or you subscribe. The paid plan, called Unlimited, is listed at <strong>$11.66 a month billed annually</strong> or <strong>$13.99 a month billed monthly</strong>.</p>

<p>Those are the numbers on <a href="https://mileiq.com/pricing" rel="noopener">MileIQ's own pricing page</a>, read on 21 September 2026. The App Store listing puts it more strangely. Under the feature list it says:</p>

<blockquote><p>Unlimited mileage tracking with 40 free drives every month</p></blockquote>

<p>Both halves of that sentence cannot be true at once. The pricing page is the one to believe: free is 40 drives, and 40 drives is a cap.</p>

<h2>What 40 drives actually buys you</h2>

<p>A drive is one trip, not one day. Leaving the house, visiting three clients and coming home is four drives, not one. That arithmetic is what catches people out.</p>

<table class="facts">
  <thead><tr><th>How you work</th><th>Drives in a month</th><th>Does the free tier hold?</th></tr></thead>
  <tbody>
    <tr><td>Two client visits a week</td><td>About 16</td><td>Yes, comfortably</td></tr>
    <tr><td>A trades business with two jobs a day, four days a week</td><td>About 48</td><td>No. You run out in the last week</td></tr>
    <tr><td>Estate agent, six viewings a week</td><td>About 52</td><td>No</td></tr>
    <tr><td>Delivery driving, three shifts a week</td><td>Hundreds</td><td>No. You run out on the first day</td></tr>
  </tbody>
</table>

<p>So the free tier fits the person who drives for business occasionally. It does not fit the person whose deduction is large enough to be worth tracking, which is the same person the cap is designed to convert.</p>

<h2>Why a cap is worse than a price</h2>

<p>This is the part worth being precise about, because it is a tax problem rather than a pricing complaint.</p>

<p>When the cap bites on the 23rd, you do not lose a feature. You lose the last eight days of the month from your record. And the IRS does not treat a record with a gap in it the way it treats a complete one. <a href="https://www.irs.gov/publications/p463" rel="noopener">Publication 463</a> is direct about timing:</p>

<blockquote><p>You should record the elements of an expense or of a business use at or near the time of the expense or use and support it with sufficient documentary evidence. A timely kept record has more value than a statement prepared later when there is generally a lack of accurate recall.</p></blockquote>

<p>Filling those eight days in from memory in April is precisely the statement prepared later. The publication does allow reconstruction, but it reserves it for records lost <em>because of reasons beyond your control</em>, and it names fire, flood and other casualties. A subscription prompt is not a casualty.</p>

<p>There is a legitimate route through an incomplete month, and it is narrower than most people assume: your own written statement plus other supporting evidence sufficient to establish the trips. That is real work, per trip, for every day the app declined to record. It is covered in full in <a href="/posts/mileage-log-for-irs-audit.html">what an auditor rejects in a mileage log</a>.</p>

<p>The money is the smaller half of the argument. Eight days of a busy month might be 300 business miles. At the second half 2026 rate of 76 cents, that is $228 of deduction that never existed on paper. Do it twice a year and the cap has cost you more than the subscription it was selling.</p>

<h2>What to check before you trust any free tier</h2>

<p>Caps are advertised. The things that actually decide whether a free tier is usable tend not to be.</p>

<ul>
  <li><strong>Is the cap on tracking or on the export?</strong> A cap on tracking puts a gap in the evidence. A cap on the export leaves the record complete and charges you to get it out, which is recoverable. The first is a tax problem; the second is a purchase decision.</li>
  <li><strong>What happens to the drives you already logged if you stop paying?</strong> Ask before you need the answer. A year of data locked behind a lapsed subscription in March is the worst version of this.</li>
  <li><strong>Can you get a full export, in a plain format, without a subscription?</strong> CSV opens anywhere in ten years. A proprietary report inside an app does not.</li>
  <li><strong>Where do the drives live?</strong> A mileage tracker knows every address you visited and at what time. Read the privacy label on the App Store listing rather than the marketing page.</li>
  <li><strong>Does the app know this year's rate?</strong> Two rates apply in 2026, and plenty of apps still carry one.</li>
</ul>

<h2>What MileIQ costs now, and what it cost before</h2>

<p>Price rises are normal. The size and the frequency of these ones are what people notice at renewal.</p>

<table class="facts">
  <thead><tr><th>Date the pricing page was captured</th><th>Annual plan</th><th>Monthly plan</th><th>Free tier</th></tr></thead>
  <tbody>
    <tr><td>21 May 2024</td><td>$4.99 a month billed annually</td><td>$5.99</td><td>40 drives a month</td></tr>
    <tr><td>17 December 2025</td><td>$7.50 a month billed annually</td><td>$8.99</td><td>40 drives a month</td></tr>
    <tr><td>21 September 2026</td><td>$11.66 a month billed annually</td><td>$13.99</td><td>40 drives a month</td></tr>
  </tbody>
</table>

<p>The first two rows come from Internet Archive captures of the same page, linked in the sources below. The annual plan has gone from $4.99 to $11.66 a month in about two and a half years, a rise of roughly 134 percent. The free tier has not moved once in that time. Forty drives in 2024, forty drives today.</p>

<!--cta-->

<h2>The free tiers, side by side</h2>

<p>Everything in this table was read on 21 September 2026 from each company's own pricing page or App Store listing. Free tiers change without announcement, so check the date before you trust the row.</p>

<table class="facts">
  <thead><tr><th>App</th><th>What the free plan allows</th><th>Cheapest paid plan</th></tr></thead>
  <tbody>
    <tr><td><strong>MileIQ</strong></td><td>40 drives a month</td><td>$11.66 a month billed annually</td></tr>
    <tr><td><strong>Everlance</strong></td><td>Manual recording plus 30 automatic trips a month</td><td>Not listed on the App Store page</td></tr>
    <tr><td><strong>Driversnote</strong></td><td>Automatic tracking, reporting of up to 15 trips</td><td>$11 a month</td></tr>
    <tr><td><strong>Hurdlr</strong></td><td>Automatic mileage tracking is a Premium feature</td><td>$9.99 a month or $99.99 a year</td></tr>
    <tr><td><strong>Stride</strong></td><td>Free, with no trip cap stated in its listing</td><td>No paid tier listed</td></tr>
    <tr><td><strong>DriveSnap</strong></td><td>Unlimited tracking and unlimited history</td><td>Free in full at version 1.0</td></tr>
  </tbody>
</table>

<p>One detail worth carrying away. Hurdlr's App Store description, today, tells you to "deduct 57.5 cents for every mile you drive". That was the rate in 2020. The correct figures for 2026 are 72.5 cents to 30 June and 76 cents from 1 July, which is on the <a href="/posts/irs-mileage-rate-2026.html">2026 rate page</a> with the IRS source. Marketing copy goes stale; your return cannot.</p>

<h2>If you already hit the cap this month</h2>

<ol>
  <li><strong>Write down today's odometer, with the date.</strong> A photo of the dashboard is fine. You need a bookend for total miles whatever you do next.</li>
  <li><strong>Reconstruct the missing days trip by trip, not in a lump.</strong> Calendar entries, job sheets, invoices, delivery history, bank card traces at fuel stops. Each one pins a date and a destination.</li>
  <li><strong>Write the purpose in your own words for each trip.</strong> That is the element no app and no bank statement can supply, and the one examiners look at first.</li>
  <li><strong>Do not round.</strong> A column of clean numbers is the single clearest sign of an estimate, and estimates are not deductible.</li>
  <li><strong>Move to something that does not stop.</strong> Any tracker without a monthly cap, ours included, removes the failure mode entirely.</li>
</ol>

<h2>Where DriveSnap sits, said plainly</h2>

<p>We build <a href="/drivesnap/">DriveSnap</a>, so read this section with that in mind.</p>

<p>DriveSnap does not cap tracking, and it is not going to. The reasoning is the argument above: capping the log is capping the evidence, and evidence with a hole in it fails at exactly the moment it is needed. Recording drives stays free and uncapped whatever the app charges for later. Nothing is uploaded either, because there is no server to upload to, which matters more than usual for an app that knows every address you visited.</p>

<p>The honest part: DriveSnap is not on the App Store yet. If you need something installed this afternoon, one of the other free tiers above will serve you better today, and the comparison is on the <a href="/compare/drivesnap-vs-mileiq/">DriveSnap and MileIQ comparison page</a>. When it ships, tracking will still be free and still be uncapped.</p>

<p>Whichever you pick, the thing that survives an examination is the record, not the app. The <a href="/posts/mileage-log-template.html">free log template</a> has the columns the IRS expects, and it never stops working on the 23rd.</p>
""",
},

# ===========================================================================
# 13. Mileage log for an IRS audit — what gets rejected
# ===========================================================================
{
 "out": "posts/mileage-log-for-irs-audit.html",
 "slug": "mileage-log-for-irs-audit",
 "seo_title": 'Mileage Log for an IRS Audit: What Gets Rejected',
 "meta": 'What an examiner rejects in a mileage log: round numbers, no business purpose, no yearly total, a log written in one sitting. With a checklist to grade yours.',
 "title": "Will your mileage log survive an IRS audit?",
 "description": "What an examiner rejects in a mileage log, the Publication 463 rule behind each one, the two allowances nobody uses, and a checklist to grade your log.",
 "dek": "An examiner is not reading your log for the truth of it. They are reading it for the four elements Publication 463 requires, and for the tells that say it was written in one sitting in April.",
 "topic": "Mileage",
 "date_iso": "2026-09-21", "updated": "2026-09-21",
 "og": "og-mileage-log-for-irs-audit.png",
 "cta": "drivesnap",
 "cta_title": "The log that passes is the one written on the day.",
 "cta_text": "DriveSnap stamps the date, the distance and the route onto every drive as it happens, and asks for the purpose with one swipe. That is a contemporaneous record by construction, not by willpower.",
 "checked": CHECKED_IRS,
 "takeaways": [
   "The vehicle elements are fixed: <strong>the mileage for each business use, the total miles for the year, the date of each use, your business destination, and the business purpose</strong>. Publication 463 lists them in Table 5.1.",
   "<strong>Estimates are not deductible.</strong> Publication 463 says so in one line, and round numbers repeating down a column are what an estimate looks like.",
   "A log written after the fact is weaker by rule, not by opinion: a timely kept record <strong>has more value than a statement prepared later</strong>.",
   "Reconstruction is allowed for records lost to <strong>fire, flood and other casualties</strong>. Forgetting is not one of them.",
   "Two allowances people leave on the table: the <strong>incomplete records</strong> rule and <strong>sampling</strong> a representative period.",
 ],
 "faq": [
   ("What does the IRS look for in a mileage log during an audit?",
    "The elements in Table 5.1 of Publication 463. For car expenses you must show the mileage for each business use and the total miles for the year, the date of each use, your business destination, and the business purpose of the trip. An examiner reads the purpose column first, because it is the one no device can fill in for you and the one that separates a business mile from a personal one."),
   ("Will the IRS accept a mileage log written after the fact?",
    "It carries less weight by rule. Publication 463 says a timely kept record has more value than a statement prepared later when there is generally a lack of accurate recall. A weekly log counts as timely, so you do not have to write at every stop. Rebuilding a whole year in April is a different thing, and it is the thing examiners are trained to spot."),
   ("Can I reconstruct a mileage log if I lost my records?",
    "Sometimes. Publication 463 allows you to prove a deduction by reconstructing your records when you cannot produce a receipt for reasons beyond your control, and it names fire, flood and other casualties. If nothing was destroyed and you simply did not keep a log, the route is different: your own written statement plus other supporting evidence sufficient to establish each element."),
   ("How long should I keep a mileage log?",
    "Publication 463 says generally three years from the date you file the return on which the deduction is claimed, and a return filed early counts as filed on the due date. If you claim depreciation on the vehicle there is a longer obligation: you must keep records of the business use of your car for each year of the recovery period."),
 ],
 "sources": [
   ("IRS Publication 463, Chapter 5: What Are Adequate Records, Timely kept records, Proving business purpose", _IRS_P463),
   ("IRS Publication 463, Table 5.1: How To Prove Certain Business Expenses", _IRS_P463),
   ("IRS Publication 463: What if I Have Incomplete Records, Sampling, Destroyed records", _IRS_P463),
   ("IRS standard mileage rates", _IRS_RATES),
 ],
 "related": ["irs-mileage-log-requirements", "is-mileiq-free", "mileage-log-template"],
 "body": """
<h2>What an examiner is actually checking</h2>

<p>Vehicle expenses sit in a category the tax code treats more strictly than most. The consequence is practical: an examiner does not weigh whether your claim seems plausible. They check whether the record contains the required elements, and whether it looks like it was kept when the driving happened.</p>

<p>That is a much easier test to pass than people fear, and a much easier one to fail on a technicality. Everything below is from <a href="https://www.irs.gov/publications/p463" rel="noopener">Publication 463</a>, quoted rather than paraphrased, because the wording is the whole point.</p>

<h2>The elements, quoted</h2>

<p>Table 5.1 of Publication 463 sets out what a record must show. For transportation, the row reads:</p>

<blockquote><p>Cost of each separate expense. For car expenses, the cost of the car and any improvements, the date you started using it for business, the mileage for each business use, and the total miles for the year. ... Date of the expense. For car expenses, the date of the use of the car. ... Your business destination. ... Business purpose for the expense.</p></blockquote>

<p>Four things per trip, then, plus one thing per year:</p>

<table class="facts">
  <thead><tr><th>Element</th><th>What satisfies it</th><th>What does not</th></tr></thead>
  <tbody>
    <tr><td>Date of the use</td><td>The actual date of the trip</td><td>A week or a month</td></tr>
    <tr><td>Business destination</td><td>A named place. "Acme Ltd, Reading"</td><td>"Client"</td></tr>
    <tr><td>Business purpose</td><td>"Site survey before quoting"</td><td>"Work", "business", or blank</td></tr>
    <tr><td>Mileage for that use</td><td>14.3 miles, measured</td><td>"About 15"</td></tr>
    <tr><td>Total miles for the year</td><td>Odometer on 1 January and 31 December</td><td>Nothing at all, which is the usual answer</td></tr>
  </tbody>
</table>

<p>That last row is the one most logs miss completely. Without a yearly total there is no denominator, so the share of the car used for business cannot be shown, and an examiner has nothing to test your business miles against.</p>

<h2>Six things that get a log rejected</h2>

<h3>1. Round numbers</h3>

<p>Publication 463 says it in one line, under How To Prove Expenses: you cannot deduct amounts that you approximate or estimate. A column reading 20, 15, 30, 25, 20 down the page is an estimate wearing a spreadsheet. Real driving produces 14.3 and 31.8 and 6.2. Measured distances are the cheapest credibility you will ever buy.</p>

<h3>2. A log with no business purpose</h3>

<p>The publication is explicit that the purpose is normally written down:</p>

<blockquote><p>You must generally provide a written statement of the business purpose of an expense. However, the degree of proof varies according to the circumstances in each case. If the business purpose of an expense is clear from the surrounding circumstances, then you don't need to give a written explanation.</p></blockquote>

<p>The exception it gives is narrow and specific: a sales representative calling on customers along an established route does not have to explain the route every time. Unless your work looks like that, write the purpose. A log full of distances with an empty purpose column is half a record, and it is the half that proves the miles were business at all.</p>

<h3>3. A whole year written in one sitting</h3>

<p>This is the rule that decides most disputes:</p>

<blockquote><p>You should record the elements of an expense or of a business use at or near the time of the expense or use and support it with sufficient documentary evidence. A timely kept record has more value than a statement prepared later when there is generally a lack of accurate recall.</p></blockquote>

<p>Note what it does not say. It does not say you must write at every stop. Publication 463 explicitly allows a weekly habit: a log maintained on a weekly basis that accounts for use during the week is a timely kept record. Friday evening is enough. April is not.</p>

<h3>4. Reconstruction with nothing behind it</h3>

<p>Reconstruction has a defined place in the rules, and it is narrower than the advice you will read elsewhere:</p>

<blockquote><p>If you can't produce a receipt because of reasons beyond your control, you can prove a deduction by reconstructing your records or expenses. Reasons beyond your control include fire, flood, and other casualties.</p></blockquote>

<p>Losing a phone, cancelling a subscription, or simply not getting round to it are not casualties. That does not leave you with nothing, but it does mean you are in the incomplete records rule below rather than in the reconstruction rule, and the evidential burden is different.</p>

<h3>5. Commuting counted as business</h3>

<p>The trip from home to your regular place of work is personal, whatever is in the back of the car. Where your home is your principal place of business the first trip of the day can be a business mile, which is a genuinely valuable distinction, but it is also a common place for a log to overstate itself. If every single day starts with an identical business mileage figure from the same address, expect that to be the first question.</p>

<h3>6. Two numbers on the return that disagree</h3>

<p>The mileage claimed on the return has to reconcile with the log, and the log has to reconcile with the odometer readings. Where a year spans two rates, as 2026 does, one rate applied across the whole year produces a total that cannot be reproduced from the log. The correct treatment is 72.5 cents for trips to 30 June and 76 cents from 1 July, with the full working on the <a href="/posts/irs-mileage-rate-2026.html">2026 rate page</a>.</p>

<!--cta-->

<h2>What the rules allow that almost nobody uses</h2>

<h3>The incomplete records rule</h3>

<p>Where you lack complete records for an element, Publication 463 gives a route:</p>

<blockquote><p>If you don't have complete records to prove an element of an expense, then you must prove the element with: Your own written or oral statement containing specific information about the element, and Other supporting evidence that is sufficient to establish the element.</p></blockquote>

<p>And for business purpose specifically, the evidence is allowed to be indirect:</p>

<blockquote><p>For example, the nature of your work, such as making deliveries, provides circumstantial evidence of the use of your car for business purposes. Invoices of deliveries establish when you used the car for business.</p></blockquote>

<p>Job sheets, invoices, calendar entries, delivery history and service receipts with odometer readings on them are all evidence of this kind. They are not a substitute for a log. They are what makes a partial log hold.</p>

<h3>Sampling</h3>

<p>The most useful paragraph in the chapter, and the least known:</p>

<blockquote><p>You can keep an adequate record for parts of a tax year and use that record to prove the amount of business or investment use for the entire year. You must demonstrate by other evidence that the periods for which an adequate record is kept are representative of the use throughout the tax year.</p></blockquote>

<p>The publication's own worked example keeps proper records for the first week of every month, shows 75 percent business use, and uses invoices and bills to demonstrate the remaining weeks ran at the same rate. The burden is on the representativeness, not on the volume of paper. A sample taken in an unusual week proves the wrong thing, in either direction.</p>

<h2>Grade your own log</h2>

<p>Ten questions. Count the yes answers.</p>

<ol>
  <li>Does every entry have a real date, and do the dates run in order?</li>
  <li>Does every entry name a destination a stranger could find on a map?</li>
  <li>Does every entry state a purpose in words, not a category?</li>
  <li>Are the distances uneven and specific rather than round?</li>
  <li>Do you have an odometer reading with a date on it near the start of the year?</li>
  <li>And another near the end of the year?</li>
  <li>Was each entry written within a week of the trip?</li>
  <li>Are commuting trips excluded, or marked personal?</li>
  <li>For 2026, are trips before and after 1 July valued at their own rate?</li>
  <li>Does something outside the log corroborate a sample of it: an invoice, a calendar entry, a service receipt?</li>
</ol>

<p><strong>Nine or ten:</strong> your log is doing its job. Keep it and stop worrying. <strong>Six to eight:</strong> fixable, and the gaps are usually purpose and the year end odometer. Fix them going forward and gather corroboration for what is already written. <strong>Five or fewer:</strong> treat this year as a rebuild. Start an adequate log today, read the incomplete records rule above, and assemble the evidence that establishes the months behind you. The <a href="/posts/mileage-log-template.html">free log template</a> has every column in this checklist, and <a href="/posts/irs-mileage-log-requirements.html">what the IRS requires in a mileage log</a> goes through each element in detail.</p>

<h2>How long you have to keep it</h2>

<blockquote><p>Generally, this means you must keep records that support your deduction (or an item of income) for 3 years from the date you file the income tax return on which the deduction is claimed. A return filed early is considered filed on the due date.</p></blockquote>

<p>There is a longer obligation attached to the car itself where you claim depreciation: you must keep records of the business use of your car for each year of the recovery period. In practice that means the log outlives the three year window, so keep it with the vehicle paperwork rather than with the year's receipts.</p>

<h2>If the letter arrives</h2>

<p>Publication 463 sets the expectation plainly:</p>

<blockquote><p>If your return is examined, you may have to provide additional information to the IRS. This information could be needed to clarify or to establish the accuracy or reliability of information contained in your records, statements, testimony, or documentary evidence before a deduction is allowed.</p></blockquote>

<p>So the log is the opening document, not the whole case. Send it with the corroboration attached rather than waiting to be asked: the odometer photographs, a handful of invoices matching logged trips, the calendar for a sampled month. A log that arrives with its own evidence reads as a record. A log that arrives alone reads as a claim.</p>

<p>And if none of this exists yet because months went unlogged, the honest path through it is set out in <a href="/posts/forgot-to-track-doordash-miles.html">what to do when you forgot to track your miles</a>.</p>
""",
},

]

INDEX = {p["slug"]: p for p in POSTS}
