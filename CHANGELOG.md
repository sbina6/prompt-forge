# Changelog

Every notable change to Prompt Forge. The rules for version numbers are in
[docs/MAINTAINING.md](docs/MAINTAINING.md#version-numbers), and the reasons behind the changes are
in [docs/DESIGN.md](docs/DESIGN.md).

## [1.1] - 2026-11-21

A rebuild of the skill around one idea: current agents do everything a prompt says, so the prompt
should be the smallest one that still gets the result proven.

### Added

- **Route step.** Settles whether the user wants a prompt or the result, whether the prompt is new
  or needs repair, and which agent will run it.
- **Scope ledger.** Everything is sorted into Asked, Needed and Extras. Only the first two go into
  the prompt; the best extras are offered in a line each.
- **Micro size, and word ceilings for all four sizes:** 150, 350, 800 and 1,600 instruction words.
- **Six loop kinds:** fix, refine, queue, coverage, long-run and watch. Each loop names its check,
  its exit, its cap and where its state lives.
- **Sub-agent delegation.** Four tests for when it pays off, a six-part delegation block, a
  sequential fallback, and a "work directly" line for small jobs.
- **Six task types.** Software, research and sourcing, design and CAD, documents and skills, data,
  and recurring automation, each with its proof of done.
- **Prompt repair.** A table of seven symptoms with their usual cause and fix.
- **A self-test.** The skill reads its own draft as the receiving agent, and gives large prompts to
  a fresh sub-agent for a cold read, for at most two rounds.
- **Agent notes** for Claude Code, Codex, Cursor and Claude chat, dated November 2026, with
  optional commands such as `/goal` and `/loop` offered in the run notes.
- **Named inputs.** Values only the user has are requested by the agent and never invented; real
  secrets stay out of the prompt.
- **A version stamp** in the skill file.
- **This repository:** usage guide, design notes, build history, maintenance guide, examples,
  checks, a zip builder, and workflows that run the checks and publish each release.

### Changed

- **One self-contained file.** The skill no longer depends on reference files.
- **A three-part spine.** Every prompt has a Goal, a Done-when list and Boundaries. The four-part
  "non-negotiable spine" is gone.
- **Verification.** The prompt gives the agent a check it can run and does not stack further
  verification on top. An independent review appears only in Large prompts or where a wrong result
  is costly, and its brief is narrow.
- **Tone.** Calm wording with reasons, and scoped rules in place of blanket bans.
- **Questions.** At most three, in one batch, and only when the answer changes what gets built.
- **Delivery.** One line, the prompt in a copyable block, run notes of at most five lines, then
  assumptions and left-out extras.
- **Triggers.** The skill now covers any task handed to an agent, not only software, and
  recognises its own name as dictation writes it.

### Removed

- Compulsory reading of `references/anatomy.md` and `references/example.md`.
- The default project harness: memory file, settings file, hooks, custom agents and project
  skills. It is now added only for work that spans sessions, or on request.
- Test-first as a default.
- References to a specific to-do tool and to model aliases, and the instruction to swap in the
  run date.
- The closing menu of variants.

### Fixed

- Prompts that made agents build and verify far more than was asked.
- Asks outside software, which the skill used to declare out of scope.
- Loops with no clear exit.
- Requests for a result that were answered with a prompt.

### Known limits

Version 1.1 was checked by scripts and by four dry runs written by its author. It has not yet
been evaluated by independent runs. See
[docs/BUILD-HISTORY.md](docs/BUILD-HISTORY.md#what-was-not-done).

## [1.0] - 2026

The original version. The exact release date was not recorded.

- Produced "build prompts" for software projects in three moves: Understand, Forge, Deliver.
- Used a fixed four-part spine, a palette of 15 sections and a worked example held in two reference
  files.
- Recommended an independent verifier sub-agent.

Archived unchanged in [`archive/v1.0/`](archive/v1.0/README.md).
