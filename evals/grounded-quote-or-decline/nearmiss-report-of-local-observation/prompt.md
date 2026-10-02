---
description: "eval-triggers.json near-miss:report-of-local-observation (should_trigger=false)"
tags: [grounded-quote-or-decline, near-miss]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I ran the test suite. Tell me which tests fail.

```
$ python3 -m pytest -q
..F...F.
FAILED tests/test_io.py::test_roundtrip - AssertionError: b'a' != b'b'
FAILED tests/test_cli.py::test_help_exit_code - assert 2 == 0
2 failed, 6 passed in 0.41s
```

