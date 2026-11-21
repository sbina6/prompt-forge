# Anatomy of a best-in-class build prompt

This is the full palette of sections a build prompt can contain. Not every project needs every
section — see "Scale the rest to the project" in `SKILL.md`. Each entry says what the section
is, **why it earns its place**, and what a strong version looks like. Assemble the ones the
project needs, in roughly this order.

Ordering principle: frame the mission → give context → define "done" → set up the harness →
give the working method → enumerate the work → lock the guardrails → say how to stop and report.

---

## 0. Operator setup (lives OUTSIDE the pasteable prompt)

A short pre-flight the human does once before pasting: open the agent in the right folder
(often an empty one for a fresh repo), enable hands-off/permission mode, accept the
workspace-trust dialog, provide any secret via a `.env`. *Why:* the best prompt still fails if
the agent is launched in the wrong directory or without permission to act. Keep it to a few
bullets and keep it separate from the prompt the agent reads.

## 1. Mission + autonomy frame

The opening. "You are building **X**, autonomously and end-to-end. Work through everything below
without stopping for confirmation — stop only under the STOP/ASK conditions in §N. When you
finish, the app must actually run and you must prove it with pasted command output and
screenshots, not assertions." Then the **context anchors**: today's date, locale, currency,
units, environment. *Why:* sets autonomy, sets the standard of proof, and pins the facts the
agent would otherwise guess. The "prove it, don't assert it" line is the spine of everything
downstream.

## 2. Read the prior art first

If anything already exists — a beta, a repo, a spec, a design doc, real data — point the agent
at it explicitly and tell it to absorb it *before writing code*, then record what it will keep,
change, and drop. Name the files and what to take from each. *Why:* porting a proven design and
real data beats reinventing them, and it grounds the agent in reality instead of a plausible
fiction. Mark reference material read-only so the agent doesn't mutate the source of truth.

## 3. What it is + the one rule that governs everything

A crisp statement of the thing, and — for anything with architecture — **the single invariant
that everything else follows from** (e.g. "the HTTP API is the substrate; the UI and every
future client are just clients of it"). *Why:* one memorable governing rule keeps a long
autonomous run coherent far better than a scattered list of preferences.

## 4. Future seams — design now, don't build

If later phases are coming, state exactly what to leave room for and, emphatically, **what not
to build yet**. *Why:* agents over-deliver when the boundary is fuzzy. Naming the seam ("it will
be just another actor with fewer rights; add the extension point and a test, implement nothing")
prevents both a rewrite later and scope creep now.

## 5. Definition of Done — the machine-checkable contract

A numbered list where **every item is demonstrable**. Not "well-tested" but "`pytest` exits 0
and covers the invariants in §N"; not "the API works" but "paste the real `curl` output for a
representative call per resource, including the JSON variant." Tell the agent to restate this as
a live checklist (e.g. via TodoWrite) before coding and to keep it current. *Why:* this is the
target the loop-until-done engine aims at. Vague adjectives here are the number-one cause of
confidently-wrong "done." End it with the independent verifier's PASS as the final gate.

## 6. Foundation first — the project harness (larger projects)

Before feature code, have the agent build the scaffolding that makes the rest reliable. For a
Claude Code target this is concrete and high-value:

- **An agent-memory file** (`.claude/CLAUDE.md`, kept lean): exact build/test/lint/run commands,
  directory layout, coding conventions, and a short **ALWAYS / NEVER** list of the project's
  hard rules. Add a compaction rule so key state (the checklist, modified files, run commands)
  survives context compaction.
- **`.claude/settings.json`**: a scoped `allow`/`deny` permission set, and optionally a **`Stop`
  hook** that runs the fast test suite and blocks a premature finish (a *soft* gate — keep it
  fast, and never rely on it instead of real fixes).
- **An independent verifier subagent** (`.claude/agents/verifier.md`): read-only, no stake in
  passing, reviews the diff against the requirements in a fresh context and returns PASS/FAIL
  with evidence. This is the single highest-leverage reliability component; see the worked
  example for a full one.
- **Project skills** (`.claude/skills/`): capture repeated procedures (run-and-verify,
  add-a-slice, commit) so they're consistent and out of the main context.

*Why:* the harness is what lets a long unattended run stay honest and on-convention. For a
non-Claude-Code agent, translate this to that agent's equivalent (a rules file, a review pass)
or fold the intent into the build loop.

## 7. The build loop — the core engine

The repeatable cycle the agent runs for every unit of work:

1. **Plan** the slice (read-only analysis first; use a subagent for multi-file investigation to
   keep the main context clean).
2. **Write the failing test first** for each acceptance criterion of non-trivial logic, and run
   it to show it failing before implementing. Never edit a test to make it pass; if a test seems
   wrong, stop and explain.
3. **Implement the minimum** to pass.
4. **Generate → verify → fix, self-re-running:** one focused change → re-run the full check
   (tests + lint + typecheck) → **paste the real output** → if red, fix the **root cause**
   (never skip/xfail, weaken an assertion, catch-and-ignore, or hard-code an output) → repeat
   until green.
5. **Verify it runs for real** — not just unit tests: start it, exercise the actual
   interface (curl the endpoint, run the CLI, drive the page in a headless browser and
   screenshot it), confirm no errors in logs/console.
6. **Independent gate:** hand the diff + Definition of Done to the verifier subagent; don't
   declare done until VERDICT: PASS.
7. **Commit** with a descriptive message; clear context between unrelated slices.

Tell the agent to order checks **cheapest-and-most-deterministic first** (parse/schema → build →
tests → endpoint/screenshot → subjective review). *Why:* this is plan-execute-verify plus
Reflexion made concrete. It's what converts "the model wrote some code" into "the feature
demonstrably works."

## 8. The work — ordered vertical slices

Break the build into slices that each deliver a working, testable increment, **in strict
dependency order**, with a rule: don't start slice N+1 until N is green and committed. Spell out
what each slice includes. *Why:* ordered slices give a long run a spine and frequent green
checkpoints (real commits are the only rollback), and they stop the agent from building four
half-features at once.

## 9. Runtime guardrails — enforced in code + tests, not prose

The invariants that must always hold at runtime (data integrity, safety, no irreversible
actions, reduced rights for automated actors, required caveats). State that they live in
application code + schema/DB constraints + tests and are proven by a green suite — **not**
satisfied by a session hook or a comment. *Why:* a guardrail that exists only as prose in the
prompt evaporates the moment the agent forgets it; one encoded as a test fails loudly forever.
Separate *build-session* guardrails (permissions/hooks protecting the repo while building) from
*runtime* guardrails (protecting the app's behavior) — they are not interchangeable.

## 10. Tech + deployment spec

The concrete stack (pinned where it matters), and the deployment artifact (container, bundle,
binary). Crucially: **how to verify honestly when the build environment differs from the
deploy environment** — e.g. run the test loop in a native venv locally, statically validate the
container config, build the image only if the toolchain is present, and clearly flag in the
final report anything that can only be confirmed on the target hardware. *Why:* an agent left to
its own devices will either claim it verified something it couldn't, or waste hours fighting a
platform mismatch. Naming the split prevents both.

## 11. Interface / UI spec

For anything with a UI or a public interface: describe each screen/endpoint/command, its
contents, and its states — concretely, at the level of "car cards with a photo, name, odometer,
and at-a-glance status; click a card → the vehicle detail." *Why:* "make a nice UI" produces
generic mush; a concrete list produces the thing the user pictured. Keep it about *what appears
and what it does*, not pixel styling, unless styling is the point.

## 12. Data / migration

If real data must move, give the exact source, insist the original stays untouched (copy, don't
move), require verification (paste row counts), and say what to do with unknowns — leave them as
drafts for the human to confirm, **never invent facts**. *Why:* data loss and fabricated data
are two of the most damaging silent failures; make both structurally hard.

## 13. Out of scope + when to stop

Two tight lists. **Out of scope:** what to leave clean seams for and not build. **Stop and ask
ONLY if:** a required secret is missing, a genuinely destructive/irreversible action would be
needed, or an external decision blocks progress — otherwise keep going. Pair this with the
loop-until-done termination: keep working until the Definition of Done holds and the verifier
passes, or until repeated no-progress, then **stop and report exactly which checks are red with
the real error output**. *Why:* this is the explicit termination condition that makes autonomy
safe — it prevents both premature stopping ("done!" at 60%) and pointless thrashing, and it
forbids the worst outcome: declaring partial success as done.

## 14. Engineering standards + honest final report

Small reviewable commits; the docs to produce (README with real run instructions, architecture
notes, a plan file). And a closing instruction: **give an honest final report** — what was
built, the pasted evidence, what was *not* done, the rough edges, and anything that still needs
the human to confirm on real hardware. No "production ready" claims. *Why:* the final report is
where an agent is most tempted to oversell; requiring the gaps and the evidence keeps the
handoff trustworthy.

---

## Assembly notes

- **Number the sections** and cross-reference them ("stop only under §13") — a long prompt the
  agent can navigate beats a wall of text.
- **Explain the why** inside the prompt for the harder demands. Smart agents cooperate with
  reasoning and lawyer bare mandates. Prefer "supersede or soft-delete, because the audit trail
  must stay intact" over a naked "NEVER DELETE."
- **Prefer capability over version.** If the prompt uses an optional feature, give the fallback
  and use model aliases, so the prompt survives across agent versions.
- **End with a kickoff line**: "Start by reading §2, then write the plan file with the
  Definition-of-Done checklist and the slice list. Then build." A clear first action beats
  leaving the agent to choose where to begin.
