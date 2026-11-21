"""Build the installable zip: dist/prompt-forge-<version>.zip.

The zip holds one folder, prompt-forge/, with SKILL.md inside it. That is the layout the
Claude apps expect when a skill is uploaded.

Run from anywhere:  python tools/package_skill.py
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_meta as sm  # noqa: E402

EXCLUDE_NAMES = {".DS_Store"}
EXCLUDE_DIRS = {"__pycache__", "node_modules", "evals"}


def main() -> int:
    data, _body, _parser = sm.read_skill()
    problems = sm.validate_frontmatter(data, sm.SKILL_DIR.name)
    version = sm.read_version()
    if str((data.get("metadata") or {}).get("version", "")) != version:
        problems.append("metadata.version in SKILL.md does not match the VERSION file")
    if problems:
        for problem in problems:
            print(f"cannot package: {problem}")
        return 1

    dist = sm.REPO / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / f"{sm.SKILL_DIR.name}-{version}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(sm.SKILL_DIR.rglob("*")):
            rel = path.relative_to(sm.SKILL_DIR.parent)
            if not path.is_file() or path.name in EXCLUDE_NAMES or EXCLUDE_DIRS & set(rel.parts):
                continue
            archive.write(path, rel.as_posix())
            print(f"added {rel.as_posix()}")
    print(f"wrote {target.relative_to(sm.REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
