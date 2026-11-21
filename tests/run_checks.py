"""Run every check in this folder and summarise the result.

Run from anywhere:  python tests/run_checks.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = ["check_skill.py", "check_examples.py", "check_links.py"]


def main() -> int:
    failed = []
    for name in CHECKS:
        print(f"\n===== {name} =====")
        result = subprocess.run([sys.executable, str(HERE / name)])
        if result.returncode != 0:
            failed.append(name)
    print("\n===== summary =====")
    for name in CHECKS:
        print(f"{'FAIL' if name in failed else 'PASS'}  {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
