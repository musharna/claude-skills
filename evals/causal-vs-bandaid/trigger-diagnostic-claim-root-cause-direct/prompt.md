---
description: "eval-triggers.json diagnostic-claim:root-cause-direct (should_trigger=true)"
tags: [causal-vs-bandaid, should-trigger, diagnostic-claim]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm debugging a problem in our service. The root cause is the cache TTL expiring while the request is still in-flight. Does that sound right, and what's the next step?
