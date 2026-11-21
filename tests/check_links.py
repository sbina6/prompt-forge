"""Check that every relative link in the repository's Markdown files points at something that exists.

Run from anywhere:  python tests/check_links.py

Checked: links to files and folders in this repository, and links to headings (anchors) in
Markdown files. Not checked: web links, which are not fetched.
The archived version 1.0 skill files are skipped because they are kept exactly as they were.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", "dist", "__pycache__"}


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code, where link syntax is only an illustration."""
    text = re.sub(r"^(`{3,})[^\n]*\n.*?^\1[^\n]*$", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def slug(heading: str) -> str:
    """Approximate the anchor GitHub generates for a heading."""
    heading = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)  # keep link text only
    heading = heading.replace("`", "").strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading)
    return heading.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    text = re.sub(r"^(`{3,})[^\n]*\n.*?^\1[^\n]*$", "", path.read_text(encoding="utf-8"), flags=re.S | re.M)
    for match in re.finditer(r"^#{1,6}\s+(.*?)\s*$", text, re.M):
        base = slug(match.group(1))
        candidate, n = base, 0
        while candidate in found:  # GitHub numbers repeated headings: name, name-1, name-2
            n += 1
            candidate = f"{base}-{n}"
        found.add(candidate)
    return found


def main() -> int:
    broken = []
    files = anchors_checked = 0
    for path in sorted(REPO.rglob("*.md")):
        rel = path.relative_to(REPO)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.parts[0] == "archive" and path.name != "README.md":
            continue  # the archived skill files are kept exactly as they were
        for target in LINK.findall(strip_code(path.read_text(encoding="utf-8"))):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue  # a web link or mailto
            file_part, _, anchor = target.partition("#")
            dest = (path.parent / file_part).resolve() if file_part else path
            files += 1
            if not dest.exists():
                broken.append(f"{path.relative_to(REPO)} -> {target} (no such file)")
                continue
            if anchor and dest.suffix == ".md":
                anchors_checked += 1
                if anchor not in anchors(dest):
                    broken.append(f"{path.relative_to(REPO)} -> {target} (no such heading)")
    for item in broken:
        print(f"[FAIL] broken link: {item}")
    status = "PASS" if not broken else "FAIL"
    print(f"[{status}] {files} relative links checked, {anchors_checked} of them to headings, {len(broken)} broken")
    print("\nRESULT:", "ALL PASS" if not broken else "SOME FAILED")
    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
