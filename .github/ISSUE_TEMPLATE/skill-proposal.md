---
name: Skill proposal
about: Propose a new reasoning-discipline skill for this plugin
title: "[skill] "
labels: skill-proposal
---

## What default failure mode does this skill counter?

<!-- One or two sentences. These are reasoning-discipline guides, not project tooling. -->

## When should it fire?

<!-- The trigger is the frontmatter `description`. Be specific about WHEN the skill
should activate (and, ideally, when it should NOT). -->

## Checklist

- [ ] It lives as a directory under `skills/` with a `SKILL.md` carrying YAML
      frontmatter: a `name` and a specific `description` (the trigger).
- [ ] It is general — no personal paths, machine names, private project names,
      library IDs, emails, or IP addresses. Useful to someone who has never seen
      my setup.
- [ ] `python3 scripts/validate_plugin.py` prints `OK`.
- [ ] (Optional) An `eval-triggers.json` with labeled should-trigger / should-not
      cases for the new skill.
