# Design system (archived): Trace Direction

Archived on 2026-11-17 when the site moved to the Liquid glass direction (see MASTER.md).
Kept so the Trace look can be restored.

## Theses (validated 2026-10-23)

**Visual.** A calm, precise portfolio with one Playwright moment. Cool light ground
with a matching dark theme, near-black ink, one inspector-magenta accent kept for
highlights, green only for "pass / done". IBM Plex Sans Condensed SemiBold for names and
headings (same family as the mono labels, fits a big name in a narrow column), IBM Plex
Sans for body, IBM Plex Mono for labels, tags and the nav. High size contrast, airy
spacing on an 8px base, sharp flat components: 2px radius, 1px borders, no shadows.

**Interaction.** One orchestrated moment: on load a magenta locator box snaps onto the
name, the pitch line and the stack list in turn, each labelled with its real Playwright
locator and a ✓ (220ms on the snap curve, 600ms apart, about 2.4s, once). Everything
else is quiet: hover and focus respond in 140ms ease-out. Nothing waits for scroll to
appear. Forbidden: bounce or elastic, parallax, glass blur, endless loops, 3D or WebGL,
gradient text.

**Allowed patterns:** mono labels and nav, the hero locator sequence, Playwright locator
code as labels, ✓ / ○ status marks, hairlines between project rows (the rows are scanned
across columns).

## Colour

| Token | Light | Dark | Use | Contrast on ground (L / D) |
|---|---|---|---|---|
| `--ground` | `#F3F5F8` | `#0F1318` | page | |
| `--surface` | `#FFFFFF` | `#161B22` | cards, hovered rows | |
| `--ink` | `#14181F` | `#E8ECF1` | text, primary button | 16.3 / 15.7 |
| `--ink-soft` | `#545C69` | `#9AA4B2` | secondary text, labels | 6.2 / 7.4 |
| `--rule` | `#D5DAE1` | `#2A313B` | hairlines (decorative) | |
| `--rule-strong` | `#C5CCD6` | `#3A4350` | tag borders | |
| `--locate` | `#C2255C` | `#F06595` | the one accent: locator box, hover, focus, "in progress" | 5.2 / 6.2 |
| `--locate-wash` | 6% of locate | 9% of locate | locator box fill | |
| `--pass` | `#1F7A4D` | `#51CF8A` | "automated", "done" only | 4.9 / 9.5 |
| `--band` / `--band-ink` / `--band-soft` / `--band-rule` | `#14181F` / `#E8ECF1` / `#9AA4B2` / `#3A4350` | `#1B212A` / same | contact band | soft on band 7.0 |

## Type

| Token | Value |
|---|---|
| `--display` | `'IBM Plex Sans Condensed', 'Arial Narrow', 'Roboto Condensed', sans-serif`, 600 |
| `--body` | `'IBM Plex Sans', 'Segoe UI', Roboto, system-ui, sans-serif`, 400 / 500 |
| `--mono` | `'IBM Plex Mono', ui-monospace, Consolas, monospace`, 400 / 500 |

Scale: name `clamp(56px, 9vw, 120px)` / 0.95 · contact headline `clamp(44px, 6vw, 80px)` ·
section h2 44px · row h3 28px · step h3 22px · lead 19–23px · body 16px / 1.6 ·
labels 12.5–13px mono.

## Spacing, shape

8px base: 4, 8, 12, 16, 24, 32, 40, 56, 88, 112. Sections pad 88px vertically, the
hero 112 / 96. Content column max 1160px with 24px gutters. Radius 2px everywhere.
No shadows. Touch targets at least 44px.

## Motion

| Token | Value | Use |
|---|---|---|
| `--snap` | `cubic-bezier(0.2, 0, 0, 1)` | locator box in |
| `--snap-ms` | 220ms | locator box in |
| `--step-ms` | 600ms (JS) | gap between locator targets |
| `--respond-ms` | 140ms ease-out | hover, focus, colour changes |

Reduced motion: the hero sequence never runs, transitions are instant.

## Components

- **Button, primary:** ink fill, surface text; hover locate fill. **Ghost:** ink border;
  hover locate border and text. Both: focus 2px locate ring, 3px offset; active nudges 1px
  down; disabled 45% opacity.
- **Project row:** 3-column grid (name + domain / description / status + tools), stacks
  under 900px; hover tints to surface and the name turns locate.
- **Step card:** surface card, 1px rule border; the current step has a locate border.
- **Fact list:** surface card, label / value rows.
