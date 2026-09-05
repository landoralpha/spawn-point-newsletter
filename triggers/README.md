# triggers/ - Spawn Point RemoteTrigger Live Instructions

This directory holds the **live instructions** for each Spawn Point claude.ai
RemoteTrigger. Each live trigger's prompt (`job_config.ccr.events[0].data.message.content`
in the RemoteTrigger config) is a SHORT pointer telling the agent to read the
corresponding `.md` file in this directory at runtime for its full
instructions. Editing one of these files and pushing to `main` changes that
trigger's behavior on its NEXT scheduled fire, no `RemoteTrigger update` call
is needed for content changes to an existing trigger's instructions.

(The pointer prompt itself, the short message that tells the agent to read
this file, is tracked separately in `triggers/kickoff/`, since editing the
pointer *does* require a `RemoteTrigger update` call. See
`triggers/kickoff/README.md`.)

## Tracked triggers

| File | Trigger ID | Cron schedule (UTC) | Description |
|---|---|---|---|
| `monitor.md` | `trig_01VTWmmrrBWxioH8DUCw364q` | `0 23 * * *` (daily 23:00 UTC) | Pokémon GO News Monitor, populates the News & Updates Notion DB. |
| `researcher.md` | `trig_01GYjXQqpCgDiFfzo3MKDH5E` | `0 21 * * 1` (Mondays 21:00 UTC) | Newsletter Research Agent, drafts the upcoming Spawn Point issue. |
| `recon.md` | `trig_01WB5YXtpMZR8zgebrsPC7Ah` | `0 22 * * 5` (Fridays 22:00 UTC = 6 PM Eastern) | Pre-Publish Fact-Check Agent, verifies the Beehiiv draft before publish. |

Each file starts with an HTML comment header block containing the trigger ID,
the prompt message UUID as of the last confirmed check, and a note on how
live-instruction edits take effect (see above).

## Why this directory exists

Keeping the full editorial/workflow logic in a tracked file, with only a
short pointer living in claude.ai's trigger config, gives:

- **Full git history on agent behavior**, every instruction change is a
  normal commit/diff, not an edit buried in claude.ai's UI history (which has
  no diff view).
- **Editing without touching the API**, most changes are a normal file edit
  + `git push`, not a `RemoteTrigger update` call.
- **Review before it goes live**, a pending PR against one of these files can
  be reviewed like any other code change before it reaches a scheduled agent.

## Refresh procedure (for the pointer prompt only)

The `.md` files in this directory ARE the live instructions, no refresh step
is needed to keep them in sync, since they ARE the source. What occasionally
needs refreshing is the *pointer* snapshot in `triggers/kickoff/`, if the
pointer text itself changes. See `triggers/kickoff/README.md`'s refresh
procedure for that.

## Rollback procedure

If an instruction edit broke something and you want to restore an earlier
version:

1. Identify the good version in git history:

   ```bash
   cd /Users/joelandor/Documents/spawn-point
   git log --oneline triggers/monitor.md      # or researcher.md / recon.md / daily-brief.md
   ```

2. Revert the file to that commit:

   ```bash
   git show <commit>:triggers/monitor.md > triggers/monitor.md
   git add triggers/monitor.md
   git commit -m "triggers: revert monitor.md to <commit>"
   git push origin main
   ```

3. The next scheduled fire reads the reverted content automatically, no
   `RemoteTrigger update` call needed, since the pointer prompt didn't change.

4. To test immediately rather than waiting for the next scheduled fire, use
   `RemoteTrigger run` against the trigger ID from a Claude Code session with
   RemoteTrigger access.

## What goes wrong if you edit these files without pushing to `main`

The live trigger reads from the `main` branch of this repo at runtime. A
local, uncommitted, or unpushed edit has NO effect on live behavior, so the
next scheduled fire still reads whatever is currently on `main`. Always
commit AND push before expecting a behavior change to take effect.
