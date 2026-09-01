"""Per-page Open Graph cards. Every page shared one generic image, so every
link looked identical when shared."""
import pathlib, subprocess, tempfile
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = pathlib.Path(__file__).resolve().parent

CARDS = [
 ("og.png", "Dune Apps", "iPhone tools that keep your data on your phone", "duneapps.com"),
 ("og-drivesnap.png", "DriveSnap", "A mileage log that never leaves your phone", "No drive caps · Free to track"),
 ("og-receiptsnap.png", "Receipt Snap", "Receipts read on your phone and kept there", "Data Not Collected · Free"),
 ("og-compare.png", "DriveSnap vs MileIQ", "No drive caps. Nothing uploaded. $29.99 a year.", "An honest comparison · 2026"),
 ("og-writing.png", "Guides", "What tax authorities actually require from your records", "duneapps.com/writing"),
]

TPL = '''<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{width:1200px;height:630px;background:#F1F3F5;font-family:Inter,sans-serif;
   position:relative;overflow:hidden;padding:74px}}
 .bubble{{position:absolute;right:-180px;top:50%;transform:translateY(-50%);
   width:660px;height:660px;border-radius:50%;
   background:radial-gradient(circle at 30% 28%,#FFE9A8 0%,transparent 42%),
     radial-gradient(circle at 68% 22%,#A8E4FF 0%,transparent 46%),
     radial-gradient(circle at 74% 74%,#D8B4FE 0%,transparent 48%),
     radial-gradient(circle at 26% 76%,#9BF6D2 0%,transparent 46%),
     conic-gradient(from 210deg,#FDE2E4,#CDE7FF,#E0D4FF,#D6F5E3,#FFF3C4,#FDE2E4);
   filter:blur(2px) saturate(1.1);opacity:.9}}
 .inner{{position:relative;z-index:2;max-width:660px;height:100%;
   display:flex;flex-direction:column;justify-content:center}}
 .brand{{display:flex;align-items:center;gap:14px;margin-bottom:34px}}
 .brand img{{width:46px;height:46px}}
 .brand span{{font-size:24px;font-weight:600;color:#0E1315;letter-spacing:-.03em}}
 h1{{font-size:60px;font-weight:600;color:#0E1315;letter-spacing:-.035em;line-height:1.05}}
 p{{font-size:27px;color:#59666A;margin-top:20px;line-height:1.35}}
 .foot{{position:absolute;bottom:74px;left:74px;font-size:19px;color:#8B979B;z-index:2}}
</style>
<div class="bubble"></div>
<div class="inner">
  <div class="brand"><img src="{mark}"><span>Dune Apps</span></div>
  <h1>{title}</h1><p>{sub}</p>
</div>
<div class="foot">{foot}</div>'''

mark = (ROOT / "brand" / "dune-mark.svg").as_uri()
for name, title, sub, foot in CARDS:
    html = TPL.format(mark=mark, title=title, sub=sub, foot=foot)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html); page = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
      "--allow-file-access-from-files", "--force-device-scale-factor=1",
      "--window-size=1200,630", f"--screenshot={ROOT/name}", f"file://{page}"],
      check=True, capture_output=True)
    print("  ", name)
