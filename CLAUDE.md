# Prompt Forge repository: working notes for Claude

This repository holds one Claude skill, Prompt Forge, and its documentation. The skill turns a
rough idea into a right-sized prompt for an autonomous agent.

## What matters most

- The product is `skill/prompt-forge/SKILL.md`. It stays a single, self-contained file.
- Its purpose is small prompts. A change that makes forged prompts longer or heavier needs
  evidence from a real run.
- Read `docs/DESIGN.md` before changing behaviour. It records why each rule exists and what was
  already rejected.

## Commands

- `python tests/run_checks.py` runs every check. Run it before each commit.
- `python tools/package_skill.py` builds `dist/prompt-forge-<version>.zip`.

## When you change the skill

1. Start from a concrete case: the ask, the prompt the skill produced, and what the agent did.
2. Make the smallest edit that fixes it, then cut anything the edit made redundant.
3. Update the matching section of `docs/USAGE.md`, add or amend a decision in `docs/DESIGN.md`,
   and add a line to `CHANGELOG.md`.
4. Change the version in `VERSION` and in both places in `SKILL.md` together. `docs/MAINTAINING.md`
   says which digit to change.
5. Run the checks again, and re-forge any example the change affects.

The full procedure is in `docs/MAINTAINING.md`.

## Limits to respect

- At the top of `SKILL.md`, use only `name`, `description`, `license`, `compatibility`, `metadata`
  and `allowed-tools`. The description is at most 1,024 characters and has no angle brackets.
- Keep `SKILL.md` under 500 lines, with the method (everything before "Agent notes") inside
  roughly 5,000 tokens.
- Do not move content out of `SKILL.md` into other files. The chat review card can replace that
  one file only.
- `archive/` is history. Do not edit it.
- Check product documentation again before changing the agent notes. Do not rely on memory.
- Keep secrets, tokens and personal details out of the repository.

## Style of the skill text

Plain, calm and in the second person. A reason is attached to each rule. No shouted mandates.
Tables for anything the reader scans.

## Honesty about testing

Say exactly how a result was obtained: by a script, by your own dry run, or by an independent run.
`docs/BUILD-HISTORY.md` shows the standard.
