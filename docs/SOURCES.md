# Sources

The pages the design of version 1.1 relies on. All were read on 21 November 2026. Each entry says
in a sentence or two what was taken from it; the pages themselves are the authority, and they
change. [DESIGN.md](DESIGN.md) refers to these entries by number.

When the agent notes are refreshed, re-read S4 to S8, S13 and S14 and update the date here. See
[MAINTAINING.md](MAINTAINING.md#refreshing-the-agent-notes).

## How current models respond to prompts

| # | Source | What was taken from it |
|---|---|---|
| S1 | [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), Anthropic | Recent models over-apply forceful wording and tend to add unrequested files and abstractions. Explaining the reason behind a rule works better than a bare rule. Long tasks need state in files, progress notes and git checkpoints. Guidance on when to delegate. |
| S2 | [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5), Anthropic | Explicit instructions to verify again cause wasted effort and should be removed. The model delegates readily and needs to be told when delegation is worth it. It can widen a task, so scope should be stated. It works best with the whole specification up front. |
| S3 | [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2), Anthropic | Absolute words are treated as absolute, so rules should be scoped. Long tasks can end early unless the prompt says to keep going past ordinary obstacles. A delegation instruction should cover cost, when to delegate and how to brief. |

## Sub-agents

| # | Source | What was taken from it |
|---|---|---|
| S4 | [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md), Claude Code docs | What a sub-agent receives (its task message, not the conversation) and returns (a summary). When to use one and when to stay in the main conversation. Running them in parallel, and isolating them in worktrees. |
| S5 | [Run agents in parallel](https://code.claude.com/docs/en/agents.md), Claude Code docs | The different ways to run several agents, and that `/batch` splits one large change across isolated sub-agents. |
| S6 | [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows.md), Claude Code docs | Asking for a workflow in plain words, what workflows are suited to, the advice to pilot on a small slice, and example wording for loops that stop after rounds with no progress. |
| S12 | [Building agents: when to fold subagents into your main agent loop](https://claude.com/blog/building-agents-when-to-fold-subagents-into-your-main-agent-loop), Anthropic | A single agent often does better than a multi-agent design. Hand-offs lose detail. Start from the simplest pattern that could work. |
| S13 | [Subagents](https://cursor.com/docs/subagents), Cursor docs | Cursor delegates by itself or by name, in the foreground, the background or in parallel, and token use grows with the number of sub-agents. |
| S14 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md), Codex docs | Codex spawns sub-agents when asked directly, and a good request says how to divide the work, whether to wait, and what to return. |

## Loops

| # | Source | What was taken from it |
|---|---|---|
| S7 | [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal.md), Claude Code docs | How `/goal` works: a separate evaluator judges the condition from the conversation after each turn. How to write a condition: one measurable end state, a stated check and a cap on turns. |
| S8 | [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks.md), Claude Code docs | The `/loop` syntax, that it lasts as long as the session, and the durable alternatives for recurring work. |
| S11 | [Loop engineering: getting started with loops](https://claude.com/blog/getting-started-with-loops), Anthropic | The kinds of loop the Claude Code team distinguishes, the importance of verifiable stop criteria and explicit caps, and the advice to choose the simplest mechanism that fits. |

## What a prompt needs most

| # | Source | What was taken from it |
|---|---|---|
| S9 | [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices.md), Claude Code docs | Give the agent a check it can run, and have it show evidence. Planning is overhead for small changes. After two failed corrections, start again with a better approach. A reviewer asked to find gaps usually finds some, so limit it to correctness and stated requirements. |

## Skills

| # | Source | What was taken from it |
|---|---|---|
| S10 | [Extend Claude with skills](https://code.claude.com/docs/en/skills.md), Claude Code docs | Where skills live, the keys an uploaded skill may carry, the guidance to stay under 500 lines, and that roughly the first 5,000 tokens of an invoked skill survive compaction. |
| S15 | [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), Claude Help Center | How to upload a custom skill in the Claude apps. |
| S16 | [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills), Claude Help Center | The zip has to hold the skill folder at its top level, and the folder name has to match the skill's name. |
| S17 | [Provision and manage skills for your organization](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization), Claude Help Center | How an owner makes a skill available to a whole organisation. |
| S18 | The skill-creator skill, Anthropic, as installed in the Claude apps | Conventions for writing a skill: explain the reason, keep it lean, avoid shouted rules, show examples. The validation rules for the top of `SKILL.md`. The method for evaluating a skill with independent runs. |

## Version 1.0

Version 1.0 of this skill is itself a source. It is kept unchanged in
[`archive/v1.0/`](../archive/v1.0/README.md).
