<!-- example: tier=Small loop=fix delegates=no review=no -->
# Example 4: version 1.0 and version 1.1 on the same request (Small)

## The ask

> Write me a prompt for Claude Code to build a CLI tool that watches a folder and auto-organizes files into subfolders by type and date. Python. Should be safe — never lose a file.

## What Prompt Forge returns

Small prompt, about 290 words: builds the organiser. A fix loop; no sub-agents.

````text
# FileTidy — folder organiser CLI

## Goal
Build a Python command-line tool that keeps a folder tidy by moving each file into a subfolder by type and month. It will run on my real files, so the thing that matters most is that no file is ever lost or overwritten.

## Requirements
1. `filetidy FOLDER` moves every file in the folder's top level to FOLDER/Category/YYYY-MM/, where Category comes from the extension (Images, Documents, Audio, Video, Archives, Code, Other) and the month from the file's modified time.
2. `filetidy FOLDER --watch` keeps running and organises new files as they arrive, waiting until a file has stopped growing before it moves it.
3. Safety: never overwrite (on a name clash add " (1)", " (2)" and so on), never delete, and never move anything out of the folder. A file it can't move stays where it is and is reported.
4. Python 3.12, standard library unless a small dependency clearly earns its place. It runs on Windows.

## Done when
- Tests pass for: category by extension, month folder, name clashes, and a second run changing nothing. Show the output.
- On a sample tree of a dozen files with mixed types, dates and two clashing names, the count and checksums of all files are identical before and after a run. Show the comparison.
- `--watch` picks up a file dropped in while it runs. Show the log lines.

## How to work
When a check fails, fix the cause and rerun; if the same failure survives two attempts, change approach. Work directly; this needs no sub-agents.

## Boundaries
Build only what's listed: no GUI, no config file, no cloud, no undo or dry-run mode. Mention ideas at the end instead of building them.
````

The prompt is 293 words.

**Run notes**

- Paste it into Claude Code in an empty folder.

**Assumptions**

- The month comes from the file's modified time.
- Only the top level of the folder is organised.

**Left out, offered instead**

- A dry-run preview.
- Undo, with a log of every move.
- Lint and type-check gates.

## Why it came out this way

**Why this example exists.** The request above is the brief from the worked example that shipped inside
version 1.0. Running the same brief through both versions shows what "overdoing" meant in practice.

| | Version 1.0 | Version 1.1 |
|---|---|---|
| Words | 519 | 293 |
| Layout | eight numbered sections | Goal, Requirements, Done when, How to work, Boundaries |
| Added without being asked | a dry-run mode, an undo command, a JSON-lines move log, lint and type-check gates, a README, test-first rules, a restated checklist, an independent check | nothing |
| "Never lose a file" | safety rules plus tests, plus the extra features above | three safety rules and one proof: file count and checksums are identical before and after |

The version 1.0 prompt is in [`archive/v1.0/references/example.md`](../archive/v1.0/references/example.md).

**The ledger**

- **Asked:** a CLI; watch a folder; organise by type and date; Python; never lose a file.
- **Needed:** clash handling and the no-delete and stay-inside-the-folder rules, because that is what
  "never lose a file" means in practice. A sample tree compared by count and checksum, because that is
  the proof. Waiting until a file has stopped growing, because watch mode would otherwise move
  half-written files.
- **Extras:** a dry-run mode, undo, a move log, lint gates, a GUI, a config file.

**Size.** One deliverable with a few rules, so Small.

**Loop.** A fix loop, because there are tests that can fail. It carries the change-approach rule as its
cap.

**Sub-agents.** None, and the prompt says so, because some agents delegate eagerly.

**The point.** Version 1.1 does not make the tool less safe. The safety requirement became checks the
agent must show, and the features nobody asked for moved to the "Left out" list, where one word from
the user brings them back.
