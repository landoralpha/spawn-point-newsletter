# Spawn Point Daily Brief + Weekly Redesign — Spec

**Date:** 2026-09-04
**Status:** Draft
**Author:** Joe + Claude (brainstorm session)

---

## Problem Statement

Spawn Point's Weekly newsletter is stalled — production has stopped multiple times for multi-week stretches (most recently, draft #21 abandoned since 2026-07-02) because the current Weekly pipeline (`triggers/researcher.md`) does heavy from-scratch research and multi-source verification for every issue, every week. There is no lighter-weight cadence that keeps content flowing between issues.

Inspired by Tucson Daily Brief (TDB) — a solo-operated, AI-driven local news outlet that publishes a daily brief plus a separate weekly digest, using a "AI for speed and scale, human for judgment and final edit" model — this redesign introduces a **Daily Brief** alongside the existing Weekly, so news capture happens continuously and lightly instead of being front-loaded into one heavy weekly push.

## Goal

1. Add a new **Daily Brief** trigger that produces a light-touch-verified daily PoGO news digest, built on top of Monitor's existing daily Notion aggregation (no duplicate infrastructure).
2. Redesign the **Weekly** trigger so its news-shaped sections roll up the week's Daily Briefs instead of researching from scratch, while its schedule-shaped sections keep their existing fresh-research rigor.
3. Do this without deleting anything — superseded content gets archived per the project's standing don't-delete rule, not removed.

## Approaches Considered

- **Approach 1 (selected):** New Daily Brief trigger layered on Monitor's existing daily aggregation; Weekly becomes a curated roll-up of the week's Daily Briefs for its news-shaped content, plus continued fresh research for schedule-shaped content. Reuses working infrastructure (Monitor's dedup/enrichment pipeline), lowest new-build cost.
- **Approach 2 (rejected):** Fully standalone Daily pipeline with its own sourcing, Weekly just trimmed down. Rejected — duplicates work Monitor already does well.
- **Approach 3 (rejected):** Single unified agent replacing Monitor, Researcher, and Recon entirely. Rejected — too large a rewrite, discards a working, well-tested pipeline for no clear benefit.

## Architecture Overview

```
Monitor (unchanged, fires daily 23:00 UTC)
    |
    v
News & Updates DB (Notion) — gets a new row/update per detected item
    |
    v
Daily Brief (NEW, fires daily ~23:20 UTC)
    | reads today's new/unprocessed rows
    | light-touch verify (primary source + sanity check)
    | drafts categorized digest -> Notion + email to Joe
    | Joe manually publishes as a Beehiiv Web-only post (no subscriber email)
    | marks rows "Daily Brief Status = Included - <date>"
    v
... repeats daily across the week ...
    |
    v
Weekly / Research Agent (MODIFIED, cron unchanged: fires Monday, publishes Saturday)
    | news-shaped sections (Trending Topic, Don't Miss): start from the week's Daily
    |   Briefs, supplemented by fresh research as needed
    | schedule-shaped sections (Raid Bosses, GBL, Max Monday, Community Day, etc.):
    |   freshly researched each Monday, unchanged
    | reference-data sections (Hundo CP Master Table, counters, movesets): unchanged
    v
Beehiiv draft -> Joe reviews and manually sends (subscribers + public), unchanged

Recon / Pre-Publish (unchanged) -- verifies whatever draft exists regardless of
how it was produced, fires Friday 22:00 UTC or manually
```

---

## Section 1: Notion Schema Changes (additive only)

- **New property `Daily Brief Status`** on the News & Updates DB (data source `1b9db417-c801-4004-a687-e09fe2976e73`). Values: blank (default, not yet processed) or `Included - <date>`. No existing property is modified, renamed, or removed.
- **New option `Daily Brief`** added to the Run Log DB's (data source `d808fb32-e641-480f-a90e-78f0685c78c9`) `Trigger` select, alongside the existing `Monitor` / `Research Agent` / `Recon` options.
- No new database is introduced (see Persistence, below) — this stays entirely inside the existing Notion schema Monitor already writes to.

## Section 2: Daily Brief Trigger

- **New file:** `triggers/daily-brief.md`, a new RemoteTrigger pointing to it.
- **Fire time:** daily at ~23:20 UTC — 20 minutes after Monitor's 23:00 UTC run, so it reads that day's freshly-written rows.
- **Source:** rows in the News & Updates DB where `Daily Brief Status` is blank (i.e., detected today and not yet covered).
- **Categories** (adaptive — only sections with actual content that day appear):
  - Raid & Event Announcements — new bosses confirmed, rotation changes, upcoming events
  - Events & Community Days — announcements/reminders
  - Datamines & Rumors — unconfirmed leaks, mined data
  - Shop & Store Updates — newsworthy store rotation changes
  - Bugs & Outliers — community-reported bugs, glitches, anomalies
  - Corporate/Niantic News — statements, business news
  - Community Buzz — trending Reddit/social discussions
  - Closing Soon — deadline reminders (reuses the existing Don't Miss deadline-callout logic)
- **Per-item format:** bold headline (8-15 words) + 2-4 sentence summary (40-80 words) + inline source attribution in the sentence itself (e.g., "per LeekDuck," "X reported"), not just a trailing link.
- **Length:** elastic, not fixed. A quiet day might be 200 words across two sections; a major-announcement day can run much longer. No default filler — an empty category is simply omitted.
- **Scope boundary:** Daily Brief covers discrete, dated things that were *detected or reported* — from any source, official or community (announcements, datamines, bugs, outliers, trending discussions). It never makes live, locally-varying schedule claims (e.g., "today's active raid boss," "current Spotlight Hour Pokémon") — those depend on the reader's timezone in a global playerbase and stay Weekly's job, or a separate always-current reference.
- **Voice:** third-person, strictly factual, no editorializing or hedging. Inline source attribution per claim. Emoji section headers are the primary personality/warmth outlet; any looser conversational tone is reserved for one low-stakes closer section (e.g., Community Buzz), never the hard-news sections. Same banned-claims list and no-em-dash rule as `newsletter-creation.md` already enforces for the Weekly.
- **Verification:** light-touch — primary source + sanity read, not Recon's full tri-source chain.
- **Output:** draft written to Notion + emailed to Joe in ready-to-paste form.
- **Approval/publish:** manual. Joe reviews the draft and manually creates/publishes the Beehiiv post as Web-only, by unchecking all subscriber groups in the Email Audience section on the post's Audience page and leaving only the Web audience checked (confirmed native Beehiiv behavior — see References). This is necessary because Beehiiv MCP is read-only and the agent has no git-push credentials either, so no automated publish path exists yet; it also reuses the same manual-publish muscle already used for the Weekly's Saturday send. Auto-publish is an explicit future revisit once the process is proven, not part of this spec.
- **Housekeeping:** marks each included row's `Daily Brief Status` as `Included - <date>`; writes a Run Log row with `Trigger = Daily Brief`.

## Section 3: Weekly Trigger Redesign

- **File:** `triggers/researcher.md` — modified, not replaced.
- **Cron/publish cadence: unchanged.** Cron fires Monday, publish is still a manual Saturday send. Explicitly decided not to move this even though the pipeline is getting lighter, since Weekly isn't relied on for breaking news and working a week ahead is fine.
- **Step 4 (research brief) gets a new first move:** review the week's Daily Briefs before doing fresh research.
  - **News-shaped sections** (Trending Topic, Don't Miss) start from what the week's Daily Briefs already surfaced — since that content is already lightly verified and written up — supplemented by fresh research to fill gaps or add depth. Not limited to daily content only.
  - **Trending Topic candidates** are drawn from the raw pool of items across *all* of the week's Daily Brief categories (a bug that won't die, a recurring datamine, an unusually engaged Community Buzz item), not from any pre-sorted "trending" bucket — Daily itself does no pre-sorting for this purpose.
  - **Schedule-shaped sections** (Raid Bosses, GBL, Spotlight Hour, Max Monday, Community Day) stay freshly researched each Monday, unchanged — these were never sourced from Monitor's feed since they're live-schedule state, not news.
  - **Reference-data sections** (Hundo CP Master Table, counters, movesets) are unaffected — same formula self-verification and Recon cross-check as today.
- **Steps 0-3 and 5-8 of researcher.md are otherwise unchanged.**

## Section 4: Archive Mechanism (don't-delete rule)

Per the project's standing instruction, nothing gets deleted — superseded content is archived.

- Before editing `triggers/researcher.md` (and `instructions/newsletter-creation.md`, if Daily's voice/section rules end up formalized there too), snapshot the pre-redesign version to a dedicated `archive/` directory that mirrors the repo structure, e.g. `archive/triggers/researcher-pre-daily-brief-2026-09-04.md`.
- Normal git commits continue as usual underneath — the archive folder is a discoverable, human-readable safety net on top of git history, not a replacement for it.
- No in-file commented-out blocks for `researcher.md` specifically — it's read fresh by a scheduled agent every Monday, so dead commented text would waste context on every run and risks being misread as active instructions.

## Section 5: Error Handling & Edge Cases

- **Zero new items that day:** Daily Brief doesn't publish. No filler post. A Run Log row is still written noting zero-content, so the gap is visible in the log.
- **Monitor didn't finish or failed:** Daily Brief checks for that day's Monitor Run Log entry before proceeding. If it's missing or shows a failed run, Daily Brief skips and alerts Joe rather than working off stale or partial data.
- **Ambiguous item under light-touch verification:** if it doesn't clear the primary-source-plus-sanity-check bar, it's omitted from that day's Brief rather than published on a guess. No disagreement-gate machinery at this weight.
- **Already-included items:** once a News & Updates row is marked `Included`, it never resurfaces in a later Daily Brief, even if Monitor enriches it further afterward. Weekly still sees the enriched version, since it reads the Notion row directly rather than the frozen daily text.
- **Validation before going live:** dry-run the new Daily Brief trigger against a past day or two of existing Notion data before wiring the live 23:20 UTC schedule, to sanity-check categorization, voice, and length elasticity without waiting on live data. Similarly, dry-run Weekly's modified Step 4 once a few days of real Daily Brief output exist to test against.

## Persistence / Infrastructure

Notion-only, consistent with the existing pipeline. Confirmed: no dedicated app database is introduced as part of this redesign. (The Hundo CP Master Table's separate JSON source of truth lives on the unrelated `pogo-hundo-generator` Vercel project and is out of scope here.)

## Recon (Pre-Publish Trigger)

Largely unchanged. Recon verifies whatever draft exists at publish time regardless of how it was produced, so it needs no structural changes from this redesign.

---

## References

- Tucson Daily Brief — daily post example: `tucsondailybrief.com/posts/2026-09-04.html` (categorized digest, ~1,800-2,000 words, 6-8 emoji-headed sections, wire-service voice)
- Tucson Daily Brief — background on the creator/pipeline: `twit.tv/posts/tech/building-ai-driven-local-newspaper-lessons-tucson` ("Live AI Reporter" pipeline, Deepgram/FFmpeg transcription -> Sonnet drafting -> brief human editorial review, ~$40/month operating cost)
- Beehiiv — confirms web-only publishing (uncheck all Email Audience groups, keep Web checked) is native, supported behavior: `beehiiv.com/support/article/13064033042199-options-on-the-audience-page-of-the-post-flow`

## Out of Scope

- Auto-publishing the Daily Brief without manual approval — explicitly deferred to a future revisit once the process is proven.
- Changes to Recon's verification logic.
- Changes to the anti-slop writing-quality infrastructure.
- Introducing a dedicated app database.
- Changing Weekly's Monday-cron / Saturday-publish cadence.
