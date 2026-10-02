---
description: "eval-triggers.json diagnostic-claim:whats-happening (should_trigger=true)"
tags: [causal-vs-bandaid, should-trigger, diagnostic-claim]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm debugging a problem in our service. What's happening is the worker is exiting before the queue drains. Does that sound right, and what's the next step?
