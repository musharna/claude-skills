---
name: causal-vs-bandaid
description: Use BEFORE stating any root cause OR proposing any bug fix or behavior change. Triggers on diagnostic-claim keywords ("the cause is", "this was caused by", "the root cause is", "X is happening because", "this is because", "what's happening is") AND fix-flow keywords ("the bug is", "the issue is", "the fix would be", "to fix this"), AND when about to write code that adds a guard, special-case, mode flag, predicate change, or "when X also do Y" branch. Forces the 3-hypothesis gate, root-cause naming, and the mechanism test before any cause is asserted or patch proposed.
---

# Causal fixes over band-aids

Default reasoning pulls toward the smallest-scope patch that makes the failing test pass. This skill counters that pull. Run it BEFORE proposing any fix to the user, not after the user pushes back.

## The 3-hypothesis gate (run BEFORE stating a cause)

Before asserting "X is happening because Y", enumerate at least three candidate hypotheses with discriminating evidence:

1. **Hypothesis 1 (current best guess):** <one-line mechanism>. Evidence for: <X>. Evidence against: <Y>.
2. **Hypothesis 2 (adjacent mechanism):** <one-line>. Evidence for. Evidence against.
3. **Hypothesis 3 (orthogonal mechanism class):** <one-line>. Evidence for. Evidence against.

Then state which one you're going with AND the discriminator that ruled the others out.

**Why three:** one hypothesis is a guess. Two is confirmation bias — the alternative exists to be dismissed. Three forces a real search across mechanism _classes_ (pairs with the two-revert reframe and the leak-direction probe — same anti-pattern, different surface).

**When you can skip:** the cause is observable directly — stack trace points at the line, query log shows the row count, file mtime confirms the staleness. Skip is allowed; "I'm pretty sure" is not. If you find yourself rationalizing skip ("this one is obvious"), the rationalization is the bust signal — enumerate.

**Red flags that you skipped:**

- Single-hypothesis statement followed by a fix proposal in the same turn.
- "The cause is X" with no "I considered Y but ruled it out because Z".
- Diagnostic names the layer of the _symptom_ (where it appeared) rather than the _mechanism_ (where it originated).

**Reference incident (an out-of-memory crash during parallel work).** Asserted "OOM from parallel fork bloat" as the cause; the user pushed back: "how sure are you of the cause? Seems like you have little evidence." Three live hypotheses existed (fork copy-on-write bloat, a separate desktop-manager crash, and host memory pressure from concurrent processes). The wrong one was named first because no enumeration happened.

## The rule

State the causal chain in one sentence:

> "Symptom X happens because Y is wrong at layer Z."

Then ask:

> "Does my proposed fix _remove_ Y, or does it _add code that works around_ Y's effects?"

If the causal fix is materially larger than the band-aid, **present `causal fix: <scope>` vs `band-aid: <scope>` as a tradeoff to the user** — do not silently default to the smaller fix.

## Red flags (the proposed fix is a band-aid)

- Adds a new special-case, guard, state flag, or mode
- Lives in a different file/layer than the root cause
- Description reads "when X, also do Y" rather than "Y was wrong, corrected"
- Grows the system: more branches, more modes, more special-cases

## Positive signals (necessary but NOT sufficient — must also pass the mechanism test below)

- Deletes code
- Unifies two existing special-cases into one
- Corrects a predicate, invariant, or constant at the layer where it's defined

## The mechanism test (primary check — overrides positive signals)

After applying the fix, does the root-cause **mechanism** still exist somewhere in the system, even if no current code path trips on it?

- **Yes** → the fix is a **tripwire removal**, not a mechanism removal. A future consumer of the bad signal will re-trip the same bug. Look one layer deeper.
- **No** → the fix removes the mechanism. Safe.

Deleting a branch is **not automatically causal**: if the branch is _consuming_ a bad signal rather than _producing_ one, deleting it leaves the bad signal intact. Real causal fixes remove the bad signal, the wrong model, or the accidental coupling — not just the current consumer of it.

## The model-first reframe (breaks edit-minimization bias)

When stuck in "smallest edit to stop the symptom" mode, ask:

> "What's the **correct model** here?"

— rather than:

> "What's the minimum change?"

For domain problems with real-world analogues (biology, physics, well-studied games, established protocols), ask:

> "How does nature / the genre / a reference implementation actually solve this?"

That framing bypasses edit-scope bias and typically surfaces the true causal layer. **Run this BEFORE proposing the fix, not after the user prompts it.**

## Workflow at the diagnostic-to-fix transition

1. **Run the 3-hypothesis gate** (above). Enumerate three candidates + discriminator before naming a cause.
2. State the root cause in one sentence (the causal chain).
3. Run the model-first question: "what's the correct model for this subsystem?" If biology / physics / prior art has an answer, use it.
4. Name the proposed fix's scope and layer.
5. Run the mechanism test: after this fix, could a future feature trip the same bug? If yes, look deeper.
6. Surface the fix to the user, alongside alternatives at other layers if scope differs materially. Let the user pick.

## Why this skill exists

Symptom patches compound — each adds a special-case that the next bug has to reason around. The "deletes code" positive signal is a trap: deletion of a branch that consumes a bad signal looks causal but leaves the mechanism intact, so the next feature built on that signal reintroduces the bug.

Pattern has recurred across multiple diagnostic sessions. Without the skill, the user has had to redirect from a partial-causal fix to the mechanism-removal fix repeatedly, and the model-first reframe almost always came from a user prompt rather than internal practice.

## Reference incident

**Pheromone-homing in an ant-colony simulation.** First proposed fix: a shaft-specific descent bias (new mode — band-aid, rejected). Second: narrow a gravity predicate I incorrectly believed was wrong — implementer correctly stopped because the predicate was already right. Third: gate FOLLOW_HOME state-transition on `!carrying`; called causal because it deleted a branch.

That third fix was a **tripwire removal**: the real mechanism — pher_home saturating at the shaft mouth because (a) non-carrying ants dynamically deposit it as a global gradient, and (b) the nest spawn colocates with the shaft column — was still in place. Any future consumer of pher_home would trip the same accidental-geometry bug.

The mechanism-removal fix came from the user's prompt: "how would real biology do this?" Real ants use path integration for long-range homing and recognize the nest entrance as a short-range olfactory landmark, not a global gradient. Reframing pher_home from "deposited by walking ants across the world" to "emitted by the entrance cell as a local landmark" (matching the queen/brood emitter pattern that already exists) removes the mechanism entirely — pher_home's peak is bounded by emission rate + decay at a single spatial point, so saturation at the shaft mouth cannot arise.

The model-first question should be the default, not the user's prompt.
