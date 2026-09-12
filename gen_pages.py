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


def main():
    spec = json.loads((PAGES / "meta.json").read_text())
    for key, page in spec.items():
        render(out=page["out"],
               title=page["title"],
               description=page["description"],
               canonical=page["canonical"],
               body=read(f"{key}.body.html"),
               style=read(f"{key}.css"),
               head=read(f"{key}.head.html"),
               og_image=page.get("og", "og.png"),
               og_type=page.get("og_type", "website"))
        print("page:", page["out"])


if __name__ == "__main__":
    main()
