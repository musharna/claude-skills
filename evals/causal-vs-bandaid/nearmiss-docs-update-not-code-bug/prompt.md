---
description: "eval-triggers.json near-miss:docs-update-not-code-bug (should_trigger=false)"
tags: [causal-vs-bandaid, near-miss]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

The README is out of date; can you update it to reflect the new CLI flags?

Current README usage section:

```
## Usage
    mytool --input FILE [--verbose]
```

The CLI now accepts `--input FILE`, `--output DIR` (default `./out`), `--quiet` (replaces `--verbose`, which was removed), and `--jobs N` (default 1).
