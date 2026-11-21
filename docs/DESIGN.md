# Design: why Prompt Forge works the way it does

This document records the reasoning behind version 1.1: what was wrong with version 1.0, what the
current documentation says about how agents behave, the principles that follow, and every design
decision with the alternatives that were rejected. It is written for the owner, for colleagues who
want to change the skill, and for future Claude sessions that are asked to build the next version.

Source numbers such as (S2) refer to [SOURCES.md](SOURCES.md). The step-by-step account of how the
work was done is in [BUILD-HISTORY.md](BUILD-HISTORY.md).

**Contents**

1. [The problem the skill solves](#1-the-problem-the-skill-solves)
2. [What version 1.0 was](#2-what-version-10-was)
3. [What went wrong with version 1.0](#3-what-went-wrong-with-version-10)
4. [What the documentation says about current agents](#4-what-the-documentation-says-about-current-agents)
5. [Principles](#5-principles)
6. [Decisions](#6-decisions)
7. [Considered and rejected](#7-considered-and-rejected)
8. [Known limits](#8-known-limits)
9. [How to challenge a decision](#9-how-to-challenge-a-decision)

---

## 1. The problem the skill solves

A person has a rough idea and an autonomous agent that could carry it out. Between the two sits
the prompt. A prompt that is too thin gets a plausible half-result with no proof that it works. A
prompt that is too heavy gets a result buried under features, files and verification that nobody
asked for, at many times the cost.

Prompt Forge exists to write the prompt that sits between those failures: the smallest one that
still gets the result proven.

## 2. What version 1.0 was

Version 1.0 produced "build prompts" for software projects. Its description excluded any prompt
that was not about building software.

| Aspect | Version 1.0 |
|---|---|
| Method | Three moves: Understand, Forge, Deliver |
| Files | `SKILL.md`, plus `references/anatomy.md` and `references/example.md`, which the skill told Claude to read before every forge |
| Size loaded per forge | 4,933 words across 496 lines |
| Structure of every prompt | A "non-negotiable spine" of four elements at every size: a mission and autonomy frame, a Definition of Done restated as a live checklist, a build loop with test-first, and stop conditions with a final report |
| Section palette | 15 numbered sections (0 to 14) in `anatomy.md` |
| Sizes | Small, Medium, Large. Small was described as "one or two pages". |
| Sub-agents | An independent verifier sub-agent, presented as the most valuable reliability component and mentioned eight times across the three files |
| Loops | One: the build loop, ending on "repeated no-progress" |

The complete version 1.0 is kept in [`archive/v1.0/`](../archive/v1.0/README.md).

## 3. What went wrong with version 1.0

The owner asked for this version with three observations: the skill has limitations, it sometimes
overdoes things, and it does not use sub-agents or loops when they are needed. The audit confirmed
all three and found the causes in the text of the skill.

### 3.1 Evidence in the files

- **The framing pushed towards the maximum.** The description promised the "single best possible"
  prompt. The body spoke of the "most advanced techniques", of a "non-negotiable spine", and said
  "Your job is to make skipping impossible."
- **The smallest size was not small.** A one-file script still got "one or two pages".
- **The skill already said "right-size it".** The instruction was there and did not work, because
  nothing made it checkable. There was no budget, and no rule that tied a deliverable to the ask.
- **Its own worked example overbuilt.** The brief was a command-line tool that organises a folder
  by type and date, in Python, that never loses a file. The example prompt was 519 words in eight
  numbered sections. It added a dry-run mode, an undo command, a JSON-lines move log, lint and
  type-check gates, a README, test-first rules, a restated checklist and an independent check. The
  brief asked for none of them.
- **Reading the heavy material was compulsory.** "Read it now" loaded the full 15-section palette
  and a "gold standard" example before every forge, including forges for trivial asks. A writer
  who has just read a complete palette tends to use it.
- **Sub-agents had one role.** They appeared as a verifier, and once as a passing suggestion for
  investigating many files. Nothing said when delegation pays off, how to brief a sub-agent, what
  it costs, or what to do without one.
- **There was one loop, with a vague exit.** "Repeated no-progress" has no number. There was no
  loop for refining quality, for working through many items, for covering a research field, for
  work that outlasts a session, or for recurring jobs.
- **Product details were part of the method.** The text named a specific to-do tool, a settings
  file with a stop hook, and model aliases. Details like these age quickly.

### 3.2 Evidence from real use

Five earlier uses of version 1.0 were reviewed. They are described here without personal detail.

| The ask | What version 1.0 produced | The problem |
|---|---|---|
| Map every supplier of tools and workshop machines in a city | Claude had to say that the skill was built for software prompts and adapt its method by hand | The skill's own description put the ask out of scope |
| A travel-planning question sent under the skill's name | Plain research; the skill added nothing | No route for an ask that is not a request for a prompt |
| A printable mechanical adapter | A build prompt with a verifier sub-agent, a parameter table, ordered slices and a two-stage flow for physical measurements | Sound ideas, such as having the user measure before the design is final, but heavy by default |
| A skill that turns an assignment brief into a document | A full folder structure, seven checker scripts and a nine-phase workflow. The owner rejected it and asked for a rebuild around "paste the brief, get the document". | Scope inflation: the forger designed a system when the ask was a simple flow |
| A to-scale 2D site plan from a rough sketch | A prompt of about 2,000 words that required a JSON source of truth, tests for ten rules, a DXF export, and PDF, SVG and PNG renders. The forging session also worked out much of the layout itself before writing the prompt. | The ask was one drawing. Extras became deliverables, and the forger did the project in order to describe it. |

### 3.3 Root causes

| Symptom | Cause in version 1.0 | Answer in version 1.1 |
|---|---|---|
| Prompts too long for small asks | A fixed four-part spine at every size; the smallest size was one or two pages | Four sizes with word ceilings, starting at a paragraph ([D03](#d03-four-sizes-with-word-ceilings), [D04](#d04-a-three-part-spine)) |
| Deliverables nobody asked for | Nothing tied a deliverable to the ask | The scope ledger ([D02](#d02-the-scope-ledger)) |
| Agents over-build and over-verify | Verification stacked on verification; wording tuned for models that needed pushing | One check, one optional review, calm tone ([D05](#d05-a-check-not-a-pile-of-verification), [D11](#d11-calm-wording-and-scoped-rules)) |
| Heavy output whatever the ask | Compulsory reading of the full palette | One file with no compulsory extras ([D01](#d01-one-self-contained-file)) |
| No delegation | Sub-agents framed only as a verifier | Four tests and a six-part block ([D07](#d07-sub-agents-on-purpose)) |
| Loops that stop early or never stop | One loop kind, an exit with no number, no state | Six kinds, four required parts ([D06](#d06-six-loops-four-parts-each)) |
| Non-software asks not served | The description excluded them | Six task types ([D09](#d09-task-types-beyond-software)) |
| Advice that ages | Product details inside the method | Capability-first wording, dated agent notes ([D08](#d08-capability-first-commands-second)) |
| The result was wanted, a prompt was delivered | No routing | The Route step ([D10](#d10-route-first-prompt-or-result)) |

## 4. What the documentation says about current agents

The design leans on what Anthropic, Cursor and OpenAI publish about their own agents. Each finding
below is paraphrased; the pages are listed in [SOURCES.md](SOURCES.md) with the date they were
read.

| Finding | Source | What it changed |
|---|---|---|
| Recent models respond strongly to the prompt, so forceful wording that older models needed now causes over-application. Words like "never" are taken as absolute. | S1, S3 | Calm tone and scoped rules ([D11](#d11-calm-wording-and-scoped-rules)) |
| Left alone, recent models add files, abstractions and flexibility that were not requested. The recommended counter is an explicit instruction to keep to the request. | S1 | The "build only what's listed" line in every prompt ([D04](#d04-a-three-part-spine)) |
| For the newest Opus-class models, instructions such as "add a final verification step" or "verify with a sub-agent" cause wasted effort and should be removed. The models work best when given the whole specification up front and left to run. | S2 | Give a check and let the agent work; give the full specification at the start ([D05](#d05-a-check-not-a-pile-of-verification)) |
| The same guidance suggests telling the model to deliver what was asked at the scope intended, and to raise a better idea in a sentence without acting on it. | S2 | "Mention other ideas at the end instead of building them" |
| Models can delegate too much or too little. The advice is to say when delegation is worth it, when it is not, what it costs, and how to brief a sub-agent. | S1, S2, S3 | The four tests, the "work directly" line and the delegation block ([D07](#d07-sub-agents-on-purpose)) |
| A sub-agent receives its task message and not the conversation. It returns a summary, and it spends its own tokens. | S4, S13 | The brief, the return and the merge parts of the delegation block |
| Codex spawns sub-agents when it is asked to. | S14 | Delegation is always written out explicitly |
| A single agent often does better than a multi-agent design on quality, cost and speed, and a design should start from the simplest pattern that could work. | S12 | One context is the default; delegation has to pass a test |
| A loop needs a stop condition that can be verified and an explicit cap, and the simplest mechanism that fits should be chosen. | S11, S6 | The four parts every loop names ([D06](#d06-six-loops-four-parts-each)) |
| The `/goal` evaluator judges the condition from the conversation alone. It does not run commands or read files. | S7 | Prompts ask for output to be shown; goal lines are written as a measurable end state with a cap |
| For long work: structured state in files, free-form progress notes, and git as the checkpoint. | S1 | The state part of the long-run loop |
| Giving the agent a check it can run is the most valuable thing a prompt can contain. | S9 | The done-list carries most of the weight ([D05](#d05-a-check-not-a-pile-of-verification)) |
| A reviewer that is asked to find gaps usually reports some, and chasing all of them leads to over-engineering. | S9 | The narrow reviewer brief |
| After a long session is compacted, Claude Code keeps roughly the first 5,000 tokens of each invoked skill. | S10 | The order of the file ([D18](#d18-the-order-of-the-file)) |
| An uploaded skill may carry only a short list of keys at the top of `SKILL.md`. | S10 | The version lives under `metadata` ([D20](#d20-the-version-number)) |

## 5. Principles

1. **The smallest prompt that still gets the result proven.** Every sentence in a prompt is work
   the agent will do.
2. **Nothing goes in without an owner in the ask.** A deliverable or a check has to trace to
   something the user said, or to something that request cannot succeed without.
3. **A check beats an instruction.** Agents steer by what they can run. A rule becomes real when
   it is a check.
4. **Loops and sub-agents have a price.** They are used on purpose, and each comes with its exit,
   its cap, its brief and its fallback.
5. **Explain, do not shout.** A reason lets the agent make the small decisions itself. Capitals
   and absolutes make it over-apply.
6. **Capability first, commands second.** The prompt says what to do in plain words that work in
   any agent. Product commands are optional extras in the run notes.
7. **One file.** The skill has to survive being updated through a chat review card.

## 6. Decisions

Each decision gives the context, what was decided, what else was considered, and what it costs.

### D01 One self-contained file

**Context.** Version 1.0 was three files, and reading two of them was compulsory. In the Claude
apps a skill is updated from a chat through a review card, and that card can replace `SKILL.md`
only.

**Decision.** Everything the skill needs is in `SKILL.md`. The text retires the version 1.0
reference files by name, so a copy that still has them does not load them.

**Considered.** Keeping reference files and using progressive disclosure, which is the usual
advice for skills: a short main file that points to detail on demand. It was rejected for two
reasons. Reference files cannot be updated through the card, so they would drift out of date. And
compulsory reading of a large palette was itself a cause of the overbuilding.

**Cost.** The file is long: 438 lines and an estimated 6,300 tokens at the 1.1 release. The order
of the file ([D18](#d18-the-order-of-the-file)) and the use of tables keep it usable.

**Revisit when** skills can be updated with several files from a chat, or the file approaches 500
lines.

### D02 The scope ledger

**Context.** Version 1.0 told the writer to right-size. That did not prevent a request for one
drawing from becoming a package with five export formats.

**Decision.** Before writing, sort everything into Asked, Needed and Extras. Only Asked and Needed
go into the prompt. Needed entries carry their reason, and the test is strict: if the Asked items
would succeed without it, it is not Needed. The best two or three Extras are offered after the
prompt, a line each.

**Considered.** A stronger exhortation to stay small, which is what version 1.0 already had. A
hard limit on the number of deliverables, which is arbitrary. The ledger was chosen because it
turns "do not overbuild" into something that can be checked: every deliverable and every check
must have an entry.

**Cost.** A useful extra now waits for the user to ask. That is intended. Offering it in a line
costs the user one word; building it unasked can cost hours.

### D03 Four sizes with word ceilings

**Context.** Version 1.0 had three sizes and the smallest was one or two pages.

**Decision.** Micro, Small, Medium and Large, with ceilings of 150, 350, 800 and 1,600 instruction
words. The smallest size that fits is used, and between two sizes the smaller wins. Data and
specifications supplied by the user do not count. A prompt may exceed its ceiling only when the
writer can name the failure each extra block prevents. The user can name a size.

**Considered.** A single hard limit, rejected because large tasks need room. No numbers, rejected
because that is what version 1.0 did. Counting everything including user data, rejected because it
would push the writer to drop the user's own specification.

**Where the numbers come from.** They are judgment calls, checked against six prompts: the two
complete examples inside the skill (95 and 235 words) and the four dry runs. Among the dry runs, a
tiny script came to 97 words, a file organiser to 293, a research sweep to 554 and an unattended
app build to 768. Each sat inside its size with room to spare, except the app build, which is close
to the Medium ceiling. The numbers have not been tuned on a larger set. See
[Known limits](#8-known-limits).

**How words are counted.** Every count in this repository splits the text on whitespace, so a
free-standing dash, bullet or heading mark counts as a word. The figures are therefore slightly
generous, and they are consistent with each other because the checks use the same counter.

### D04 A three-part spine

**Context.** Version 1.0 required four heavy elements in every prompt, including a restated
checklist and a test-first build loop.

**Decision.** Every prompt has three things, in as few words as its size allows: a Goal with the
reason behind it, a Done-when list with evidence to show, and Boundaries. Everything else is added
only when it applies: context, ordered requirements, milestones, loop and delegation blocks, honest
limits, and a closing report.

**Considered.** Keeping the four-part spine and shrinking each part. It was rejected because the
parts themselves, not their length, made small prompts heavy. A paragraph cannot carry a restated
checklist and a test-first loop.

**Why the reason is part of the Goal.** An agent that knows what the result is for makes the many
small decisions itself, and makes them well.

### D05 A check, not a pile of verification

**Context.** Version 1.0 stacked several layers: test-first, pasted output for every step, a
verifier sub-agent and a stop hook. Current guidance says this now causes over-verification
(S2), while a single check the agent can run remains the most valuable thing a prompt can hold
(S9).

**Decision.** The done-list carries the weight. Each item is something the agent can run or look
at and then show, and each belongs to a ledger entry. Rules that must always hold become checks.
The prompt does not add "double-check" or "verify again". An independent review appears only in
Large prompts, or at any size where a wrong result is costly, and there is exactly one, at the
end. The reviewer gets the done-list and the result, and reports only gaps that break correctness
or a stated requirement.

**Considered.** A verifier for every non-trivial prompt, as in version 1.0. No review at all,
rejected because some results are expensive to get wrong: a data import, money, safety, a part
that will be manufactured.

**Cost.** A Small or Medium prompt relies on the agent running its own checks and reporting them
truthfully. The requirement to show the output is the safeguard.

### D06 Six loops, four parts each

**Context.** One loop kind could not describe a design that improves by iteration, a research
sweep, a queue of items, a multi-day build or a recurring job. And a loop with no numbers either
stops early or never stops.

**Decision.** Six kinds: fix, refine, queue, coverage, long-run and watch. Every loop written into
a prompt names its check, its exit, its cap and, for anything long, where its state lives. The
default cap for a fix loop is: the same failure twice means a change of approach, and three
approaches mean stop and report what is still failing with the real output. A task with a single
pass gets no loop.

**Considered.** A general "keep going until done" instruction, rejected because it is the vague
exit again. Relying on product commands such as `/goal` alone, rejected because they exist in one
agent and are typed by the user, so they cannot be part of a pasted prompt. The loops are written
in plain words so they work anywhere, and the commands are offered as optional reinforcement.

**Why the change-approach rule.** Repeating a fix that has already failed twice fills the context
with failed attempts. The guidance for people is the same: after two failed corrections, start
again with a better approach (S9).

### D07 Sub-agents on purpose

**Context.** Sub-agents give parallel work and a clean context, and they cost tokens, start
without context and return a summary that loses detail. Some agents delegate too readily and some
only when asked (S2, S3, S14).

**Decision.** Delegation has to pass one of four tests: parallel tracks, heavy reading, fresh eyes
or fan-out. When it does, the prompt writes a block with six parts: the split, the brief, the
return, the run, the merge and the fallback. The default is at most four at once and one level
deep. When it does not, a small job gets a line telling the agent to work directly. If the user
asks for sub-agents outright, they are included and the cost is flagged.

**Considered.** Leaving delegation to the agent, rejected because behaviour differs between agents
and because agents split work better when told how. Mandatory delegation for anything large,
rejected because a single context often does better (S12). Nested teams, rejected for cost and
because one level is enough for every case reviewed.

**Why the fallback is always written.** The prompt may be pasted into an agent that cannot spawn
sub-agents. Without the fallback it would stall or improvise.

**A change made during the build.** The first draft required three or more chunks for the
parallel-tracks test. One of the skill's own examples then delegated two tracks, which
contradicted the rule. The rule was changed to two or more sizeable chunks, because size and
independence matter more than the count.

### D08 Capability first, commands second

**Context.** Version 1.0 named specific tools inside its method. Agent products change every few
weeks.

**Decision.** Prompts are written in terms of what the agent can do: run code, browse, spawn
sub-agents, keep going unattended. Product commands are confined to one section, "Agent notes",
which carries the date it was checked. A command is offered only in the run notes, as an optional
extra, and is left out when there is doubt that it exists.

**Considered.** A separate variant of the prompt for each agent, rejected as three times the
maintenance for little gain. No commands at all, rejected because `/goal` and similar are useful
for unattended runs.

### D09 Task types beyond software

**Context.** Most of the real uses reviewed were not software builds.

**Decision.** One table maps six kinds of task to their proof of done, their usual loop, and where
sub-agents pay off: software, research and sourcing, design and CAD, documents and skills, data,
and recurring automation.

**Considered.** A separate skill for each kind, rejected because the method is the same and the
difference fits in one table row.

### D10 Route first: prompt or result

**Context.** Two of the five reviewed uses were asks for the thing itself, sent under the skill's
name. One received a 2,000-word prompt when the user wanted a drawing.

**Decision.** The first step settles whether the user wants a prompt or the result. When the ask
names the thing itself and the session could produce it, the skill asks once. If nobody can
answer, it delivers the prompt and offers to run it. When the work is done in the session, the
same brief is written as the plan and carried out under the same rules.

**Considered.** Always delivering a prompt, which repeats the observed failure. Deciding silently,
rejected because the owner prefers a confirmation to a silent assumption.

**Cost.** One extra question in ambiguous cases. Saying "a prompt to…" or "do it here" avoids it.

### D11 Calm wording and scoped rules

**Context.** Recent models over-apply forceful wording, and they treat absolutes as absolute (S1,
S3).

**Decision.** Prompts are written in the second person, plainly, with the reason attached to
anything demanding. Scoped rules replace blanket bans: "ask before deleting or overwriting
anything outside the project folder" in place of a list of things never to do. Stop-and-ask
conditions are few and specific. The skill file is written the same way, and a check fails if a
shouted mandate appears in it.

**Considered.** Keeping emphasis for the truly critical rules. Where a rule is truly absolute,
such as never overwriting a user's file, the word "never" is still used. It is used rarely so that
it keeps its meaning.

### D12 Questions, assumptions and named inputs

**Context.** Version 1.0 listed twelve dimensions to gather. The owner prefers that nothing is
assumed silently, and also prefers not to be questioned when it is not needed.

**Decision.** A question is asked only when the answer would change what gets built, with at most
three in one batch and normally none for Micro or Small prompts. Anything the skill settles that
changes the result is listed as an assumption. Values that only the user has, such as measurements
and credentials, become named inputs that the agent asks for and does not invent. Real secrets
stay out of the prompt.

**Considered.** A fixed interview, rejected as friction. No questions at all, rejected because
some answers change the whole build.

### D13 The forge tests its own draft

**Context.** Version 1.0 ended with "read it once with fresh eyes". The author of a text reads
what they meant, not what they wrote.

**Decision.** For Medium and Large prompts the skill reads the draft as the receiving agent, from
the text alone, with five questions: what would you deliver, what is ambiguous or missing, what
looks unnecessary, what are your first three actions, and when would you stop. For a Large prompt,
or one that will run unattended for hours, it gives the same questions and only the prompt text to
a fresh sub-agent when it can spawn one. There are at most two rounds.

This is the skill using a sub-agent and a loop in its own process, with the same discipline it
asks of the prompts it writes: a check, an exit and a cap.

**Evidence that it works.** During the build, the self-read of a Medium draft caught two problems:
a documentation check that nobody had requested, and a requirement the agent could not have met
without guessing. That result is why the self-read applies to Medium prompts and not only to Large
ones. See [BUILD-HISTORY.md](BUILD-HISTORY.md#step-5-dry-runs).

**Cost.** One sub-agent for the largest prompts. Micro and Small prompts skip the step.

### D14 A fixed delivery format

**Decision.** One line, the prompt in a single copyable block, run notes of at most five lines,
then up to three assumptions and up to three left-out extras. Nothing more.

**Why.** Earlier answers arrived with long explanations and menus of variants. The caps apply the
skill's own rule to its own output. The copyable block matters on a phone, where plain text has no
copy button.

### D15 Repairing an existing prompt

**Decision.** Diagnose what is missing and what is too much, change as little as solves it, and
return the revised prompt with three lines on what changed. A table maps seven symptoms to their
usual cause and fix.

**Why a table.** The owner's complaints about version 1.0 were symptoms of this kind: it overbuilt,
and it did not delegate. The same table that fixes other people's prompts is a checklist for this
skill's own output.

### D16 Examples inside the skill

**Decision.** Four short examples: a complete Micro prompt, a complete Small prompt, and two "How
to work" blocks that show a loop and delegation written out. The two complete prompts show the ask
that produced them.

**Why the ask is shown.** The first draft of the Micro example included a dry-run flag with no ask
shown. It looked as though dry-run modes were standard, which is exactly the kind of extra the
ledger is meant to stop. Showing the ask makes it visible that every item in the prompt traces to
it.

**Why they are generic.** Examples steer strongly. Examples taken from one person's projects would
pull every later prompt towards those projects.

### D17 What was removed from version 1.0

| Removed | Why |
|---|---|
| Compulsory reading of the palette and the example | It primed heavy output on every forge |
| The four-part spine at every size | It made small prompts large |
| A project harness by default: memory file, settings, hooks, custom agents, project skills | Needed only for work that spans sessions, or on request |
| Test-first as a default | Kept only where the logic is not trivial and a test is the natural check |
| A named to-do tool, model aliases, swapping in the run date | Product details that age; the date is given only when recency matters |
| A closing offer of variants and tailoring | Replaced by the user naming a size or an extra |
| A "kickoff line" telling the agent where to start | Agents do not need it |

Nothing that protected the user was removed. Reading prior material first, honest limits when the
build and deploy environments differ, treating outside content as data, working on a copy of real
data, and the honest closing report are all still in the skill.

### D18 The order of the file

**Context.** Claude Code keeps roughly the first 5,000 tokens of an invoked skill once a long
session has been compacted (S10).

**Decision.** The method comes first: Route, Scope, Size, Shape and Write end at an estimated
4,500 tokens. The agent notes, the repair table and the examples follow. If the tail is dropped
after compaction, the method survives. A check enforces the order and the estimate.

### D19 The description and its triggers

**Decision.** The description names what the skill makes, the kinds of task, the phrases that
should trigger it, the repair use, and what should not trigger it. It includes "prompt fort",
because dictation writes the name that way.

**Considered.** A short description, rejected because the description is what decides whether the
skill is used, and Claude tends to under-use skills. A plain request to do a task is excluded so
the skill does not appear where no prompt is wanted.

**Not yet done.** The trigger accuracy has not been measured. See [Known limits](#8-known-limits).

### D20 The version number

**Decision.** This release is 1.1. The owner asked for that number in place of 2. It fits: the
name, the purpose and the way the skill is invoked are unchanged, and a 2.0 is reserved for a
change of method. The number is stored in `VERSION`, under `metadata.version` at the top of
`SKILL.md`, and in the first paragraph of the skill text.

**Why three places.** The review card keeps only the name and description from the top of the
file, so the number in the body is the one that survives every install route. The `metadata` entry
is the standard place and survives a zip upload. A check keeps the three in step.

## 7. Considered and rejected

| Idea | Why it was not adopted |
|---|---|
| A hard word limit for every prompt | Large tasks need room; ceilings with an escape hatch keep the pressure without the damage |
| Always including a verifier sub-agent | Over-verification and cost; see [D05](#d05-a-check-not-a-pile-of-verification) |
| Always asking which agent will run the prompt | One more question on every forge; capability-first wording makes it unnecessary |
| Doing the task without asking when the ask names the thing itself | A silent assumption; see [D10](#d10-route-first-prompt-or-result) |
| Putting `/goal` inside the prompt | It is a command the user types, and it exists in one agent |
| A bundled script that counts the words of each prompt | It would need code execution on every forge; an estimate is enough, and the repository checks the examples exactly |
| A separate prompt variant for each agent | Three times the maintenance; the fallback line covers the difference |
| Keeping the version 1.0 "gold standard" as the template for Large prompts | It primes heavy output; Large is defined by what it adds |
| Splitting the skill into one file per task type | Cannot be updated through the review card; see [D01](#d01-one-self-contained-file) |
| Calling the release 2.0 | See [D20](#d20-the-version-number) |

## 8. Known limits

These are stated plainly so that nobody mistakes the current evidence for more than it is.

- **No independent evaluation yet.** The four dry runs were written by the same session that wrote
  the skill. That is a sanity check, not a test.
- **No end-to-end runs.** None of the forged prompts has been executed by a coding agent. The
  claim that version 1.1 prompts lead to better runs rests on the documentation and on the
  before-and-after comparison, not on measured outcomes.
- **Trigger accuracy is unmeasured.** The description was written with care and not tested against
  a set of should-trigger and should-not-trigger asks.
- **The numbers are judgment calls.** The ceilings, the default of four sub-agents, and the caps of
  two attempts and three approaches were chosen by reasoning and checked on six prompts.
- **The agent notes will age.** They were checked in November 2026.
- **The file is long.** It is one file for good reasons, and it is near the size where a skill
  becomes harder to follow.
- **The examples are few.** Four cases cannot cover six task types and four sizes.

[MAINTAINING.md](MAINTAINING.md#testing-properly) describes the evaluation that would close the
first three gaps.

## 9. How to challenge a decision

Bring a case. The most useful challenge is an ask, the prompt the skill produced, and what the
agent did with it. With that in hand, find the decision above that produced the behaviour, read
what was considered, and propose the smallest change. [MAINTAINING.md](MAINTAINING.md) has the
procedure, and [CONTRIBUTING.md](../CONTRIBUTING.md) has the issue template.

A decision should not be reversed on taste alone. Each one was made in response to a failure that
was observed, and reversing it without new evidence invites the failure back.
