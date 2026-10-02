---
description: "eval-triggers.json fix-flow:bug-is (should_trigger=true)"
tags: [causal-vs-bandaid, should-trigger, fix-flow]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm debugging a problem in our service. The bug is in the retry loop - it doesn't reset the backoff timer on success. Does that sound right, and what's the next step?
