# Build history: how version 1.1 was made

This is the account of the work, in the order it happened: what was asked, what was examined, what
was read, how the draft changed, how it was checked, and what was not done. The reasons behind the
design are in [DESIGN.md](DESIGN.md). This file is the record of the process, so that the next
person or the next Claude session can repeat it, improve on it, or see where it was weak.

| | |
|---|---|
| Date | 21 November 2026 |
| Built by | Claude (Fable 5.2), working with the owner of the skill in a Claude chat |
| Starting point | Version 1.0, as installed in the owner's account |
| Result | Version 1.1: one `SKILL.md` of 438 lines, plus this repository |

**Contents**

- [The request](#the-request)
- [Step 1: Audit](#step-1-audit)
- [Step 2: Research](#step-2-research)
- [Step 3: First draft](#step-3-first-draft)
- [Step 4: Revisions](#step-4-revisions)
- [Step 5: Dry runs](#step-5-dry-runs)
- [Step 6: Mechanical checks](#step-6-mechanical-checks)
- [Step 7: Delivery](#step-7-delivery)
- [Step 8: The repository](#step-8-the-repository)
- [What was not done](#what-was-not-done)
- [What to do differently next time](#what-to-do-differently-next-time)

---

## The request

The owner asked for the skill to be upgraded and named three things: look at its limitations; it
sometimes overdoes things; and it does not use sub-agents or loops when they are needed.

A second request followed: put the result on GitHub with full documentation for the owner, for
colleagues and for future Claude sessions, explain in detail how it was built and why, and number
the release 1.1.

## Step 1: Audit

**The files.** All three files of version 1.0 were read in full: `SKILL.md` (1,911 words),
`references/anatomy.md` (1,822 words) and `references/example.md` (1,200 words). Because the skill
told Claude to read both reference files before every forge, all 4,933 words were in play each
time.

A search for the wording that drives behaviour found the maximal framing described in
[DESIGN.md](DESIGN.md#31-evidence-in-the-files): "single best possible", "most advanced",
"non-negotiable", "make skipping impossible" and "read it now".

**The skill's own example.** The worked example in `references/example.md` was measured against
the brief it claimed to answer. The prompt was 519 words and contained eight items the brief never
mentioned.

**Real use.** Five earlier conversations in which the owner used the skill were reviewed. In one
the skill declared itself out of scope, in one it contributed nothing, in one it was heavy but
sound, in one the output was rejected and rebuilt, and in one a request for a single drawing
produced a 2,000-word specification. The cases are tabulated in
[DESIGN.md](DESIGN.md#32-evidence-from-real-use).

**What the audit changed.** Before it, "overdoing" could have meant long answers. After it, the
cause was specific: nothing in version 1.0 tied a deliverable to the ask, and the compulsory
reading primed heavy output. That pointed at a mechanism, the scope ledger, and not at a stronger
request to be brief.

## Step 2: Research

The owner's second and third points concern features of agent products that change every few
weeks, so nothing about them was taken from memory. Eighteen sources were read on the day; they are
listed with links in [SOURCES.md](SOURCES.md). The main lines of enquiry:

| Question | Where the answer came from |
|---|---|
| How do current models react to forceful prompts, long verification instructions and open scope? | Anthropic's prompting guides, including the pages for the newest models |
| When do sub-agents help, what do they receive, and what do they cost? | The sub-agent documentation for Claude Code, Cursor and Codex, and Anthropic's article on when not to use them |
| What kinds of loop exist, and what makes one stop correctly? | Anthropic's article on loops, and the Claude Code pages on `/goal`, `/loop`, scheduled tasks and workflows |
| What does a prompt need most? | Claude Code's best-practice guide: a check the agent can run |
| What limits apply to a skill file? | Claude Code's skills documentation and Anthropic's skill-creator skill |

Two findings reshaped the plan.

1. **The heavy style of version 1.0 is now counter-productive.** It was written for models that
   had to be pushed. The current guidance says to remove stacked verification and soften forceful
   wording, because recent models over-apply both. So the overbuilding was not only a matter of
   length. The style itself had to change.
2. **Loop commands cannot live inside a prompt.** `/goal` and `/loop` are typed by the user, in one
   product. So loops had to be written into the prompt in plain words that work anywhere, with the
   commands offered separately in the run notes.

## Step 3: First draft

The first draft was written as one file in five steps: Route, Scope, Size, Shape, Write. Three
structural choices were made before any text:

- **One file.** The chat review card can replace `SKILL.md` only
  ([D01](DESIGN.md#d01-one-self-contained-file)).
- **Tables for anything the reader scans.** The sizes, the task types, the loops and the repair
  symptoms are tables.
- **A reason attached to every rule.** Anthropic's skill-writing guidance says a model follows an
  explained rule better than a bare one. Each loop part, for example, is listed with the failure
  it prevents.

The first draft was 425 lines.

## Step 4: Revisions

The draft was read again as a fresh reader would read it, and against the old file, and it changed
in these ways.

| Change | What prompted it |
|---|---|
| The parallel-tracks test went from "three or more chunks" to "two or more sizeable chunks" | One of the skill's own examples delegated two tracks, which contradicted the rule. Size and independence matter more than the count. |
| The self-read was extended from Large prompts to Medium ones | A dry run showed the self-read catching real problems in a Medium prompt (see Step 5) |
| The two complete examples gained a line showing the ask | The Micro example included a dry-run flag with no ask in sight, which made an extra look standard |
| A sentence was added on things the agent cannot see: sketches, files, earlier chat | In one reviewed use, the forging session solved the layout itself because the receiving agent would not have seen the sketch |
| "Real secrets stay out of the prompt" was added | Named inputs often are secrets |
| The trigger description gained "prompt fort" | Dictation writes the skill's name that way |
| Tappable choices for questions, and units, currency and locale under Context | Both were in version 1.0 and worth keeping. They were found when the old file was compared once more before delivery. |
| Wordier passages in the Route step and the agent notes were tightened | The skill's own Cut pass, applied to the skill |

## Step 5: Dry runs

Four asks were run through the draft by following the skill by hand: a tiny script, a research
sweep, an unattended app build, and the brief from the version 1.0 example. The four results are
in [`examples/`](../examples/README.md).

| Ask | Size | Words | Loop | Sub-agents |
|---|---|---|---|---|
| A script that converts HEIC photos to JPG | Micro | 97 | none | none |
| A directory of every tool and workshop supplier in a city | Medium | 554 | coverage | four parallel tracks |
| A home maintenance tracker, left to run unattended | Medium | 768 | fix and long-run | none for the build; one review at the end |
| A folder organiser that never loses a file (the version 1.0 brief) | Small | 293 | fix | none |

**The before and after.** On the same brief, version 1.0's prompt was 519 words with eight
unrequested items, and version 1.1's was 293 words with none. The safety requirement was not
weakened. It became a comparison of file counts and checksums that the agent has to show.

**What the self-read caught.** The app-build prompt was read as the receiving agent would read it,
using the five questions from the skill's Test step. It found two faults:

- The done-list asked for backup and restore instructions in the readme. Nobody had asked for
  them. It was an extra that had slipped past the ledger, and it was cut.
- The requirements said car maintenance is due by kilometres or months, and gave the agent no way
  to learn the odometer reading. The agent would have had to invent one. The requirement was
  completed.

This is the evidence behind extending the self-read to Medium prompts.

**The limit of these runs.** The same session wrote the skill and ran it, with the reasoning behind
every rule fresh in its context. An independent run would not have that advantage. These runs show
that the rules can be followed and that the sizes are achievable. They do not show how a fresh
session behaves.

## Step 6: Mechanical checks

Scripts were written to check what can be checked without judgment. They are in
[`tests/`](../tests), and a workflow runs them on every pull request and on every push to the main
branch.

| Check | What it guards |
|---|---|
| The top of the file parses, and holds only keys an upload accepts | An install that fails |
| The description is at most 1,024 characters and has no angle brackets | An install that fails |
| The version matches in `VERSION`, in the metadata and in the body, and the changelog has an entry | Version drift |
| The file is under 500 lines, with balanced code fences and no stray whitespace | A file that is hard to follow or renders badly |
| The method ends before an estimated 5,000 tokens | Losing the method when a long session is compacted |
| The examples inside the skill fit their own sizes | A skill that breaks its own rules |
| No shouted mandates | The tone the skill asks for |
| The ledger, the four sizes, the six loops, the four loop parts, the four delegation tests and the six-part block are all present | An edit that silently removes a feature |
| Each prompt in `examples/` fits its size, has its sections and its done-list, and has every part of any loop or delegation block it declares | Examples that drift from the rules |
| The word counts quoted in the documentation match the files | Stale numbers |
| Every relative link and anchor in the documentation resolves | Broken documentation |

One more check was made by hand for the delivery. The text passed to the review card was written
to a file first and compared byte for byte with the validated skill file.

## Step 7: Delivery

The skill was delivered as a review card in the chat, which the owner saves to replace the
installed version. The card first refused the update because it required the current file to be
shown in the conversation. That prompted one more comparison with version 1.0, which is where the
last two items in the revision table came from.

## Step 8: The repository

The repository was built in the same session. The owner created the repository, because the
session was not permitted to create one. The work was done on a branch and proposed as a pull
request, because the repository already had a first commit on its main branch.

The release was renumbered from the working label to 1.1 at the owner's request
([D20](DESIGN.md#d20-the-version-number)). Version 1.0 was archived unchanged.

Two workflows were added. One runs the checks on every pull request and on the main branch. The
other publishes a release when a version tag is pushed, building the zip from the tagged source so
that the download always matches the tag.

## What was not done

- **No independent evaluation.** The standard method for testing a skill is to run a set of asks
  in fresh sessions, with and without the skill, and compare the results. It was not run. The
  session was not asked to start sub-agents for its own work, and it did not start any.
- **No end-to-end runs.** None of the four prompts was executed by a coding agent.
- **No trigger test.** The description was not measured against asks that should and should not
  trigger the skill.
- **No comparison across agents.** The notes for Cursor and Codex come from their documentation.
  Nothing was run in either.
- **A small sample.** Four dry runs cover three of the four sizes and two of the six task types.

Each of these is a task for the next version. [MAINTAINING.md](MAINTAINING.md#testing-properly)
describes how to do them.

## What to do differently next time

1. **Run the independent evaluation before releasing.** It is the largest gap.
2. **Save the failing cases as they happen.** This build had to reconstruct five uses from old
   conversations. An issue filed at the time, with the ask, the prompt and the outcome, would be
   better evidence.
3. **Execute at least one Medium prompt end to end**, and compare what the agent built with the
   ledger.
4. **Re-read the product documentation first.** The agent notes were correct on the day and will
   not stay that way.
