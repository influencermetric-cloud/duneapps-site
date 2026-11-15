#!/usr/bin/env python3
"""Invoice templates by country: a hub, six country pages, and a PDF for each.

Each page is something to use, not read: the fields the tax authority requires (with
the clause cited), a blank PDF in the country's paper size, and an invoice you fill
in on the page and print or save as PDF. Nothing typed is sent anywhere; the draft
is kept in the visitor's own browser storage.

Every legal fact below was read at the source on 15 November 2026:
  UAE   FTA Public Clarification VATP006 (Article 59 of the VAT Executive Regulation),
        Ministerial Decision 244 of 2025 and the MoF e-invoicing guidelines v2.0
  India CGST Rule 46 (CBIC), CBIC press release on HSN digits (Notification 78/2020),
        GST e-invoice portal (Notification 10/2023, AATO above Rs 5 crore)
  UK    GOV.UK "Invoices: what they must include", VAT Notice 700/21 sections 3.1, 4.1, 4.5
  US    IRS "What kind of records should I keep", IRS 1099-NEC FAQ, Form W-9
  CA    CRA "Input tax credits" information table, CRA GST/HST rate table
  AU    ATO "Tax invoices"
PaidSnap claims are read from the app's code (CountryPack.swift, PDFRenderer.swift):
heading, tax-number labels, client tax number, India HSN/SAC, place of supply and
reverse charge. It has no signature field, so no page may say it does.

Run: python3 gen5.py   (or build_all.py, which calls main())
"""
import html
import json

from build import render, render_article, SITE, APPS, ROOT

CHECKED_ON = "15 November 2026"
DL = "downloads/invoice"

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------
UAE_VATP006 = "https://tax.gov.ae/DataFolder/Files/Pdf/06-Tax-Invoices.pdf"
UAE_FTA_INV = "https://tax.gov.ae/en/content/tax.invoices.aspx"
UAE_MD244 = "https://mof.gov.ae/wp-content/uploads/2025/09/Ministerial-Decision-No.-244-of-2025-on-the-Implementation-of-the-Electronic-Invoicing-System.pdf"
UAE_EINV_GUIDE = "https://mof.gov.ae/wp-content/uploads/2026/10/UAE-Electronic-Invoicing-Guidelines_En.pdf"
IN_RULE46 = "https://taxinformation.cbic.gov.in/content/html/tax_repository/gst/rules/cgst_rules/active/chapter6/rule46_v1.00.html"
IN_HSN = "https://cbic-gst.gov.in/pdf/press-release/Press-release-HSN-code-SAC-issue.pdf"
IN_EINV = "https://einvoice.gst.gov.in/einvoice/dashboard"
UK_INVOICE = "https://www.gov.uk/invoicing-and-taking-payment-from-customers/invoices-what-they-must-include"
UK_700_21 = "https://www.gov.uk/guidance/record-keeping-for-vat-notice-70021"
US_RECORDS = "https://www.irs.gov/businesses/small-businesses-self-employed/what-kind-of-records-should-i-keep"
US_1099 = "https://www.irs.gov/faqs/small-business-self-employed-other-business/form-1099-nec-independent-contractors/form-1099-nec-independent-contractors"
US_W9 = "https://www.irs.gov/forms-pubs/about-form-w-9"
US_KEEP = "https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records"
CA_ITC = "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/calculate-prepare-report/input-tax-credit.html"
CA_RATES = "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/charge-collect-which-rate/calculator.html"
CA_KEEP = "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/keeping-records/where-keep-your-records-long-request-permission-destroy-them-early.html"
AU_TAXINV = "https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/tax-invoices"
AU_RECORDS = "https://www.ato.gov.au/individuals-and-families/income-deductions-offsets-and-records/records-you-need-to-keep"


def checked(*links):
    parts = [f'<a href="{u}">{html.escape(t)}</a>' for t, u in links]
    return f"Checked against {', '.join(parts[:-1]) + ' and ' + parts[-1] if len(parts) > 1 else parts[0]} on {CHECKED_ON}."


def facts(rows, head=("What it must show", "When", "Rule")):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="facts"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


# ---------------------------------------------------------------------------
# The fill-in invoice. One component, configured per country.
# ---------------------------------------------------------------------------
def editor(cfg):
    """cfg keys: key, title, untaxed_title, currency, locale, tax_name, tax_label,
    mode ('line' | 'set'), presets (line rates), set_taxes, provinces, india, hsn,
    fx (UAE: tax in AED when invoiced in another currency), extra (list of (name, label, placeholder)),
    sign (signature box), rule (footer note)."""
    js_cfg = {k: cfg.get(k) for k in ("key", "title", "untaxed_title", "currency", "locale", "tax_name",
                                       "mode", "presets", "set_taxes", "provinces", "india", "hsn", "fx")}
    extra = "".join(
        f'<label class="f"><span>{lab}</span><input name="{n}" placeholder="{ph}"></label>'
        for n, lab, ph in cfg.get("extra", []))
    province = ""
    if cfg.get("provinces"):
        opts = "".join(f'<option value="{c}">{html.escape(n)}</option>' for c, n, _ in cfg["provinces"])
        province = f'<label class="f"><span>Province of supply</span><select name="prov" data-prov>{opts}</select></label>'
    fx = ""
    if cfg.get("fx"):
        fx = ('<label class="f"><span>Invoice currency</span><select name="cur" data-cur>'
              '<option>AED</option><option>USD</option><option>EUR</option><option>GBP</option><option>INR</option><option>SAR</option></select></label>'
              '<label class="f" data-fxrow><span>Exchange rate to AED (Central Bank, date of supply)</span><input name="fxrate" inputmode="decimal" placeholder="e.g. 3.6725"></label>')
    india = ""
    if cfg.get("india"):
        india = ('<label class="f chk"><input type="checkbox" name="intra" checked> <span>Supplier and place of supply in the same state (CGST + SGST). Untick for IGST.</span></label>'
                 '<label class="f"><span>Tax payable on reverse charge</span><select name="rc"><option>No</option><option>Yes</option></select></label>')
    hsn_th = '<th class="c-hsn">HSN/SAC</th>' if cfg.get("hsn") else ""
    rate_th = f'<th class="c-rate">{cfg["tax_name"]} %</th>' if cfg["mode"] == "line" else '<th class="c-rate">Taxable</th>'
    sign = ('<div class="inv-sign"><div class="line"></div><span>Signature or digital signature of the supplier '
            'or authorised representative</span></div>') if cfg.get("sign") else ""
    return f'''
<div class="inv-ed" id="fill" data-cfg='{html.escape(json.dumps(js_cfg), quote=True)}'>
  <div class="inv-tools no-print">
    <button class="btn btn-primary btn-sm" type="button" data-act="print">Print or save as PDF</button>
    <button class="btn btn-dark btn-sm" type="button" data-act="add">Add a line</button>
    <button class="btn btn-sm inv-clear" type="button" data-act="clear">Clear</button>
    <label class="f chk taxreg"><input type="checkbox" name="taxreg" checked> <span>{cfg.get("reg_label", "I charge " + cfg["tax_name"])}</span></label>
  </div>
  <p class="inv-note no-print">What you type stays in this browser. Nothing is sent anywhere, and there is nothing to sign up for. To save a PDF, choose Print, then Save as PDF.</p>
  <div class="inv-sheet">
    <div class="inv-head">
      <div class="inv-from">
        <input class="big" name="s_name" placeholder="Your business name">
        <textarea name="s_addr" rows="3" placeholder="Address&#10;City&#10;Email or phone"></textarea>
        <label class="f taxonly"><span>{cfg["tax_label"]}</span><input name="s_tax" placeholder="{cfg.get("tax_ph", "")}"></label>
      </div>
      <div class="inv-titlebox">
        <div class="inv-title" data-title>{cfg["title"]}</div>
        <label class="f"><span>Invoice number</span><input name="no" placeholder="{cfg.get("no_ph", "INV-0001")}"></label>
        <label class="f"><span>Date of issue</span><input name="d_issue" type="date"></label>
        <label class="f"><span>{cfg.get("supply_label", "Date of supply")}</span><input name="d_supply" type="date"></label>
        <label class="f"><span>Due date</span><input name="d_due" type="date"></label>
      </div>
    </div>
    <div class="inv-to">
      <div class="lab">Bill to</div>
      <input class="mid" name="c_name" placeholder="Customer name">
      <textarea name="c_addr" rows="2" placeholder="Customer address"></textarea>
      <label class="f taxonly"><span>Customer {cfg["tax_label"]} {cfg.get("client_tax_note", "(if registered)")}</span><input name="c_tax"></label>
    </div>
    <div class="inv-extra">{extra}{province}{fx}{india}</div>
    <div class="inv-tablewrap"><table class="inv-lines">
      <thead><tr><th class="c-desc">Description</th>{hsn_th}<th class="c-qty">Qty</th><th class="c-price">Unit price</th>{rate_th}<th class="c-amt">Amount{" excl. " + cfg["tax_name"] if cfg["mode"] == "line" else ""}</th><th class="c-x no-print"></th></tr></thead>
      <tbody data-lines></tbody>
    </table></div>
    <div class="inv-totals" data-totals></div>
    <div class="inv-foot">
      <textarea name="notes" rows="3" placeholder="How to pay: bank details, payment link, terms"></textarea>
      {sign}
      <p class="inv-rule">{cfg["rule"]}</p>
    </div>
  </div>
</div>'''


EDITOR_CSS = """
.inv-ed { margin: 34px 0 40px; }
.inv-tools { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
.inv-tools .inv-clear { background: transparent; color: var(--muted); border: 1px solid var(--line); }
.inv-note { font-size: .88rem; color: var(--faint); margin: 10px 0 16px; }
.inv-sheet { background: #fff; border-radius: 18px; box-shadow: var(--e2); padding: 34px 34px 28px;
  font-size: .95rem; color: #0E1315; }
.inv-tablewrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.inv-tablewrap table.inv-lines { min-width: 600px; }
.inv-sheet input, .inv-sheet textarea, .inv-sheet select { font: inherit; color: inherit; width: 100%;
  border: 1px solid transparent; border-bottom-color: #DCE2E3; border-radius: 6px; padding: 5px 6px; background: #FAFBFB; }
.inv-sheet input:focus, .inv-sheet textarea:focus, .inv-sheet select:focus { outline: 2px solid var(--teal); outline-offset: 0; background: #fff; }
.inv-sheet textarea { resize: vertical; }
.inv-sheet .big { font-size: 1.25rem; font-weight: 700; }
.inv-sheet .mid { font-weight: 600; }
.inv-sheet .f { display: block; margin-top: 6px; }
.inv-sheet .f > span { display: block; font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; color: #59666A; margin-bottom: 2px; }
.inv-ed .chk { display: flex; gap: 8px; align-items: center; margin: 0; }
.inv-ed .chk input { width: auto; }
.inv-ed .chk span { font-size: .9rem; text-transform: none; letter-spacing: 0; color: var(--text); margin: 0; }
.inv-head { display: grid; grid-template-columns: 1.3fr 1fr; gap: 28px; }
.inv-title { font-size: 1.6rem; font-weight: 700; letter-spacing: -.02em; color: #1A4B44; text-transform: uppercase; }
.inv-to { margin-top: 22px; max-width: 60%; }
.inv-to .lab { font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; color: #59666A; }
.inv-extra { display: grid; grid-template-columns: 1fr 1fr; gap: 0 28px; margin-top: 14px; }
.inv-extra:empty { display: none; }
table.inv-lines { width: 100%; border-collapse: collapse; margin-top: 22px; }
table.inv-lines th { font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; color: #fff; background: #1A4B44;
  text-align: left; padding: 8px 6px; }
table.inv-lines td { padding: 4px 3px; border-bottom: 1px solid #E8ECED; vertical-align: top; }
table.inv-lines .c-qty { width: 9%; } table.inv-lines .c-price { width: 15%; } table.inv-lines .c-rate { width: 11%; }
table.inv-lines .c-hsn { width: 12%; } table.inv-lines .c-amt { width: 16%; text-align: right; } table.inv-lines .c-x { width: 4%; }
table.inv-lines td.amt { text-align: right; padding-top: 9px; font-variant-numeric: tabular-nums; }
table.inv-lines td input[type=checkbox] { width: auto; margin-top: 9px; }
.inv-sheet .txv { display: none; }
.inv-x { border: 0; background: none; color: #8B979B; font-size: 1.1rem; cursor: pointer; padding: 4px; }
.inv-totals { margin: 16px 0 0 auto; width: 46%; font-variant-numeric: tabular-nums; }
.inv-totals div { display: flex; justify-content: space-between; padding: 5px 0; }
.inv-totals .grand { border-top: 2px solid #0E1315; margin-top: 4px; padding-top: 9px; font-weight: 700; font-size: 1.1rem; }
.inv-totals .sub { color: #59666A; font-size: .88rem; }
.inv-foot { margin-top: 22px; }
.inv-sign { margin-top: 26px; width: 50%; margin-left: auto; text-align: center; font-size: .78rem; color: #59666A; }
.inv-sign .line { border-bottom: 1px solid #0E1315; height: 38px; margin-bottom: 6px; }
.inv-rule { font-size: .75rem; color: #8B979B; margin-top: 16px; }
.inv-ed.untaxed .taxonly, .inv-ed.untaxed .c-rate, .inv-ed.untaxed td.rate { display: none; }
.inv-dl { display: flex; flex-wrap: wrap; gap: 12px; margin: 22px 0 6px; }
.prose .inv-dl a.btn { text-decoration: none; }
.prose .inv-dl a.btn-dark { color: #fff; }
.prose .inv-dl a.btn-primary { color: var(--teal); }
@media (max-width: 700px) {
  .inv-sheet { padding: 22px 16px; }
  .inv-head, .inv-extra { grid-template-columns: 1fr; gap: 0; }
  .inv-titlebox { margin-top: 18px; }
  .inv-to { max-width: 100%; }
  .inv-totals { width: 100%; }
  .inv-sign { width: 100%; }
}
@media print {
  @page { margin: 14mm; }
  body *:not(:has(.inv-sheet)):not(.inv-sheet):not(.inv-sheet *) { display: none !important; }
  body *:has(.inv-sheet) { display: block !important; margin: 0 !important; padding: 0 !important; max-width: none !important;
    width: auto !important; box-shadow: none !important; background: none !important; border: 0 !important; }
  html, body { background: #fff !important; }
  .inv-sheet { box-shadow: none; border-radius: 0; padding: 0; }
  .inv-head { grid-template-columns: 1.3fr 1fr !important; }
  .inv-extra { grid-template-columns: 1fr 1fr !important; }
  .inv-totals { width: 46% !important; }
  .inv-tablewrap { overflow: visible; }
  .inv-tablewrap table.inv-lines { min-width: 0; }
  .inv-sheet .f.is-empty, .inv-sheet .chk, .inv-sheet td.rate input[type=checkbox] { display: none !important; }
  .inv-sheet .txv { display: inline !important; }
  .inv-sheet input::-webkit-calendar-picker-indicator { display: none; }
  .inv-sheet select { background-image: none; }
  .inv-sheet input, .inv-sheet textarea, .inv-sheet select { border: 0; background: none; padding: 2px 0; -webkit-appearance: none; appearance: none; }
  .inv-sheet ::placeholder { color: transparent; }
  .inv-sheet textarea { resize: none; overflow: hidden; }
  .no-print, tr.blank { display: none !important; }
  table.inv-lines th { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
"""

EDITOR_JS = r"""<script>
(function(){
  var root=document.getElementById('fill'); if(!root) return;
  var cfg=JSON.parse(root.getAttribute('data-cfg'));
  var body=root.querySelector('[data-lines]'), totals=root.querySelector('[data-totals]');
  var titleEl=root.querySelector('[data-title]');
  var KEY='dune-invoice-'+cfg.key;
  var store={get:function(){try{return JSON.parse(localStorage.getItem(KEY)||'null');}catch(e){return null;}},
             set:function(v){try{localStorage.setItem(KEY,JSON.stringify(v));}catch(e){}},
             clear:function(){try{localStorage.removeItem(KEY);}catch(e){}}};
  var curCode=function(){var s=root.querySelector('[data-cur]');return s?s.value:cfg.currency;};
  var money=function(n,c){try{return n.toLocaleString(cfg.locale,{style:'currency',currency:c||curCode()});}catch(e){return (c||curCode())+' '+n.toFixed(2);}};
  var num=function(v){var n=parseFloat(String(v||'').replace(/,/g,''));return isFinite(n)?n:0;};
  var r2=function(n){return Math.round((n+Number.EPSILON)*100)/100;};
  var esc=function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};

  function rateCell(l){
    if(cfg.mode==='line'){
      var o=cfg.presets.map(function(p){return '<option value="'+p+'"'+(String(l.rate)===String(p)?' selected':'')+'>'+p+'%</option>';}).join('');
      return '<td class="rate"><select data-f="rate">'+o+'</select></td>';
    }
    return '<td class="rate"><input type="checkbox" data-f="tx"'+(l.tx===false?'':' checked')+' aria-label="Taxable"><span class="txv"></span></td>';
  }
  function row(l){
    l=l||{};
    var tr=document.createElement('tr');
    tr.innerHTML='<td><input data-f="desc" placeholder="What you supplied" value="'+esc(l.desc)+'"></td>'+
      (cfg.hsn?'<td><input data-f="hsn" inputmode="numeric" value="'+esc(l.hsn)+'"></td>':'')+
      '<td><input data-f="qty" inputmode="decimal" value="'+esc(l.qty==null?'':l.qty)+'"></td>'+
      '<td><input data-f="price" inputmode="decimal" value="'+esc(l.price==null?'':l.price)+'"></td>'+
      rateCell(l)+'<td class="amt">&nbsp;</td><td class="no-print"><button type="button" class="inv-x" data-act="del" aria-label="Remove line">×</button></td>';
    if(l.rate==null && cfg.mode==='line'){ tr.querySelector('[data-f=rate]').value=String(cfg.presets[0]); }
    body.appendChild(tr);
  }
  function lines(){
    return [].map.call(body.rows,function(tr){
      var g=function(f){var el=tr.querySelector('[data-f='+f+']');return el?(el.type==='checkbox'?el.checked:el.value):null;};
      return {desc:g('desc'),hsn:g('hsn'),qty:g('qty'),price:g('price'),rate:g('rate'),tx:g('tx'),tr:tr};
    });
  }
  function taxSet(){
    if(cfg.provinces){
      var s=root.querySelector('[data-prov]'), code=s?s.value:null;
      for(var i=0;i<cfg.provinces.length;i++){ if(cfg.provinces[i][0]===code) return cfg.provinces[i][2]; }
    }
    return cfg.set_taxes||[];
  }
  function calc(){
    var taxed=root.querySelector('[name=taxreg]').checked;
    root.classList.toggle('untaxed',!taxed);
    titleEl.textContent=taxed?cfg.title:cfg.untaxed_title;
    var sub=0, byRate={}, taxableSub=0;
    lines().forEach(function(l){
      var amt=r2(num(l.qty)*num(l.price));
      l.tr.querySelector('.amt').textContent=(l.qty||l.price)?money(amt):'';
      l.tr.classList.toggle('blank',!l.desc&&!amt);
      sub+=amt;
      if(cfg.mode==='line'){ var r=num(l.rate); byRate[r]=(byRate[r]||0)+amt; }
      else { var tv=l.tr.querySelector('.txv'); if(tv) tv.textContent=l.tx!==false?'Yes':'No'; if(l.tx!==false) taxableSub+=amt; }
    });
    sub=r2(sub);
    var named=taxed&&cfg.mode==='line';
    var h='<div><span>Subtotal'+(named?' excl. '+cfg.tax_name:'')+'</span><span>'+money(sub)+'</span></div>', tax=0;
    if(taxed){
      if(cfg.mode==='line'){
        Object.keys(byRate).sort(function(a,b){return b-a;}).forEach(function(r){
          var base=r2(byRate[r]), t=r2(base*num(r)/100);
          if(cfg.india){
            var intra=root.querySelector('[name=intra]').checked;
            if(intra){ var half=r2(t/2);
              h+='<div><span>CGST '+(num(r)/2)+'% on '+money(base)+'</span><span>'+money(half)+'</span></div>';
              h+='<div><span>SGST '+(num(r)/2)+'% on '+money(base)+'</span><span>'+money(t-half)+'</span></div>';
            } else h+='<div><span>IGST '+r+'% on '+money(base)+'</span><span>'+money(t)+'</span></div>';
          } else h+='<div><span>'+cfg.tax_name+' '+r+'% on '+money(base)+'</span><span>'+money(t)+'</span></div>';
          tax+=t;
        });
      } else {
        taxSet().forEach(function(t){
          var rateEl=root.querySelector('[name=setrate]');
          var rate=(t[1]==null&&rateEl)?num(rateEl.value):t[1];
          var v=r2(taxableSub*rate/100); tax+=v;
          h+='<div><span>'+t[0]+' '+rate+'%'+(taxableSub!==sub?' on '+money(taxableSub):'')+'</span><span>'+money(v)+'</span></div>';
        });
      }
    }
    tax=r2(tax);
    h+='<div class="grand"><span>Total'+(named?' incl. '+cfg.tax_name:'')+'</span><span>'+money(r2(sub+tax))+'</span></div>';
    if(taxed && cfg.fx && curCode()!=='AED'){
      var fx=num((root.querySelector('[name=fxrate]')||{}).value);
      h+='<div class="sub"><span>VAT in AED'+(fx?' at '+fx:'')+'</span><span>'+(fx?money(r2(tax*fx),'AED'):'enter the exchange rate')+'</span></div>';
    }
    totals.innerHTML=h;
    var fxrow=root.querySelector('[data-fxrow]'); if(fxrow) fxrow.style.display=curCode()==='AED'?'none':'';
    [].forEach.call(root.querySelectorAll('.inv-sheet .f'),function(f){var el=f.querySelector('input:not([type=checkbox]),textarea');if(el)f.classList.toggle('is-empty',!el.value);});
    save();
  }
  function save(){
    var o={f:{},lines:lines().map(function(l){return {desc:l.desc,hsn:l.hsn,qty:l.qty,price:l.price,rate:l.rate,tx:l.tx};})};
    [].forEach.call(root.querySelectorAll('[name]'),function(el){o.f[el.name]=el.type==='checkbox'?el.checked:el.value;});
    store.set(o);
  }
  function load(){
    var o=store.get();
    if(o&&o.f){ Object.keys(o.f).forEach(function(n){var el=root.querySelector('[name="'+n+'"]');if(!el)return;if(el.type==='checkbox')el.checked=!!o.f[n];else el.value=o.f[n];}); }
    var ls=(o&&o.lines&&o.lines.length)?o.lines:[{},{},{}];
    ls.forEach(row);
    if(!(o&&o.f&&o.f.d_issue)){ var d=new Date(), iso=new Date(d.getTime()-d.getTimezoneOffset()*60000).toISOString().slice(0,10);
      root.querySelector('[name=d_issue]').value=iso; }
  }
  root.addEventListener('input',calc); root.addEventListener('change',calc);
  root.addEventListener('click',function(e){
    var b=e.target.closest('[data-act]'); if(!b) return;
    var a=b.getAttribute('data-act');
    if(a==='print'){ window.print(); }
    else if(a==='add'){ row({}); calc(); }
    else if(a==='del'){ var tr=b.closest('tr'); if(body.rows.length>1){ tr.remove(); } else { [].forEach.call(tr.querySelectorAll('input'),function(i){if(i.type!=='checkbox')i.value='';}); } calc(); }
    else if(a==='clear'){
      if(b.getAttribute('data-armed')!=='1'){ b.setAttribute('data-armed','1'); b.textContent='Tap again to clear'; setTimeout(function(){b.removeAttribute('data-armed');b.textContent='Clear';},3000); return; }
      store.clear(); [].forEach.call(root.querySelectorAll('[name]'),function(el){ if(el.type==='checkbox'){el.checked=(el.name==='taxreg'||el.name==='intra');} else if(el.tagName==='SELECT'){el.selectedIndex=0;} else el.value=''; });
      body.innerHTML=''; [{},{},{}].forEach(row); b.removeAttribute('data-armed'); b.textContent='Clear'; calc();
    }
  });
  load(); calc();
})();
</script>"""


# ---------------------------------------------------------------------------
# The six countries
# ---------------------------------------------------------------------------
PAIDSNAP_LINE = ('PaidSnap, our iPhone invoice app, does the same from the country you pick: {heading}'
                 'the {label} label, your customer\'s {label}, and the tax lines.')

# The tax-number label PaidSnap itself prints (CountryPack.taxNumberLabel), which is not
# always the label these templates use.
PAIDSNAP_LABEL = {"ae": "TRN", "in": "GSTIN", "gb": "VAT number", "us": "Tax ID (EIN)",
                  "ca": "Business Number (BN)", "au": "ABN"}

COUNTRIES = []

# ---------------- UAE ----------------
COUNTRIES.append({
 "slug": "uae-tax-invoice-template", "out": "invoice-templates/uae-tax-invoice.html",
 "code": "ae", "paper": "a4",
 "seo_title": "UAE Tax Invoice Template (Free PDF) with Every FTA Field",
 "meta": "Free UAE tax invoice template with every Article 59 field: Tax Invoice heading, TRN, VAT per line in AED. PDF or fill it in online. Plus 2027 e-invoicing.",
 "title": "UAE tax invoice template, with every field the FTA requires",
 "description": "A free UAE tax invoice: PDF or fill it in online, with the Article 59 fields cited, the simplified invoice rule, foreign currency invoices, and what e-invoicing changes from 2027.",
 "dek": "A UAE tax invoice is not a format choice. Article 59 of the VAT Executive Regulation lists what it must show, and an invoice in dollars that leaves the VAT out of dirhams is not a valid tax invoice at all.",
 "checked": checked(("FTA Public Clarification VATP006 on tax invoices", UAE_VATP006),
                    ("Ministerial Decision 244 of 2025", UAE_MD244)),
 "takeaways": [
   "Heading <strong>\"Tax Invoice\"</strong>, plus your name, address and <strong>TRN</strong>. Your customer's name, address and TRN too when they are registered.",
   "On a full tax invoice every line shows the <strong>unit price, quantity, VAT rate and amount in AED</strong>, and the invoice shows the gross total in AED.",
   "Invoicing in dollars or euros is allowed, but the <strong>VAT must also be shown in AED</strong>, with the exchange rate used.",
   "A <strong>simplified tax invoice</strong> is enough when the customer is not registered, or is registered and the supply is AED 10,000 or less.",
   "From <strong>1 July 2027</strong>, businesses under AED 50 million revenue must issue B2B invoices through e-invoicing. Sales to consumers stay outside it.",
 ],
 "editor": {
   "key": "ae", "title": "Tax Invoice", "untaxed_title": "Invoice", "currency": "AED", "locale": "en-AE",
   "tax_name": "VAT", "tax_label": "TRN", "tax_ph": "15-digit TRN", "mode": "line", "presets": [5, 0],
   "fx": True, "reg_label": "I am VAT registered",
   "rule": "Fields follow Article 59 of the UAE VAT Executive Regulation (FTA VATP006). Template from duneapps.com.",
 },
 "pdf": {"heading": "TAX INVOICE", "tax_label": "TRN", "client_tax": "Customer TRN (if registered)",
         "meta": ["Tax invoice no.", "Date of issue", "Date of supply", "Currency", "Exchange rate to AED (if not AED)"],
         "cols": [("Description", 64), ("Qty", 14), ("Unit price", 24), ("VAT rate", 18), ("VAT (AED)", 24), ("Amount excl. VAT", 28)],
         "totals": ["Total excluding VAT", "VAT at 5%", "Total including VAT (AED)", "VAT in AED, if invoiced in another currency"],
         "rule": "Required by Article 59 of the VAT Executive Regulation. Simplified tax invoice allowed if the customer is unregistered, or registered and the supply is AED 10,000 or less."},
 "faq": [
   ("What must a UAE tax invoice show?",
    "On a full tax invoice: the words Tax Invoice; your name, address and TRN; your customer's name, address and TRN where they are registered; a sequential or unique invoice number; the date of issue and the date of supply if different; a description; for each line the unit price, quantity, VAT rate and amount payable in AED; any discount; the gross total in AED; and the VAT in AED."),
   ("When can I issue a simplified tax invoice in the UAE?",
    "Article 59(5) allows one when the customer is not registered for VAT, or when the customer is registered and the supply is AED 10,000 or less. It still needs the words Tax Invoice, your name, address and TRN, the date of issue, a description, and the total with the VAT amount. You still have to issue it: the FTA says offering to print one on request does not meet the obligation."),
   ("Can I invoice in US dollars in the UAE?",
    "Yes, but the FTA's clarification says the invoice must show the VAT payable in AED and the exchange rate applied, at the UAE Central Bank's rate on the date of supply. An invoice in a foreign currency without the VAT in dirhams is not a valid tax invoice."),
   ("Will a PDF invoice still work after UAE e-invoicing starts?",
    "For sales to consumers, yes: business-to-consumer transactions are outside the e-invoicing system under Ministerial Decision 244 of 2025. For sales to businesses and government, no. A business with revenue under AED 50 million must appoint an accredited service provider by 31 March 2027 and invoice through the system by 1 July 2027; above AED 50 million it applied from 1 January 2027."),
 ],
 "sources": [
   ("FTA Public Clarification VATP006: Tax invoices (Article 59 of the Executive Regulation)", UAE_VATP006),
   ("Federal Tax Authority: Tax invoices", UAE_FTA_INV),
   ("Ministerial Decision No. 244 of 2025 on the implementation of the e-invoicing system", UAE_MD244),
   ("Ministry of Finance: UAE Electronic Invoicing Guidelines v2.0, 26 October 2026", UAE_EINV_GUIDE),
 ],
 "related": ["uae-vat-record-keeping", "how-long-to-keep-receipts", "india-gst-invoice-template"],
 "body": f"""
<p>This is a tax invoice for a VAT-registered business in the UAE. Download the PDF and fill it in by hand, or fill it in on this page and save it as a PDF. Both carry every field below.</p>
<!--downloads-->

<h2>What a UAE tax invoice must show</h2>

{facts([
  ("The words <strong>\"Tax Invoice\"</strong>, clearly displayed", "Full and simplified", "Art. 59(1)(a), 59(2)"),
  ("Your <strong>name, address and TRN</strong>", "Full and simplified", "Art. 59(1)(b), 59(2)"),
  ("Your customer's <strong>name, address and TRN</strong>", "Full, when the customer is registered", "Art. 59(1)(c)"),
  ("A <strong>sequential or unique invoice number</strong>", "Full", "Art. 59(1)(d)"),
  ("Date of issue, and date of supply if different", "Full (simplified: date of issue)", "Art. 59(1), 59(2)"),
  ("A description of the goods or services", "Full and simplified", "Art. 59(1), 59(2)"),
  ("Per line: <strong>unit price, quantity, VAT rate, amount in AED</strong>", "Full", "Art. 59(1); FTA VATP006"),
  ("Any discount", "Full, when given", "Art. 59(1)"),
  ("The gross total payable, in AED", "Full", "Art. 59(1); FTA VATP006"),
  ("The VAT charged, <strong>in AED</strong>, and the exchange rate if invoiced in another currency", "Full", "FTA VATP006"),
  ("A statement that the customer accounts for the VAT", "Reverse charge supplies", "Art. 59(1)"),
  ("Total consideration and the VAT amount", "Simplified", "Art. 59(2)"),
])}

<h3>Full or simplified</h3>

<p>Article 59(5) allows a simplified tax invoice in two cases: the customer is not registered for VAT, or the customer is registered and the supply is <strong>AED 10,000 or less</strong>. A simplified invoice can show its lines at the gross value with the VAT on a separate line at the bottom. A full one shows each line net, with its own VAT. Either way it has to be issued and delivered. The FTA's clarification is blunt about shops that only print one when asked: <em>"This is not optional."</em></p>

<h3>Invoicing in another currency</h3>

<p>You can invoice a customer in dollars. The FTA says the invoice must then show <em>"the tax amount payable expressed in AED"</em> and <em>"the exchange rate applied"</em>, at the UAE Central Bank's published rate on the date of supply, and that invoices which do not are <em>"failing to issue a valid tax invoice for VAT purposes."</em> The fill-in version below asks for the rate as soon as you pick a currency other than AED.</p>

<p>Rounding is per line: where the VAT on a line comes to a fraction of a fils, round it to the nearest fils on that line.</p>
""",
 "after": f"""
<h2>What e-invoicing changes in 2027</h2>

<p>The UAE is moving business invoices onto an electronic system run through accredited service providers. Ministerial Decision 244 of 2025 sets the dates, and the Ministry of Finance's guidelines of 26 October 2026 confirm them:</p>

{facts([
  ("Revenue of AED 50 million or more", "31 October 2026", "1 January 2027"),
  ("Revenue under AED 50 million", "31 March 2027", "1 July 2027"),
  ("Government entities", "31 March 2027", "1 October 2027"),
], head=("Who", "Appoint a service provider by", "Invoice through the system by"))}

<p>Two things matter for a small business. Sales to consumers are outside it: the decision says business-to-consumer transactions <em>"shall not be subject to the Electronic Invoicing System"</em>. Sales to other businesses and to government are inside it, so from 1 July 2027 a PDF invoice to a business customer, from this template or from any app that makes PDFs, is no longer the invoice that counts. Until then, a tax invoice with every field above is what the law asks for.</p>

<p>Keep every tax invoice you issue for five years, and fifteen for anything to do with real estate. <a href="/posts/uae-vat-record-keeping.html">What UAE VAT requires you to keep</a> covers the rest of the records.</p>
""",
})

# ---------------- India ----------------
COUNTRIES.append({
 "slug": "india-gst-invoice-template", "out": "invoice-templates/india-gst-invoice.html",
 "code": "in", "paper": "a4",
 "seo_title": "GST Invoice Template (Free PDF) with Every Rule 46 Field",
 "meta": "Free GST tax invoice template with every Rule 46 field: GSTIN, HSN/SAC, CGST and SGST or IGST, place of supply, reverse charge. PDF or fill in online.",
 "title": "GST invoice template for India, with every Rule 46 field",
 "description": "A free GST tax invoice: PDF or fill it in online, with the CGST Rule 46 particulars cited, HSN digits by turnover, CGST and SGST or IGST, and when you need an e-invoice instead.",
 "dek": "Rule 46 of the CGST Rules lists the particulars a tax invoice must carry, from a serial number of at most sixteen characters to the signature at the bottom. Most free templates leave three or four of them out.",
 "checked": checked(("CGST Rule 46", IN_RULE46), ("the CBIC note on HSN digits", IN_HSN), ("the GST e-invoice portal", IN_EINV)),
 "takeaways": [
   "Supplier name, address and <strong>GSTIN</strong>; a <strong>serial number of up to 16 characters</strong>, unique for the financial year; the date.",
   "Customer name, address and GSTIN if registered. An unregistered customer at <strong>₹50,000 or more</strong> also needs the delivery address and state name and code.",
   "<strong>HSN or SAC:</strong> 4 digits on B2B invoices up to ₹5 crore turnover, 6 digits above it.",
   "Same state: <strong>CGST + SGST</strong>, half each. Different state: <strong>IGST</strong>, with the place of supply and its state.",
   "Reverse charge Yes or No, and a <strong>signature or digital signature</strong>. Above ₹5 crore turnover, B2B invoices need an IRN from the e-invoice portal.",
 ],
 "editor": {
   "key": "in", "title": "Tax Invoice", "untaxed_title": "Invoice", "currency": "INR", "locale": "en-IN",
   "tax_name": "GST", "tax_label": "GSTIN", "tax_ph": "15-character GSTIN", "mode": "line", "presets": [18, 5, 40, 0],
   "india": True, "hsn": True, "sign": True, "no_ph": "2026-27/001", "reg_label": "I am GST registered",
   "extra": [("pos", "Place of supply (state and code)", "e.g. Karnataka (29)"), ("deliv", "Delivery address, if different", "")],
   "rule": "Particulars follow Rule 46 of the CGST Rules, 2017. HSN digits: CBIC Notification 78/2020. Template from duneapps.com.",
 },
 "pdf": {"heading": "TAX INVOICE", "tax_label": "GSTIN", "client_tax": "Customer GSTIN (if registered)",
         "meta": ["Invoice no. (max 16 characters)", "Date of issue", "Place of supply (state, code)", "Reverse charge (Yes / No)", "Delivery address, if different"],
         "cols": [("Description", 50), ("HSN/SAC", 18), ("Qty", 11), ("Rate", 17), ("Taxable value", 23), ("GST %", 11), ("CGST", 18), ("SGST", 18), ("IGST", 18)],
         "totals": ["Taxable value", "CGST", "SGST", "IGST", "Invoice total"],
         "sign": "Signature or digital signature of the supplier or authorised representative",
         "rule": "Particulars required by Rule 46 of the CGST Rules, 2017. HSN: 4 digits up to Rs 5 crore turnover (B2B), 6 digits above (Notification 78/2020)."},
 "faq": [
   ("What must a GST tax invoice contain?",
    "Rule 46 lists it: supplier name, address and GSTIN; a consecutive serial number of up to sixteen characters, unique for the financial year; the date; the customer's name, address and GSTIN if registered; the HSN or SAC code; a description; quantity and unit for goods; total value; taxable value after any discount; the rate and amount of CGST, SGST or IGST; the place of supply with the state name for inter-state supplies; the delivery address if different; whether tax is payable on reverse charge; and a signature or digital signature."),
   ("How many HSN digits do I need on a GST invoice?",
    "Based on turnover in the previous financial year. Up to ₹5 crore, 4 digits are mandatory on B2B invoices, and B2C invoices to unregistered buyers can leave HSN out. Above ₹5 crore, 6 digits on every taxable invoice. This has applied since 1 April 2021 under Notification 78/2020."),
   ("Is a signature required on a GST invoice?",
    "Rule 46 includes a signature or digital signature of the supplier or an authorised representative. A proviso removes it for an electronic invoice issued in accordance with the Information Technology Act, 2000. Whether an emailed PDF counts as that is worth confirming with your CA; signing the invoice removes the question."),
   ("When do I need an e-invoice instead?",
    "When your aggregate turnover is above ₹5 crore in any financial year from 2017-18. From 1 August 2023, those businesses must register B2B invoices on the Invoice Registration Portal and print the IRN and QR code. A template like this one is not an e-invoice. B2C invoices do not need an IRN."),
 ],
 "sources": [
   ("CBIC: Rule 46, CGST Rules 2017 (tax invoice particulars)", IN_RULE46),
   ("CBIC press release: HSN/SAC digits on invoices from 1 April 2021 (Notification 78/2020)", IN_HSN),
   ("GST e-invoice portal (mandatory above ₹5 crore aggregate turnover)", IN_EINV),
 ],
 "related": ["uae-tax-invoice-template", "how-long-to-keep-receipts", "uae-vat-record-keeping"],
 "body": f"""
<p>This is a GST tax invoice for a registered business. Download the PDF and fill it in by hand, or fill it in on this page and save it as a PDF: it works out CGST and SGST, or IGST, as you type.</p>
<!--downloads-->

<h2>The Rule 46 particulars</h2>

{facts([
  ("Supplier <strong>name, address and GSTIN</strong>", "Always", "Rule 46(a)"),
  ("Consecutive <strong>serial number</strong>, up to 16 characters (letters, numbers, hyphen, slash), unique for the financial year", "Always", "Rule 46(b)"),
  ("Date of issue", "Always", "Rule 46(c)"),
  ("Customer <strong>name, address and GSTIN</strong>", "Customer is registered", "Rule 46(d)"),
  ("Customer name and address, delivery address, <strong>state name and code</strong>", "Unregistered customer, supply of ₹50,000 or more (or on request below that)", "Rule 46(e), (f)"),
  ("<strong>HSN</strong> code for goods or <strong>SAC</strong> for services", "Digits depend on turnover, see below", "Rule 46(g)"),
  ("Description; quantity and unit for goods", "Always", "Rule 46(h), (i)"),
  ("Total value, and taxable value after any discount", "Always", "Rule 46(j), (k)"),
  ("Rate and amount of <strong>CGST, SGST or IGST</strong> (and cess)", "Always", "Rule 46(l), (m)"),
  ("<strong>Place of supply</strong> with the state name", "Inter-state supplies", "Rule 46(n)"),
  ("Delivery address", "When different from the place of supply", "Rule 46(o)"),
  ("Whether tax is payable on <strong>reverse charge</strong>", "Always", "Rule 46(p)"),
  ("<strong>Signature or digital signature</strong>", "Not needed for an electronic invoice under the IT Act, 2000", "Rule 46(q)"),
])}

<h3>HSN digits</h3>

{facts([
  ("Up to ₹5 crore", "4 digits on B2B invoices; may be left off invoices to unregistered buyers"),
  ("More than ₹5 crore", "6 digits on every invoice for taxable supplies"),
], head=("Turnover in the previous financial year", "HSN or SAC on the invoice"))}

<p>The CBIC's own summary: <em>"A taxpayer having turnover of upto five crore in the preceding financial year is required to mandatorily furnish 4 digits HSN code on B2B invoices."</em> The 6-digit codes are the same ones used in the customs tariff.</p>

<h3>CGST and SGST, or IGST</h3>

<p>When you and the place of supply are in the same state, the GST rate is charged as two equal halves: 18% becomes CGST 9% and SGST 9%. When they are in different states, the whole rate is IGST, and the invoice must name the place of supply and its state. Untick "same state" on the fill-in version and it switches to IGST.</p>
""",
 "after": """
<h2>When this template is not enough</h2>

<p>Two kinds of business need something else. Above ₹5 crore aggregate turnover, B2B invoices have to be registered on the Invoice Registration Portal, which returns an IRN and a QR code to print on the invoice; the GST portal says a B2B invoice without a valid IRN is not valid. A paper or PDF template cannot do that step for you. And a business that is not registered for GST does not issue a tax invoice at all, which is why the fill-in version drops the GST fields when you untick "I am GST registered".</p>

<p>PaidSnap prints the GSTIN, HSN or SAC on each line, the place of supply and the reverse-charge Yes or No, and splits CGST and SGST for you. It does not add a signature, so sign the copy you send, or sign the PDF digitally.</p>
""",
})

# ---------------- UK ----------------
COUNTRIES.append({
 "slug": "uk-invoice-template", "out": "invoice-templates/uk-vat-invoice.html",
 "code": "gb", "paper": "a4",
 "seo_title": "UK Invoice Template (Free): VAT and Non-VAT Registered",
 "meta": "Free UK invoice templates, VAT registered or not: what GOV.UK and VAT Notice 700/21 require, the £250 simplified invoice and the 30-day rule. PDF or online.",
 "title": "UK invoice template, for VAT registered and not",
 "description": "Free UK invoice templates as PDF or to fill in online: what GOV.UK requires on every invoice, the extra fields on a VAT invoice from Notice 700/21, the £250 simplified invoice, and the 30-day rule.",
 "dek": "Most UK freelancers are not VAT registered, and most invoice templates are built as if they were. There are two different documents here, and the law asks different things of each.",
 "checked": checked(("GOV.UK: Invoices, what they must include", UK_INVOICE), ("VAT Notice 700/21", UK_700_21)),
 "takeaways": [
   "Every invoice: a <strong>unique number</strong>, your name, address and contact details, the customer's name and address, a description, the <strong>supply date</strong>, the invoice date, the amounts and the total owed.",
   "Sole traders: your own name as well as any business name. Limited companies: the <strong>full company name</strong> as on the certificate of incorporation.",
   "VAT registered and selling to a VAT-registered customer: a <strong>VAT invoice</strong>, with your VAT number, the time of supply, the rate per line and the VAT total <strong>in sterling</strong>.",
   "A <strong>simplified VAT invoice</strong> is allowed when the supply is £250 or less including VAT.",
   "Issue a VAT invoice <strong>within 30 days</strong> of the supply.",
 ],
 "editor": {
   "key": "gb", "title": "VAT Invoice", "untaxed_title": "Invoice", "currency": "GBP", "locale": "en-GB",
   "tax_name": "VAT", "tax_label": "VAT registration number", "tax_ph": "GB123456789", "mode": "line", "presets": [20, 5, 0],
   "supply_label": "Time of supply (tax point)", "reg_label": "I am VAT registered",
   "rule": "Fields follow GOV.UK invoicing guidance and VAT Notice 700/21 section 4.1. Template from duneapps.com.",
 },
 "pdf": {"heading": "VAT INVOICE", "tax_label": "VAT registration no.", "client_tax": None,
         "meta": ["Invoice no.", "Date of issue", "Time of supply (tax point)", "Payment due"],
         "cols": [("Description", 76), ("Qty", 16), ("Unit price", 26), ("VAT rate", 20), ("Amount excl. VAT", 34)],
         "totals": ["Total excluding VAT", "VAT (in sterling)", "Total payable"],
         "rule": "Fields required for a full VAT invoice by VAT Notice 700/21 section 4.1. Issue within 30 days of the supply.",
         "second": {"file": "uk-invoice-not-vat-registered", "heading": "INVOICE", "tax_label": None,
                    "meta": ["Invoice no.", "Date of issue", "Date of supply", "Payment due"],
                    "cols": [("Description", 96), ("Qty", 18), ("Unit price", 28), ("Amount", 30)],
                    "totals": ["Total owed"],
                    "rule": "Fields listed by GOV.UK for an invoice from a business that is not VAT registered."}},
 "faq": [
   ("What must a UK invoice include if I'm not VAT registered?",
    "GOV.UK lists a unique identification number, your company name, address and contact information, the customer's company name and address, a clear description of what you are charging for, the supply date, the invoice date, the amounts charged and the total owed. A sole trader also shows their own name and any business name, and an address where legal documents can be delivered if using a business name."),
   ("What extra goes on a VAT invoice?",
    "VAT Notice 700/21 section 4.1: a sequential number, the time of supply, the date of issue where different, your name, address and VAT registration number, the customer's name and address, a description, and for each line the quantity, the VAT rate and the amount excluding VAT, plus the total excluding VAT, the rate of any cash discount, the unit price, and the total VAT in sterling."),
   ("When can I use a simplified VAT invoice?",
    "When the total value of the supply, including VAT, is £250 or less. It shows your name, address and VAT number, the time of supply, a description, and for each VAT rate the total including VAT and the rate. Exempt supplies cannot go on one. Above £250 you issue a full or a modified VAT invoice."),
   ("How long do I have to send a VAT invoice?",
    "Notice 700/21: normally you must issue a VAT invoice within 30 days of the date you make the supply."),
 ],
 "sources": [
   ("GOV.UK: Invoicing and taking payment from customers, what invoices must include", UK_INVOICE),
   ("HMRC VAT Notice 700/21: Record keeping for VAT (sections 3.1, 4.1, 4.5)", UK_700_21),
 ],
 "related": ["how-long-to-keep-receipts", "hmrc-mileage-rates-2026", "us-invoice-template"],
 "body": f"""
<p>Two templates on one page. Leave "I am VAT registered" ticked for a VAT invoice; untick it for the plain invoice a sole trader or small company outside VAT sends. The PDFs come in both versions too.</p>
<!--downloads-->

<h2>What each invoice must show</h2>

{facts([
  ("A <strong>unique</strong> invoice number", "Yes", "Yes, <strong>sequential</strong>"),
  ("Your name, address and contact details", "Yes", "Yes"),
  ("Your <strong>VAT registration number</strong>", "No", "Yes"),
  ("Customer name and address", "Yes", "Yes"),
  ("Description of what you supplied", "Yes", "Yes, enough to identify it"),
  ("Date of supply / <strong>time of supply</strong> (tax point)", "Yes", "Yes"),
  ("Date of the invoice", "Yes", "Yes, where different from the time of supply"),
  ("Per line: quantity, <strong>VAT rate</strong>, amount excluding VAT", "No", "Yes"),
  ("Unit price", "No", "Yes"),
  ("Rate of any cash discount offered", "No", "Yes"),
  ("Total excluding VAT", "No", "Yes"),
  ("<strong>Total VAT, in sterling</strong>", "No", "Yes, even if you invoice in another currency"),
  ("Total owed", "Yes", "Yes"),
], head=("Field", "Not VAT registered (GOV.UK)", "VAT invoice (Notice 700/21, 4.1)"))}

<h3>Sole trader or limited company</h3>

<p>GOV.UK adds two rules that templates often miss. A sole trader shows <em>"your name and any business name being used"</em>, and if trading under a business name, <em>"an address where any legal documents can be delivered to you"</em>. A limited company <em>"must include the full company name as it appears on the certificate of incorporation"</em>, and if it names any directors on the invoice, it has to name all of them.</p>

<h3>The £250 simplified VAT invoice</h3>

<p>When the supply is £250 or less including VAT, Notice 700/21 lets you issue a simplified invoice: your name, address and VAT number, the time of supply, a description, and for each VAT rate the total including VAT and the rate charged. Exempt supplies cannot go on one. Above £250 it must be a full VAT invoice, or a modified one showing VAT-inclusive values.</p>

<p>And the clock: <em>"Normally you must issue a VAT invoice within 30 days of the date you make the supply."</em></p>
""",
 "after": """
<h2>Keeping them</h2>

<p>Keep a copy of every invoice you issue. Self-employed records are kept for at least five years after the 31 January deadline for the tax year, and VAT records for six years. <a href="/posts/how-long-to-keep-receipts.html">How long to keep receipts and invoices</a> has the detail and the sources.</p>
""",
})

# ---------------- US ----------------
COUNTRIES.append({
 "slug": "us-invoice-template", "out": "invoice-templates/us-invoice.html",
 "code": "us", "paper": "letter",
 "seo_title": "Free Invoice Template (US): PDF or Fill It In Online",
 "meta": "Free US invoice template: PDF in Letter size or fill it in online, with sales tax. What to include, why there is no federal format, and the 2026 1099 change.",
 "title": "Free invoice template for US freelancers and small businesses",
 "description": "A free US invoice: PDF in Letter size or fill it in online with an optional sales tax line. What to include, why no federal law sets the format, and what the $2,000 1099-NEC threshold means in 2026.",
 "dek": "No federal law tells you what an American invoice must show. That is freedom and a trap: what decides whether you get paid on time is what your client's accounts payable team needs to see.",
 "checked": checked(("IRS: What kind of records should I keep", US_RECORDS), ("the IRS Form 1099-NEC FAQ", US_1099)),
 "takeaways": [
   "There is <strong>no federal invoice format</strong>. The IRS treats your invoices as records of gross receipts, kept with your books.",
   "<strong>Sales tax is state law.</strong> Whether you charge it, and at what rate, depends on the state, often the county and city, and what you sell.",
   "For payments in 2026, a client only has to send a <strong>1099-NEC at $2,000</strong> or more. They ask for your taxpayer number on a <strong>Form W-9</strong>, not on the invoice.",
   "What gets invoices paid: a unique number, the dates, the <strong>payment terms</strong>, a clear description, the total, and exactly <strong>how to pay</strong>.",
 ],
 "editor": {
   "key": "us", "title": "Invoice", "untaxed_title": "Invoice", "currency": "USD", "locale": "en-US",
   "tax_name": "Sales tax", "tax_label": "Sales tax permit no.", "tax_ph": "if you collect sales tax", "mode": "set",
   "set_taxes": [["Sales tax", None]], "client_tax_note": "(if exempt, their certificate no.)", "reg_label": "I charge sales tax",
   "extra": [("setrate", "Sales tax rate for this sale (%)", "e.g. 8.875"), ("terms", "Payment terms", "e.g. Net 30")],
   "rule": "No federal format applies; sales tax rules are set by each state. Template from duneapps.com.",
 },
 "pdf": {"heading": "INVOICE", "tax_label": None, "client_tax": None,
         "meta": ["Invoice no.", "Invoice date", "Payment terms", "Due date"],
         "cols": [("Description", 104), ("Qty", 18), ("Rate", 28), ("Amount", 30)],
         "totals": ["Subtotal", "Sales tax (if you collect it)", "Total due"],
         "rule": "No federal law sets invoice contents. Keep a copy: the IRS treats invoices as records of gross receipts."},
 "faq": [
   ("What should an invoice include in the US?",
    "No federal law sets a list. In practice: your name or business name and contact details, the client's name, a unique invoice number, the invoice date, the payment terms and due date, a description of the work, quantities and rates, any sales tax, the total, and how to pay. Keep a copy: the IRS lists invoices among the documents that show your gross receipts."),
   ("Do I have to charge sales tax on my invoices?",
    "It depends on the state, and on what you sell. Sales tax is set by each state, with county and city rates on top in many places, and many states do not tax most services. Check with the state's department of revenue for each state you sell into. PaidSnap does not fill in a US rate for that reason: the right one depends on where the sale happens."),
   ("Should I put my Social Security number on an invoice?",
    "There is no need. A client who has to report what they paid you asks for your taxpayer identification number on Form W-9. For payments made in 2026, they only have to file a 1099-NEC once they have paid you $2,000 or more in the year, up from $600."),
   ("How long should I keep copies of my invoices?",
    "The IRS's general period is three years from when you filed, six if income was underreported by more than 25%, and seven for a claim for a loss from worthless securities or bad debt. Many people keep invoices longer because they also prove when a client paid."),
 ],
 "sources": [
   ("IRS: What kind of records should I keep (invoices as gross receipts records)", US_RECORDS),
   ("IRS: Form 1099-NEC and independent contractors ($2,000 for payments after 31 Dec 2025)", US_1099),
   ("IRS: About Form W-9", US_W9),
   ("IRS: How long should I keep records", US_KEEP),
 ],
 "related": ["delivery-driver-mileage-deduction", "do-you-need-receipts-for-tax-deductions", "how-long-to-keep-receipts"],
 "body": f"""
<p>A plain US invoice in Letter size, with an optional sales tax line. Download the PDF, or fill it in here and save it as a PDF.</p>
<!--downloads-->

<h2>What to put on it, and why</h2>

<p>Because no federal rule sets the contents, this list comes from what gets an invoice approved and paid, and from what the IRS expects your records to show:</p>

{facts([
  ("A <strong>unique invoice number</strong>", "Clients' systems reject duplicates, and it is how you match a payment to a job."),
  ("Your name or business name, address, email", "Who to pay, and who to ask about it."),
  ("The client's name, and a contact or PO number if they gave one", "Many companies cannot approve an invoice without its purchase order number."),
  ("Invoice date, <strong>payment terms</strong> and due date", "\"Net 30\" with no date invites a later payment."),
  ("A clear description, quantity and rate", "So the person approving it can see what it was for."),
  ("Sales tax, if you collect it", "As a separate line, at the rate for where the sale takes place."),
  ("Total due, and <strong>how to pay</strong>", "Bank details or a payment link. The commonest reason for a late payment is not knowing how."),
], head=("Field", "Why it is there"))}

<h3>Sales tax</h3>

<p>Whether a sale is taxable, and at what rate, is decided by each state, and in many places the county and city add their own rate. Many states do not tax most services. If you do collect it, show it as its own line and keep your permit number to hand. The fill-in version applies one rate to the lines you tick as taxable.</p>

<h3>The 2026 change to 1099s</h3>

<p>For payments made after 31 December 2025, a business only has to report what it paid you on Form 1099-NEC once the total reaches <strong>$2,000</strong>, up from $600. It asks for your taxpayer number on a <a href="{US_W9}">Form W-9</a>, so there is no reason to print a Social Security number on an invoice. The income is reportable whether a form arrives or not, which makes your own copies of every invoice the record that counts.</p>
""",
 "after": "",
})

# ---------------- Canada ----------------
CA_PROVINCES = [
  ("ON", "Ontario: HST 13%", [["HST", 13]]),
  ("AB", "Alberta: GST 5%", [["GST", 5]]),
  ("BC", "British Columbia: GST 5% + PST 7%", [["GST", 5], ["PST", 7]]),
  ("MB", "Manitoba: GST 5% + RST 7%", [["GST", 5], ["RST", 7]]),
  ("NB", "New Brunswick: HST 15%", [["HST", 15]]),
  ("NL", "Newfoundland and Labrador: HST 15%", [["HST", 15]]),
  ("NS", "Nova Scotia: HST 14%", [["HST", 14]]),
  ("NT", "Northwest Territories: GST 5%", [["GST", 5]]),
  ("NU", "Nunavut: GST 5%", [["GST", 5]]),
  ("PE", "Prince Edward Island: HST 15%", [["HST", 15]]),
  ("QC", "Quebec: GST 5% + QST 9.975%", [["GST", 5], ["QST", 9.975]]),
  ("SK", "Saskatchewan: GST 5% + PST 6%", [["GST", 5], ["PST", 6]]),
  ("YT", "Yukon: GST 5%", [["GST", 5]]),
]
COUNTRIES.append({
 "slug": "canada-gst-hst-invoice-template", "out": "invoice-templates/canada-gst-hst-invoice.html",
 "code": "ca", "paper": "letter",
 "seo_title": "Canada GST/HST Invoice Template (Free) with CRA Fields",
 "meta": "Free GST/HST invoice template with the CRA's fields at under $100, $100 to $499.99 and $500 or more, and every province's rate. PDF or fill it in online.",
 "title": "Canadian GST/HST invoice template, with the CRA's three thresholds",
 "description": "A free GST/HST invoice: PDF in Letter size or fill it in online with each province's rate. What the CRA requires at under $100, $100 to $499.99 and $500 or more, and the registration number format.",
 "dek": "What a Canadian invoice must show depends on its total. The CRA sets three bands, and your customer needs the right fields on it to claim their input tax credit.",
 "checked": checked(("CRA: Input tax credits", CA_ITC), ("the CRA GST/HST rate table", CA_RATES)),
 "takeaways": [
   "Every invoice: your business or trading name, the date, and the total.",
   "<strong>$100 to $499.99:</strong> add the GST/HST charged (or a statement that it is included), and your <strong>GST/HST registration number</strong>.",
   "<strong>$500 or more:</strong> add the buyer's name, a brief description, and the <strong>terms of payment</strong>.",
   "Rates by province since 1 April 2025: <strong>HST 13%</strong> Ontario, <strong>14%</strong> Nova Scotia, <strong>15%</strong> NB, NL and PEI; <strong>GST 5%</strong> elsewhere.",
   "BC, Manitoba, Saskatchewan and Quebec add their own provincial sales tax on top of the 5% GST.",
 ],
 "editor": {
   "key": "ca", "title": "Invoice", "untaxed_title": "Invoice", "currency": "CAD", "locale": "en-CA",
   "tax_name": "GST/HST", "tax_label": "GST/HST registration no.", "tax_ph": "123456789 RT 0001", "mode": "set",
   "provinces": CA_PROVINCES, "client_tax_note": "(optional)", "reg_label": "I am GST/HST registered",
   "extra": [("terms", "Terms of payment", "e.g. Due in 30 days")],
   "rule": "Fields follow the CRA's information requirements for input tax credits. Template from duneapps.com.",
 },
 "pdf": {"heading": "INVOICE", "tax_label": "GST/HST registration no.", "client_tax": None,
         "meta": ["Invoice no.", "Invoice date", "Terms of payment", "Province of supply"],
         "cols": [("Description", 92), ("Qty", 16), ("Unit price", 26), ("Taxable", 18), ("Amount", 28)],
         "totals": ["Subtotal", "GST / HST", "PST / RST / QST (BC, MB, SK, QC)", "Total"],
         "rule": "Required by the CRA for input tax credits: registration number from $100; buyer name, description and terms from $500."},
 "faq": [
   ("What does the CRA require on an invoice?",
    "It depends on the total. Under $100: the supplier's business or trading name, the date, and the total. From $100 to $499.99, add the GST/HST charged or a statement that the price includes it, the status of each supply if some are exempt, and the supplier's GST/HST registration number. At $500 or more, add the buyer's name, a brief description, and the terms of payment."),
   ("What does a GST/HST registration number look like?",
    "Fifteen characters: the nine-digit Business Number, the letters RT for the GST/HST program, and a four-digit account number, as in 123456789 RT 0001. It goes on invoices of $100 or more."),
   ("What GST/HST rate do I charge in each province?",
    "From 1 April 2025: HST of 13% in Ontario, 14% in Nova Scotia, and 15% in New Brunswick, Newfoundland and Labrador, and Prince Edward Island; GST of 5% in Alberta, British Columbia, Manitoba, Quebec, Saskatchewan and the three territories. British Columbia, Manitoba, Saskatchewan and Quebec also have their own provincial sales tax, administered by the province."),
   ("How long do I keep invoices in Canada?",
    "Generally six years from the end of the last tax year they relate to."),
 ],
 "sources": [
   ("CRA: Input tax credits, information required on invoices", CA_ITC),
   ("CRA: GST/HST rates by province (from 1 April 2025)", CA_RATES),
   ("CRA: Where to keep your records and for how long", CA_KEEP),
 ],
 "related": ["us-invoice-template", "how-long-to-keep-receipts", "australia-tax-invoice-template"],
 "body": f"""
<p>A Canadian invoice in Letter size. Pick the province of supply on the fill-in version and it applies that province's GST or HST, plus the provincial tax where there is one. The PDF has every field the CRA asks for at $500 and above, so one form covers all three bands.</p>
<!--downloads-->

<h2>What the CRA requires, by total</h2>

{facts([
  ("Your business or trading name", "Yes", "Yes", "Yes"),
  ("Invoice date", "Yes", "Yes", "Yes"),
  ("Total amount paid or payable", "Yes", "Yes", "Yes"),
  ("GST/HST charged, or a statement that the price includes it", "", "Yes", "Yes"),
  ("Which supplies are taxable, when some are exempt", "", "Yes", "Yes"),
  ("Your <strong>GST/HST registration number</strong>", "", "Yes", "Yes"),
  ("The buyer's name or trading name", "", "", "Yes"),
  ("A brief description", "", "", "Yes"),
  ("The <strong>terms of payment</strong>", "", "", "Yes"),
], head=("Field", "Under $100", "$100 to $499.99", "$500 or more"))}

<p>These are the CRA's requirements for your customer to claim an input tax credit, and without them, the CRA says, it may deny the claim. That makes the bands your problem too: a business customer who cannot claim the credit will ask you for a new invoice.</p>

<h3>The rate</h3>

{facts([
  ("Ontario", "HST 13%"),
  ("Nova Scotia", "HST 14% (15% until 31 March 2025)"),
  ("New Brunswick, Newfoundland and Labrador, Prince Edward Island", "HST 15%"),
  ("Alberta, Northwest Territories, Nunavut, Yukon", "GST 5%"),
  ("British Columbia, Manitoba, Quebec, Saskatchewan", "GST 5%, plus the provincial sales tax"),
], head=("Province or territory", "Federal GST/HST"))}

<p>The provincial taxes in the four provinces that keep one (BC PST 7%, Manitoba RST 7%, Saskatchewan PST 6%, Quebec QST 9.975%) are set by those provinces, which is where to confirm them and register. The fill-in version uses those rates; change the province and the lines change with it.</p>
""",
 "after": "",
})

# ---------------- Australia ----------------
COUNTRIES.append({
 "slug": "australia-tax-invoice-template", "out": "invoice-templates/australia-tax-invoice.html",
 "code": "au", "paper": "a4",
 "seo_title": "Tax Invoice Template Australia (Free) with the ATO's 7 Details",
 "meta": "Free Australian tax invoice template with the ATO's seven details, the buyer's ABN from $1,000 and the 28-day rule. PDF or fill it in online, GST worked out.",
 "title": "Australian tax invoice template, with the ATO's seven details",
 "description": "A free Australian tax invoice: PDF or fill it in online with GST worked out. The seven details the ATO requires, the buyer's identity or ABN from $1,000, and when you must provide one.",
 "dek": "The ATO's rule is short enough to fit on a card: seven details under $1,000, an eighth from $1,000. The template carries all eight, so it works at any amount.",
 "checked": checked(("ATO: Tax invoices", AU_TAXINV),),
 "takeaways": [
   "Under $1,000 a tax invoice must show seven things: that it is a <strong>tax invoice</strong>, your identity, your <strong>ABN</strong>, the date, what you sold with quantity and price, the <strong>GST</strong>, and how far each item is taxable.",
   "From <strong>$1,000</strong>, add the buyer's identity or ABN.",
   "If a customer asks, you must provide a tax invoice <strong>within 28 days</strong>, unless the sale is $82.50 or less including GST.",
   "The GST can be shown as an amount, or, if it is exactly one eleventh of the total, as the words \"Total price includes GST\".",
 ],
 "editor": {
   "key": "au", "title": "Tax Invoice", "untaxed_title": "Invoice", "currency": "AUD", "locale": "en-AU",
   "tax_name": "GST", "tax_label": "ABN", "tax_ph": "11-digit ABN", "mode": "line", "presets": [10, 0],
   "client_tax_note": "(needed at $1,000 or more, or their name)", "reg_label": "I am registered for GST",
   "rule": "Fields follow the ATO's tax invoice requirements. Template from duneapps.com.",
 },
 "pdf": {"heading": "TAX INVOICE", "tax_label": "ABN", "client_tax": "Buyer's ABN (required at $1,000 or more)",
         "meta": ["Invoice no.", "Date of issue", "Payment due"],
         "cols": [("Description", 82), ("Qty", 16), ("Unit price", 26), ("GST", 22), ("Amount", 30)],
         "totals": ["Total excluding GST", "GST", "Total including GST"],
         "rule": "The seven details the ATO requires on a tax invoice, plus the buyer's identity or ABN for sales of $1,000 or more."},
 "faq": [
   ("What must an Australian tax invoice show?",
    "For a taxable sale of less than $1,000, the ATO lists seven details: that the document is intended to be a tax invoice, the seller's identity, the seller's ABN, the date of issue, a brief description of what was sold with the quantity and price, the GST amount payable, and the extent to which each sale on the invoice is taxable. For sales of $1,000 or more, add the buyer's identity or ABN."),
   ("Do I have to give a tax invoice for a small sale?",
    "Only if the customer asks, and then within 28 days, unless the sale is $82.50 or less including GST. A business customer needs a tax invoice to claim a GST credit on a purchase above $82.50."),
   ("Can I write 'Total price includes GST' instead of the GST amount?",
    "Yes, where the GST is exactly one eleventh of the total price. Otherwise show the GST amount."),
   ("How long do I keep tax invoices in Australia?",
    "Five years is the ATO's general rule for records."),
 ],
 "sources": [
   ("ATO: Tax invoices (seven details, $1,000 rule, 28 days, $82.50)", AU_TAXINV),
   ("ATO: Records you need to keep", AU_RECORDS),
 ],
 "related": ["uk-invoice-template", "how-long-to-keep-receipts", "do-you-need-receipts-for-tax-deductions"],
 "body": f"""
<p>An Australian tax invoice with GST worked out per line. Download the PDF, or fill it in here and save it as a PDF.</p>
<!--downloads-->

<h2>What the ATO requires</h2>

{facts([
  ("That the document is intended to be a <strong>tax invoice</strong>", "Yes", "Yes"),
  ("Your identity", "Yes", "Yes"),
  ("Your <strong>ABN</strong>", "Yes", "Yes"),
  ("The date of issue", "Yes", "Yes"),
  ("A brief description, with quantity (if applicable) and price", "Yes", "Yes"),
  ("The <strong>GST</strong> amount, or \"Total price includes GST\" if it is one eleventh", "Yes", "Yes"),
  ("The extent to which each sale is taxable", "Yes", "Yes"),
  ("The buyer's identity or ABN", "", "Yes"),
], head=("Detail", "Under $1,000", "$1,000 or more"))}

<p>The ATO's own shortcut: if your tax invoices meet the requirements for sales of $1,000 or more, you can use them for smaller sales too. That is why this template carries the buyer's details on every version.</p>

<h3>When you have to provide one</h3>

<p>If a customer asks for a tax invoice, you must give them one within 28 days, unless the sale was $82.50 or less including GST. Below that amount a business customer can claim the GST credit from a receipt or a docket. Above it, they need a tax invoice from you, so most business customers will ask.</p>
""",
 "after": "",
})


# ---------------------------------------------------------------------------
# PDFs
# ---------------------------------------------------------------------------
def draw_invoice_pdf(path, pdf, paper):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as pdfcanvas

    W, H = A4 if paper == "a4" else letter
    c = pdfcanvas.Canvas(str(path), pagesize=(W, H))
    c.setTitle(pdf["heading"].title() + " template")
    c.setAuthor("Dune Apps")
    TEAL, INK, GREY, LINE = (colors.HexColor(h) for h in ("#1A4B44", "#0E1315", "#59666A", "#C9D2D4"))
    L, R = 14 * mm, W - 14 * mm
    y = H - 16 * mm

    def label(x, yy, text, size=7):
        c.setFillColor(GREY); c.setFont("Helvetica", size); c.drawString(x, yy, text.upper())

    def blank(x, yy, w):
        c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(x, yy, x + w, yy)

    # Supplier block (left) and heading + meta (right)
    c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 20)
    c.drawRightString(R, y, pdf["heading"])
    label(L, y + 2, "From")
    yy = y - 8 * mm
    for _ in range(3):
        blank(L, yy, 82 * mm); yy -= 7 * mm
    if pdf.get("tax_label"):
        label(L, yy + 2, pdf["tax_label"]); blank(L + 40 * mm, yy, 42 * mm); yy -= 7 * mm
    left_bottom = yy

    my = y - 10 * mm
    mx = R - 78 * mm
    for m in pdf["meta"]:
        label(mx, my + 1, m, 6.5); blank(mx, my - 4 * mm, 78 * mm); my -= 10 * mm

    y = min(left_bottom, my) - 4 * mm
    label(L, y, "Bill to")
    y -= 7 * mm
    for _ in range(2):
        blank(L, y, 100 * mm); y -= 7 * mm
    if pdf.get("client_tax"):
        label(L, y + 2, pdf["client_tax"]); blank(L + 62 * mm, y, 38 * mm); y -= 7 * mm
    y -= 5 * mm

    cols = pdf["cols"]
    unit = (R - L) / sum(w for _, w in cols)
    xs, x = [], L
    for name, w in cols:
        xs.append((name, x, w * unit)); x += w * unit
    head_h = 7 * mm
    c.setFillColor(TEAL); c.rect(L, y - head_h, R - L, head_h, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 7.2 if len(cols) > 6 else 8)
    for name, x0, w in xs:
        c.drawString(x0 + 1.6 * mm, y - head_h + 2.4 * mm, name)
    y -= head_h
    rows, row_h = 12, 7.5 * mm
    c.setStrokeColor(LINE); c.setLineWidth(0.5)
    top = y
    for i in range(rows + 1):
        c.line(L, y - i * row_h, R, y - i * row_h)
    for _, x0, _w in xs[1:]:
        c.line(x0, top, x0, top - rows * row_h)
    y = top - rows * row_h - 6 * mm

    tx = R - 84 * mm
    for t in pdf["totals"]:
        bold = t == pdf["totals"][-1] or t.startswith("Total")
        c.setFillColor(INK); c.setFont("Helvetica-Bold" if bold else "Helvetica", 8.5)
        c.drawString(tx, y, t)
        blank(R - 30 * mm, y - 1, 30 * mm)
        y -= 7 * mm

    label(L, y + 2, "How to pay")
    yy = y - 6 * mm
    for _ in range(2):
        blank(L, yy, 100 * mm); yy -= 7 * mm
    if pdf.get("sign"):
        c.setStrokeColor(INK); c.setLineWidth(0.6); c.line(R - 80 * mm, yy - 8 * mm, R, yy - 8 * mm)
        c.setFillColor(GREY); c.setFont("Helvetica", 6.8)
        c.drawRightString(R, yy - 12 * mm, pdf["sign"])

    c.setFillColor(GREY); c.setFont("Helvetica", 6.8)
    c.drawString(L, 12 * mm, pdf["rule"])
    c.drawString(L, 8.5 * mm, "Free template from duneapps.com/invoice-templates/  ·  Not legal or tax advice.")
    c.showPage()
    c.save()


def pdf_files(country):
    """[(filename, label)] for the downloads row, in the order shown."""
    out = [(f"{country['slug']}.pdf", f"Download the PDF ({'A4' if country['paper'] == 'a4' else 'US Letter'})")]
    second = country["pdf"].get("second")
    if second:
        out.append((f"{second['file']}.pdf", "PDF, not VAT registered"))
    return out


def downloads_row(country):
    links = "".join(f'<a class="btn btn-primary" href="/{DL}/{f}">{html.escape(t)}</a>' for f, t in pdf_files(country))
    return f'<div class="inv-dl">{links}<a class="btn btn-dark" href="#fill">Fill it in online</a></div>'


def build_pdfs():
    try:
        import reportlab  # noqa: F401
    except ImportError:
        print("invoice PDFs: reportlab not installed, committed files left alone")
        return
    d = ROOT / DL
    d.mkdir(parents=True, exist_ok=True)
    for co in COUNTRIES:
        draw_invoice_pdf(d / f"{co['slug']}.pdf", co["pdf"], co["paper"])
        second = co["pdf"].get("second")
        if second:
            draw_invoice_pdf(d / f"{second['file']}.pdf", {**co["pdf"], **second}, co["paper"])
    print("invoice PDFs:", len(list(d.glob("*.pdf"))))


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_post(co):
    e = co["editor"]
    body = co["body"].replace("<!--downloads-->", downloads_row(co))
    body += "\n<h2>Fill it in here</h2>\n" + editor(e) + "\n<!--cta-->\n" + co.get("after", "")
    return {
        "out": co["out"], "slug": co["slug"], "seo_title": co["seo_title"], "meta": co["meta"],
        "title": co["title"], "description": co["description"], "dek": co["dek"], "topic": "Invoices",
        "date_iso": "2026-11-15", "updated": "2026-11-15", "og": f"og-{co['slug']}.png",
        "cta": "paidsnap",
        "cta_title": "Or make it on your iPhone.",
        # CountryPack.registeredTitle: only AE, IN and AU (of these six) print "Tax Invoice".
        "cta_text": PAIDSNAP_LINE.format(label=PAIDSNAP_LABEL[co["code"]],
                                         heading="the Tax Invoice heading, " if co["code"] in ("ae", "in", "au") else "")
                    + " It sends a real PDF, and the free plan covers three documents a month.",
        "checked": co["checked"], "takeaways": co["takeaways"], "faq": co["faq"], "sources": co["sources"],
        "related": co["related"], "body": body, "style": EDITOR_CSS, "script": EDITOR_JS,
        "disclaimer": "General information, not legal or tax advice. Invoice rules and rates change; check the current position with your tax authority or an accountant.",
    }


PAGES = [page_post(co) for co in COUNTRIES]


def hub():
    cards = "".join(
        f'<a class="post-card reveal" href="/{p["out"]}"><span class="topic">{name}</span><h3>{html.escape(p["title"])}</h3>'
        f'<p>{html.escape(p["description"])}</p><span class="when">PDF · fill in online · checked {CHECKED_ON}</span></a>'
        for p, name in zip(PAGES, ["UAE", "India", "United Kingdom", "United States", "Canada", "Australia"]))
    a = APPS["paidsnap"]
    body = f'''<section class="hub-head"><div class="wrap">
  <span class="eyebrow">Free templates</span>
  <h1>Invoice templates by country, with the rules cited</h1>
  <p>An invoice that is missing a required field can cost your customer their tax credit and cost you the payment. Each template below carries the fields that country's tax authority lists, with the clause next to each one. Download the PDF, or fill it in on the page and save it as a PDF. Nothing you type leaves your browser.</p>
</div></section>
<section class="hub-group"><div class="wrap"><div class="grid g-3">{cards}</div></div></section>
<section class="section" style="padding-top:40px"><div class="wrap"><div class="final reveal" style="background:var(--card);border-radius:40px;padding:56px 32px;text-align:center;box-shadow:var(--e2)">
  <h2 style="font-size:clamp(1.7rem,4vw,2.4rem)">Making invoices every week?</h2>
  <p style="max-width:58ch;margin:16px auto 0">PaidSnap is our iPhone invoice app. Pick your country and it sets the heading, the tax number label and the tax lines, then sends a real PDF. No account; the free plan covers three documents a month.</p>
  <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:28px">
    <a class="btn btn-primary" href="{a["store"]}" data-app="paidsnap" data-place="invoice-hub">Get PaidSnap</a>
    <a class="btn btn-dark" href="/paidsnap/">See PaidSnap</a>
  </div>
</div></div></section>'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Invoice templates by country",
          "url": f"{SITE}/invoice-templates/",
          "hasPart": [{"@type": "WebPage", "name": p["title"], "url": f"{SITE}/{p['out']}"} for p in PAGES]}
    render(out="invoice-templates/index.html",
           title="Free Invoice Templates by Country (PDF) · Dune Apps",
           description="Free invoice templates for the UAE, India, UK, US, Canada and Australia, with the fields each tax authority requires and the rule cited. PDF or online.",
           canonical=f"{SITE}/invoice-templates/", body=body, og_image="og-invoice-templates.png", priority="0.8",
           head='<script type="application/ld+json">' + json.dumps(ld) + "</script>")


def main():
    from content_posts import INDEX
    index = {**INDEX, **{p["slug"]: p for p in PAGES}}
    build_pdfs()
    for p in PAGES:
        render_article(p, index)
        print("invoice page:", p["out"])
    hub()
    print("invoice hub")


if __name__ == "__main__":
    main()
