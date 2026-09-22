#!/usr/bin/env python3
"""One command renders the whole site and checks it.

    python3 build_all.py

Every generator is imported into this one process so they share
build.PAGES, which is what the sitemap is written from. The checks at the
end are the ones that caught real regressions before: chrome drift between
pages, the old tagline, and internal links to files that do not exist.
"""
import hashlib
import pathlib
import re
import sys

import build

import gen_pages; gen_pages.main()   # home, DriveSnap
import gen2                          # Receipt Snap, comparison (renders on import)
import gen3; gen3.main()             # PaidSnap page + its privacy policy
import gen                           # guides, hub, template, csv (renders on import)
from content_posts import POSTS

build.render_go_pages()
build.write_sitemap()
build.write_llms(POSTS)

# ---------- checks ----------
ROOT = build.ROOT
htmls = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "_pages" not in p.parts
         and "_ported" not in p.parts and "go" not in p.parts]
problems = []

def block(s, tag):
    m = re.search(rf"<{tag}[ >].*?</{tag}>", s, re.S)
    return m.group(0) if m else ""

hdr = set(); ftr = set()
for p in htmls:
    s = p.read_text()
    hdr.add(hashlib.md5(block(s, "header").encode()).hexdigest())
    ftr.add(hashlib.md5(block(s, "footer").encode()).hexdigest())
    if "built in Dubai" in s:
        problems.append(f"old tagline in {p}")
    for href in re.findall(r'href="(/[^"#?]+)', s):
        target = ROOT / href.lstrip("/")
        if href.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            problems.append(f"{p.relative_to(ROOT)} → broken link {href}")
if len(hdr) != 1: problems.append(f"header differs across pages ({len(hdr)} variants)")
if len(ftr) != 1: problems.append(f"footer differs across pages ({len(ftr)} variants)")

print(f"\n{len(htmls)} pages rendered")
if problems:
    print("PROBLEMS:"); [print("  -", x) for x in problems]; sys.exit(1)
print("checks: chrome identical on every page, no old tagline, no broken internal links")
