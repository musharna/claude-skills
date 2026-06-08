# Contributing

Contributions and new skill proposals are welcome.

## Adding or editing a skill

1. Each skill is a directory under `skills/` containing a `SKILL.md` with YAML
   frontmatter: a `name` and a `description` (the description is the trigger — be
   specific about _when_ the skill should fire).
2. Skills are reasoning-discipline guides, not project-specific tooling. Keep them
   general: no personal paths, machine names, private project names, library IDs,
   emails, or IP addresses. The validator enforces generic hygiene; the bar for a
   merged skill is "useful to someone who has never seen my setup."
3. Run `python3 scripts/validate_plugin.py` — it must print `OK` before you open a PR.

## License

By contributing you agree your contribution is licensed under the MIT License.
