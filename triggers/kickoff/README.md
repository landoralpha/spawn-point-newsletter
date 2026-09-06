# triggers/kickoff/ — RemoteTrigger kickoff message snapshots

Read-only snapshots of the **kickoff message** passed into each Spawn Point RemoteTrigger session. This is the short pointer prompt that lives in the claude.ai trigger config's `events[0].data.message.content` field. It tells the agent to read the corresponding `triggers/{name}.md` file at runtime for full instructions.

## Why these are tracked

Edits to the kickoff message in claude.ai have no git history. When we override-and-revert (as for a manual #18 rerun), the only record is the API. These snapshots give:

- **Git diff visibility** — see what changed between iterations
- **Manual rollback reference** — copy-paste back into the trigger if a kickoff edit breaks something

The kickoff itself rarely changes; all editorial / workflow logic belongs in `triggers/{name}.md`. If you find yourself wanting to edit a kickoff for more than a one-time override, that's a signal the change should live in the `.md` file instead.

## Refresh procedure

After any kickoff edit:

1. In a Claude Code session with RemoteTrigger access, ask:
   > "Snapshot the kickoff messages for all three Spawn Point triggers into `triggers/kickoff/`."
2. Claude will run `RemoteTrigger get` against each trigger ID and rewrite the three `*-kickoff.md` files.
3. Commit the diff.

## Trigger IDs

| File | Trigger ID | Cron | Description |
|---|---|---|---|
| `researcher-kickoff.md` | `trig_01GYjXQqpCgDiFfzo3MKDH5E` | `0 21 * * 1` (Mon 21:00 UTC) | Newsletter research agent |
| `recon-kickoff.md` | `trig_01WB5YXtpMZR8zgebrsPC7Ah` | `0 22 * * 5` (Fri 22:00 UTC = 6 PM Eastern) | Pre-publish fact-check agent (moved from Sun 00:00 UTC 2026-06-12 for a longer pre-publish fix window) |
| `monitor-kickoff.md` | `trig_01VTWmmrrBWxioH8DUCw364q` | `0 23 * * *` (daily 23:00 UTC) | Niantic announcement monitor |
| `daily-brief-kickoff.md` | `trig_01GcLo7vBWXV1CER6cBQNNkU` | `20 23 * * *` (daily 23:20 UTC) | Daily Brief digest agent |
