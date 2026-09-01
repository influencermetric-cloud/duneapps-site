# Dune Apps — brand mark (LOCKED, 1 Sep 2026)

Approved by the founder. **Do not redraw, recolour or replace this mark**
without an explicit instruction. It was once swapped for a generic circle
copied off a reference template; that was wrong, and it is the one piece of
identity this brand owns.

## Files

| File | Use |
|---|---|
| `dune-mark.svg` | The mark. Source of truth. |
| `dune-mark-mono.svg` | Single-colour version — inherits `currentColor`. For dark grounds, stamps, favicons. |
| `dune-lockup.svg` | Mark + "Dune Apps" wordmark, horizontal. |
| `dune-mark-{32,64,128,180,512,1024}.png` | Raster, transparent. 180 = apple-touch-icon, 512/1024 = stores and OG. |
| `dune-lockup-{660,1320}.png` | Raster lockup, transparent. 1320 for retina. |

## Colours
- Sun — lime `#C3F04C`
- Back ridge — muted teal `#9DB8B2`
- Front ridge — deep teal `#1A4B44`
- Disc — off-white `#EFF3F1`
- Wordmark — near-black `#0E1315`, Inter 600, −0.6 tracking

## Rules
- The live site renders the mark from **one place**: `.brand .mark` in
  `style.css`, as a background image. Never paste an inline copy into a page —
  that is exactly how the pages drifted apart before.
- Minimum size 24px. Below that use `dune-mark-mono.svg`.
- Clear space around the mark ≥ half its width.
- Never place the colour mark on a mid-tone background; use the mono version.

## Regenerating the PNGs
Rendered from the SVGs with headless Chrome at a transparent background —
see the command in the commit that added this folder.
