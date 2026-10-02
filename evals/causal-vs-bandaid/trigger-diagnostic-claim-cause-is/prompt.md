---
description: "eval-triggers.json diagnostic-claim:cause-is (should_trigger=true)"
tags: [causal-vs-bandaid, should-trigger, diagnostic-claim]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm debugging a problem in our service. The cause is that the lock is being released before the commit completes. Does that sound right, and what's the next step?
