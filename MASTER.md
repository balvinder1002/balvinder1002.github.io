# Design system: balvinder1002.github.io

The single source of truth for the site's look. Every colour, size and timing in
`index.html` comes from the tokens below (they live in the `:root` block at the top
of its `<style>`). The full machine-readable profile is `design-dna.json`; this file
is the human summary and wins if the two disagree.

Direction: **Liquid glass** (replaced Trace Direction on 2026-11-17). Mock-up:
https://claude.ai/artifact/V2j4aeSbheQHWh8Robq9Av

## Theses

**Visual.** Calm, modern and precise. Frosted glass panels with bright gradient edges
float over a few large blurred colour orbs on a deep navy ground, with a matching
light theme. One sky-blue accent for actions, focus and the locator lens; green only for
"automated / done"; violet and teal live only in the orbs, never on text or controls.
Inter Tight for headings, Inter for body, JetBrains Mono for labels, chips, statuses
and locator tags. Big type contrast, spacious 8px rhythm, pills and large radii.

**Interaction.** One orchestrated moment: on load a glass locator lens snaps onto the
name, the pitch line and the stack list in turn, each tagged with its real Playwright
locator and a ✓ (1.4s per pass, 0.6s apart, starting at 0.4s, once). Everything else is
quiet: hover and focus respond in 140-160ms. Nothing waits for scroll to appear.

**Forbidden:** gradient text, parallax, scroll-triggered reveals, bounce or elastic
easing, endless loops on content, 3D or WebGL, animated blur, emoji as icons, solid
borders on glass, accent colours other than the one accent.

**Allowed patterns:** glass panels, gradient edges, top sheen, colour orbs behind glass,
mono labels and status pills, the hero locator lens, ✓ / ○ status marks.

## Colour

| Token | Dark (default) | Light | Use |
|---|---|---|---|
| `--bg` | `#0A0F1E` | `#E8EDF7` | page ground |
| `--ink` | `#EEF2FF` | `#0E1428` | text, headings |
| `--soft` | `#AEB8D3` | `#3F4862` | secondary text, labels |
| `--accent` | `#7DD3FC` | `#0369A1` | primary button, lens, focus ring, hover title, "in progress" |
| `--on-accent` | `#06202E` | `#FFFFFF` | text on accent |
| `--accent-glow` | `rgba(125,211,252,.35)` | `rgba(3,105,161,.28)` | primary button glow |
| `--pass` | `#6EE7A0` | `#166534` | "automated", "done" only (tint behind pills: 12% / 10%) |
| `--glass` | `rgba(14,20,40,.42)` (dark-tinted glass) | `rgba(255,255,255,.62)` | panel fill |
| `--glass-strong` | `rgba(255,255,255,.07)` | `rgba(255,255,255,.75)` | hover fill, chips, status pills |
| `--edge` | `rgba(255,255,255,.45)` | `rgba(255,255,255,.95)` | gradient edge highlight |
| `--sheen` | `rgba(255,255,255,.07)` | `rgba(255,255,255,.40)` | top sheen |
| `--hair` | `rgba(255,255,255,.10)` | `rgba(14,20,40,.09)` | hairlines, chip borders |
| `--lens` | `rgba(125,211,252,.10)` | `rgba(3,105,161,.08)` | lens wash |
| orbs | sky `rgba(56,189,248,.42)`, violet `rgba(139,92,246,.40)`, teal `rgba(45,212,191,.32)` | sky `.45`, violet `rgba(167,139,250,.45)`, teal `rgba(94,234,212,.40)` | atmosphere only |

Contrast rule: every text colour must reach 4.5:1 (3:1 for 24px+) against the **composited**
glass over the brightest orb behind it, not just the ground. `test_text_contrast_on_glass`
checks every text node from a real screenshot in both themes at 375 and 1440px. It is why
dark glass is navy-tinted rather than 6% white (6% white let a bright orb drop the eyebrow
label to 2.9:1).

## Type

| Token | Value |
|---|---|
| `--display` | `'Inter Tight', 'Arial Narrow', system-ui, sans-serif`, 600 |
| `--body` | `'Inter', 'Segoe UI', system-ui, sans-serif`, 400 / 500 / 600 |
| `--mono` | `'JetBrains Mono', ui-monospace, Consolas, monospace`, 400 / 500 |

Scale: name `clamp(56px, 9.2cqi, 132px)` / 0.92 / -0.035em · contact headline
`clamp(44px, 6.4cqi, 88px)` / 1 / -0.03em · section h2 48px / 1.05 · project h3 26px ·
role h3 30px · roadmap h3 22px · pitch `clamp(19px, 1.9cqi, 24px)` · lead 20px · body 16px / 1.6 ·
small 15px · labels 12.5px mono · lens tag 11.5px mono. `cqi` units: the page root is a
size container, so type scales with the page, not the window.

## Spacing, layout, shape

8px base: 4, 8, 12, 16, 24, 28, 32, 40, 48, 56, 80, 112. Sections 112px apart; heading
row to content 32px. Content max 1200px with 24px side padding. Layout is flex-wrap and
`repeat(auto-fit, minmax(min(Npx, 100%), 1fr))` grids, so there are no fixed breakpoints
and every row collapses to one column on a phone.

Radius: lens 20px · rows, tiles, cards 22-24px · panels 28px · contact panel 36px ·
pills 999px. No solid borders on glass. Touch targets at least 44px.

## Glass recipe

```css
.glass{
  background: var(--glass);
  backdrop-filter: blur(24px) saturate(170%);
  box-shadow: 0 24px 60px rgba(0,0,0,.35);   /* light: 0 20px 50px rgba(30,45,90,.14) */
  border-radius: 28px;
}
.glass::before{ /* 1px gradient edge, light from the top-left (about 145deg) */
  padding: 1px;
  background: linear-gradient(145deg, var(--edge) 0%, transparent 38%, transparent 62%, var(--edge) 100%);
  mask: linear-gradient(#000 0 0) content-box exclude, linear-gradient(#000 0 0);
}
.glass::after{ background: linear-gradient(170deg, var(--sheen) 0%, transparent 30%); } /* top sheen */
```

Fallback without `backdrop-filter`: panel fill rises to `rgba(14,20,40,.88)` dark /
`rgba(255,255,255,.80)` light. Never nest blurred glass (contact tiles are plain fills on
the contact panel); about 13 blurred panels per page; never animate blur. Every panel
needs an orb somewhere behind it, or it reads as flat grey.

## Motion

**Personality:** Corporate precision on a glass material: decisive, no overshoot
anywhere (glass is rigid), calm. Emotional target: "this person is careful and sure".
One signature moment on load, then the page is still; motion only answers the visitor.

### Tokens

| Token | Value | Use |
|---|---|---|
| `--ease` | `cubic-bezier(0.2, 0, 0, 1)` | signature curve, about 80% of motion: hover, focus, press release |
| `--ease-enter` | `cubic-bezier(0.05, 0.7, 0.1, 1)` | lens appearing, orbs settling |
| `--ease-move` | `cubic-bezier(0.4, 0, 0.2, 1)` | lens travelling between targets |
| `--ease-exit` | `cubic-bezier(0.3, 0, 1, 1)` | lens leaving |
| `--t-quick` | 90ms | hover in, press down |
| `--t-standard` | 180ms | hover out, press release, focus ring |
| `--t-slow` | 420ms | lens travel |

Hover enters fast and leaves slower (90ms in, 180ms out), so it feels responsive and
then settles. Only `transform` and `opacity` animate, plus colour and background fills
on hover. The lens box (one element) is the only thing that changes size.

### The locator lens (signature moment, once per load)

One lens travels through the three hero targets like a test stepping through
assertions. Setup: appear on the name. Action: move to the pitch, then to the stack.
Resolution: each stop confirms with ✓, then the lens leaves.

| Time | What happens | Duration, easing |
|---|---|---|
| 0.40s | Lens appears on the name: opacity 0 to 1, scale 1.04 to 1 | 240ms, `--ease-enter` |
| +120ms | Tag shows the locator; ✓ pops in green, scale 0.6 to 1 | 150ms, `--ease` |
| hold | stays on target | 500ms |
| travel | Lens moves and resizes to the pitch; tag text crossfades on the way; ✓ hides, then pops again on arrival | 420ms, `--ease-move`; text 120ms |
| hold | | 500ms |
| travel | Same, to the stack list | 420ms, `--ease-move` |
| hold | | 500ms |
| exit | Lens fades out and settles to scale 0.98 | 200ms, `--ease-exit` |

About 3.2s in total. The longest move (name to pitch) is about 200px, well under a third
of the screen. Starts after fonts load, only if the hero is on screen (a deep link to
`#projects` skips it). On phones (under 600px wide) every lens time is 0.8x.

**Ambient layer, same moment:** the two hero orbs settle in once: opacity 0 to 1, scale
0.92 to 1, 1600ms `--ease-enter`, 150ms apart. All other orbs are static from the start.
There is no continuous orb drift: moving colour behind `backdrop-filter` makes every
panel re-blur each frame (heavy on phones), and motion over 5 seconds would need a
pause control (WCAG 2.2.2).

### Feedback on interactive elements

Only things you can click move. Glass panels that only hold content never react.

| Element | Hover (`@media (hover: hover)` only) | Press (`:active`) | Focus (`:focus-visible`) |
|---|---|---|---|
| Primary pill button | lift 1px; glow layer opacity 0.6 to 1 | scale 0.97, 90ms; release 180ms | ring |
| Glass pill button | fill `--glass` to `--glass-strong`; edge glow brightens | scale 0.97 | ring |
| Nav link | text `--soft` to `--ink`; pill fill fades in | none | ring |
| Project row | fill fades in; title turns `--accent` | none (rows are not links) | n/a |
| Contact tile | fill fades in; lift 2px | scale 0.99 | ring |
| Chips, panels, cards | none | none | n/a |

Focus ring: 2px `--accent` outline; offset animates 6px to 3px with the colour fading
in, 180ms `--ease`. It shows instantly under reduced motion. No hover effects on touch
screens: press feedback only, under 100ms.

The button glow is a `::after` layer whose opacity changes. `box-shadow` itself is never
animated.

### Reduced motion (`prefers-reduced-motion: reduce`)

- No lens pass at all, and the lens is hidden.
- Orbs are visible and still from the start.
- No lift, scale or offset changes; colour and fill changes stay, applied instantly.
- `scroll-behavior: auto` for nav jumps.
- Nothing conveys information through motion alone: every ✓ and status is also static text.

## Components

- **Nav:** floating glass pill bar, not sticky: monogram badge + name, section links as
  pill hovers, resume button. Wraps on phones.
- **Button, primary:** accent pill, `--on-accent` text, glow, min 48px; hover lifts 1px,
  active presses 1px. **Secondary:** glass pill, ink text. Both: 2px accent focus ring,
  3px offset.
- **Glass panel:** recipe above. Holds facts, project rows, experience, contact.
- **Project row:** 3 auto-fit columns (name + domain / description / status + tools) inside
  one panel; hover fills `--glass-strong` and turns the name accent.
- **Status pill:** mono; Automated = `--pass` on a green tint, Manual = `--soft` on
  `--glass-strong`.
- **Roadmap card:** glass card, mono step number and status; the current step adds a 1.5px
  accent ring.
- **Contact tile:** `--glass` fill with a hairline (not blurred), mono label over the value; hover fills `--glass-strong` and lifts 2px.
- **Locator lens:** 1.5px accent border, `--lens` wash, `saturate(180%)` (no blur: it
  smeared the text under it), tag in an accent pill with a green ✓ badge. The tag text comes from `data-loc` via CSS so it is never page text;
  `tests/test_site.py` runs each locator in Playwright strict mode.
