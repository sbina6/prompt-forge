# Worked example + the gold-standard structure

Two things here: (1) a compact, self-contained worked example at *medium* size, so you can see
the spine and scaling in a small footprint, and (2) notes on what a *large* gold-standard build
prompt adds on top.

---

## Compact worked example (medium project)

**User brief:** "Write me a prompt for Claude Code to build a CLI tool that watches a folder and
auto-organizes files into subfolders by type and date. Python. Should be safe — never lose a
file."

**What Move 1 elicited / assumed:** greenfield; Python 3.12; runs on the user's Windows laptop;
must-haves = watch a folder, classify by extension into `Images/`, `Docs/`, etc., then by
`YYYY-MM`, with a dry-run mode; non-goals = no GUI, no cloud; hard invariant = never overwrite
or delete, moves must be reversible; target agent = Claude Code, hands-off. Everything unstated
was assumed and the assumptions were stated back to the user.

**The forged build prompt (what gets pasted):**

> You are building **FileTidy**, a Python CLI that organizes a folder, autonomously and
> end-to-end. Work through everything below without stopping for confirmation except under the
> STOP/ASK conditions in §7. When you finish, it must actually run and you must prove it with
> pasted command output — not assertions. Today is <DATE>. You are running on Windows; target
> Python 3.12, standard library only where reasonable.
>
> **§1 What it is.** A CLI, `filetidy`, that scans a source folder and moves each file into
> `<dest>/<Category>/<YYYY-MM>/`, where Category is derived from extension (Images, Documents,
> Audio, Video, Archives, Code, Other). It has a `--dry-run` that prints every planned move and
> changes nothing, and a `--watch` that re-runs on change.
>
> **§2 Definition of Done** (restate as a TodoWrite checklist before coding; each item must be
> demonstrated with pasted output):
> 1. `pytest` exits 0 and covers: classification, the dry-run makes no filesystem changes,
>    name-collision handling, and the reversibility log.
> 2. `ruff` + `mypy` clean.
> 3. `filetidy --dry-run <sample>` prints a correct plan for a seeded sample tree — paste it.
> 4. `filetidy <sample>` performs the moves; a second run is a no-op — paste both.
> 5. Every move is recorded to an append-only `filetidy.log` (JSON lines: src, dest, time) and
>    `filetidy --undo` restores the last run exactly — demonstrate a round-trip.
>
> **§3 Safety invariants — in code + tests, not comments.** Never overwrite: on a name
> collision, suffix ` (1)`, ` (2)`, …. Never delete. Every move is logged before it happens so
> `--undo` can reverse it. A move that would leave the source folder must be refused. Add tests
> for each.
>
> **§4 Build loop, per slice.** Plan → write the failing test first → implement the minimum →
> run tests + ruff + mypy and **paste the output** → fix the root cause if red (never weaken a
> test) → run the CLI on the seeded sample and paste it → commit. Order: (a) classification pure
> function, (b) dry-run planner, (c) executor with collision + logging, (d) `--undo`,
> (e) `--watch`. Don't start a slice until the previous is green and committed.
>
> **§5 Verify for real.** Beyond unit tests, build a throwaway sample tree of a dozen files with
> varied extensions and dates, run `--dry-run` then the real run then `--undo`, and paste each
> result. A passing unit test is not proof the CLI works end-to-end — the sample run is.
>
> **§6 Independent check.** After the build, re-read the diff against §2 and §3 in a fresh pass
> (or spawn a verifier subagent) and confirm every item with evidence before declaring done. If
> anything is unverified, it is not done.
>
> **§7 Stop and ask ONLY if** a destructive/irreversible action would be unavoidable or a
> required detail is genuinely missing. Otherwise keep going until §2 holds. If you hit repeated
> no-progress, stop and report exactly which checks are red with the real error output.
>
> **§8 Finish** with an honest report: what works (with pasted evidence), what doesn't, and any
> rough edges. Provide a README with real usage examples. No "production ready" claims. Start by
> writing the plan with the §2 checklist and the slice list, then build.

**Why it's shaped this way:** even at this size it carries the spine — mission + "prove it",
a demonstrable Definition of Done, the plan→test→verify→commit loop, an independent check, stop
conditions, honest report — and it right-sizes everything else (no container spec, no migration,
no multi-service harness). The safety requirement became *tests and an undo log*, not a prose
plea. That's the whole game: turn every wish into a check.

---

## What a large, gold-standard prompt adds

For a multi-service app with real data, future phases, and strict invariants, the same spine
carries much more around it. The pattern (as in a full "Phase 1" application build prompt):

- **Read prior art first** — point at an existing beta/spec/data and record keep/change/drop.
- **One governing architectural rule** — e.g. "the HTTP API is the substrate; the UI and every
  future client are clients of it" — repeated so a long run stays coherent.
- **A future seam** — design the extension point for the next phase, build none of it, add a
  test that the seam holds.
- **Foundation first** — a lean `CLAUDE.md`, a `settings.json` with a `Stop` verification hook,
  and especially a full **independent verifier subagent** that reviews the diff in a fresh
  context and returns PASS/FAIL with evidence. A strong verifier subagent looks like:

  > You are an independent verification engineer and skeptic. You did NOT write this code and
  > have no stake in it passing. Run `git diff` to see exactly what changed. Re-derive what it is
  > supposed to do from the requirements, not the narrative. Actually exercise it — run the
  > tests, lint, typecheck, and the repro command; read the real output, never assume a command
  > passed. Trace each requirement to concrete evidence and hunt the edge cases the implementer
  > skipped. End with VERDICT: PASS or FAIL (FAIL if any requirement is unverified), each
  > requirement mapped to its evidence, and the blocking gaps. Show evidence, do not assert; if
  > you cannot verify a requirement, it is FAIL.

- **Runtime guardrails in code + DB + tests** — soft-delete instead of hard-delete, an
  append-only audit log, validation surfaced as warnings, reduced rights for automated actors —
  each with a test, explicitly *not* satisfied by a session hook.
- **Honest cross-environment verification** — build/test in a native local env, statically
  validate the deployment container, build the image only if the toolchain is present, and flag
  in the final report whatever can only be confirmed on the real target hardware.

The lesson to carry from the gold standard: it is long **only where length buys reliability** —
every heavy section is there to convert a way the build could silently go wrong into a check the
agent must pass. Match that discipline at whatever size the user's project calls for.
