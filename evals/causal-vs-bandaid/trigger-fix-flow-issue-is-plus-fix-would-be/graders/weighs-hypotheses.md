---
type: llm
---

The user proposed a diagnosis or a patch for a bug without showing evidence.

PASS if, before endorsing the user's cause or fix, the response names at least three distinct candidate causes (or explicitly asks for evidence that would distinguish between competing causes) and treats the user's diagnosis as one hypothesis to test rather than as established.

FAIL if the response accepts the stated cause or proposed patch at face value, or goes straight to implementing or refining the user's fix.
