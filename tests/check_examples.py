"""Hold the prompts in examples/ to the skill's own rules.

Each example file starts with a comment such as
    <!-- example: tier=Medium loop=coverage delegates=yes review=no -->
and contains the forged prompt in its first ````text block.

Run from anywhere:  python tests/check_examples.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import skill_meta as sm  # noqa: E402

CEILINGS = {"Micro": 150, "Small": 350, "Medium": 800, "Large": 1600}
DONE_RANGE = {"Micro": (1, 2), "Small": (2, 4), "Medium": (4, 7), "Large": (6, 10)}

ok = True


def report(label: str, passed: bool, detail: str = "") -> None:
    global ok
    ok = ok and passed
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}{(' — ' + detail) if detail else ''}")


def section(text: str, name: str) -> str:
    match = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1) if match else ""


def load_example(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    meta_match = re.match(r"<!-- example: (.*?) -->", text)
    prompt_match = re.search(r"^````text\n(.*?)\n````", text, re.S | re.M)
    if not meta_match or not prompt_match:
        raise ValueError(f"{path.name}: needs an '<!-- example: ... -->' line and a ````text block")
    meta = dict(pair.split("=", 1) for pair in meta_match.group(1).split())
    return meta, prompt_match.group(1)


def check_example(path: Path) -> None:
    meta, prompt = load_example(path)
    tier, loop = meta["tier"], meta["loop"]
    low = prompt.lower()
    n = sm.words(prompt)
    print(f"\n{path.name}  ({tier}, {n} words)")
    report(f"within the {tier} ceiling of {CEILINGS[tier]}", n <= CEILINGS[tier], str(n))

    shouts = re.findall(r"\b(NEVER|ALWAYS|MUST|ONLY|CRITICAL|IMPORTANT|DO NOT|STOP)\b", prompt)
    report("no shouted mandates", not shouts, str(shouts) if shouts else "")
    stacked = [p for p in ("double-check", "double check", "re-verify", "verify again", "triple-check") if p in low]
    report("no stacked verification", not stacked, str(stacked) if stacked else "")

    if tier == "Micro":
        report("plain paragraph, no headings", "#" not in prompt)
        report("asks for the output to be shown", "show me" in low)
        report("states a scope limit", re.search(r"\bno \w+", low) is not None)
        return

    for head in ("Goal", "Requirements", "Done when", "Boundaries"):
        report(f"has a '{head}' section", bool(section(prompt, head)))

    done = section(prompt, "Done when")
    items = len(re.findall(r"^- ", done, re.M))
    lo, hi = DONE_RANGE[tier]
    report(f"done-list has {lo} to {hi} checks", lo <= items <= hi, f"{items} checks")
    report("done-list asks for evidence", len(re.findall(r"\bshow\b", done, re.I)) >= 1)

    bounds = section(prompt, "Boundaries").lower()
    report("boundaries limit the scope", "only" in bounds and re.search(r"\bno \w+", bounds) is not None)

    how = section(prompt, "How to work").lower()
    if loop != "none":
        has_exit = any(k in how for k in ("stop when", "when a check fails", "until"))
        has_cap = any(
            k in how
            for k in ("after five rounds", "after four rounds", "two attempts", "after three approaches", "rounds in a row")
        )
        report(f"loop ({loop}) has an exit and a cap", has_exit and has_cap)
    if "long-run" in loop:
        report("long-run loop says where state lives", "progress.md" in how and "git log" in how)

    if meta["delegates"] == "yes":
        parts = {
            "split": "tracks" in how,
            "brief": "brief" in how and "can't see this conversation" in how,
            "return": "returns only" in how,
            "run": "parallel" in how and "at most" in how,
            "merge": "merge" in how and "spot check" in how,
            "fallback": "if you can't spawn sub-agents" in how,
        }
        missing = [k for k, present in parts.items() if not present]
        report("delegation block has all six parts", not missing, f"missing {missing}" if missing else "")
    else:
        report("tells the agent to work directly", "work directly" in how)

    if meta["review"] == "yes":
        report("one narrowly briefed review", "against the done-list only" in how and "nothing else" in how)
        report("review has a fallback without sub-agents", "if you can't spawn one" in how)


def before_after() -> None:
    """Compare example 4 with the prompt version 1.0 shipped for the same brief."""
    old_doc = (sm.REPO / "archive" / "v1.0" / "references" / "example.md").read_text(encoding="utf-8")
    block = re.search(r"\*\*The forged build prompt.*?\n\n(.*?)\n\n\*\*Why it's shaped", old_doc, re.S).group(1)
    old_prompt = "\n".join(l[2:] if l.startswith("> ") else l.lstrip(">") for l in block.splitlines())
    new_path = next((sm.REPO / "examples").glob("04-*.md"))
    _, new_prompt = load_example(new_path)
    old_n, new_n = sm.words(old_prompt), sm.words(new_prompt)
    extras = [k for k in ("--dry-run", "--undo", "filetidy.log", "ruff", "mypy", "README", "TodoWrite") if k in old_prompt]
    print("\nVersion 1.0 and 1.1 on the same brief (example 4)")
    print(f"  1.0: {old_n} words; items the brief never asked for: {', '.join(extras)}")
    print(f"  1.1: {new_n} words ({100 * new_n // old_n}% of 1.0)")
    report("1.1 is shorter than 1.0 on the same brief", new_n < old_n)
    stated = re.search(r"\| Words \| (\d+) \| (\d+) \|", new_path.read_text(encoding="utf-8"))
    report(
        "the word counts quoted in example 4 are current",
        bool(stated) and (int(stated.group(1)), int(stated.group(2))) == (old_n, new_n),
    )


def main() -> int:
    files = sorted(p for p in (sm.REPO / "examples").glob("*.md") if p.name != "README.md")
    if not files:
        print("no example files found")
        return 1
    index = (sm.REPO / "examples" / "README.md").read_text(encoding="utf-8")
    for path in files:
        check_example(path)
        _, prompt = load_example(path)
        report("word count in the examples index is current", f"| {sm.words(prompt)} |" in index and path.name in index)
        own = re.search(r"The prompt is (\d+) words\.", path.read_text(encoding="utf-8"))
        report("word count stated in the file is current", bool(own) and int(own.group(1)) == sm.words(prompt))
    before_after()
    print("\nRESULT:", "ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
