# Installing Prompt Forge

Prompt Forge is a single folder, `prompt-forge/`, with one file inside it, `SKILL.md`. Installing
it means putting that folder where Claude looks for skills.

The menu names below were checked against Anthropic's help pages in November 2026. If a label has
moved since then, the linked pages are the authority:
[Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude),
[How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
and, for Claude Code, [Extend Claude with skills](https://code.claude.com/docs/en/skills.md).

## 1. Get the zip

Use either route.

- **Download it.** Take `prompt-forge-1.1.zip` from the repository's Releases page.
- **Build it.** From a copy of this repository:

  ```text
  python tools/package_skill.py
  ```

  The file appears at `dist/prompt-forge-1.1.zip`. The script refuses to build a zip that the
  Claude apps would reject.

The zip holds the `prompt-forge` folder at its top level. That layout matters: the upload expects
the skill folder itself, not a folder that contains it.

## 2. Install in the Claude apps

This covers Claude on the web, the desktop app and the phone app. The skill is added to your
account, so one upload is enough.

1. Open **Customize**, then **Skills**.
2. Press **+**, then **Create skill**, then **Upload a skill**.
3. Choose the zip.
4. Check that Prompt Forge appears in your skills list and is switched on.

Skills need code execution and file creation to be enabled. On Team and Enterprise plans an owner
controls that setting.

### For a whole organisation

An owner can upload the zip once in the organisation's skill settings, and it then appears for
everyone. The steps are in
[Provision and manage skills for your organization](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization).

## 3. Install in Claude Code

If you sign in to Claude Code with the same Claude account, skills from your account are synced to
it, so the upload in step 2 may be all you need. To install it directly instead, copy the folder.

**For yourself, in every project**

macOS and Linux:

```bash
git clone https://github.com/sbina6/prompt-forge
mkdir -p ~/.claude/skills
cp -r prompt-forge/skill/prompt-forge ~/.claude/skills/
```

Windows PowerShell:

```powershell
git clone https://github.com/sbina6/prompt-forge
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force prompt-forge\skill\prompt-forge "$HOME\.claude\skills\"
```

**For one project, shared with everyone who clones it**

Copy `skill/prompt-forge` to `.claude/skills/prompt-forge` inside that project and commit it.

In Claude Code you can describe what you want and let the skill load by itself, or call it by
name:

```text
/prompt-forge a prompt to build a CLI that organises my downloads folder
```

## 4. Check that it works

Ask this:

```text
Prompt forge: a prompt for a script that renames my photos by the date taken.
```

A working install answers with one line of summary, a single paragraph of roughly 100 words in a
copyable block, and a few short notes. If you get a long multi-section specification for that ask,
the old version is still installed.

## Updating

- **With a zip:** upload the new version's zip, or replace the folder in `~/.claude/skills/`.
- **In a chat:** ask Claude to update Prompt Forge. It shows a review card and you save the change
  from there. The card can replace `SKILL.md` only, which is one reason the skill is a single file.

### Coming from version 1.0

Version 1.0 shipped two extra files in a `references/` folder. Version 1.1 does not use them and
tells Claude not to load them. If you update through the review card they stay where they are,
unused. For a clean copy, remove the 1.0 skill from your skills list and upload the 1.1 zip.

## Troubleshooting

| Problem | Likely cause | What to do |
|---|---|---|
| The skill never triggers | It is switched off, or the ask did not mention a prompt | Switch it on in your skills list, or say "prompt forge" by name |
| The upload is rejected | The zip has the wrong layout, or `SKILL.md` has an extra key at the top | Build the zip with `tools/package_skill.py`; only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` are accepted |
| Claude Code does not see it | The skills folder was created after the session started | Run `/reload-skills`, or start a new session |
| The answers are long and heavy | Version 1.0 is still installed | Install 1.1, then repeat the check in step 4 |
