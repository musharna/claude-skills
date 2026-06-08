---
name: grounded-quote-or-decline
description: Use when about to assert a fact that came from a source — paper, doc, code, transcript, prior chat, training-data recall. The per-claim grounding ritual for any skill or workflow that produces load-bearing prose. Each substantive claim either ships with a verbatim quote tied to a locatable source, or is declined (rewritten as "unknown" / cut entirely). No paraphrase-without-quote in load-bearing prose.
---

# Grounded quote or decline

The rule. Every substantive factual claim in load-bearing prose ships in one of two states:

1. **Grounded** — paired with a verbatim quote (≤25 words) AND a locatable source pointer (DOI, file:line, URL+anchor, transcript+timestamp).
2. **Declined** — explicitly marked "unknown" / "couldn't verify" / cut from the artifact.

There is no third state. Paraphrase-without-quote is not allowed in load-bearing prose. "I recall X" is not grounding. "Per general knowledge" is not grounding. If you can't produce the quote, decline the claim.

## What counts as load-bearing prose

- Audit memos, RFCs, wiki pages, background sections, synthesis docs, citations.
- Any place future-you (or another agent) will re-cite the claim.
- Inline code comments asserting WHY (not WHAT) — if the WHY came from a source, it needs a pointer.

**Not** load-bearing: brainstorming scratch, conversational replies, exploration. Apply the ritual when you're about to _ship_ the prose, not while you're thinking.

## The ritual (run for each substantive claim)

1. **Name the claim** in one sentence. If it has two claims joined by "and", split them and ritual each separately.
2. **Locate the source.** Where did this come from? If you can't name a specific source, the claim is unsourced — go to step 5.
3. **Pull the verbatim quote** that supports the claim. ≤25 words. If the quote is longer, the claim is too broad — narrow it.
4. **Check the quote actually supports the claim.** A common failure mode is quote-claim drift: the quote is real, the claim sounds related, but the quote doesn't actually establish what the claim asserts. Re-read both side by side.
5. **Decide:**
   - Steps 1-4 all passed → ship the claim with `quote + pointer` inline or in a footnote.
   - Step 2 failed → decline (rewrite as "unknown" or cut).
   - Step 3 failed → decline (can't be supported at this granularity).
   - Step 4 failed → decline (the source doesn't say this).

## Source pointer formats

| Source type | Pointer format                                     |
| ----------- | -------------------------------------------------- |
| Paper       | `Author Year, DOI:10.xxxx/yyyy` (verify w/ Zotero) |
| Code        | `path/to/file.py:42`                               |
| Doc / RFC   | `path/to/doc.md#section-anchor`                    |
| URL         | `https://… (accessed YYYY-MM-DD)`                  |
| Transcript  | `session-id.jsonl@<timestamp or msg-N>`            |
| Prior chat  | `[[memory-name]]` + verbatim quote from the memo   |

For papers, a citation-audit chain — your reference manager → PubMed/DOI → CrossRef author+year cross-check — is the ground truth. Ghost citations (right DOI, wrong author/year) are the dominant failure mode; the [`ghostcite`](https://github.com/musharna/ghostcite) CLI does this check deterministically.

## Composes with

- **causal-vs-bandaid** (sibling in this plugin) — when stating a root cause, the cause-claim is load-bearing prose and gets ritual'd.
- **Literature-synthesis workflows** — run every claim in the synthesis through this ritual before shipping the prose.
- **Fetch-and-quote workflows** — when the quote source is reachable via an MCP tool (stored fulltext, an abstract API, etc.), pull the verbatim quote directly rather than paraphrasing from memory.

## Red flags (decline immediately)

- "I recall that..." / "I believe..." / "as I remember..."
- "Per general knowledge..." / "It's well known that..."
- "The literature shows..." with no specific paper named
- "The code does X" without a `file:line` pointer
- "The user said X earlier" without a session-id + msg-N reference

If you catch yourself writing any of these in load-bearing prose, stop and run the ritual.

## What this skill is NOT

- Not a substitute for the citation audit chain — for papers, still verify Zotero → DOI → CrossRef.
- Not a license to over-quote — ≤25 words per quote keeps the prose readable. Long blockquotes mean the claim is too coarse.
- Not for casual replies — apply only when prose is load-bearing.
