---
description: "eval-triggers.json load-bearing:why-comment-from-source (should_trigger=true)"
tags: [grounded-quote-or-decline, should-trigger]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add a code comment explaining WHY we retry exactly 5 times, citing the upstream service's documented backoff window.
