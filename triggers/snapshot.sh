#!/bin/bash
# snapshot.sh — Refresh the local snapshots of Spawn Point trigger prompts.
#
# Triggers tracked:
#   Monitor:    trig_01VTWmmrrBWxioH8DUCw364q  → triggers/monitor.md
#   Researcher: trig_01GYjXQqpCgDiFfzo3MKDH5E  → triggers/researcher.md
#   Recon:      trig_01WB5YXtpMZR8zgebrsPC7Ah  → triggers/recon.md
#
# This script is a PLACEHOLDER. The actual snapshotting requires the RemoteTrigger
# tool inside a Claude Code session — that tool is not available to raw bash.
#
# To refresh snapshots, run one of:
#   1. From a Claude Code session: ask Claude "snapshot the trigger prompts"
#      (or invoke /loop snapshot triggers if you have such a slash command).
#   2. Manually instruct Claude: "Run RemoteTrigger get for each of these three
#      trigger IDs and write the prompt content from
#      trigger.job_config.ccr.events[0].data.message.content to the corresponding
#      .md file under triggers/, preserving the header block at the top of each file
#      and updating only the 'Snapshot fetched' timestamp."

set -e

cat <<'EOF'
============================================================
spawn-point trigger snapshot helper (placeholder)
============================================================

This script cannot directly call the claude.ai RemoteTrigger API — that
endpoint is reachable only via Claude Code's internal RemoteTrigger tool,
which is not exposed to raw bash.

To refresh the snapshots in this directory:

  Option A (recommended): open a Claude Code session in this repo and ask:
      "Snapshot all three Spawn Point trigger prompts to triggers/"

  Option B: manually have Claude run, for each trigger ID below, the
      RemoteTrigger get action, then write
      trigger.job_config.ccr.events[0].data.message.content
      to the corresponding .md file under triggers/, preserving the
      header block at the top and updating only the timestamp line.

Trigger IDs and target files:

  Monitor       trig_01VTWmmrrBWxioH8DUCw364q   triggers/monitor.md
  Researcher    trig_01GYjXQqpCgDiFfzo3MKDH5E   triggers/researcher.md
  Recon         trig_01WB5YXtpMZR8zgebrsPC7Ah   triggers/recon.md

After refresh, review with:
  git -C /Users/joelandor/Documents/spawn-point diff triggers/
  git -C /Users/joelandor/Documents/spawn-point add triggers/
  git -C /Users/joelandor/Documents/spawn-point commit -m "triggers: refresh snapshots $(date -u +%Y-%m-%dT%H:%MZ)"

============================================================
EOF
