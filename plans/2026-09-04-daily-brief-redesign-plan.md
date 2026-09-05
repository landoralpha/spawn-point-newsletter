# Spawn Point Daily Brief + Weekly Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up a new daily "Daily Brief" RemoteTrigger that turns Monitor's existing News & Updates aggregation into a light-touch-verified, categorized daily digest, and modify the Weekly (`researcher.md`) trigger so its news-shaped sections roll up the week's Daily Briefs instead of researching from scratch — without deleting or replacing any existing working pipeline.

**Architecture:** Monitor (unchanged) keeps writing rows to the News & Updates Notion DB every night at 23:00 UTC. A new Daily Brief trigger fires 20 minutes later, reads that day's unprocessed rows, verifies each lightly (one primary-source re-fetch + sanity check, not Recon's full tri-source chain), drafts an adaptive categorized digest, pushes it to a persistent Notion parent page, emails Joe a ready-to-paste copy, and marks each included row `Daily Brief Status = Included - <date>`. Weekly's Step 4 gains a new Step 3.5 that pulls the past week's `Included` rows as first-pass material for its Trending Topic and Don't Miss sections, before falling back to fresh research; Weekly's schedule-shaped and reference-data sections are untouched. Recon needs no changes — it verifies whatever draft exists at publish time regardless of how it was produced.

**Tech Stack:** claude.ai RemoteTrigger (cron-scheduled Claude Code sessions), Notion MCP (`mcp__claude_ai_Notion__*`) against two existing Notion data sources, Spawn-Point-Fetcher MCP (`fetch_url`, `send_email`), WebFetch, git (spawn-point-newsletter repo, `main` branch). No new database, no new hosting, no new language/runtime — this is entirely markdown-instruction-file and Notion-schema work plus one new RemoteTrigger.

**Spec:** `/Users/joelandor/Documents/spawn-point/specs/2026-09-04-daily-brief-redesign.md`

## Global Constraints

- **Don't delete, archive instead** (standing project rule): before editing any existing tracked file, copy its pre-edit content to `archive/<same-relative-path>-pre-daily-brief-2026-09-04.<ext>`. Normal git history continues underneath — the archive folder is a discoverable, human-readable safety net on top of it, not a replacement for it. No in-file commented-out blocks in `researcher.md` — it's read fresh by a scheduled agent every Monday, so dead commented text wastes context and risks being misread as active instruction (Spec Section 4).
- **Pokémon spelling:** always "Pokémon" with the accent — never "Pokemon".
- **No em dashes**, anywhere, in any newly-written copy (plan text, trigger instructions, emails). Commas/parens/periods instead.
- **Third-person, strictly factual voice** in Daily Brief's hard-news categories; inline source attribution per claim (e.g., "per LeekDuck"), not just a trailing link. Same banned-editorial-claims list `instructions/newsletter-creation.md` already enforces for Weekly.
- **Cloud sandbox blocks outbound curl/wget.** WebFetch, WebSearch, and the Spawn-Point-Fetcher MCP `fetch_url` tool are the only outbound network primitives available to any trigger.
- **Secret handling:** the real Notion curl-fallback token exists only in live trigger config (via `RemoteTrigger get`), never in a committed file. Every task below that touches a file referencing this token MUST use the literal redacted placeholder string `ntn_REDACTED_IN_SNAPSHOT` with the same explanatory note already used at `triggers/researcher.md:764` — never paste the real value into any file this plan creates or edits.
- **`main`-branch-is-live:** every trigger's live prompt is a short pointer that tells the agent to read its corresponding `triggers/<name>.md` file in this repo at runtime. A file edit only takes effect once committed AND pushed to `origin main` — every task below that edits a `triggers/*.md` file ends with a push, not just a local commit.
- **Weekly's cadence is unchanged**: cron still fires Monday, publish is still a manual Saturday send (Spec Section 3) — nothing in this plan touches `researcher.md`'s cron or Steps 0-3 / 5-8.
- **No auto-publish**: Daily Brief has no Beehiiv write access and no git-push credentials; its output is always manually reviewed and published by Joe (Spec Section 2, "Out of Scope").
- **Reused identifiers** (do not re-derive, use verbatim): News & Updates DB data source ID `1b9db417-c801-4004-a687-e09fe2976e73`; Run Log DB data source ID `d808fb32-e641-480f-a90e-78f0685c78c9`; shared `environment_id` for all Spawn Point triggers `env_01VSb95kc6a7pofXsvGasHhc`; shared `allowed_tools` list `["preset:default","Task","Bash","Glob","Grep","Read","Edit","MultiEdit","Write","NotebookEdit","WebFetch","TodoWrite","WebSearch","BashOutput","KillBash","Skill","Tmux","Monitor","SendUserFile","REPL"]`; shared MCP connectors Gmail (`ed9bce03-43bd-45a3-b6f0-4cb80740be87`, `https://gmailmcp.googleapis.com/mcp/v1`), Notion (`9be38711-d9fe-4445-b85c-ad7cad41946a`, `https://mcp.notion.com/mcp`), Spawn-Point-Fetcher (`cf7c80bc-f8e1-4ae1-a87a-e2a04108ecbc`, `https://fetcher-mcp.vercel.app/mcp/Lyu2UTyvxgOm84fqnjETWyQXX8bLP2NMvNTcKrsBOpQ`).

---

## File Structure

```
spawn-point/
├── archive/
│   └── triggers/
│       ├── researcher-pre-daily-brief-2026-09-04.md   # NEW — pre-edit snapshot
│       └── README-pre-daily-brief-2026-09-04.md        # NEW — pre-edit snapshot
├── triggers/
│   ├── researcher.md      # MODIFIED — new Step 3.5, small edits to Step 4/4.5
│   ├── daily-brief.md     # NEW — full Daily Brief trigger instructions
│   ├── README.md          # MODIFIED — corrected to reflect actual live-read behavior + new row
│   └── kickoff/
│       ├── daily-brief-kickoff.md   # NEW — pointer snapshot, written after trigger creation
│       └── README.md               # MODIFIED — new table row
```

No other files are touched. `triggers/monitor.md` and `triggers/recon.md` are read-only references for this plan and are not modified (Spec: "Recon... needs no structural changes"; Monitor is explicitly unchanged infrastructure the Daily Brief builds on top of).

---

### Task 1: Add `Daily Brief Status` property to the News & Updates Notion DB

**Files:** none (Notion schema change via MCP, no local files)

**Depends on:** nothing.
**Produces:** a new property `Daily Brief Status` (type: rich text) on data source `1b9db417-c801-4004-a687-e09fe2976e73`, present (blank) on every existing row. Values this property will ever hold: empty string (not yet processed) or the literal string `Included - <YYYY-MM-DD>`. Tasks 3, 5, 6, 7 depend on this property existing.

- [ ] **Step 1: Load the Notion MCP schema-update tool**

Call `ToolSearch` with `query: "select:mcp__claude_ai_Notion__notion-update-data-source"` to load its parameter schema (it is deferred and not callable until loaded).

- [ ] **Step 2: Add the property**

Call `mcp__claude_ai_Notion__notion-update-data-source` against data source `1b9db417-c801-4004-a687-e09fe2976e73`, adding a new property named exactly `Daily Brief Status` with type `rich_text` (plain text, not select — the value embeds a variable date so it can't be a fixed enum). Do not modify, rename, or remove any of the 15 existing properties (Title, Type, Status, Source, Source URL, Published Date, Detected At, Start Date, End Date, Description, Newsletter Treatment, Content Completeness, Last Enrichment Attempt, Pokémon Mentioned, Hero Image URL).

- [ ] **Step 3: Verify**

Call `mcp__claude_ai_Notion__notion-query-data-sources` against `1b9db417-c801-4004-a687-e09fe2976e73` with `query.limit: 3` (no filter) and confirm the returned rows now include a `Daily Brief Status` key (empty string on all of them, since this is a brand-new property on pre-existing rows).

---

### Task 2: Add `Daily Brief` option to the Run Log DB's `Trigger` select

**Files:** none (Notion schema change via MCP)

**Depends on:** nothing (independent of Task 1).
**Produces:** a fourth option `Daily Brief` on the `Trigger` select property of data source `d808fb32-e641-480f-a90e-78f0685c78c9`, alongside the existing `Monitor` / `Research Agent` / `Recon`. Tasks 5, 6, 7 depend on this option existing (Daily Brief's Run Log rows set `Trigger = Daily Brief`).

- [ ] **Step 1: Add the option**

Using the same `mcp__claude_ai_Notion__notion-update-data-source` tool loaded in Task 1, add option `Daily Brief` to the existing `Trigger` select property on data source `d808fb32-e641-480f-a90e-78f0685c78c9`. Do not remove or rename `Monitor`, `Research Agent`, or `Recon`, and do not touch any of the other 15 properties (Run Title, Run Timestamp, Run Status, New Entries Added, Duplicates Prevented, Backfill Dupes Marked, Enrichments Succeeded, Dedup Enrichments, fetch_url MCP Rescues, Tier Mix, Sources Failed, CF Regressions, Notes, Email Sent, Email Subject).

- [ ] **Step 2: Verify**

Call `mcp__claude_ai_Notion__notion-query-data-sources` against `d808fb32-e641-480f-a90e-78f0685c78c9` with `query.limit: 1` and inspect the schema/property metadata in the response (or a follow-up describe-style call if the query response doesn't surface select options) to confirm `Daily Brief` is now a valid option on `Trigger`.

---

### Task 3: Insert Weekly's new Step 3.5 and update its Step 4/4.5 cross-references

**Files:**
- Create: `archive/triggers/researcher-pre-daily-brief-2026-09-04.md`
- Modify: `triggers/researcher.md:467-469` (insertion), `triggers/researcher.md:480` (edit), `triggers/researcher.md:488` (edit), `triggers/researcher.md:507` (edit)

**Depends on:** nothing structurally, but should follow Tasks 1-2 since the new step references `Daily Brief Status`, which must exist first for the description to be accurate.
**Produces:** `researcher.md` Step 4 now draws Trending Topic and Don't Miss candidates from the week's Daily Brief pool first. No other trigger depends on this file's content (Weekly is the terminal consumer), but Task 9's dry-run validates it.

- [ ] **Step 1: Archive the pre-edit file**

```bash
cd /Users/joelandor/Documents/spawn-point
mkdir -p archive/triggers
cp triggers/researcher.md archive/triggers/researcher-pre-daily-brief-2026-09-04.md
```

- [ ] **Step 2: Verify the archive is byte-identical to the current file**

```bash
diff triggers/researcher.md archive/triggers/researcher-pre-daily-brief-2026-09-04.md
```

Expected: no output (files identical).

- [ ] **Step 3: Insert the new Step 3.5**

Using the Edit tool on `triggers/researcher.md`, replace this exact text (the boundary between Step 3 and Step 4):

```
## Step 3: Verify Phase

Flags: `[UNVERIFIED]`, `[RULE CHANGE]`, `[ROTATION CONFLICT]`, `[PENDING]`, `[fallback: fetch_url]`, `[fallback: search-snippet]`, `[fallback: computed]`, `[REFERENCE DRIFT]`, `[STALE REFERENCE]`, `[SPEC DRIFT]`.

## Step 4: Write the Research Brief
```

with:

```
## Step 3: Verify Phase

Flags: `[UNVERIFIED]`, `[RULE CHANGE]`, `[ROTATION CONFLICT]`, `[PENDING]`, `[fallback: fetch_url]`, `[fallback: search-snippet]`, `[fallback: computed]`, `[REFERENCE DRIFT]`, `[STALE REFERENCE]`, `[SPEC DRIFT]`.

## Step 3.5: Review the Week's Daily Briefs

Before starting fresh research, pull the past week's Daily Brief output — the news-shaped sections below draw from this pool first, not from a blank page.

Query the News & Updates DB (`1b9db417-c801-4004-a687-e09fe2976e73`) for rows where `Daily Brief Status` starts with `Included` AND `Detected At` falls within the last 7 days (`today` back through `today - 6`, i.e. the week Daily Brief has actually already covered — NOT the upcoming Monday-Sunday newsletter week computed in Step 0, since that week hasn't happened yet). Pull Title, Type, Source, Source URL, Description, Pokémon Mentioned, Content Completeness for each.

**If the query returns zero rows** (Daily Brief hasn't run yet, or nothing cleared verification that week): note `No Daily Brief pool this week — falling back to fresh research only` and proceed to Step 4 exactly as before this redesign.

**Otherwise**, this pool becomes the first material for two specific places in Step 4:
- **Trending Topic Candidates:** draw candidate angles from across the WHOLE pool (any category — a bug that won't die, a recurring datamine, an unusually engaged Community Buzz item), not from a pre-sorted "trending" bucket. Daily Brief does no pre-sorting for this purpose; treat every row as raw material. Still generate four distinct angles and still verify against `newsletter-archive.md`'s dedup rule — the pool supplements fresh research, it doesn't replace the angle-diversity requirement.
- **Don't Miss candidates:** the pool's `Closing Soon` category rows (if any) are strong Don't Miss material almost by definition — pull them in alongside anything fresh research turns up.

This step does not touch the schedule-shaped sections (Raid Bosses, GBL, Max Monday, Community Day, Spotlight Hour) — those stay freshly researched in Step 4 exactly as before, since Daily Brief explicitly never covers live-schedule state.

## Step 4: Write the Research Brief
```

- [ ] **Step 4: Update the Trending Topic Candidates bullet to reference the new pool**

Replace:

```
- **Trending Topic Candidates — generate FOUR distinct angles** (the editorial frame for the Trending Topic newsletter section). For each, write:
```

with:

```
- **Trending Topic Candidates — generate FOUR distinct angles**, drawing first from Step 3.5's Daily Brief pool (if any) and supplementing with fresh research (the editorial frame for the Trending Topic newsletter section). For each, write:
```

- [ ] **Step 5: Update the Don't Miss candidates bullet to reference the new pool**

Replace:

```
- Don't Miss candidates (5-6, Joe picks 3)
```

with:

```
- Don't Miss candidates (5-6, Joe picks 3) — pull in Step 3.5's `Closing Soon` pool rows first, then fill any remaining slots with fresh research
```

- [ ] **Step 6: Update the now-redundant Step 4.5 cross-reference**

Replace this clause inside the Step 4.5 Trending Topic Candidates bullet:

```
also read the freshest 5 entries in the News & Updates Notion DB (populated daily by the monitor trigger).
```

with:

```
also cross-check against Step 3.5's week-of-Daily-Brief pool, now the primary source for this week's candidates rather than just a freshness check.
```

- [ ] **Step 7: Read back the full edited region and confirm no stray duplication**

```bash
sed -n '463,515p' triggers/researcher.md
```

Confirm exactly one `## Step 3.5` heading, the three edited bullets read correctly in context, and Step 4's heading still appears exactly once.

- [ ] **Step 8: Commit and push**

```bash
cd /Users/joelandor/Documents/spawn-point
git add archive/triggers/researcher-pre-daily-brief-2026-09-04.md triggers/researcher.md
git commit -m "researcher: add Step 3.5 to roll up the week's Daily Briefs before fresh research"
git push origin main
```

---

### Task 4: Correct `triggers/README.md`'s stale claims

**Files:**
- Create: `archive/triggers/README-pre-daily-brief-2026-09-04.md`
- Modify: `triggers/README.md` (full rewrite of the existing content)

**Depends on:** nothing.
**Produces:** an accurate `triggers/README.md` that states the true live-read behavior and correct cron values. Task 8 adds one more row to this file once the Daily Brief trigger exists — this task fixes the pre-existing errors first so that follow-on edit lands on correct content.

The current file claims these `.md` files are "read-only snapshots" that do NOT affect live behavior, and that "the agents do not read these files at runtime" — this is backwards. Confirmed via live `RemoteTrigger get` calls against all three existing triggers: each trigger's live prompt is a short pointer instructing the agent to read the corresponding `triggers/<name>.md` file in this repo at runtime, so editing and pushing DOES change live behavior on the next scheduled fire. The file's cron table is also stale: it lists `researcher.md` at `0 22 * * 1` (should be `0 21 * * 1`) and `recon.md` at `0 12 * * 6` (should be `0 22 * * 5`) — both confirmed against `triggers/kickoff/README.md`'s ground-truth table and live `RemoteTrigger get` calls.

- [ ] **Step 1: Archive the pre-edit file**

```bash
cd /Users/joelandor/Documents/spawn-point
cp triggers/README.md archive/triggers/README-pre-daily-brief-2026-09-04.md
diff triggers/README.md archive/triggers/README-pre-daily-brief-2026-09-04.md
```

Expected: no diff output.

- [ ] **Step 2: Rewrite `triggers/README.md`**

Use the Write tool to replace the entire file with:

```markdown
# triggers/ — Spawn Point RemoteTrigger Live Instructions

This directory holds the **live instructions** for each Spawn Point claude.ai
RemoteTrigger. Each live trigger's prompt (`job_config.ccr.events[0].data.message.content`
in the RemoteTrigger config) is a SHORT pointer telling the agent to read the
corresponding `.md` file in this directory at runtime for its full
instructions. Editing one of these files and pushing to `main` changes that
trigger's behavior on its NEXT scheduled fire — no `RemoteTrigger update` call
is needed for content changes to an existing trigger's instructions.

(The pointer prompt itself — the short message that tells the agent to read
this file — is tracked separately in `triggers/kickoff/`, since editing the
pointer *does* require a `RemoteTrigger update` call. See
`triggers/kickoff/README.md`.)

## Tracked triggers

| File | Trigger ID | Cron schedule (UTC) | Description |
|---|---|---|---|
| `monitor.md` | `trig_01VTWmmrrBWxioH8DUCw364q` | `0 23 * * *` (daily 23:00 UTC) | Pokémon GO News Monitor — populates the News & Updates Notion DB. |
| `researcher.md` | `trig_01GYjXQqpCgDiFfzo3MKDH5E` | `0 21 * * 1` (Mondays 21:00 UTC) | Newsletter Research Agent — drafts the upcoming Spawn Point issue. |
| `recon.md` | `trig_01WB5YXtpMZR8zgebrsPC7Ah` | `0 22 * * 5` (Fridays 22:00 UTC = 6 PM Eastern) | Pre-Publish Fact-Check Agent — verifies the Beehiiv draft before publish. |

Each file starts with an HTML comment header block containing the trigger ID,
the prompt message UUID as of the last confirmed check, and a note on how
live-instruction edits take effect (see above).

## Why this directory exists

Keeping the full editorial/workflow logic in a tracked file, with only a
short pointer living in claude.ai's trigger config, gives:

- **Full git history on agent behavior** — every instruction change is a
  normal commit/diff, not an edit buried in claude.ai's UI history (which has
  no diff view).
- **Editing without touching the API** — most changes are a normal file edit
  + `git push`, not a `RemoteTrigger update` call.
- **Review before it goes live** — a pending PR against one of these files can
  be reviewed like any other code change before it reaches a scheduled agent.

## Refresh procedure (for the pointer prompt only)

The `.md` files in this directory ARE the live instructions — no refresh step
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

3. The next scheduled fire reads the reverted content automatically — no
   `RemoteTrigger update` call needed, since the pointer prompt didn't change.

4. To test immediately rather than waiting for the next scheduled fire, use
   `RemoteTrigger run` against the trigger ID from a Claude Code session with
   RemoteTrigger access.

## What goes wrong if you edit these files without pushing to `main`

The live trigger reads from the `main` branch of this repo at runtime. A
local, uncommitted, or unpushed edit has NO effect on live behavior — the
next scheduled fire still reads whatever is currently on `main`. Always
commit AND push before expecting a behavior change to take effect.
```

- [ ] **Step 3: Verify**

```bash
cat triggers/README.md
```

Confirm the cron table shows `0 21 * * 1` for researcher.md and `0 22 * * 5` for recon.md, and that no sentence in the file claims these files are read-only or unread at runtime.

- [ ] **Step 4: Commit and push**

```bash
cd /Users/joelandor/Documents/spawn-point
git add archive/triggers/README-pre-daily-brief-2026-09-04.md triggers/README.md
git commit -m "triggers/README: correct stale live-read claim and cron table"
git push origin main
```

---

### Task 5: Write `triggers/daily-brief.md`

**Files:**
- Create: `triggers/daily-brief.md`

**Depends on:** Task 1 (`Daily Brief Status` property must exist), Task 2 (`Daily Brief` Trigger option must exist).
**Produces:** the full instruction file the new trigger will read at runtime. Task 6's pointer prompt references this exact file path. Task 9's dry-run executes these instructions against real data.

- [ ] **Step 1: Write the file**

Use the Write tool to create `triggers/daily-brief.md` with this exact content:

````markdown
<!--
Trigger ID: PENDING — filled in after Task 6 (RemoteTrigger create) succeeds.
Trigger UUID: PENDING — filled in after Task 6.
File status: LIVE INSTRUCTIONS for the Spawn Point Daily Brief trigger.

As of 2026-09-04, the live trigger prompt is a SHORT pointer that instructs
the agent to read THIS file at run time. Edits to this file take effect on
the NEXT trigger fire once committed and pushed to the spawn-point-newsletter
repo's main branch — no manual dashboard re-paste, no API push required.
-->

You are the Spawn Point Daily Brief Agent. Run **daily at 23:20 UTC** (live cron `20 23 * * *`), 20 minutes after the News Monitor's 23:00 UTC run. Your job: take the day's freshly-detected rows from the News & Updates Notion database, light-touch verify each one, draft a categorized daily digest, push it to Notion, email Joe a ready-to-paste copy, mark the rows as covered, and write a Run Log row. Joe manually publishes the digest to Beehiiv as a Web-only post — this agent never touches Beehiiv.

## CRITICAL: Spelling & Style
- Always write "Pokémon" with the accent (é). Never write "Pokemon".
- Time format: AM/PM (caps, no periods).
- Date commas: always after weekday names.
- No em dashes.
- Third-person, strictly factual. Inline source attribution per claim (e.g., "per LeekDuck," "per a Reddit thread on r/TheSilphRoad"), not just a trailing link. No editorializing or hedging in the hard-news categories — the emoji section headers are the personality outlet. The one exception is the Community Buzz category, which may run a slightly looser conversational tone as the issue's low-stakes closer; never let that tone leak into the other categories.
- Same banned-claims list as `instructions/newsletter-creation.md` (the "Banned editorial claims" table there) — check the drafted digest against it before sending. Same zero-em-dash rule Joe locked in for the Weekly.

## Scope Boundary (CRITICAL)
Daily Brief covers discrete, dated things that were *detected or reported* that day — announcements, datamines, bugs, outliers, trending community discussion — from any source, official or community. It NEVER makes live, locally-varying schedule claims ("today's active raid boss," "the current Spotlight Hour Pokémon") — those depend on the reader's timezone in a global playerbase and stay the Weekly's job. If a News & Updates row is really a live-schedule claim rather than a dated announcement, skip it here (Weekly's schedule-shaped sections handle it fresh each Monday).

## Notion Databases

**News & Updates (read + status-write only — Monitor owns creation/enrichment):**
- Name: Pokémon GO News & Updates
- URL: https://www.notion.so/b173baf260c4473e9dd9111c8820c0d3
- Data source ID: `1b9db417-c801-4004-a687-e09fe2976e73`
- 16 properties (as of the 2026-09-04 Daily Brief redesign): Title, Type (multi-select), Status, Source, Source URL, Published Date, Detected At, Start Date, End Date, Description, Newsletter Treatment, Content Completeness, Last Enrichment Attempt, Pokémon Mentioned, Hero Image URL, **Daily Brief Status** (rich text — blank = not yet processed, `Included - <YYYY-MM-DD>` = covered by that day's Brief). This agent only ever WRITES to `Daily Brief Status`; every other property is Monitor's territory.

**Spawn Point Run Log (Step 7 destination):**
- URL: https://www.notion.so/e57321c855844e22b41285873853e26c
- Data source ID: `d808fb32-e641-480f-a90e-78f0685c78c9`
- 16 properties: Run Title (title), Run Timestamp (datetime), Trigger (select — options Monitor / Research Agent / Recon / **Daily Brief**), Run Status (select Success/Partial/Failed), New Entries Added, Duplicates Prevented, Backfill Dupes Marked, Enrichments Succeeded, Dedup Enrichments, fetch_url MCP Rescues, Tier Mix, Sources Failed, CF Regressions, Notes, Email Sent (checkbox), Email Subject.

**Spawn Point Daily Briefs (the digest archive — this agent owns it):**
- A single persistent Notion page titled exactly `Spawn Point Daily Briefs`, holding one child page per day.
- **Step 5 finds-or-creates it every run** via `notion-search` for a page titled exactly `Spawn Point Daily Briefs`. If found, use its page ID as the parent for that day's child page. If genuinely not found (first-ever run), create it as a new top-level page via `notion-create-pages` with no parent, then use its returned page ID. Joe can move it under a different Notion parent later via the UI if he wants — that doesn't break this lookup, since the search is by title, not by location.

## Content Completeness (reference only — set by Monitor, not by this agent)
1. **Full** — complete article body fetched.
2. **Partial** — truncated due to 5000-word cap or partial render.
3. **Snippet only** — only WebSearch tier-3 snippet OR aggregator RSS metadata.
4. **Stub** — only title + URL + minimal metadata.

A row's Content Completeness is a helpful signal (a `Stub` row has less to verify against) but is NOT itself the light-touch verification this agent performs — see Step 2.

## Step 0: Determine Today + Confirm Monitor Ran

```python
from datetime import date
today = date.today()
```

Before doing anything else, query the Spawn Point Run Log (`d808fb32-e641-480f-a90e-78f0685c78c9`) for today's Monitor row: `Trigger = Monitor` AND `Run Timestamp` falls on `today`'s UTC date. This should be the run that fired at 23:00 UTC, 20 minutes before this trigger.

- **If no Monitor row exists for today, or the row's Run Status = `Failed`:** STOP. Do not proceed to Step 1. Send Joe an email (Subject `[Spawn Point Daily Brief] Skipped — Monitor run missing or failed for [YYYY-MM-DD]`, rendered per `instructions/email-format.md` v3: eyebrow `SKIPPED · NO MONITOR DATA`, no hero image, one section explaining what was checked and what was found, footer band with Run Log link). Write a Run Log row (Step 7) with Run Status = `Failed`, Notes = `Skipped: Monitor run for [date] missing or Failed — working from stale/partial data would risk publishing on bad input.` Exit.
- **If Monitor's row shows Run Status = `Partial`:** proceed, but note `Monitor ran degraded today (Partial)` in this run's Notes (Step 7) and in the digest email's status line — a degraded Monitor run may mean a thinner-than-usual pool, not an error in this agent.
- **Otherwise (Run Status = `Success`):** proceed normally to Step 0.5.

## Step 0.5: MCP Availability Gate (PRE-FLIGHT)

At run start, check whether `fetch_url` from the Spawn-Point-Fetcher MCP appears in your tool surface (after deferred-tool loading).

**If `fetch_url` is NOT available:** mark the run degraded, skip the fetch_url escalation tier in Step 2 (WebFetch-only verification, more items will land as `[UNVERIFIED — fetch_url unavailable]` and get omitted per Step 2's ambiguous-item rule), and send the degraded-mode email at the end of the run regardless of content (subject `[Spawn Point Daily Brief] DEGRADED RUN — fetch_url MCP unavailable`, rendered per `instructions/email-format.md` v3, mirroring Monitor's Step 0.5 degraded email: eyebrow `DEGRADED RUN`, no hero image, a "What ran anyway" table, a "What was lost" table, footer band). In Step 7, set Run Status = `Partial` and prepend Notes with `DEGRADED RUN: fetch_url MCP unavailable.`

## Step 1: Pull Today's Unprocessed Rows

`notion-query-data-sources` against `1b9db417-c801-4004-a687-e09fe2976e73` for rows where `Daily Brief Status` is empty. Pull Title, Type, Source, Source URL, Published Date, Detected At, Description, Pokémon Mentioned, Content Completeness.

**Zero-row case:** if the query returns zero rows, skip straight to Step 7. Write a Run Log row with Run Status = `Success`, New Entries Added = `0`, Notes = `Zero-content day — no unprocessed News & Updates rows, no Daily Brief published.` Do NOT send an email and do NOT create a Notion child page for the day (an empty digest is not worth Joe's attention). Exit.

## Step 2: Light-Touch Verify Each Row

For each row, re-fetch its Source URL: WebFetch first; on 403, escalate to the Spawn-Point-Fetcher MCP `fetch_url` tool; on a CF-challenge body from `fetch_url`, treat as failed (no WebSearch snippet fallback here — light-touch verification needs the actual page, not a search snippet). Confirm the fetched content still supports the row's Title/Description (the primary-source check) and skim for anything that contradicts it (the sanity check).

- **Clears both checks:** keep the row, carry its data into Step 3.
- **Fails to fetch through both tiers, OR the content contradicts/doesn't support the row:** omit the row from today's Brief. Leave `Daily Brief Status` blank (do not mark it) so tomorrow's run retries it naturally as Monitor keeps enriching it. Do not publish on a guess — there is no disagreement-gate machinery at this verification weight.

This is a lighter pass than Recon's full tri-source cross-check (`triggers/recon.md`) — one primary-source re-fetch plus a sanity read, not a three-way disagreement gate.

## Step 3: Categorize

Sort each verified row into ONE of these eight categories, based on its Type/Description (judgment call — Type is a free multi-select, not a locked enum):

- **Raid & Event Announcements** — new bosses confirmed, rotation changes, upcoming events
- **Events & Community Days** — announcements/reminders for named events
- **Datamines & Rumors** — unconfirmed leaks, mined data (`Status = Unconfirmed` rows land here almost always)
- **Shop & Store Updates** — newsworthy store rotation changes
- **Bugs & Outliers** — community-reported bugs, glitches, anomalies
- **Corporate/Niantic News** — statements, business news (Niantic for game-dev, Scopely for corporate, same convention as Monitor/Researcher)
- **Community Buzz** — trending Reddit/social discussions
- **Closing Soon** — deadline reminders. Reuses the exact Don't Miss callout format from `instructions/newsletter-creation.md` Section 12: `**[emoji] [Short header]**` + one sentence of consequence/CTA, ~25 words. A row lands here INSTEAD of its natural category when its main news value that day IS the approaching deadline.

**Adaptive sections:** only categories with at least one item that day appear in the digest. An empty category is omitted, never filled with default text.

## Step 4: Draft the Digest

Write to `output/daily-brief-[YYYY-MM-DD].md`, category by category, in the fixed order listed in Step 3.

**Per-item format:** bold headline (8-15 words) + 2-4 sentence summary (40-80 words) + inline source attribution in the sentence itself (e.g., "per LeekDuck," "X reported"), not just a trailing link. End each item with a `Source: [Site](URL)` line (singular, Daily Brief items are single-source by design, unlike Weekly's multi-source sections).

**Length is elastic, not fixed.** A quiet day might be 200 words across two categories; a major-announcement day can run much longer. No default filler.

**Title:** `Spawn Point Daily Brief — [Month Day, Year]` (e.g., `Spawn Point Daily Brief — September 4, 2026`).

## Step 5: Push to Notion

Find-or-create the `Spawn Point Daily Briefs` parent page per the Notion Databases section above. Under it, `notion-create-pages` a child page:
- **Title:** `Daily Brief — [YYYY-MM-DD]`
- **Body:** the Step 4 draft, category by category, each as an H2 heading + the item blocks underneath (paragraph blocks, no Notion image blocks, same limitation as Weekly; render any image reference as `Image: [alt](URL)` per the existing convention).

## Step 6: Email Joe

Subject `[Spawn Point Daily Brief] [Month Day, Year] — [N] items` (or `— quiet day` if only 1-2 items). Content spec (render per `instructions/email-format.md` v3):
- **Eyebrow:** `DAILY BRIEF · [YYYY-MM-DD]` (newspaper.png). No hero image, this is an operational digest email meant to be read-and-paste material, not a branded milestone announcement.
- **Headline:** e.g. `Today's Daily Brief is ready to paste`.
- **Status line:** Date = [YYYY-MM-DD] · Items = [N] · Categories = [list the categories that have content] · Status = Ready to publish (Web-only) / Degraded (if Step 0.5 or Step 0's Monitor-Partial note applies).

Section blocks, in order:
1. **The digest itself** — the full Step 4 draft, rendered category by category exactly as it'll be pasted into Beehiiv (headings + item blocks), so Joe can copy straight from the email if he doesn't want to open Notion.
2. **Publish reminder** — one line: "Publish as Beehiiv Web-only: on the post's Audience page, uncheck all Email Audience subscriber groups and leave only Web checked."
3. **Links** — Notion child page (titled link), Run Log (titled link, this run's row at top).

- **Footer band:** Agent = Spawn Point Daily Brief Agent, Run Log link, filter Trigger = Daily Brief.
- Run the v3 pre-send checklist before sending.

## Step 7: Mark Rows + Write Run Log Entry (ALWAYS RUN, last step before exit)

For every row actually included in today's digest (Step 2 survivors that made it into Step 4): `notion-update-page` to set `Daily Brief Status = Included - [YYYY-MM-DD]`.

Then `notion-create-pages` with parent `data_source_id: "d808fb32-e641-480f-a90e-78f0685c78c9"` (the Spawn Point Run Log). Properties:
- **Run Title** (title): `Daily Brief [YYYY-MM-DD]`
- **Run Timestamp** (datetime): actual run start time in UTC, ISO-8601, `is_datetime=1`
- **Trigger** (select): `Daily Brief`
- **Run Status** (select): `Success` if the digest published to Notion + email cleanly; `Partial` if degraded (Step 0.5, or Monitor-Partial per Step 0) but still produced output; `Failed` if Step 0 aborted the run, or the Notion push failed
- **New Entries Added** (number): count of rows marked `Included` this run (0 on a zero-content day)
- **Duplicates Prevented** (number): 0 (not applicable, this agent doesn't dedup, Monitor already did)
- **Backfill Dupes Marked** (number): 0
- **Enrichments Succeeded** (number): 0
- **Dedup Enrichments** (number): 0
- **fetch_url MCP Rescues** (number): count of Step 2 fetch_url calls that returned 200 after a WebFetch 403
- **Tier Mix** (rich text): e.g., `WebFetch: 6 / fetch_url rescue: 2 / omitted-ambiguous: 1`
- **Sources Failed** (rich text): rows omitted in Step 2 because verification failed both tiers
- **CF Regressions** (rich text): URLs that returned a CF-challenge body via fetch_url
- **Notes** (rich text): category breakdown, Monitor-Partial note if applicable, any Step 0.5 degradation, zero-content note if applicable
- **Email Sent** (checkbox): checked if Step 6 sent, unchecked otherwise (zero-content days = unchecked)
- **Email Subject** (rich text): actual subject if sent, else empty

**This step is NOT skippable**, including on a Step 0 abort (that path writes its own Failed row directly, per Step 0) and on a zero-content day (that path writes its own Success/0 row directly, per Step 1).

## Important Rules
- The user's name is **Joe Landor** (not "Joel").
- This agent has NO Beehiiv access and NO git push credentials. Publishing is 100% manual, Joe copies from the email or the Notion child page into a new Beehiiv Web-only post.
- The cloud sandbox blocks outbound curl/wget. WebFetch, WebSearch, and the Spawn-Point-Fetcher MCP `fetch_url` tool are the only outbound primitives.
- **Notion MCP fallback:** if the Notion MCP is unavailable mid-run, use the sandbox's allowed Notion endpoint via curl with token `ntn_REDACTED_IN_SNAPSHOT` (redacted per GitHub push protection, live value in trigger config; see the live trigger via `RemoteTrigger get` once this trigger exists, or `RemoteTrigger get trig_01GYjXQqpCgDiFfzo3MKDH5E` for Researcher's copy of the same token, if you need the value). This is a Notion API token routed through the sandbox's allowed Notion endpoint, NOT general curl.
- This agent never creates, edits, or enriches News & Updates rows beyond writing `Daily Brief Status`, that's Monitor's job.
- Once a row's `Daily Brief Status` is `Included - <date>`, it never resurfaces in a later Daily Brief, even if Monitor enriches it further afterward.
- All outbound email goes through the Spawn-Point-Fetcher MCP `send_email` tool (Resend-backed). Gmail MCP is NOT used for sending.
- CRITICAL: Step 0 (Monitor-ran check), Step 0.5 (MCP gate), and Step 7 (Run Log write) are NOT skippable.
- CRITICAL: Zero new items is not a failure, it's a `Success` row with `New Entries Added = 0` and no email.
````

- [ ] **Step 2: Verify**

```bash
cd /Users/joelandor/Documents/spawn-point
grep -c "^## Step" triggers/daily-brief.md
```

Expected: `8` (Step 0, 0.5, 1, 2, 3, 4, 5, 6, 7 — note Step 0.5 also matches `^## Step`, so expected count is actually 9; confirm the count matches the number of `## Step` headings you intended, then spot-check each heading text with `grep "^## Step" triggers/daily-brief.md`).

- [ ] **Step 3: Commit and push**

```bash
cd /Users/joelandor/Documents/spawn-point
git add triggers/daily-brief.md
git commit -m "triggers: add Daily Brief trigger instructions"
git push origin main
```

---

### Task 6: Create the Daily Brief RemoteTrigger (disabled)

**Files:** none (RemoteTrigger API call)

**Depends on:** Task 5 (the file the pointer references must already be on `main`, since Task 9's dry-run will have the agent read it from the repo).
**Produces:** a new RemoteTrigger with a real trigger ID and UUID. Task 7 (dry-run) and Task 8 (kickoff snapshot, enablement) depend on this ID.

- [ ] **Step 1: Draft the pointer prompt, matching Monitor's phrasing**

Call `RemoteTrigger get trig_01VTWmmrrBWxioH8DUCw364q` (Monitor) to re-confirm its exact live pointer text in `job_config.ccr.events[0].data.message.content`. Use that exact sentence structure, substituting only the trigger name and filename, to write the Daily Brief pointer. Starting draft (adapt phrasing to match Monitor's exact style once re-confirmed):

```
It's time for the Spawn Point Daily Brief run. Read triggers/daily-brief.md in the spawn-point-newsletter repo (github.com/landoralpha/spawn-point-newsletter, branch main) for your full instructions, then execute them.
```

- [ ] **Step 2: Build the create request body**

```json
{
  "name": "Spawn Point Daily Brief",
  "cron_expression": "20 23 * * *",
  "enabled": false,
  "job_config": {
    "ccr": {
      "environment_id": "env_01VSb95kc6a7pofXsvGasHhc",
      "events": [
        {
          "data": {
            "message": {
              "content": "It's time for the Spawn Point Daily Brief run. Read triggers/daily-brief.md in the spawn-point-newsletter repo (github.com/landoralpha/spawn-point-newsletter, branch main) for your full instructions, then execute them.",
              "role": "user"
            },
            "type": "user"
          }
        }
      ],
      "session_context": {
        "allowed_tools": ["preset:default","Task","Bash","Glob","Grep","Read","Edit","MultiEdit","Write","NotebookEdit","WebFetch","TodoWrite","WebSearch","BashOutput","KillBash","Skill","Tmux","Monitor","SendUserFile","REPL"]
      }
    }
  },
  "mcp_connections": [
    {"connector_uuid": "ed9bce03-43bd-45a3-b6f0-4cb80740be87", "name": "Gmail", "url": "https://gmailmcp.googleapis.com/mcp/v1", "clear_tool_policy_overrides": false, "permitted_tools": [], "tool_policy_overrides": []},
    {"connector_uuid": "9be38711-d9fe-4445-b85c-ad7cad41946a", "name": "Notion", "url": "https://mcp.notion.com/mcp", "clear_tool_policy_overrides": false, "permitted_tools": [], "tool_policy_overrides": []},
    {"connector_uuid": "cf7c80bc-f8e1-4ae1-a87a-e2a04108ecbc", "name": "Spawn-Point-Fetcher", "url": "https://fetcher-mcp.vercel.app/mcp/Lyu2UTyvxgOm84fqnjETWyQXX8bLP2NMvNTcKrsBOpQ", "clear_tool_policy_overrides": false, "permitted_tools": [], "tool_policy_overrides": []}
  ]
}
```

Note: Monitor's `RemoteTrigger get` response also includes a `session_request` field that appears to be a server-derived near-duplicate of the same event data (different field names: `ephemeral`, `historical`, `mentioned_account_ids`, `payload.message`, `user_declared_urls`). Do NOT include `session_request` in the create body. Attempt the create with only the fields above first; if the tool rejects the call for a missing required field, run `ToolSearch query: "select:RemoteTrigger"` to re-inspect the exact schema before retrying.

Deliberately `enabled: false` for this step, so the trigger cannot fire on its own cron before Task 7's dry-run validates it.

- [ ] **Step 3: Call RemoteTrigger create**

Call `RemoteTrigger` with `action: "create"` and the body from Step 2.

- [ ] **Step 4: Verify**

Call `RemoteTrigger get <new trigger ID>` and confirm: `name` = `Spawn Point Daily Brief`, `cron_expression` = `20 23 * * *`, `enabled` = `false`, the three `mcp_connections` entries match Step 2 exactly, `job_config.ccr.environment_id` = `env_01VSb95kc6a7pofXsvGasHhc`.

- [ ] **Step 5: Record the new trigger ID**

Note the returned trigger ID and UUID for use in Tasks 7 and 8 (Task 8 also fills these into `triggers/daily-brief.md`'s header comment block, replacing the two `PENDING` placeholders written in Task 5).

---

### Task 7: Dry-run the Daily Brief trigger against real backlog

**Files:** none (RemoteTrigger + Notion inspection only)

**Depends on:** Task 6.
**Produces:** confirmation that Steps 0-7 of `daily-brief.md` behave correctly against real data before the live cron is turned on. Task 8 depends on this passing.

- [ ] **Step 1: Fire the trigger manually**

Call `RemoteTrigger` with `action: "run"` against the Task 6 trigger ID.

If the call fails specifically because the trigger is disabled: temporarily call `RemoteTrigger update` with `enabled: true`, immediately call `run`, then call `update` again with `enabled: false` right after (before the next real 23:20 UTC fire) so it doesn't fire again unsupervised before review completes.

- [ ] **Step 2: Inspect the run**

Call `RemoteTrigger list_runs` against the trigger ID, find the run from Step 1, and call `RemoteTrigger get_run_log` on it. Read through the transcript for: which Step 0/0.5 branch it took, how many rows it pulled in Step 1, how many survived Step 2's light-touch verification, how the surviving rows were categorized in Step 3, and the resulting draft from Step 4.

- [ ] **Step 3: Check the Notion and email side effects**

Query `1b9db417-c801-4004-a687-e09fe2976e73` for any rows now showing `Daily Brief Status = Included - <date>` and confirm they match the run log's account. Confirm a `Spawn Point Daily Briefs` parent page now exists in Notion with a same-day child page (or, on a zero-content day, confirm no child page was created, per Step 1's zero-row branch). Confirm the Run Log DB (`d808fb32-e641-480f-a90e-78f0685c78c9`) has a new row with `Trigger = Daily Brief`. If Step 6 sent an email, confirm Joe received it and that its content matches the Notion child page.

- [ ] **Step 4: Judge the output against the spec**

Read the drafted digest against Spec Section 2's requirements: adaptive categories (no empty-category filler), per-item format (bold headline 8-15 words, 2-4 sentence summary 40-80 words, inline attribution), voice (third-person, factual, no em dashes, "Pokémon" spelled correctly), and the Closing Soon category's Don't Miss-style format if any row landed there. If something is off, fix `triggers/daily-brief.md` (repeating Task 5's verify/commit/push steps for the fix), then repeat Steps 1-4 of this task before proceeding to Task 8.

---

### Task 8: Enable the live cron and finish documentation

**Files:**
- Modify: `triggers/daily-brief.md` (fill in the two `PENDING` header placeholders with the real trigger ID/UUID from Task 6)
- Create: `triggers/kickoff/daily-brief-kickoff.md`
- Modify: `triggers/kickoff/README.md` (new table row)
- Modify: `triggers/README.md` (new table row)

**Depends on:** Task 7 passing.
**Produces:** the Daily Brief trigger live on its real schedule, with the same documentation completeness as the three pre-existing triggers.

- [ ] **Step 1: Enable the trigger**

Call `RemoteTrigger update` against the Task 6 trigger ID with `enabled: true`.

- [ ] **Step 2: Verify**

Call `RemoteTrigger get <trigger ID>` and confirm `enabled: true`, `cron_expression: "20 23 * * *"` still intact.

- [ ] **Step 3: Fill in the header placeholders in `daily-brief.md`**

Using the Edit tool, replace:

```
Trigger ID: PENDING — filled in after Task 6 (RemoteTrigger create) succeeds.
Trigger UUID: PENDING — filled in after Task 6.
```

with the actual trigger ID and UUID returned by Task 6 (e.g. `Trigger ID: trig_XXXXXXXXXXXXXXXXXXXXXXXX` / `Trigger UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).

- [ ] **Step 4: Write `triggers/kickoff/daily-brief-kickoff.md`**

Follow the same snapshot format as the three existing `*-kickoff.md` files: call `RemoteTrigger get <trigger ID>` fresh, and write its `job_config.ccr.events[0].data.message.content` value into a new file `triggers/kickoff/daily-brief-kickoff.md`, with a one-line header comment noting the trigger ID and the UTC timestamp of the snapshot (mirroring the existing three kickoff files' format).

- [ ] **Step 5: Add a row to `triggers/kickoff/README.md`**

Using the Edit tool, replace:

```
| `monitor-kickoff.md` | `trig_01VTWmmrrBWxioH8DUCw364q` | `0 23 * * *` (daily 23:00 UTC) | Niantic announcement monitor |
```

with:

```
| `monitor-kickoff.md` | `trig_01VTWmmrrBWxioH8DUCw364q` | `0 23 * * *` (daily 23:00 UTC) | Niantic announcement monitor |
| `daily-brief-kickoff.md` | `<trigger ID from Task 6>` | `20 23 * * *` (daily 23:20 UTC) | Daily Brief digest agent |
```

(Substitute the real trigger ID from Task 6 for `<trigger ID from Task 6>`.)

- [ ] **Step 6: Add a row to `triggers/README.md`**

Using the Edit tool, replace:

```
| `recon.md` | `trig_01WB5YXtpMZR8zgebrsPC7Ah` | `0 22 * * 5` (Fridays 22:00 UTC = 6 PM Eastern) | Pre-Publish Fact-Check Agent — verifies the Beehiiv draft before publish. |
```

with:

```
| `recon.md` | `trig_01WB5YXtpMZR8zgebrsPC7Ah` | `0 22 * * 5` (Fridays 22:00 UTC = 6 PM Eastern) | Pre-Publish Fact-Check Agent — verifies the Beehiiv draft before publish. |
| `daily-brief.md` | `<trigger ID from Task 6>` | `20 23 * * *` (daily 23:20 UTC) | Daily Brief Agent — drafts the daily digest from Monitor's News & Updates rows. |
```

(Substitute the real trigger ID from Task 6.)

- [ ] **Step 7: Commit and push**

```bash
cd /Users/joelandor/Documents/spawn-point
git add triggers/daily-brief.md triggers/kickoff/daily-brief-kickoff.md triggers/kickoff/README.md triggers/README.md
git commit -m "triggers: enable Daily Brief live cron, add kickoff snapshot and docs rows"
git push origin main
```

---

### Task 9 (time-gated, run at least 5-7 days after Task 8): Dry-run Weekly's Step 3.5 against real Daily Brief output

**Files:** none (RemoteTrigger inspection only)

**Depends on:** Task 3 (Step 3.5 exists) and Task 8 (enough real Daily Brief runs must have accumulated `Included` rows for Step 3.5 to have real material to pull from — the spec explicitly calls for this dry-run to happen once real output exists, not immediately).

- [ ] **Step 1: Confirm there's real data to test against**

Query `1b9db417-c801-4004-a687-e09fe2976e73` for rows where `Daily Brief Status` starts with `Included` and `Detected At` is within the last 7 days. If this returns zero rows, wait longer before running this task (Daily Brief hasn't accumulated a week of real output yet).

- [ ] **Step 2: Fire the Researcher trigger manually**

Call `RemoteTrigger run` against `trig_01GYjXQqpCgDiFfzo3MKDH5E` (Researcher).

- [ ] **Step 3: Inspect the run**

Call `RemoteTrigger list_runs` and `get_run_log` for the fired run. Confirm the transcript shows Step 3.5 executing (querying the Daily Brief pool, either finding rows or correctly falling back to fresh-research-only on an empty pool), and confirm the Step 4 Trending Topic Candidates and Don't Miss candidates sections in the resulting Pre-Research Plan email visibly draw on that pool where material existed.

- [ ] **Step 4: Judge the result**

If Step 3.5 is skipped, errors, or the Trending Topic / Don't Miss candidates show no trace of pulling from the Daily Brief pool despite real `Included` rows existing, fix `triggers/researcher.md` (repeating Task 3's edit/verify/commit/push pattern for the fix) and repeat Steps 2-4 of this task.

---

## Self-Review

**1. Spec coverage:**
- Section 1 (Notion Schema Changes) → Tasks 1, 2.
- Section 2 (Daily Brief Trigger, all 10 sub-bullets: new file, fire time, source, 8 categories, per-item format, elastic length, scope boundary, voice, verification, output, approval/publish, housekeeping) → Task 5 (full file content), validated live by Task 7.
- Section 3 (Weekly Trigger Redesign: new Step 3.5, Trending Topic/Don't Miss sourcing, schedule-shaped sections untouched, Steps 0-3/5-8 unchanged) → Task 3, validated by Task 9.
- Section 4 (Archive Mechanism) → Tasks 3 and 4 both archive before editing; no in-file commented blocks added to `researcher.md`.
- Section 5 (Error Handling & Edge Cases: zero new items, Monitor didn't finish, ambiguous item, already-included items, validation before going live) → all five covered explicitly in Task 5's `daily-brief.md` content (Steps 0, 1, 2, Important Rules) and in Tasks 7 and 9 (the two-stage dry-run the spec calls for).
- Persistence/Infrastructure (Notion-only, no new DB) → confirmed, no task introduces a new database.
- Recon → confirmed unchanged, no task touches `recon.md`.
- Out of Scope (no auto-publish, no Recon changes, no anti-slop changes, no new DB, no cadence change) → none of the 9 tasks touch any of these.

**2. Placeholder scan:** the only literal `PENDING` placeholders in this plan are in Task 5's `daily-brief.md` header comment (`Trigger ID: PENDING`, `Trigger UUID: PENDING`), which is intentional and explicitly resolved by Task 8 Step 3, since the real trigger ID cannot exist before Task 6 runs. No other placeholder language appears; every step includes literal, usable content (exact markdown, exact JSON, exact bash, exact old/new text for edits).

**3. Type/name consistency:** `Daily Brief Status` (Task 1) matches its usage in Task 3's Step 3.5 text, Task 5's Notion Databases section, Step 1, and Step 7. `Daily Brief` as the Trigger select option (Task 2) matches its usage in Task 5's Step 7 and Task 7's verification query. The trigger ID placeholder flows consistently: Task 6 creates and records it, Task 7 uses it, Task 8 substitutes it into `daily-brief.md`, `kickoff/README.md`, and `README.md` in three separate edits, all keyed off the same "Task 6 trigger ID" reference. The environment_id, allowed_tools list, and three mcp_connections entries in Task 6 are copied verbatim from the Global Constraints section, which was itself copied verbatim from Monitor's live `RemoteTrigger get` response.

---

## Execution Handoff

Plan complete and saved to `/Users/joelandor/Documents/spawn-point/plans/2026-09-04-daily-brief-redesign-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

**Which approach?**
