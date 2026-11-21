# Using Prompt Forge

This guide covers every feature of version 1.1 and how to use it. The behaviour itself is defined
in [`skill/prompt-forge/SKILL.md`](../skill/prompt-forge/SKILL.md). If this guide and the skill
file ever disagree, the skill file is right and this guide needs fixing.

**Contents**

1. [Asking for a prompt](#1-asking-for-a-prompt)
2. [What comes back](#2-what-comes-back)
3. [Prompt or result](#3-prompt-or-result)
4. [Sizes](#4-sizes)
5. [The scope ledger and "Left out"](#5-the-scope-ledger-and-left-out)
6. [Questions, assumptions and inputs only you have](#6-questions-assumptions-and-inputs-only-you-have)
7. [The done-list](#7-the-done-list)
8. [Loops](#8-loops)
9. [Sub-agents](#9-sub-agents)
10. [Which agent](#10-which-agent)
11. [Task types beyond software](#11-task-types-beyond-software)
12. [Working from existing material](#12-working-from-existing-material)
13. [Fixing a prompt that misbehaved](#13-fixing-a-prompt-that-misbehaved)
14. [Running the prompt](#14-running-the-prompt)
15. [Phrase sheet](#15-phrase-sheet)
16. [Questions people ask](#16-questions-people-ask)

---

## 1. Asking for a prompt

Say what you want and that you want a prompt for it. Typing and dictation both work, and the
skill reads for intent, so a dictated "prompt fort" is understood.

```text
Prompt forge: a prompt for Claude Code to build a script that renames my photos by date.
Write me a hands-off prompt to map every supplier of CNC tooling in my city.
Best prompt to make a to-scale 2D plan of my workshop from this sketch.
Turn this idea into a prompt: a home maintenance tracker with reminders.
```

You do not need to write a specification. These details help when you have them:

- what you want at the end, and what you will use it for;
- where it has to run, and anything it must not do;
- which agent will run the prompt;
- whether you will watch the run or leave it alone.

Anything you leave out is either asked about, if it would change what gets built, or settled for
you and listed as an assumption.

## 2. What comes back

Every answer has the same four parts, in the same order.

1. **One line** that says what the prompt produces, its size and rough word count, and whether it
   uses a loop or sub-agents. For example: "Small prompt, about 290 words: builds the organiser. A
   fix loop; no sub-agents."
2. **The prompt**, in one block you can copy. It is written to stand alone in a fresh session, so
   it never refers to your conversation.
3. **Run notes**, at most five short lines: where to paste it, any command worth typing (each in
   its own copyable block), and a warning about cost when sub-agents or a workflow are involved.
4. **Assumptions and Left out**: up to three lines of each. Assumptions are decisions made for
   you. Left out lists the best extras that were kept out of the prompt.

Nothing else is added: no menu of variants and no tour of techniques.

## 3. Prompt or result

The skill writes prompts. Sometimes an ask names the thing itself:

```text
Prompt forge, make me a 2D plan of my workshop.
```

If the session you are in could do that work, the ask is ambiguous. The skill asks once: do you
want a prompt to paste elsewhere, or the work done here now?

- **A prompt:** you get the four parts described above.
- **Do it here:** it writes the same right-sized brief as its own plan and carries it out under
  the same rules. You get the result, not a prompt.

To skip the question, say which you want: "a prompt to…" or "do it here".

## 4. Sizes

Every prompt is one of four sizes. The skill picks the smallest that fits, and when a task sits
between two it takes the smaller.

| Size | Fits | Instruction words | Checks | Layout |
|---|---|---|---|---|
| Micro | one artifact you can check at a glance: a one-file script, a single diagram or render, a lookup | up to 150 | 1–2 | a paragraph or two, no headings |
| Small | one deliverable with a few parts or rules | 150–350 | 2–4 | Goal, Requirements, Done when, Boundaries |
| Medium | a real app, tool or service; a multi-source report; a multi-part design | 350–800 | 4–7 | adds Context, How to work, Finish |
| Large | multi-service systems, migrations, long unattended runs, strict invariants, sweeps over many items | 800–1,600 | 6–10 | adds state files, an orchestration plan, one independent review |

Some calibration points: a script that renames photos is Micro. A to-scale 2D plan from a sketch,
or a folder organiser with undo, is Small. Mapping every supplier in a city, or a web app with a
few screens, is Medium. A multi-service system with a data migration, or a 300-file code migration,
is Large.

**The word counts are ceilings, not targets.** Data and specifications you supply, such as a
dimension table or a schema, do not count towards them. A prompt may go over its ceiling only when
each extra block prevents a failure that can be named.

**Choosing the size yourself.** Name it and the skill uses it:

```text
Prompt forge, quick: a prompt to scrape this page into a CSV.
Prompt forge, full version: the maintenance tracker.
Make it Small.
```

**What stays out unless the size or you call for it**

| Left out by default | When it comes in | How to ask for it |
|---|---|---|
| Plan files and restated checklists | Medium and up | "have it write a plan first" |
| Test-first rules | where the logic is not trivial and a test is the natural check | "test-first" |
| An independent review | Large, or any size where a wrong result is costly | "add a review at the end" |
| Project scaffolding: agent memory files, hooks, custom agents, project skills | work that spans sessions | "set up the project files too" |
| Documentation beyond a short readme | on request | "include full docs" |

## 5. The scope ledger and "Left out"

Before writing anything, the skill sorts everything into three lists.

- **Asked:** what you said you want, with your constraints and the things you said to avoid.
- **Needed:** what must exist for an Asked item to work, or to be shown to work. Each entry has a
  reason. If the Asked items would succeed without it, it is not Needed.
- **Extras:** everything else it thought of, such as more formats, more platforms, exports,
  dashboards and future phases.

Only Asked and Needed go into the prompt. The best two or three Extras appear under **Left out**
after the prompt, a line each.

This is the main guard against a prompt that makes the agent overbuild. An agent that is handed
"also export a DXF and an A3 PDF" builds both, however small the original ask was.

**Bringing an extra in.** Name it:

```text
Add the dry-run preview and the undo.
```

**Taking something out.** Name that too:

```text
Drop the readme. I only need the script.
```

[Example 4](../examples/04-small-file-organiser-before-after.md) shows the ledger at work: the
same request under version 1.0 picked up eight items nobody asked for.

## 6. Questions, assumptions and inputs only you have

**Questions.** The skill asks only when the answer would change what gets built. It asks at most
three questions, in one batch, as tappable choices where the app offers them. A Micro or Small
prompt normally comes with no questions at all.

**Assumptions.** Whatever it settles for you is listed under the prompt. To change one, say so:

```text
Use Postgres, not SQLite.
```

**Inputs only you have.** Measurements, credentials and account choices cannot be guessed. The
prompt names them as inputs, and tells the agent to ask you for them at the right moment and never
to invent a value. Real secrets are kept out of the prompt itself. In
[example 3](../examples/03-medium-build-home-maintenance-tracker.md) the agent builds against a
fake Telegram sender and asks for the real token last.

**Things the agent cannot see.** A sketch, a file, or something you said earlier in the chat does
not travel with the prompt automatically. Either the facts are written into the prompt as data, or
the run notes tell you to attach the file when you paste.

## 7. The done-list

The done-list is the target the agent steers by. Each item is something the agent can run or look
at, and then show you.

| Not a check | A check |
|---|---|
| "The tool is robust." | "On a sample tree of twelve files, the count and checksums are identical before and after a run. Show the comparison." |
| "The page looks good." | "Open the PNG and confirm every label is readable and nothing is clipped." |
| "Tests are written." | "The test suite passes. Show the output." |
| "The research is thorough." | "Every category has rows, or a line saying what was searched and that nothing exists in range." |

Three rules shape it.

- **Every check belongs to something you asked for.** A check with no owner in the ledger is an
  extra in disguise.
- **Rules that must always hold become checks.** "Never lose a file" is written as a comparison
  the agent has to show, because a rule that lives only in prose gets forgotten.
- **One check, no pile of verification.** The prompt gives the agent a check it can run and lets
  it work. It does not add "double-check" or "verify again with a sub-agent", because that buys
  extra passes and no extra correctness.

What "done" looks like depends on the kind of task:

| Task | Proof of done |
|---|---|
| Software build | commands exit 0, and the real interface is exercised: run the CLI, call the endpoint, open the page |
| Research, sourcing | every category on the coverage list is filled; each claim has a link and a date checked; conflicts are noted |
| Design, CAD, 2D or 3D | a parametric source; a script that checks rules and dimensions; the render opened and inspected |
| Document, skill, content | the required structure is present; it was tried on two or three realistic inputs |
| Data, analysis | numbers reproduced by a script; row counts and totals reconcile; real data worked on as a copy |
| Automation, recurring job | one full run end to end; a second run does no harm |

## 8. Loops

A loop goes into a prompt when "done" cannot be reached or confirmed in one pass. There are six
kinds.

| Kind | Used when | Each round | It stops when | How it reads in a prompt |
|---|---|---|---|---|
| Fix | a check can fail: tests, a build, a validator | run the check, fix the cause, rerun | every check passes | "When a check fails, fix the cause and rerun. If the same failure survives two attempts, change approach." |
| Refine | quality comes from iterating: a render, a layout, a score, a draft | produce, inspect or measure, fix the worst problem | the bar is met, or two rounds bring no gain | "Render, open the image, fix the worst problem. Stop when it reads cleanly, or after four rounds." |
| Queue | there are many items of the same shape | take the next item from a ledger file, do it, record the result | nothing is pending | "Work through items.csv one row at a time and record the result in the status column." |
| Coverage | breadth matters: research, audits | search, add to the table, go after the thinnest category | every category is filled, or two rounds add nothing new | "Find the thinnest category and run one more round for it. Stop when two rounds in a row add nothing new, or after five rounds." |
| Long-run | the work outlasts one session | read state, do the next milestone, run checks, commit, update state | the done-list holds | "After each milestone, commit and update PROGRESS.md. In a fresh session, read it first." |
| Watch | something recurs or has to be polled | read state, handle only what is new, write state | a named condition, or until cancelled | "Every 15 minutes, check the queue, handle new items only, and record what you handled." |

**Every loop names four things**, and each one prevents a specific failure:

| Part | Without it |
|---|---|
| The check that drives the loop | the agent stops when the work merely looks done |
| The exit | it stops too early, or never |
| A cap | it burns tokens going round in circles |
| Where state lives, for anything long | a fresh session cannot pick up where the last one stopped |

The prompt also tells the agent that bending a check does not count. If a check looks wrong, the
agent should say so, not edit it, skip it or hard-code the expected output.

**A task with a single pass gets no loop.** The check runs once at the end.

**Asking for a loop yourself.** Describe it and it goes in, even where the skill would have left
it out:

```text
Have it keep improving the layout until nothing overlaps.
It should check the inbox every 15 minutes until I stop it.
```

**Loop commands in Claude Code.** The loops above are written into the prompt in plain words, so
they work in any agent. Claude Code also has commands that enforce a loop from outside, and the
run notes offer one when it would help:

| Command | What it does | When the run notes suggest it |
|---|---|---|
| `/goal [condition]` | Keeps the session working until a separate evaluator agrees the condition holds | A fix or long-run loop you want to leave unattended |
| `/loop 10m [prompt]` | Reruns a prompt on an interval while the session is open | A watch loop that only needs to last a working session |
| Scheduled tasks | Run a prompt on a schedule without an open session | A watch loop that has to keep going for days |

A `/goal` line is sent after the prompt and looks like this:

```text
/goal every item under "Done when" is shown with its command output, or stop after 40 turns
```

It is written as one measurable end state, the check, and a cap. The evaluator can only read the
conversation, which is one reason the prompt asks the agent to show its output.

## 9. Sub-agents

A sub-agent is a helper with its own fresh context that returns a summary. It buys parallel work
and a clean main context. It also costs: each one starts cold, spends its own tokens, and hands
back less than it learned. Four sub-agents in parallel cost roughly four times one pass.

**When the skill delegates.** At least one of these has to hold:

| Test | Meaning | Example |
|---|---|---|
| Parallel tracks | two or more sizeable chunks that do not touch the same files and do not need each other's results | the scheduler and the web page, once the API is finished |
| Heavy reading | so much searching or reading that only the conclusion matters | understanding a large codebase before changing it |
| Fresh eyes | work that matters needs a reviewer who did not produce it | a review before a data import is declared done |
| Fan-out | the same step over many items | one track per category, competitor or file |

Otherwise the work stays in one context. For a small job the prompt says so in a line, "work
directly; this needs no sub-agents", because some agents delegate eagerly and that line saves
real cost.

**The delegation block.** When delegation is right, the prompt spells it out in six parts:

1. **The split:** named tracks, one line each, with the files or area each one owns.
2. **The brief:** a self-contained task for each sub-agent. It cannot see the conversation, so
   the lead agent passes the goal, the inputs and paths, the constraints and what to return.
3. **The return:** a compact result in a fixed shape, such as a table or a findings list, not a
   transcript.
4. **The run:** in parallel, wait for all, at most four at once by default, and one level deep.
5. **The merge:** the lead agent integrates, resolves conflicts, spot-checks the summaries and
   runs the done-list itself.
6. **The fallback:** if the agent cannot spawn sub-agents, it does the tracks one after another.

[Example 2](../examples/02-medium-research-supplier-directory.md) contains a complete block.

**Reviews.** An independent review appears in Large prompts, and at any size where a wrong result
is costly: money, data loss, safety, or a physical part that will be made. There is one review, at
the end. The reviewer is briefed narrowly. It gets the done-list and the result, runs the checks,
and reports only gaps that break correctness or a stated requirement. It gives no style notes and
adds no requirements, because a reviewer asked to find problems usually finds some, and chasing
all of them turns a finished build into an over-engineered one.

**Parallel edits to code.** Sub-agents that change the same codebase get separate worktrees or
strictly separate files. Otherwise the code changes run in sequence and only the reading is done
in parallel.

**Very large fan-outs.** Past roughly ten items of the same shape, hand-run delegation becomes
unwieldy. In Claude Code the prompt asks for a workflow and has it pilot on a small slice first, so
the cost is known before the full run.

**Deciding yourself.**

```text
Use sub-agents for the research part.
No sub-agents. Keep it in one session.
```

Either instruction goes into the prompt. When you ask for sub-agents the run notes tell you what
they will cost.

## 10. Which agent

Tell the skill where the prompt will run if you know. The prompt itself is written in plain
capability terms, so it works anywhere. The agent only decides which commands the run notes may
mention.

| Agent | What changes |
|---|---|
| Claude Code | Delegates by itself and when asked. Run notes may offer `/goal`, `/loop`, scheduled tasks, "use a workflow to…", `/batch`, `/deep-research` or `/code-review`, and auto mode for hands-off runs. |
| Codex | Spawns sub-agents when asked directly, so the prompt says how many, how the work divides, to wait for all, and what summary to return. |
| Cursor | Delegates by itself or by name, in the background or in parallel. The run notes flag that token cost scales with the number of sub-agents. |
| Claude chat | Sub-agents and scheduled tasks depend on the session, so the prompt asks for them explicitly and keeps the sequential fallback. |
| Unknown | Wording that works anywhere. Any command is offered as an optional extra. |

These notes were checked in November 2026. The products change quickly, so treat a command as a
suggestion and leave it out if your version does not have it.

## 11. Task types beyond software

The skill is not limited to code. Here is one ask of each kind and what the prompt stresses.

| Kind | An ask | What the prompt stresses |
|---|---|---|
| Software build | "A prompt to build a CLI that organises my downloads folder." | Commands that exit 0 and a real run of the tool; a fix loop |
| Research, sourcing | "A prompt to find every workshop supplier within 60 km." | A coverage list, a row format with source links and dates, parallel tracks, a coverage loop |
| Design, CAD, 2D or 3D | "A prompt for a to-scale plan of my workshop from this sketch." | A data file to draw from, a script that checks the rules, a render that gets opened and inspected; a refine loop |
| Document, skill, content | "A prompt to build a skill that turns my notes into a weekly report." | The required structure, and a trial on two or three realistic inputs; a refine loop |
| Data, analysis | "A prompt to reconcile these two exports and list the mismatches." | A script that reproduces the numbers, totals that reconcile, work on a copy of the data |
| Automation, recurring job | "A prompt for a job that checks my server every morning and messages me if something is wrong." | One full run end to end, a harmless second run, a state file; a watch loop |

## 12. Working from existing material

When there is something to build on, such as a repository, a folder, a specification or data, say
where it is. The skill grounds the prompt in it:

- it reads the few files that define the material: the readme, the manifest, the entry point, the
  specification;
- if the material is too big to skim and the session can spawn sub-agents, it sends one read-only
  explorer to report the stack, the real run and test commands, the layout and the conventions;
- the prompt then cites real paths and commands, not guesses.

It gathers facts only. Solving the task is the receiving agent's job, so the skill does not start
building your project in order to describe it.

## 13. Fixing a prompt that misbehaved

Paste the prompt and say what went wrong:

```text
This prompt made Claude Code build far more than I asked. Fix it:
[the prompt]
```

The skill diagnoses before it edits. It looks for what is missing and for what is too much,
changes as little as solves the problem, and returns the revised prompt with a three-line list of
what changed and why.

| What you saw | Usual cause | The fix |
|---|---|---|
| It built far more than asked | open-ended deliverables, stacked verification, "be thorough" | cut to the ledger; add the build-only-what's-listed line; delete the re-verify instructions |
| It stopped early and asked "want me to continue?" | no done-list, no loop | add checks and a fix or long-run loop; suggest a `/goal` line |
| It went in circles | a loop with no cap or exit | add the cap and the change-approach rule |
| It claimed success and nothing works | the checks were adjectives | checks that can be run, and "show the output" |
| It did everything in one context, slowly | delegation was never requested | add a delegation block for the parallel or read-heavy parts |
| It spawned sub-agents for trivia | the prompt invites delegation everywhere | say when not to delegate; cap the count |
| It lost the thread on a long run | state lived only in the conversation | add a progress note, a ledger, commits at milestones |

If a prompt this skill produced misbehaves, please also
[open an issue](../CONTRIBUTING.md#reporting-a-prompt-that-misbehaved). Real failures are what the
next version is built from.

## 14. Running the prompt

1. Start a fresh session in your agent, in the right folder if files are involved.
2. Attach anything the run notes tell you to attach.
3. Paste the prompt as the first message.
4. If the run notes give a command, such as a `/goal` line, send it after the prompt.

**Leaving it alone.** For a long build in Claude Code, auto mode removes the routine approvals and
a `/goal` line keeps the session going until the done-list holds or the cap is reached. Both are
optional. The prompt works without them.

**What to expect at the end.** Medium and Large prompts ask for a short report: what works, with
the evidence; what does not; and what the agent needs from you. Smaller prompts end by showing the
output of their check.

**When to expect questions from the agent.** Rarely. The prompt keeps stop-and-ask conditions few
and specific: a missing secret, a destructive or irreversible action, or a decision only you can
make. Everything else is the agent's to decide, note and move past.

**Cost.** Sub-agents multiply token use, and workflows multiply it further. The run notes say so
whenever a prompt uses them.

## 15. Phrase sheet

| You say | What happens |
|---|---|
| "Prompt forge: …", "a prompt to …", "best prompt for …" | A new prompt |
| "Prompt forge, make me …" | It asks once: a prompt, or do it here? |
| "Do it here" | It does the work in this session under the same rules |
| "Quick", "light", "full", "make it Small" | That size is used |
| "Add the …" (an item from Left out) | The extra goes into the prompt |
| "Drop the …" | The item comes out |
| "Use …, not …" | An assumption is changed |
| "Use sub-agents for …" | A delegation block is added and the cost is flagged |
| "No sub-agents" | The prompt tells the agent to work directly |
| "Keep going until …" or "check every …" | A loop is added |
| "Add a review at the end" | One narrowly briefed independent review |
| "It's for Codex" (or Cursor, Claude Code, a Claude chat) | Wording and run notes fit that agent |
| "This prompt made the agent … Fix it" | Diagnosis and the smallest repair |

## 16. Questions people ask

**The prompt looks short. Is that enough?**
Usually, yes. Current agents carry out everything a prompt says, so every extra sentence is extra
work, and some of it is work you did not want. If a run shows that something was missing, say
what, and it gets added. If you want the heavier treatment from the start, ask for "full".

**It asked whether I want a prompt or the result. Why?**
Because the ask named the thing itself and the session could have produced it. Say "a prompt to…"
or "do it here" next time and the question does not appear.

**Why were no sub-agents used?**
None of the four tests held. The work was small, or its steps built on each other. Ask for
sub-agents and they go in.

**Why was something I expected left out?**
It was not in your ask, and the ask works without it. Look under Left out and name what you want
back.

**The skill did not trigger.**
Say "prompt forge" by name, and check that the skill is switched on. A plain "build me X" with no
mention of a prompt is not meant to trigger it.

**Can I have the old, heavier style?**
Version 1.0 is kept in [`archive/v1.0/`](../archive/v1.0/README.md). Before going back, consider
asking version 1.1 for "full", or for the specific parts you miss, such as a plan file, a review
or test-first rules.

**Something in this guide is wrong.**
The skill file is the authority. Please
[open an issue](../CONTRIBUTING.md#suggesting-a-change) so the guide can be fixed.
