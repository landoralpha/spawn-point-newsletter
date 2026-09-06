# triggers/ — Spawn Point RemoteTrigger Prompt Snapshots

This directory holds **read-only snapshots** of the live prompt content for the
four Spawn Point claude.ai RemoteTriggers. Editing files here does **NOT**
change live trigger behavior — these snapshots exist purely for `git diff`
visibility on prompt edits and for manual rollback reference.

## Tracked triggers

| File | Trigger ID | Cron schedule (UTC) | Description |
|---|---|---|---|
| `monitor.md` | `trig_01VTWmmrrBWxioH8DUCw364q` | `0 23 * * *` (daily 23:00 UTC) | Pokémon GO News Monitor, populates the News & Updates Notion DB. |
| `researcher.md` | `trig_01GYjXQqpCgDiFfzo3MKDH5E` | `0 21 * * 1` (Mondays 21:00 UTC) | Newsletter Research Agent, drafts the upcoming Spawn Point issue. |
| `recon.md` | `trig_01WB5YXtpMZR8zgebrsPC7Ah` | `0 22 * * 5` (Fridays 22:00 UTC = 6 PM Eastern) | Pre-Publish Fact-Check Agent, verifies the Beehiiv draft before publish. |
| `daily-brief.md` | `trig_01GcLo7vBWXV1CER6cBQNNkU` | `20 23 * * *` (daily 23:20 UTC) | Daily Brief Agent, drafts the daily digest from Monitor's News & Updates rows. |

Each file starts with an HTML comment header block containing the trigger ID,
the prompt message UUID at the time of the snapshot, the UTC timestamp of the
snapshot fetch, and a notice that edits here do not affect the live trigger.

## Why this directory exists

claude.ai RemoteTrigger prompts are edited directly in the claude.ai UI; the
canonical store lives behind the RemoteTrigger API. Without a local mirror,
prompt history is invisible to git, and reverting a bad edit means scrolling
through the claude.ai edit history (which has no diff view).

These snapshots give:

- **Git diff visibility** — see exactly what changed between iterations of each
  prompt by diffing the relevant `.md` file across commits.
- **Manual rollback reference** — if a future prompt edit breaks something, the
  prior `.md` content can be copy-pasted back into the trigger (via Claude with
  `RemoteTrigger update` or via the claude.ai UI).

The directory is **not** bound as a session source for any of the three
triggers. The agents do not read these files at runtime.

## Refresh procedure

After any major prompt edit, refresh the snapshots so `git log` reflects the
current live state:

1. Open a Claude Code session anywhere with RemoteTrigger access (or use
   `/loop` with the snapshotting prompt if you've wired one).
2. Ask Claude: **"Snapshot all three Spawn Point trigger prompts to
   `/Users/joelandor/Documents/spawn-point/triggers/`."**
3. Claude will run `RemoteTrigger get` against each of the three IDs and
   rewrite the three `.md` files, preserving the header block and updating
   the `Snapshot fetched` timestamp.
4. Commit the diff:

   ```bash
   cd /Users/joelandor/Documents/spawn-point
   git diff triggers/                       # review
   git add triggers/
   git commit -m "triggers: refresh snapshots"
   ```

`snapshot.sh` in this directory is a placeholder helper that prints these
instructions — it cannot call RemoteTrigger directly (that tool is only
available inside a Claude Code session).

## Rollback procedure

If a prompt edit broke something and you want to restore an earlier version:

1. Identify the good version in git history:

   ```bash
   cd /Users/joelandor/Documents/spawn-point
   git log --oneline triggers/monitor.md      # or researcher.md / recon.md
   ```

2. View the previous content:

   ```bash
   git show <commit>:triggers/monitor.md
   ```

3. Copy the prompt body (everything after the `-->` closing the header block)
   into your clipboard.

4. Push it back to the live trigger. From a Claude Code session with
   `RemoteTrigger`, ask Claude to run a `RemoteTrigger update` against the
   trigger ID with the rolled-back content, or paste the content into the
   prompt field in the claude.ai UI for that trigger.

5. Fire the trigger manually ("Run now" in claude.ai) and confirm behavior is
   restored.

6. Refresh the snapshots (per the previous section) so the local mirror
   reflects the post-rollback state.

## What goes wrong if you edit these files directly

Nothing functional — but you will have introduced **drift between the snapshot
and the live trigger**. The next snapshot refresh will overwrite your edits.
If you want to change live trigger behavior, edit in claude.ai (or via
`RemoteTrigger update`), then refresh the snapshot.
