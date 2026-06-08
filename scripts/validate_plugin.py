#!/usr/bin/env python3
"""Validate the claude-skills plugin: manifests parse, skills have frontmatter,
no obvious local-machine hygiene leaks. GENERIC patterns only — the private-term
scrub is a separate local gate, never committed."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS = []


def err(msg):
    ERRORS.append(msg)


def check_manifests():
    mp = ROOT / ".claude-plugin" / "marketplace.json"
    pj = ROOT / ".claude-plugin" / "plugin.json"
    for f in (mp, pj):
        if not f.exists():
            err(f"missing manifest: {f.relative_to(ROOT)}")
            continue
        try:
            json.loads(f.read_text())
        except json.JSONDecodeError as e:
            err(f"invalid JSON in {f.relative_to(ROOT)}: {e}")
    if pj.exists():
        data = json.loads(pj.read_text())
        for key in ("name", "description", "version", "license"):
            if not data.get(key):
                err(f"plugin.json missing/empty key: {key}")
        skills_dir = data.get("skills", "./skills/").lstrip("./").rstrip("/")
        if not (ROOT / skills_dir).is_dir():
            err(f"plugin.json skills path does not resolve: {skills_dir}")


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    fields = {}
    for line in block.splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def check_skills():
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        err("no skills/*/SKILL.md found")
    for sk in skills:
        fm = parse_frontmatter(sk.read_text())
        rel = sk.relative_to(ROOT)
        if fm is None:
            err(f"{rel}: missing YAML frontmatter")
            continue
        if not fm.get("name"):
            err(f"{rel}: frontmatter missing 'name'")
        if not fm.get("description"):
            err(f"{rel}: frontmatter missing 'description'")


HYGIENE = [
    (re.compile(r"/home/[a-z]"), "absolute home path"),
    (re.compile(r"/mnt/c/Users/"), "Windows mount path"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "email address"),
    (re.compile(r"\b100\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "Tailscale/CGNAT IP"),
]


def check_hygiene():
    for f in ROOT.rglob("*"):
        if not f.is_file():
            continue
        if any(part in (".git", "docs") for part in f.relative_to(ROOT).parts):
            continue
        if f.name == "validate_plugin.py":
            continue
        try:
            text = f.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for pat, label in HYGIENE:
            if pat.search(text):
                err(f"{f.relative_to(ROOT)}: hygiene hit ({label})")


def main():
    check_manifests()
    check_skills()
    check_hygiene()
    if ERRORS:
        print("VALIDATION FAILED:")
        for e in ERRORS:
            print(f"  - {e}")
        return 1
    print("validate_plugin.py: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
