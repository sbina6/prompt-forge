# Examples

Four requests and the prompts version 1.1 produces for them. Each file shows the ask, the full output, and the reasoning: the scope ledger, the size, and why a loop or sub-agents were or were not used.

| Example | Tier | Words | Loop | Sub-agents | Review |
|---|---|---|---|---|---|
| [a tiny script (Micro)](01-micro-heic-to-jpg.md) | Micro | 97 | none | no | none |
| [a research sweep with sub-agents and a coverage loop (Medium)](02-medium-research-supplier-directory.md) | Medium | 554 | coverage | yes | none |
| [a real app left running unattended (Medium)](03-medium-build-home-maintenance-tracker.md) | Medium | 768 | fix+long-run | no | one, at the end |
| [version 1.0 and version 1.1 on the same request (Small)](04-small-file-organiser-before-after.md) | Small | 293 | fix | no | none |

These prompts were written by following the skill by hand during the 1.1 build. They have not yet been run by an independent agent; see [`docs/BUILD-HISTORY.md`](../docs/BUILD-HISTORY.md) for what was and was not tested.

The checks in [`tests/check_examples.py`](../tests/check_examples.py) read these files. Each one starts with a comment line that declares its tier, loop, delegation and review, and the checks hold the prompt to the skill's own rules for that declaration.
