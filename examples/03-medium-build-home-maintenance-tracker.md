<!-- example: tier=Medium loop=fix+long-run delegates=no review=yes -->
# Example 3: a real app left running unattended (Medium)

## The ask

> Prompt for Claude Code to build me a home maintenance tracker: an asset registry for appliances and cars, maintenance schedules with Telegram reminders, and a simple web page showing what's due. It runs in Docker on my Mac mini. I have an Excel sheet with my assets and past services: import it and don't mess it up. I want to leave it running by itself.

## What Prompt Forge returns

Medium prompt, about 770 words: builds the tracker end to end. A fix loop plus a progress file for long runs; the agent works directly, with one fresh-context review at the end.

````text
# HomeKeep — home maintenance tracker

## Goal
Build a small self-hosted app that tracks my appliances and cars, knows when each one is due for maintenance, reminds me on Telegram, and shows what's due on a simple web page. It will run unattended in Docker on my Mac mini (Apple silicon), so it has to start cleanly and keep its data across restarts.

## Context
- My existing records are in assets.xlsx in this folder: one sheet of assets, one of past services. Read it first and tell me in two lines what you found before designing the tables.
- Stack: Python, FastAPI, SQLite in a mounted volume, plain server-rendered HTML. One container.
- Inputs only I can supply: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID, read from .env. Build and test everything with a fake sender; ask me for the real values only when everything else is done.

## Requirements
1. Assets: name, type (appliance or car), make and model, location, purchase date, notes. Add, edit and retire; a retired asset keeps its history.
2. Schedules: each asset has one or more tasks with an interval in days, or for cars in kilometres or months, whichever comes first, worked out from an odometer reading I can update on the car's page. Logging a service resets the clock for that task.
3. Due list: one function returns what is overdue and what falls due in the next 14 days. The web page and the reminders both use it; neither works out dates on its own.
4. Reminders: once a day at 08:00 local time, one Telegram message listing overdue and due-soon tasks. Nothing is sent when the list is empty.
5. Web page: a single page with the due list on top and all assets below, each linking to its history and a form to log a service.
6. Import: load assets.xlsx into the database. Work from a copy and leave the original file as it is. Rows that don't fit go to import_review.csv with the reason; don't guess missing values.

## Done when
- The test suite passes, including tests for the due-date rules (interval, kilometres-or-months, reset after a service) with fixed dates. Show the output.
- The import reports rows read, rows loaded and rows sent to review for each sheet, and they add up. assets.xlsx has the same checksum before and after. Show both.
- `docker compose up` starts the app, the health endpoint answers, and after a restart the data is still there. Show the commands and output.
- The web page loads with the imported data. Show a screenshot or the fetched HTML of the due list.
- A dry run of the daily reminder prints the exact message it would send.
- README.md has the real steps to configure and start it.

## How to work
Milestones, in order: 1) read the spreadsheet and design the tables, 2) due-date logic with tests, 3) import, 4) web page, 5) reminders with the fake sender, 6) Docker packaging. After each one, run its checks, commit when green, and update PROGRESS.md (done, next, decisions). If you start in a fresh session, read PROGRESS.md and the git log first and continue from there.

When a check fails, fix the cause and rerun. If the same failure survives two attempts, change approach; after three approaches, stop and report what is still red with the real output. If a check itself looks wrong, tell me rather than changing it.

Work directly: the parts are small and share one data model, so sub-agents would cost more than they save. The one exception comes before the final report: have a fresh sub-agent review the result against the done-list only. It runs the checks and reports gaps that break a requirement, nothing else. If you can't spawn one, re-run the done-list yourself from a clean checkout.

## Boundaries
Build only what's listed. No logins, no mobile app, no cost tracking, no file attachments, no calendar or smart-home integration; mention ideas at the end instead of building them. Ask before deleting or overwriting anything outside this project folder. Otherwise decide, note the decision in PROGRESS.md and keep going; errors, missing packages and timeouts are yours to work around.

If you aren't running on the Mac mini itself, you can't prove the container runs there. Build and test it here, and say plainly in the report what still needs checking on the mini.

## Finish
Report each done item with its evidence, what isn't done, the rows waiting in import_review.csv, and what you need from me: the Telegram values, and anything to check on the mini.
````

The prompt is 768 words.

**Run notes**

- Open Claude Code in an empty folder that contains `assets.xlsx`, and paste the prompt as the first message.
- For a hands-off run, use auto mode and send the `/goal` line below after the prompt.
- Cost: one reviewer sub-agent at the end.

```text
/goal every item under "Done when" is shown with its command output and the reviewer reports no gaps, or stop after 40 turns
```

**Assumptions**

- Python, FastAPI and SQLite.
- A single user, so no login.
- A daily reminder at 08:00 and a 14-day look-ahead.

**Left out, offered instead**

- User logins.
- Attaching manuals or receipts to an asset.
- A smart-home hook.

## Why it came out this way

**The ledger**

- **Asked:** an asset registry; schedules; Telegram reminders; a web page of what is due; Docker on a
  Mac mini; a safe import of the spreadsheet; an unattended run.
- **Needed:** a single due-list function, so the page and the reminders cannot disagree. A fake
  Telegram sender, so everything can be tested before the real token exists. Import counts that add up
  and a checksum of the spreadsheet, because that is the proof that "don't mess it up" held. Tests for
  the date rules, because the logic is not trivial and a test is the natural check. `PROGRESS.md`,
  because an unattended run can outlast one context.
- **Extras:** logins, attachments, cost tracking, calendar and smart-home integrations, backup tooling.

**Size.** One small service. It sits between Medium and Large, and the rule is to take the smaller.

**Loops.** A fix loop (the same failure twice means a change of approach; three approaches means stop and
report) and a long-run loop (commit at each green milestone, update `PROGRESS.md`, read it first in a
fresh session).

**Sub-agents.** None for the build. The parts are small and share one data model, so the prompt says
"work directly". There is one review at the end because the import touches real data, which is the
"costly if wrong" case. The reviewer is briefed narrowly: the done-list only, and only gaps that break a
requirement.

**Named inputs.** The Telegram token and chat ID are values only the user has. The prompt has the agent
build against a fake sender and ask for the real values last, and it keeps the secret out of the prompt.

**Honest limits.** If the agent is not running on the Mac mini, it cannot prove the container runs
there, so the prompt tells it to say so in the report.

**What the cold read caught.** Reading the draft as the receiving agent found two problems before
delivery. The README check asked for backup and restore steps, which nobody requested, so it was cut.
The kilometre rule for cars had no way to learn the odometer reading, so the requirement now says the
reading can be updated on the car's page.
