# Prompt Forge 1.0 (archived)

This folder is the previous version of the skill, exactly as it was installed before version 1.1
replaced it. It is kept for two reasons: so that the reasoning in
[`docs/DESIGN.md`](../../docs/DESIGN.md) can be checked against the text it criticises, and so that
version 1.0 can be used as the baseline when the skill is evaluated.

**Do not install this version, and do not edit these files.**

| File | What it was |
|---|---|
| `SKILL.md` | The skill: three moves (Understand, Forge, Deliver) and a four-part spine in every prompt |
| `references/anatomy.md` | The palette of 15 numbered sections that the skill told Claude to read before every forge |
| `references/example.md` | A worked example and notes on a "gold standard" structure |

## What changed, in one paragraph

Version 1.0 wrote thorough build prompts for software and tended to make agents overbuild: it
loaded all three files on every run, required the same heavy structure at every size, and had no
rule that tied a deliverable to what the user asked for. Version 1.1 is one file. It sizes each
prompt to the task, admits only what the ask needs, and adds loops and sub-agents only where they
pay off. [Example 4](../../examples/04-small-file-organiser-before-after.md) runs the brief from
`references/example.md` through both versions.

## Using it as a baseline

To compare the two versions on a new ask, give a fresh session this folder as the skill and run
the ask, then do the same with [`skill/prompt-forge/`](../../skill/prompt-forge/SKILL.md). The
procedure is in [`docs/MAINTAINING.md`](../../docs/MAINTAINING.md#testing-properly).
