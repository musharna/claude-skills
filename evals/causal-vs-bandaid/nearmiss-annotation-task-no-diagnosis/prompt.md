---
description: "eval-triggers.json near-miss:annotation-task-no-diagnosis (should_trigger=false)"
tags: [causal-vs-bandaid, near-miss]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Add type hints to all the public functions in utils.py.

```python
# utils.py
def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]

def slugify(text, sep="-"):
    return sep.join(text.lower().split())

def _private_helper(x):
    return x * 2
```
