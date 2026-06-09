# claude-skills

Three general-purpose **rigor skills** for agentic coding in [Claude Code](https://claude.com/claude-code) — packaged as an installable plugin.

[![validate](https://github.com/musharna/claude-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/musharna/claude-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

These are reasoning-discipline skills, not domain tools. Each one counters a specific
default failure mode of an LLM agent: jumping to a fix before finding the cause,
asserting facts it can't ground, and burning tokens on raw browser screenshots.

## Install

```
/plugin marketplace add musharna/claude-skills
/plugin install claude-skills@musharna-claude-skills
```

Claude Code will load the three skills and invoke them automatically when their
trigger conditions match (or you can invoke one by name).

## The skills

### causal-vs-bandaid

Fires before you state a root cause or propose a fix. Forces a 3-hypothesis gate
(enumerate three candidate mechanisms before naming one), a one-sentence causal
chain, and a "mechanism test" that distinguishes a real fix from a tripwire
removal that leaves the bug's mechanism intact. Counters the pull toward the
smallest-scope patch that makes the test pass.

<details><summary>Example</summary>

> Symptom: requests intermittently 500 after a deploy.
> **H1 (cache):** stale config cached past TTL. For: timing lines up with restarts. Against: errors persist past one TTL.
> **H2 (migration):** new column nullable, code assumes non-null. For: stack trace hits that field. Against: only some rows.
> **H3 (connection pool):** pool sized below worker count, exhaustion under load. For: errors cluster at peak. Against: pool metrics look idle.
> Going with **H2** — discriminator: failing requests all touch rows written before the migration. Fix corrects the column default at the schema layer, not a null-guard at the call site.

</details>

### grounded-quote-or-decline

Fires when you're about to assert a sourced fact in load-bearing prose (audit
memos, RFCs, wiki pages, citations). Every substantive claim either ships with a
verbatim quote tied to a locatable source, or is declined — there is no
paraphrase-without-quote third state. Pairs with the [`ghostcite`](https://github.com/musharna/ghostcite)
CLI for deterministic citation byline checks.

<details><summary>Example</summary>

> **Grounded:** "The default request timeout is 30s." → quote: _"`DEFAULT_TIMEOUT = 30  # seconds`"_ — pointer: `src/client.py:12`.
> **Declined:** "The library was benchmarked at 40% faster than the alternative." → no source located; rewritten as "Relative performance vs the alternative is unverified" (or cut).

</details>

### playwright-token-budget

Fires before driving the Playwright MCP. Encodes the five quantitative DOM-serializer
rules from [`browser-use`](https://github.com/browser-use/browser-use) that cut a
typical page from ~150k tokens to ~1.5k — default to the accessibility tree, not
screenshots; drop non-content and decorative nodes; select interactive elements only.

<details><summary>Example</summary>

> Task: click the "Checkout" button.
> **Tempting:** `browser_take_screenshot` (full page) to "see" the layout → ~30k tokens, opaque.
> **Routed:** `browser_snapshot` → a11y tree lists `button "Checkout" [ref=e42]` in ~2k tokens → click `e42` directly.
> Screenshot only if the deliverable is the picture itself, and then with `fullPage: false` + a narrow `element` selector.

</details>

## Companion

[`musharna/fresh-read-guard`](https://github.com/musharna/fresh-read-guard) — hooks
that enforce read-before-write, a complementary discipline at the harness level.

## Validating / contributing

`python3 scripts/validate_plugin.py` checks the manifests and skill frontmatter.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
