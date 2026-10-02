---
description: "eval-triggers.json near-miss:style-only-edit (should_trigger=false)"
tags: [grounded-quote-or-decline, near-miss]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Reformat this paragraph to use shorter sentences, don't change any facts:

The nightly job, which was introduced in March after the old cron setup kept silently failing whenever the disk filled up, now writes its logs to a rotating file and sends a summary email to the on-call engineer, who is expected to acknowledge it before 9 a.m.

