# Maintaining Prompt Forge

How to change the skill, test it and release a version. This is for the owner, for colleagues, and
for Claude sessions that are asked to work on it. Read [DESIGN.md](DESIGN.md) before changing
behaviour: it records why each rule exists and what was already tried.

**Contents**

- [The short version](#the-short-version)
- [Where things are](#where-things-are)
- [Changing the skill](#changing-the-skill)
- [Version numbers](#version-numbers)
- [Refreshing the agent notes](#refreshing-the-agent-notes)
- [Testing properly](#testing-properly)
- [Constraints that are easy to break](#constraints-that-are-easy-to-break)
- [Releasing](#releasing)
- [Notes for Claude sessions](#notes-for-claude-sessions)

---

## The short version

1. The product is one file, [`skill/prompt-forge/SKILL.md`](../skill/prompt-forge/SKILL.md).
   Everything else describes it.
2. Change it only in response to a real case: an ask, the prompt it produced, and what went wrong.
3. Make the smallest edit that fixes the case, then cut whatever the edit made redundant.
4. Run `python tests/run_checks.py` before every commit.
5. Keep the documentation, the changelog and the version number in step with the skill.

The skill's purpose is small prompts. The easiest way to damage it is to add a helpful rule for
every case anyone thinks of. Version 1.0 grew that way.

## Where things are

| What | Where | Notes |
|---|---|---|
| The skill | `skill/prompt-forge/SKILL.md` | The single source of truth for behaviour |
| The version number | `VERSION`, and twice in `SKILL.md` | See [Version numbers](#version-numbers) |
| How to use each feature | `docs/USAGE.md` | Has to match the skill; the skill wins any disagreement |
| Why each rule exists | `docs/DESIGN.md` | Add a decision when behaviour changes |
| What was done and tested | `docs/BUILD-HISTORY.md` | A record of the 1.1 build; add a section for each later build |
| Sources and the date they were read | `docs/SOURCES.md` | Update when the agent notes are refreshed |
| Worked examples | `examples/` | Each declares its size, loop, delegation and review in its first line |
| Checks | `tests/` | Standard library only; PyYAML is used if it is installed |
| The zip builder | `tools/package_skill.py` | Writes `dist/prompt-forge-<version>.zip` |
| Workflows | `.github/workflows/` | `validate` runs the checks on pull requests and on the main branch; `release` publishes a release when a version tag is pushed |
| The previous version | `archive/v1.0/` | History. Do not edit. |

## Changing the skill

This procedure is a loop of the kind the skill itself describes: it has a check, an exit and a
cap.

1. **Start from a case.** Write down the ask, the prompt the skill produced, and what the agent
   did. If there is no case, there is no change to make yet. An issue filed with the
   [template](../.github/ISSUE_TEMPLATE/forged-prompt-problem.md) has all three.
2. **Find the decision behind the behaviour.** Look it up in [DESIGN.md](DESIGN.md#6-decisions).
   Read what was considered and rejected. The change you have in mind may be there.
3. **Write a ledger for the change.** Asked: the failure to fix. Needed: what the fix cannot work
   without. Extras: everything else you would like to add. Only the first two go in.
4. **Edit `SKILL.md`.** Change the fewest lines that fix the case. Prefer changing a rule to
   adding one.
5. **Cut.** Delete any sentence the edit made redundant. Check the line count and the token
   estimate that `tests/check_skill.py` prints.
6. **Run the checks.**

   ```text
   python tests/run_checks.py
   ```

7. **Re-forge the case.** Follow the edited skill on the original ask and confirm that the failure
   is gone. Then re-forge any example in `examples/` that the change affects, and update the word
   counts in the example file and in `examples/README.md`. The checks fail if those counts are
   stale.
8. **Update the documentation.** The matching section of `docs/USAGE.md`. A new or amended
   decision in `docs/DESIGN.md`, with what was considered. A line in `CHANGELOG.md`.
9. **Bump the version** as described below.
10. **Release** as described under [Releasing](#releasing).

**Exit:** the case is fixed, the checks pass and the documentation matches.
**Cap:** if two attempts at a fix both fail on the re-forge, stop editing. The cause is probably a
different decision from the one you started with, so go back to step 2.

## Version numbers

| Change | Example | New number |
|---|---|---|
| Wording, a refreshed agent note, a documentation-only correction to the skill text | A command was renamed | 1.1 → 1.1.1 |
| Behaviour changes inside the same method | A new loop kind; different ceilings; a new rule in a step | 1.1 → 1.2 |
| A change of method | The five steps are replaced | → 2.0 |

The number appears in these places. The first four are enforced by a check.

| Place | What to change |
|---|---|
| `VERSION` | The number alone |
| `skill/prompt-forge/SKILL.md`, at the top | `metadata.version` |
| `skill/prompt-forge/SKILL.md`, first paragraphs | The sentence "This is version …" |
| `CHANGELOG.md` | A new `## [number] - date` section |
| `README.md` | The version line and the versions table |
| `docs/INSTALL.md` | The zip file names |

The number is in the body of the skill as well as at the top because the chat review card keeps
only the name and description from the top of the file. The sentence in the body is the copy that
survives every way of installing.

## Refreshing the agent notes

The "Agent notes" section of the skill names commands in products that change quickly. Refresh it
every three months, and whenever someone reports that a command in their run notes did not exist.

1. Re-read the pages listed as S4 to S8, S13 and S14 in [SOURCES.md](SOURCES.md).
2. Check each statement in the section against them:
   - Does `/goal` still exist, and does its evaluator still judge from the conversation alone?
   - Is the `/loop` syntax unchanged? Are scheduled tasks still the durable option?
   - Is "use a workflow to…" still the way to ask for a large fan-out? Do `/batch`,
     `/deep-research` and `/code-review` still exist?
   - Does Codex still delegate only on request? Does Cursor still delegate by itself?
   - Is there a new agent that deserves a line, or a line that no longer deserves its place?
3. Edit the section. Keep it short. A command that cannot be verified is removed, not hedged.
4. Change "Checked November 2026" to the current month, in `SKILL.md` and in
   `docs/USAGE.md` section 10.
5. Update the dates in `docs/SOURCES.md`, add a changelog line, and bump the third digit of the
   version.

## Testing properly

Version 1.1 was checked by its author and by scripts. The evaluation below has not been done yet,
and it is the most valuable next piece of work.

### An independent evaluation

The idea is to run a fixed set of asks in fresh sessions that have never seen this repository,
once with the current skill and once with a baseline, and to compare the results. Anthropic's
skill-creator skill automates this when sub-agents are available: ask Claude to "evaluate the
prompt-forge skill with skill-creator" and give it the asks below. Use `archive/v1.0` as the
baseline.

A set that covers the sizes, the task types and the special routes:

| # | Ask | What a good result shows |
|---|---|---|
| 1 | "Prompt forge: a script that converts a folder of HEIC photos to JPG." | Micro; one paragraph; one check; no loop |
| 2 | "A prompt for a to-scale 2D plan of my workshop from this sketch." | Small; a refine loop with a cap; "work directly" |
| 3 | "A hands-off prompt to map every supplier of X within 60 km." | Medium; a coverage loop; a full delegation block |
| 4 | "A prompt for Claude Code to build a small web app with three screens and a login." | Medium; a fix loop; no extras beyond the three screens and the login |
| 5 | "A prompt to migrate 300 Python files to a new API and prove nothing broke." | Large; a queue loop with a ledger; fan-out or a workflow; a pilot on a small slice; one review |
| 6 | "A prompt for a job that checks my server each morning and messages me on a problem." | A watch loop with a state file; a scheduled task in the run notes |
| 7 | "A prompt to reconcile two CSV exports and list every mismatch." | Data task; totals that reconcile; work on a copy |
| 8 | "Prompt forge, make me a comparison table of these three options." | The prompt-or-result question, asked once |
| 9 | "This prompt made the agent build far too much. Fix it:" with the version 1.0 example prompt | Repair mode; a smaller prompt; a three-line list of changes |
| 10 | "Build me a to-do app." | The skill does not trigger |

For each result, record:

- the size chosen, and the word count against the ceiling;
- every deliverable or check that does not trace to the ask;
- for each loop, whether the check, the exit, the cap and the state are all present;
- for each delegation, whether the choice passes one of the four tests and the block has six
  parts;
- whether the answer kept to the four-part delivery format.

### An end-to-end run

Take one Medium result, run it in a coding agent, and compare what was built with the ledger.
Anything built that is in neither Asked nor Needed is overbuilding, and the prompt has to be
tightened. Any done-list item the agent did not show is under-proof, and the check has to be
sharpened. Record the result in an issue.

### A trigger test

Write twenty asks: ten that should trigger the skill and ten near misses that should not, such as
"build me a to-do app" or "what makes a good prompt?". Run each a few times in fresh sessions and
note whether the skill loads. Adjust the description if the miss rate is high. The skill-creator
skill has a procedure for this as well.

### Recording results

Add a dated section to `docs/BUILD-HISTORY.md` with the asks, the numbers and what changed as a
result. Evidence that is not written down is lost by the next build.

## Constraints that are easy to break

| Constraint | Why | Enforced by |
|---|---|---|
| Only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` at the top of `SKILL.md` | An upload with any other key is rejected | `check_skill.py`, `package_skill.py` |
| Description at most 1,024 characters, with no angle brackets | Upload limit | `check_skill.py` |
| `name` equals the folder name, `prompt-forge` | Upload requirement | `check_skill.py` |
| Exactly one `SKILL.md` inside `skill/prompt-forge/` | Upload requirement | `check_skill.py` |
| Under 500 lines | Skills get harder to follow past that | `check_skill.py` |
| The method ends before about 5,000 tokens | Claude Code keeps roughly that much of a skill after compacting a long session | `check_skill.py` (an estimate) |
| One self-contained file | The chat review card can replace `SKILL.md` only | Review |
| No shouted mandates in the skill | The skill asks for calm prompts and should model them | `check_skill.py` |
| `archive/` is not edited | It is the record of what version 1.0 was | Review |
| No secrets, tokens or personal details anywhere in the repository | The repository is shared | Review |

## Releasing

1. `python tests/run_checks.py` passes.
2. The version is updated in every place listed under [Version numbers](#version-numbers).
3. Build the zip:

   ```text
   python tools/package_skill.py
   ```

4. Commit on a branch, open a pull request, and merge it once the checks are green.
5. Tag the merged commit on the main branch and push the tag:

   ```text
   git tag -a v1.2 -m "Prompt Forge 1.2"
   git push origin v1.2
   ```

   The release workflow does the rest. It confirms that the tag matches `VERSION`, runs the
   checks, builds the zip from the tagged source and publishes a GitHub release, with that
   version's changelog section as the notes and the zip attached.
6. Install the new version: upload the zip as described in [INSTALL.md](INSTALL.md), or ask Claude
   in a chat to update the skill from the repository's `SKILL.md`.
7. Run the check ask from [INSTALL.md](INSTALL.md#4-check-that-it-works) to confirm that the new
   version is the one answering.

## Notes for Claude sessions

If you are a Claude session asked to upgrade, fix or extend this skill:

- **Read first.** [CLAUDE.md](../CLAUDE.md), then [DESIGN.md](DESIGN.md), then the current
  `SKILL.md` in full. Check the product documentation again before touching the agent notes. Do
  not rely on memory for product details.
- **Ask for the case.** If the request is "make it better", ask what went wrong, or look for past
  uses. A build without evidence adds weight and fixes nothing.
- **Resist adding.** Your instinct will be to add a rule. First try to change or remove one. Report
  the line count and the token estimate before and after.
- **Follow the skill's own method.** Write the ledger for the change. Give the change a check.
  Apply the Cut pass to your edit.
- **Use sub-agents and loops as the skill would.** An independent evaluation is the "fresh eyes"
  case and is worth a sub-agent when you are permitted to start one. A fix that fails twice calls
  for a change of approach.
- **Be exact about what you tested.** Say whether a result came from a script, from your own dry
  run, or from an independent run. [BUILD-HISTORY.md](BUILD-HISTORY.md#what-was-not-done) shows
  the standard.
- **Keep the installed copy and the repository in step.** The repository is the source of truth.
  If you update the skill through a chat review card, the card replaces the whole `SKILL.md` and
  keeps only the name and description from the top of the file. Commit the same text here, with
  the same version number.
- **Leave personal details out.** Describe real uses in general terms, as
  [DESIGN.md](DESIGN.md#32-evidence-from-real-use) does.
