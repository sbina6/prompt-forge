# Contributing to Prompt Forge

Prompt Forge improves through real cases. The most useful thing you can contribute is a prompt
that went wrong, with enough detail to see why.

## Reporting a prompt that misbehaved

Open an issue with the "A forged prompt misbehaved" template. It asks for three things:

1. **The ask.** What you said to the skill, as closely as you can recall it.
2. **The prompt.** What the skill gave you, pasted in full.
3. **What happened.** Which agent ran it, and what it did: built too much, stopped early, went in
   circles, claimed success, ignored sub-agents, used too many, or lost track.

Take out anything private before you paste: names, addresses, keys, account details.

## Suggesting a change

Open an issue with the "Suggest a change" template, or a pull request. A good suggestion has:

- **A case behind it.** A real ask where the current behaviour let you down.
- **The smallest change that would fix it.** A changed rule is better than a new one.
- **What it costs.** How many lines it adds to the skill, and whether it makes forged prompts
  longer.

Before proposing a change to how the skill behaves, read the matching decision in
[docs/DESIGN.md](docs/DESIGN.md#6-decisions). It may already list your idea under what was
considered.

## Making a change yourself

1. Read [docs/MAINTAINING.md](docs/MAINTAINING.md). It has the full procedure.
2. Work on a branch.
3. Edit [`skill/prompt-forge/SKILL.md`](skill/prompt-forge/SKILL.md), then the documentation that
   describes what you changed.
4. Run the checks:

   ```text
   python tests/run_checks.py
   ```

5. Open a pull request and fill in the template.

## Ground rules

- **Small prompts are the point.** Every sentence added to the skill makes it a little harder to
  follow, and every rule added to forged prompts is work an agent will do.
- **Evidence over taste.** "I would prefer" is not a case. "This ask produced this prompt, and the
  agent did this" is.
- **Say how you tested.** A script, your own reading, or an independent run are different levels of
  evidence. Name the one you used.
- **Keep it calm.** The skill text explains its rules and does not shout them.
- **No private material.** This repository is shared with colleagues.

## Where things are

The [README](README.md#repository-map) has a map of the repository.
