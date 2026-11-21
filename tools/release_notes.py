"""Print the release notes for the current version: its section of CHANGELOG.md.

Run from anywhere:  python tools/release_notes.py
The release workflow uses the output as the text of the GitHub release.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_meta as sm  # noqa: E402


def notes(version: str) -> str:
    """Return the changelog section for a version, without its heading. Empty if there is none."""
    changelog = (sm.REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", changelog, re.S | re.M)
    return match.group(1).strip() if match else ""


def main() -> int:
    version = sm.read_version()
    body = notes(version)
    if not body:
        print(f"CHANGELOG.md has no section for version {version}", file=sys.stderr)
        return 1
    # Links in the changelog are relative to the repository root; a release page needs them absolute.
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repository = os.environ.get("GITHUB_REPOSITORY", "sbina6/prompt-forge")
    base = f"{server}/{repository}/blob/v{version}"
    body = re.sub(r"\]\((?!https?://)([^)#][^)]*)\)", rf"]({base}/\1)", body)
    print(body)
    print()
    print(
        f"**Install:** download `prompt-forge-{version}.zip` below and follow "
        f"[docs/INSTALL.md]({base}/docs/INSTALL.md)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
