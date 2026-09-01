#!/usr/bin/env python3
"""Renders every page from one shared shell.

The pages drifted apart before because each carried its own copy of the
header, footer, fonts and meta. Now there is exactly one definition of the
chrome and each page supplies only its own body.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
GA = "G-BTY3LVJMBB"
FAVICON = ('data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20'
  'viewBox%3D%270%200%2040%2040%27%3E%3Cdefs%3E%3CclipPath%20id%3D%27d%27%3E%3Ccircle%20cx%3D%2720%27%20'
  'cy%3D%2720%27%20r%3D%2719%27%2F%3E%3C%2FclipPath%3E%3C%2Fdefs%3E%3Ccircle%20cx%3D%2720%27%20cy%3D%2720%27%20'
  'r%3D%2719%27%20fill%3D%27%23EFF3F1%27%2F%3E%3Cg%20clip-path%3D%27url%28%23d%29%27%3E%3Ccircle%20cx%3D%2713%27%20'
  'cy%3D%2713%27%20r%3D%275%27%20fill%3D%27%23C3F04C%27%2F%3E%3Cpath%20d%3D%27M13%2041%20L41%2041%20L41%2025%20'
  'C%2034%2025.8%2027.5%2028.8%2022%2033.8%20L13%2041%20Z%27%20fill%3D%27%239DB8B2%27%2F%3E%3Cpath%20d%3D%27'
  'M-1%2041%20L-1%2029.4%20C%208%2028.6%2015.2%2025.8%2020.4%2021%20C%2021.6%2019.9%2022.9%2019.9%2024%2021.1%20'
  'C%2028%2025.4%2033.4%2029%2041%2030.8%20L41%2041%20Z%27%20fill%3D%27%231A4B44%27%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E')

HEADER = '''<a class="skip" href="#main">Skip to content</a>

<header id="hdr"><div class="wrap bar">
  <a class="brand" href="/"><span class="mark" aria-hidden="true"></span><span>Dune Apps</span></a>
  <nav class="site-nav">
    <a href="/#apps">Apps</a>
    <a href="/writing/">Writing</a>
    <a href="/drivesnap/">DriveSnap</a>
    <a class="btn btn-primary btn-sm" href="/drivesnap/">Get Started</a>
  </nav>
</div></header>'''

FOOTER = '''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="/"><span class="mark" aria-hidden="true"></span><span>Dune Apps</span></a>
        <p style="margin-top:18px;max-width:34ch;color:rgba(255,255,255,.72)">Small, careful iPhone tools that run entirely on your device — no servers, no accounts, nothing collected.</p>
      </div>
      <div><h4>Apps</h4>
        <a href="/drivesnap/">DriveSnap</a>
        <a href="/receiptsnap/">Receipt Snap</a>
        <a href="/compare/drivesnap-vs-mileiq/">DriveSnap vs MileIQ</a></div>
      <div><h4>Guides</h4>
        <a href="/writing/">All writing</a>
        <a href="/posts/irs-mileage-log-requirements.html">IRS mileage log rules</a>
        <a href="/posts/how-long-to-keep-receipts.html">How long to keep receipts</a>
        <a href="/posts/uae-vat-record-keeping.html">UAE VAT records</a></div>
      <div><h4>Support</h4>
        <a href="https://github.com/influencermetric-cloud/drivesnap-support">DriveSnap support</a>
        <a href="https://github.com/influencermetric-cloud/receiptsnap-support">Receipt Snap support</a>
        <a href="https://github.com/influencermetric-cloud/drivesnap-support/blob/main/PRIVACY.md">Privacy policy</a></div>
    </div>
    <p class="disclosure">Dune Apps · built in Dubai. This website uses Google Analytics to see which pages help people. The apps themselves collect nothing at all.</p>
  </div>
</footer>

<script>
  const hdr = document.getElementById('hdr');
  addEventListener('scroll', () => hdr.classList.toggle('stuck', scrollY > 8), { passive: true });
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  } else document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
</script>'''


def render(*, out, title, description, canonical, body, style="", head="", og_image="og.png"):
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
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="/brand/dune-mark-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Dune Apps">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://duneapps.com/{og_image}">
<meta name="twitter:card" content="summary_large_image">
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
    return path
