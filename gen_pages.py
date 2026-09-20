#!/usr/bin/env python3
"""Renders the homepage and the DriveSnap page through the shared shell.

These two were the only pages no generator produced. They had been emitted by
an older version of build.py and then edited by hand, which is exactly how the
chrome drifts: drivesnap/index.html still opened its content with <main>, while
the shell emits <main id="main">, so the header's "Skip to content" link
pointed at an anchor that did not exist on that page.

Body, page CSS and any JSON-LD live in _pages/ so they stay editable
(the underscore keeps Jekyll from serving the fragments); the header,
footer, fonts and meta come from build.render() like every other page.
"""
import json
import pathlib

from build import render

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ROOT / "_pages"


def read(name):
    path = PAGES / name
    return path.read_text() if path.exists() else ""


HOME_GUIDES = ["irs-mileage-rate-2026", "do-you-need-receipts-for-tax-deductions", "hmrc-mileage-rates-2026",
               "how-long-to-keep-receipts", "expense-tracker-apps-that-dont-sell-your-data", "mileage-log-template"]


def guide_cards():
    from build import nice_date, reading_minutes
    from content_posts import INDEX
    return "".join(
        f'<a class="post-card reveal" href="/{p["out"]}"><span class="topic">{p["topic"]}</span><h3>{p["title"]}</h3>'
        f'<p>{p["description"]}</p><span class="when">Updated {nice_date(p["updated"])} · {reading_minutes(p["body"])} min</span></a>'
        for p in (INDEX[s] for s in HOME_GUIDES if s in INDEX))


def main():
    spec = json.loads((PAGES / "meta.json").read_text())
    for key, page in spec.items():
        body = read(f"{key}.body.html").replace("<!--guides-->", guide_cards())
        render(out=page["out"],
               title=page["title"],
               description=page["description"],
               canonical=page["canonical"],
               body=body,
               priority="1.0" if key == "index" else "0.9",
               style=read(f"{key}.css"),
               head=read(f"{key}.head.html"),
               og_image=page.get("og", "og.png"),
               og_type=page.get("og_type", "website"))
        print("page:", page["out"])


if __name__ == "__main__":
    main()
