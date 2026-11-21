<!-- example: tier=Micro loop=none delegates=no review=no -->
# Example 1: a tiny script (Micro)

## The ask

> Prompt for Claude Code: a script that converts every HEIC in a folder to JPG.

## What Prompt Forge returns

Micro prompt, about 100 words: one script and one check at the end. No loop, no sub-agents.

````text
Write a Python 3 script, heic2jpg.py, that converts every .heic file in a folder I pass as an argument into a .jpg with the same name in the same folder. Leave the original files untouched, and skip any file whose .jpg already exists. Print one line per file (converted, skipped, or failed with the reason) and a count at the end. Use Pillow with pillow-heif; one file; no config, GUI or extra options. When it's written, run it on a temp folder with three sample HEIC images, run it a second time, and show me both outputs.
````

The prompt is 97 words.

**Run notes**

- Paste it into Claude Code, or any agent that can run Python, in the folder where you want the script.

**Assumptions**

- The original files are kept.
- Each JPG is written next to its source file.

**Left out, offered instead**

- Converting subfolders as well.
- A setting for JPG quality.
- Copying the photo's date into the JPG.

## Why it came out this way

**The ledger**

- **Asked:** a script; HEIC to JPG; a whole folder at once.
- **Needed:** three sample images and two runs, because that is what shows the script works and that
  running it twice does no harm. Keeping the originals, because a converter that deleted photos would
  be a nasty surprise; it is stated as an assumption so the user can overrule it.
- **Extras:** subfolders, a quality setting, metadata copying, a GUI, parallel conversion.

**Size.** One artifact that can be checked at a glance, so Micro: a single paragraph with no headings.

**Loop.** None. There is one pass and one check, so the prompt asks for the check once at the end.

**Sub-agents.** None. The whole job is a handful of tool calls.
