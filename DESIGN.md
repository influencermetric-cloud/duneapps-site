# Dune Apps — site design system ("Desert Editorial", Sep 2026)

References studied: Anthropic.com (warm cream + serif editorial), iA.net (typography-as-design),
Ghost.org (blog index structure), Stripe (structural rigor), 2026 warm-minimalism trend
(terracotta / sand / clay replacing white+black+neon).

## Palette (single committed light look — printed-paper metaphor, no dark mode)
- Paper        #F7F3EB   page ground (warm ivory)
- Raised       #FCFAF5   panels/cards
- Ink          #221E15   headlines, body emphasis (warm near-black)
- Ink-2        #57503F   body text
- Faint        #7A7264   meta, captions (≥4.5:1 on paper)
- Line         #E4DCCB   hairline rules
- Terracotta   #A0481A   links, accents (text-safe, 5.9:1)
- Terracotta-2 #C05B2B   graphic accents only
- Gold         #D9A441   sun / graphic accents only, never text

## Type
- Display/headlines: **Fraunces** (variable, opsz 9–144) — warm, classic, characterful
- Prose/ledes:       **Newsreader** (variable, opsz) — editorial body
- Meta/labels/nav:   **IBM Plex Mono** 400/500, uppercase, tracked +0.14em, 11–12px
- Fallbacks: Iowan Old Style/Georgia (serifs), ui-monospace

## Logo
Line-drawn crescent-dune mark: two overlapping ridges (ink front, sand back) + terracotta sun.
Wordmark "Dune Apps" in Fraunces 560. Mark must read at 16px (favicon-tested).

## Layout rules
- Max content 1064px, generous vertical rhythm (sections 96px apart)
- Hairline rules, not shadows. Panels: 1px line border, radius 12, raised paper fill
- Blog index = editorial rows (mono date column + serif title), not card grid
- Hero: mono kicker → huge Fraunces headline → Newsreader lede → dune-horizon line art
- Motion: fade-up reveals (IntersectionObserver, reduced-motion guarded), underline
  transitions, 2px hover lifts. Nothing else.
