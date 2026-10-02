---
description: "eval-triggers.json fix-flow:issue-is-plus-fix-would-be (should_trigger=true)"
tags: [causal-vs-bandaid, should-trigger, fix-flow]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm debugging a problem in our service. The issue is the timeout being too short; the fix would be to bump it to 30s. Does that sound right, and what's the next step?
