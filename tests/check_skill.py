"""Mechanical checks on skill/prompt-forge/SKILL.md.

Run from anywhere:  python tests/check_skill.py
Exit code 0 means every check passed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import skill_meta as sm  # noqa: E402

CEILINGS = {"Micro": 150, "Small": 350, "Medium": 800, "Large": 1600}

ok = True


def report(label: str, passed: bool, detail: str = "") -> None:
    global ok
    ok = ok and passed
    print(f"[{'PASS' if passed else 'FAIL'}] {label}{(' — ' + detail) if detail else ''}")


def info(text: str) -> None:
    print(f"       {text}")


def main() -> int:
    text = sm.SKILL_MD.read_text(encoding="utf-8")
    version = sm.read_version()

    # --- frontmatter --------------------------------------------------------
    try:
        data, body, parser = sm.read_skill()
    except ValueError as err:
        report("frontmatter parses", False, str(err))
        return 1
    report("frontmatter parses", True, parser)
    problems = sm.validate_frontmatter(data, sm.SKILL_DIR.name)
    report("frontmatter is valid for upload", not problems, "; ".join(problems))
    desc = " ".join(str(data.get("description", "")).split())
    info(f"description: {len(desc)} of {sm.MAX_DESCRIPTION} characters")

    # --- version ------------------------------------------------------------
    meta_version = str((data.get("metadata") or {}).get("version", ""))
    report("metadata.version matches VERSION", meta_version == version, f"{meta_version!r} vs {version!r}")
    report("body states the version", f"version {version}" in body, f"looking for 'version {version}'")
    changelog_path = sm.REPO / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else ""
    report("CHANGELOG has an entry for this version", f"## [{version}]" in changelog)
    import release_notes  # in tools/, next to skill_meta

    report("release notes can be extracted for this version", bool(release_notes.notes(version)))
    stale = re.findall(r"\bv2\b|\bversion 2\b|prompt-forge-v2", text, re.I)
    report("no leftover 'v2' labels", not stale, str(stale) if stale else "")

    # --- shape and size -----------------------------------------------------
    skill_files = [p for p in sm.SKILL_DIR.rglob("SKILL.md")]
    report("exactly one SKILL.md in the skill folder", len(skill_files) == 1, str(len(skill_files)))
    lines = len(text.splitlines())
    report(f"under {sm.MAX_LINES} lines", lines < sm.MAX_LINES, f"{lines} lines")
    fences = len(re.findall(r"^```", text, re.M))
    report("code fences are balanced", fences % 2 == 0, f"{fences} fence lines")
    report("no tabs or trailing spaces", "\t" not in text and all(l == l.rstrip() for l in text.splitlines()))
    long_lines = [i + 1 for i, l in enumerate(text.splitlines()) if len(l) > 100 and not l.startswith("|")]
    report("prose lines are at most 100 characters", not long_lines, f"lines {long_lines}" if long_lines else "")

    # Claude Code keeps roughly the first 5,000 tokens of an invoked skill after it compacts
    # a long session, so the method has to come before the reference material.
    core_end = text.find("## Agent notes")
    est_total = len(text) // 4
    est_core = core_end // 4 if core_end > 0 else est_total
    info(f"estimated tokens: about {est_total} in total, about {est_core} before 'Agent notes' (4 characters per token)")
    report("the method sits before 'Agent notes'", core_end > 0)
    report("the method fits in roughly 5,000 tokens", est_core <= 5000, f"about {est_core}")

    # --- embedded examples respect their own ceilings -------------------------
    blocks = re.findall(r"```text\n(.*?)```", body, re.S)
    report("five fenced text blocks (skeleton and four examples)", len(blocks) == 5, str(len(blocks)))
    if len(blocks) == 5:
        micro, small = sm.words(blocks[1]), sm.words(blocks[2])
        report("embedded Micro example is within its ceiling", micro <= CEILINGS["Micro"], f"{micro} words")
        report("embedded Small example is within its ceiling", small <= CEILINGS["Small"], f"{small} words")

    # --- tone -----------------------------------------------------------------
    shouts = re.findall(r"\b(NEVER|ALWAYS|MUST|ONLY|CRITICAL|IMPORTANT|DO NOT)\b", body)
    allowed = {"CRITICAL": 1}  # quoted once, as a thing to avoid
    bad = sorted(s for s in set(shouts) if shouts.count(s) > allowed.get(s, 0))
    report("no shouted mandates", not bad, str(bad) if bad else "")

    # --- the parts that make the skill what it is -----------------------------
    needles = {
        "five steps": ["## 1. Route", "## 2. Scope", "## 3. Size", "## 4. Shape", "## 5. Write"],
        "scope ledger": ["**Asked**", "**Needed**", "**Extras**"],
        "four tiers": ["| Micro |", "| Small |", "| Medium |", "| Large |"],
        "six loop kinds": ["| Fix |", "| Refine |", "| Queue |", "| Coverage |", "| Long-run |", "| Watch |"],
        "loop anatomy": ["**check**", "**exit**", "**cap**", "**where state lives**"],
        "four delegation tests": ["**Parallel tracks**", "**Heavy reading**", "**Fresh eyes**", "**Fan-out**"],
        "six-part delegation block": [
            "**The split**", "**The brief**", "**The return**", "**The run**", "**The merge**", "**The fallback**",
        ],
        "write, cut, test, deliver": ["### Write", "### Cut", "### Test", "### Deliver"],
        "agent notes and fix table": ["## Agent notes", "## Fixing an existing prompt", "| Symptom |"],
    }
    for label, keys in needles.items():
        missing = [k for k in keys if k not in body]
        report(label, not missing, f"missing {missing}" if missing else "")

    info(f"SKILL.md: {lines} lines, {sm.words(text)} words")
    print("\nRESULT:", "ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
