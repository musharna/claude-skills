---
name: playwright-token-budget
description: Use BEFORE driving the Playwright MCP for any browser-interaction task — keeps DOM/snapshot payloads under control by preferring the accessibility tree over raw screenshots, filtering noise, and applying the 5 quantitative rules browser-use's serializer uses to hit a ~99% token reduction on real pages.
---

# Playwright token budget

The Playwright MCP can return three kinds of page state: full PNG screenshots (huge, opaque to the LLM), the accessibility tree via `browser_snapshot` (compact, structured), and arbitrary `browser_evaluate` payloads. Token cost dominates browser-driving sessions when the default impulse is "screenshot first" — a single 1080p screenshot is ~30k tokens of base64 + a 1000-line a11y dump, and most pages only need a handful of interactive elements.

This skill enforces the token discipline that `browser-use` arrived at empirically (their serializer reduces a typical e-commerce page from ~150k DOM tokens to ~1.5k a11y-filtered tokens — the "99% reduction" claim).

## When this skill applies

Any time you're about to call one of:

- `mcp__plugin_playwright_playwright__browser_snapshot` (decide what to ask for)
- `mcp__plugin_playwright_playwright__browser_take_screenshot` (default-deny unless visual is the deliverable)
- `mcp__plugin_playwright_playwright__browser_evaluate` (don't dump `document.body.outerHTML`)

You do NOT need this skill for `browser_navigate`, `browser_click`, `browser_type` — those don't carry payloads in the response.

## Default routing

| Goal                                                          | Default tool                                                                     | Why                                                |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| Find an interactive element to click/type                     | `browser_snapshot`                                                               | a11y tree already does rules 1, 2, 5 natively      |
| Verify a piece of text is visible                             | `browser_snapshot` + grep                                                        | text nodes are in the a11y dump                    |
| Capture visual evidence for the user (screenshot deliverable) | `browser_take_screenshot` with `fullPage: false` and a narrow `element` selector | full-viewport only when the user wants the picture |
| Pull a specific value (price, count) from a known selector    | `browser_evaluate` returning ONLY the value                                      | never return the whole element / outerHTML         |
| Diagnose layout / paint-order bug                             | screenshot + a11y, in that order                                                 | rule 4 (paint-order) needs pixels                  |

If you're tempted to screenshot "just to see what's on the page," `browser_snapshot` first. Re-evaluate after reading the a11y dump.

## Quantitative rules (browser-use lift)

The five rules below are lifted from `browser-use/browser-use` commit `157779338afdcc03023010ec3c24ad63d820453c`, file `browser_use/dom/serializer/serializer.py`. They are the filters that get the 99% reduction. The Playwright MCP a11y snapshot already applies some of them natively; others need caller-side post-processing.

### Rule 1: Drop non-content elements

**Source:** `serializer.py:18` constant, applied at `serializer.py:461`.

```python
DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
```

**How to apply in Playwright MCP:** native — `browser_snapshot` returns an a11y tree which excludes these by construction (they have no accessible role). If you fall through to `browser_evaluate` and pull raw HTML, strip these tags explicitly:

```javascript
// in browser_evaluate
const el = document.querySelector("main");
el.querySelectorAll("style, script, head, meta, link, title").forEach((n) =>
  n.remove(),
);
return el.outerHTML;
```

### Rule 2: Drop SVG decorative children

**Source:** `serializer.py:21-38` constant, applied at `serializer.py:465`.

```python
SVG_ELEMENTS = {'path', 'rect', 'g', 'circle', 'ellipse', 'line', 'polyline', 'polygon',
                'use', 'defs', 'clipPath', 'mask', 'pattern', 'image', 'text', 'tspan'}
```

Decorative SVG children carry no interaction value but bloat any HTML dump. Icon-heavy pages (admin dashboards, e-commerce nav) can be 30-50% SVG by token count.

**How to apply in Playwright MCP:** mostly native — `browser_snapshot` a11y tree omits decorative SVG (only SVG with `role` or `aria-label` survives). For `browser_evaluate` raw-HTML calls, add `svg *` to the strip selector list.

### Rule 3: Drop children 99%-contained within an interactive ancestor's bounds

**Source:** `serializer.py:57` threshold (`DEFAULT_CONTAINMENT_THRESHOLD = 0.99`); containment check at `serializer.py:840-858`; usage at `serializer.py:799`.

When an `<a>`, `<button>`, or `[role="button"]` element's bounding box ≥99% contains a child's bounding box, the child is redundant for interaction purposes — clicking the child clicks the parent. Form controls (`input/select/textarea/label`) are exempted (line 812) because each one needs its own interaction.

**How to apply in Playwright MCP:** NOT native — Playwright's a11y tree doesn't do bbox-containment dedup. If you find yourself reasoning about which of several nested elements to click, prefer the outermost ancestor with the role you need. If you've already pulled a huge a11y dump and see clusters of redundant child elements under the same `<a href>`, that's the symptom — switch to a more specific selector at the parent level rather than enumerating children.

### Rule 4: Paint-order occlusion filter

**Source:** `serializer.py:65` flag, applied at `serializer.py:119-120` via `PaintOrderRemover`.

Elements painted over by later siblings (modal overlays, cookie banners, ad iframes) are not actually clickable. Including them in the LLM-facing snapshot wastes tokens AND invites clicks that won't fire.

**How to apply in Playwright MCP:** NOT native — Playwright's a11y tree includes occluded elements. Symptom: you call `browser_click` on an element that appears in the snapshot but the click doesn't take effect. Diagnosis: take ONE screenshot (`browser_take_screenshot` with `element: <selector>`) to confirm visual occlusion, then dismiss the overlay first (escape key via `browser_press_key`, or click the cookie-banner accept button) before the actual target click.

### Rule 5: Interactive-only selection

**Source:** `serializer.py:617-665` (`_assign_interactive_indices_and_mark_new_nodes`); detector at `browser_use/dom/serializer/clickable_elements.py:5` (`ClickableElementDetector.is_interactive`).

Only nodes that pass `is_interactive` (form controls, links, role-button, role-combobox, contenteditable, anything with a click handler in the snapshot, etc.) get assigned an index in the simplified tree. Pure text + layout divs are kept as context but get no handle.

**How to apply in Playwright MCP:** mostly native — `browser_snapshot` a11y tree only assigns `[ref=...]` handles to elements with an accessible role + name. If you find yourself trying to click a `<div>` with no role, you're almost certainly missing the actual interactive parent. Look one level up.

## What this skill is NOT

- **Not a hard cap on screenshots.** Visual evidence is sometimes the deliverable (user asks "what does the homepage look like?", a designer reviewing a mock, a bug report needing pixels). The discipline is _default to a11y_, not _never screenshot_.
- **Not a substitute for a real browser-use install.** If you find yourself routinely reimplementing the 99%-containment filter in `browser_evaluate`, the right move is to install the `browser-use` library directly (it ships the serializer as a Python package) — but route that decision through an explicit install-discipline check first (weigh the per-session cost of the new dependency before adding it).

## Why this exists

`mcp__plugin_playwright_playwright__browser_snapshot` returns the Playwright a11y tree in one shot. Without this skill, the default failure mode is: take a screenshot to "see" the page, then take a snapshot to find the element, then click. That's 3 tool calls and ~30k tokens for what should be 1 call and ~2k tokens. The browser-use project measured the cost of each filter rule on real pages; this skill carries the result so you don't have to rediscover it.
