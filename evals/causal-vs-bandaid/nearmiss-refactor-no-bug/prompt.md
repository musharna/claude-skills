---
description: "eval-triggers.json near-miss:refactor-no-bug (should_trigger=false)"
tags: [causal-vs-bandaid, near-miss]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Refactor this module to use dataclasses instead of dicts.

```python
def make_user(name, email):
    return {"name": name, "email": email, "active": True}

def deactivate(user):
    user["active"] = False
    return user

def display(user):
    return f"{user['name']} <{user['email']}>"
```
