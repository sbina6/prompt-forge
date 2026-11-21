"""Shared helpers: read and validate a skill's SKILL.md.

Used by the checks in tests/ and by tools/package_skill.py. Standard library only;
PyYAML is used when it is installed and a small built-in parser is the fallback.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "skill" / "prompt-forge"
SKILL_MD = SKILL_DIR / "SKILL.md"
VERSION_FILE = REPO / "VERSION"

# Keys the Claude apps accept when a skill is uploaded. Any other key is rejected there,
# even though Claude Code itself ignores unknown keys.
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
MAX_DESCRIPTION = 1024
MAX_NAME = 64
MAX_LINES = 500


def read_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_text, body). Raises ValueError when there is no frontmatter."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("SKILL.md must start with a YAML frontmatter block between --- lines")
    return match.group(1), text[match.end():]


def _mini_yaml(src: str) -> dict:
    """Parse the small YAML subset this repo uses: scalars, folded or literal blocks, one-level maps."""
    data: dict = {}
    lines = src.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            raise ValueError(f"unexpected indentation in frontmatter: {line!r}")
        key, sep, rest = line.partition(":")
        if not sep:
            raise ValueError(f"cannot parse frontmatter line: {line!r}")
        key, rest = key.strip(), rest.strip()
        block = []
        j = i + 1
        while j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
            block.append(lines[j])
            j += 1
        if rest in (">", ">-", ">+", "|", "|-", "|+"):
            parts = [b.strip() for b in block]
            data[key] = (" " if rest.startswith(">") else "\n").join(p for p in parts if p).strip()
        elif rest == "" and block:
            sub = {}
            for b in block:
                if not b.strip():
                    continue
                k, s, v = b.strip().partition(":")
                if not s:
                    raise ValueError(f"cannot parse nested frontmatter line: {b!r}")
                sub[k.strip()] = v.strip().strip("\"'")
            data[key] = sub
        else:
            data[key] = rest.strip("\"'")
            j = i + 1
        i = j
    return data


def parse_frontmatter(src: str) -> tuple[dict, str]:
    """Return (data, parser_name)."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return _mini_yaml(src), "built-in parser"
    data = yaml.safe_load(src)
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, "PyYAML"


def read_skill(path: Path = SKILL_MD) -> tuple[dict, str, str]:
    """Return (frontmatter, body, parser_name) for a SKILL.md file."""
    text = path.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(text)
    data, parser = parse_frontmatter(fm_text)
    return data, body, parser


def validate_frontmatter(data: dict, folder_name: str) -> list[str]:
    """Return a list of problems; an empty list means the skill can be uploaded."""
    problems = []
    extra = set(data) - ALLOWED_KEYS
    if extra:
        problems.append(f"frontmatter keys not accepted on upload: {sorted(extra)}")
    name = str(data.get("name", "")).strip()
    if not name:
        problems.append("missing name")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > MAX_NAME:
        problems.append(f"name must be kebab-case and at most {MAX_NAME} characters: {name!r}")
    elif name != folder_name:
        problems.append(f"name {name!r} must match the folder name {folder_name!r}")
    desc = " ".join(str(data.get("description", "")).split())
    if not desc:
        problems.append("missing description")
    if len(desc) > MAX_DESCRIPTION:
        problems.append(f"description is {len(desc)} characters; the limit is {MAX_DESCRIPTION}")
    if "<" in desc or ">" in desc:
        problems.append("description must not contain angle brackets")
    meta = data.get("metadata")
    if meta is not None and not isinstance(meta, dict):
        problems.append("metadata must be a mapping")
    return problems


def words(text: str) -> int:
    return len(text.split())
