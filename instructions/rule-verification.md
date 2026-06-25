# Rule Verification Reference

Pokémon GO rules change over time. Cup bans rotate, season schedules shift, mechanics get reworked, shiny rates get adjusted, new Pokémon become Dynamax-eligible. **Never trust cached values from this repo or from prior conversations as ground truth — always re-verify against current sources during each newsletter run.**

This file documents which game rules are volatile, where to verify them, and how stale information has burned the agent before.

## Rules That Change Frequently

### 1. Cup Ban Lists (themed PvP cups)
**Volatility:** High — Niantic adjusts bans between iterations of the same cup name.

**Verify each newsletter run if a themed cup is active:**
- Official @PokemonGoApp Twitter/X (announcement post for the current cup)
- LeekDuck event page for the cup
- Pokémon GO Hub "Nifty or Thrifty" article for that specific iteration

**Past examples:**
- Jungle Cup (October 2025 iteration vs May 2026 iteration) — both banned Galarian Stunfisk + Gligar, but this isn't guaranteed for future iterations
- Some cup iterations add or remove bans based on community feedback

**Rule:** Don't assume "Jungle Cup bans X" applies to every Jungle Cup forever. Re-fetch the ban list for the current week's cup.

### 2. Daily Discoveries / Weekly Schedule
**Volatility:** Medium — set per season, can change at season transitions.

**Verify each newsletter run:**
- Official Pokémon GO blog season post
- LeekDuck season page
- Pokémon GO Hub season summary

**Past examples:**
- Memories in Motion (March 3, 2026): replaced Spotlight Hours with day-of-week Daily Discoveries
- Daily Discovery bonuses (which day gets which boost) can shift between seasons
- GO Battle Thursday's 4x Stardust + 50 battles cap is current as of Memories in Motion but may change next season

**Rule:** At each newsletter run, confirm the current season's Daily Discoveries schedule before writing the section.

### 3. Shiny Rates
**Volatility:** Low-Medium — major changes are rare but happen (like the wild flattening to 1/512 in March 2026).

**Verify periodically:**
- Bulbapedia Shiny Pokémon (GO) page
- Community research on r/TheSilphRoad
- Pokémon GO Hub shiny rate guide

**Past examples:**
- March 3, 2026 (Memories in Motion): all wild Pokémon shiny rate flattened to 1/512, perma-boost system removed for wild
- Lake Trio "technical issue" with reduced shiny rates in remote raids — Niantic acknowledged and fixed

**Rule:** Check the shiny-odds-reference.md file in this repo, but if a community-noticed change isn't reflected there, flag it as `[VERIFY: shiny rate may have changed]` and prioritize updating the reference.

### 4. Raid Mechanics
**Volatility:** Medium — Niantic occasionally reworks raid systems.

**Verify periodically:**
- Official Pokémon GO blog
- LeekDuck event pages
- Pokémon GO Hub raid guides

**Past examples:**
- Shadow Raids became Remote Raid-eligible (no longer in-person only)
- Monthly Legendary Shadow Pokémon now raid every day during their window, not just weekends
- 1-Star and 3-Star Shadow Raids can appear during the week, not just weekends

**Rule:** When writing about raids, don't assume past mechanic restrictions still apply. Verify current rotation and accessibility.

### 5. Dynamax / Max Battle Eligibility
**Volatility:** Medium — Niantic adds new Dynamax-eligible Pokémon over time.

**Verify each newsletter run when Max Monday or Max Battles are featured:**
- Pokémon GO Hub Max Battle tier lists (attack/defense/healers)
- LeekDuck Max Battle pages
- Pokebase.app Dynamax tier list

**Past examples:**
- Necrozma forms (Dusk Mane / Dawn Wings) have NOT been Dynamax-eligible historically
- Shadow Pokémon CANNOT Dynamax (this rule appears stable but always verify when in doubt)

**Rule:** Before recommending a Pokémon as a Max Battle attacker/defender/healer, verify it's currently on the Dynamax-eligible list. Don't assume past tier lists still apply.

### 6. GO Pass / Ticket Pricing & Contents
**Volatility:** Medium — changes per event.

**Verify each newsletter run for paid offers:**
- Official event announcement
- LeekDuck event page

**Past examples:**
- 2026 shift from paid event tickets to "Event GO Passes"
- Special Research ticket prices have varied ($1.99 standard, sometimes higher for premium)

**Rule:** Don't assume historical pricing or contents. Confirm against the current event page.

### 7. Trading Mechanics
**Volatility:** Low-Medium — occasional seasonal bonuses.

**Verify during seasons with trading-related changes:**
- Memories in Motion 2026: L31+ in-person trades give 1 guaranteed XL Candy + 1 regular candy
- Lucky cap: raised from 35 to 45 lifetime in January 2026
- Lucky guarantee species window: shifted to include 2020 catches

**Rule:** Trading bonuses listed in past references may be specific to a particular season. Check if they're still active.

### 8. Egg Pools
**Volatility:** High — pools change with seasons and events.

**Verify each newsletter run:**
- LeekDuck egg hatching guide
- Pokémon GO Hub current egg pool article

**Rule:** Past Adventure Sync 50km exclusives or 7km pool contents may be wrong for the current week.

### 9. Catch Mechanics & Bonuses
**Volatility:** Low — core mechanics stable, event bonuses change.

**Verify:**
- Type medal bonuses (Bronze +1, Silver +2, Gold +3, Platinum +4) — stable
- Excellent throw / Curveball multipliers — stable
- Quick-catch technique — stable, Niantic-tolerated
- Same-type Mega bonus catch candy — adjusted in February 2026

**Rule:** Mechanics described in framework angles are stable unless explicitly noted. Event-specific bonuses always need fresh verification.

### 10. Team GO Rocket
**Volatility:** Medium — balloon schedule and event variations change.

**Verify when Rocket events are active:**
- Standard balloons: every 6 hours (12:00 and 6:00 AM/PM)
- Takeover events: every 2 hours (12 balloons/day)
- New leader lineups, Giovanni rotations, Shadow Pokémon rosters

**Rule:** Balloon schedule appears stable but always verify if the agent's information predates the current week.

## How the Agent Should Apply This

### At the start of each newsletter run

After Step 0 (date determination) and Step 1 (read project files), perform a **Rule Verification Pass** before diving into research:

1. Check if the current GBL season changed since the last reference data
2. If a themed cup is active, fetch its current ban list (don't trust cached lists)
3. If Max Battles or Max Monday are featured, verify the current Dynamax-eligible list
4. If a paid event is featured, verify current pricing/contents
5. Note any rule changes detected in the Attention Items section of the research brief

### During research

- When citing a fact that involves a "rule" (eligibility, ban, schedule, multiplier, mechanic), confirm it's current
- Prefer authoritative sources (Niantic announcements, LeekDuck) over cached repo data for any volatile rule
- If a repo reference file says "X is true" but a current source contradicts it, **trust the current source** and flag the staleness for follow-up update

### Rule conflict resolution

When this repo's reference files conflict with current sources:
1. Trust the current authoritative source
2. Flag in the research brief: `[STALE REFERENCE: instructions/X.md says Y but current source says Z]`
3. Continue with the current information for the newsletter
4. Joe can update the reference file based on the flag

### What to flag in the Attention Items

At the top of the research brief, flag any rule changes detected:
- `[RULE CHANGE: GBL Thursday cap changed from 50 to N battles]`
- `[RULE CHANGE: Jungle Cup ban list now includes [new ban]]`
- `[RULE CHANGE: New season started: [name], schedule changes affect Daily Discoveries section]`
- `[POSSIBLE RULE CHANGE: shiny rate for X seems different from reference, needs verification]`

This lets Joe update the repo's reference files if a real change occurred.

## Quarterly Reference-File Verification (Drift Detection)

The repo's reference files are static snapshots. When pricing, mechanics, or eligibility values change in-game, the files don't auto-update — they go stale, and the agent confidently cites old values until someone notices.

**The riskiest files for drift:**

| File | What drifts | Detection cadence |
|---|---|---|
| `instructions/cost-reference.md` | PokéCoin shop pricing, Stardust costs at L48-50, Mega Energy initial costs, Link Charge bundles | Quarterly |
| `instructions/niantic-help-reference.md` | Friend cap, level cap, Mega Energy storage cap, feature retirements (Spotlight Hour-style) | Quarterly |
| `instructions/shiny-odds-reference.md` | Boosted shiny rates for events, Lucky odds | Per relevant event run |
| `instructions/dynamax-reference.md` | MP soft cap, storage cap, Gigantamax species count | Per Niantic patch |
| `instructions/mega-evolution-reference.md` | Mega Levels, Mega-Evolved attack boost percentages (Niantic FAQ #3334; not "aura"), eligible species | Per Niantic patch |

**Quarterly check (every ~13 issues, or trigger run on the first Monday of Feb / May / Aug / Nov):**

The agent does a special pre-research pass:
1. Spot-check 5 high-traffic values from `cost-reference.md` against the in-app shop or recent Niantic news. Examples: 100 PokéCoins → 0.99 USD, 600,000 Stardust to power up L40→50, 200 Mega Energy first-time Mega.
2. Spot-check 5 high-traffic values from `niantic-help-reference.md` against current Niantic news/help center. Examples: friend cap (650), level cap (80), Mega Energy storage cap (10,000), Spotlight Hour status (retired).
3. For each value that has changed: flag `[REFERENCE DRIFT: instructions/X.md value Y should be Z per [source URL]]` in the email summary.
4. The agent does NOT auto-update the reference files (that's a human review step). Joe sees the drift report and updates files as needed.

**Trigger:** the agent checks the date in Step 0; if `today.day <= 7` AND `today.month in [2, 5, 8, 11]`, run the quarterly verification before Step 4. Otherwise skip.

## Spec Authority (Canonical Sources for Each Rule)

The trigger prompt and the repo files have grown to overlap on many rules. To avoid drift between them, this is the authority order:

| Rule category | Canonical source (single source of truth) |
|---|---|
| Newsletter section structure (sections 1–13, what's required, formatting) | `instructions/newsletter-creation.md` |
| Voice, tone, banned phrases, sign-off, headline patterns, default-filler rule, gap-acknowledgment, reader-segment asides | `instructions/brand-voice.md` |
| Source routing (where to fetch data) | `instructions/meta-data-sources.md` (and source routing table in trigger prompt mirrors it) |
| Trainer Tip angles + drift tracking | `instructions/trainer-tips-framework.md` |
| Audit checklist | `instructions/pre-publish-checklist.md` |
| Volatile rules + verification policy | `instructions/rule-verification.md` (this file) |
| Costs (PokéCoins, Stardust, Candy, Mega Energy, etc.) | `instructions/cost-reference.md` |
| Niantic-confirmed mechanics + stale-help-center flags | `instructions/niantic-help-reference.md` |
| Shiny + hundo odds | `instructions/shiny-odds-reference.md` + `instructions/hundo-odds-reference.md` |
| Adventure Effects / Mega+Primal / Dynamax mechanics | three dedicated reference files |
| Past Spawn Point issues (dedup, drift) | `instructions/newsletter-archive.md` |
| Social copy structure (IG / Twitter / TikTok / Facebook) | `instructions/social-copy.md` |

**Trigger prompt's role:** orchestrate the steps and keep CRITICAL constraints visible at runtime. The trigger should NOT re-encode the full spec for each rule — it should reference the canonical file. When a rule changes, update the canonical file; the trigger picks it up automatically because the agent reads the file in Step 1.

**When the trigger inlines a rule** (e.g., "Hundo CPs required for raid bosses"), it's a runtime reminder, NOT the source of truth. If the inline reminder contradicts the canonical file, **trust the canonical file**.

**Drift audit:** quarterly (during the Quarterly Reference-File Verification check above), the agent should also flag CRITICAL rules in the trigger prompt that contradict their canonical file. Format: `[SPEC DRIFT: trigger says X but instructions/Y.md says Z]`. Joe consolidates by editing whichever is wrong.

## Niantic vs Scopely — Who to Credit

**Scopely officially acquired Niantic's games division on May 29, 2025** (announced March 12, 2025). The deal includes Pokémon GO, Pikmin Bloom, Monster Hunter Now, Campfire, and Wayfarer. Roughly 400 Niantic gamemakers joined Scopely. Niantic Spatial Inc. continues separately as a geospatial AI company (and still operates Ingress Prime and Peridot).

### Convention for the newsletter

| Context | Use |
|---|---|
| Corporate/business announcements (acquisitions, financials, future event releases) | **Scopely** |
| Game development decisions, design choices, in-game events | **Niantic** (the game team retained leadership and branding) |
| Direct quotes from press releases or PR | Match the source |
| When in doubt | **Niantic** — community convention still defaults here for game-related coverage |

### Examples
- ✓ "Niantic announced a new Community Day move for Lechonk."
- ✓ "Scopely's first-quarter Pokémon GO revenue figures..."
- ✓ "Niantic hasn't announced a Shiny Volcanion event yet" (game decision)
- ✗ "Scopely hasn't announced..." reads odd in game-development context even though technically true

### Verification step
The community still largely uses "Niantic" in game-related coverage. Check current articles before defaulting to Scopely — if Pokémon GO Hub, LeekDuck, and content creators are saying "Niantic," the newsletter should match that convention to feel native to readers.

## Niantic Help Center Pages Are Often Stale

**The Niantic help center FAQ pages are routinely 6+ months stale.** They are useful for canonical mechanics descriptions but unreliable for any value that has been changed in the last ~6 months.

When a help center FAQ disagrees with an official Niantic news post (`pokemongo.com/news/...`) or a recent patch announcement, **trust the news post**.

Examples of stale help center values surfaced in May 2026:
- Help center says friend cap is 550. Actual cap is **650** (raised late 2025).
- Help center references levels 70-80 ambiguously. Actual cap is **80** (raised Oct 15, 2025).
- Help center for Spotlight Hour still active. Spotlight Hours **retired March 3, 2026**.
- Help center says Mega Energy storage 9,999. Actual cap **10,000** (raised Feb 20, 2026).
- Help center lists 8 Adventure Effects. Actual count is **9** (Eternatus Dynamax Cannon added Aug 2025).

When researching Pokémon GO mechanics for the newsletter, treat the help center as a starting point, not the final word for current values. See `instructions/niantic-help-reference.md` for the full Niantic-confirmed reference with stale-value flags.

## Past-Iteration Inference Is Not Verification

**The single most common failure mode in newsletter drafting:** treating last year's rules as this year's rules.

When a recurring event (Jungle Cup, Retro Cup, Holiday Cup, Community Day Classic, etc.) returns, the agent's training data and past articles often describe a previous iteration. **This is not the same as the current iteration.** Niantic adjusts bans, eligibility, schedules, and bonuses between runs of the same-named event.

### The rule

If a claim is based on a past iteration of a recurring event:
1. Treat it as `[UNVERIFIED]` until confirmed against THIS iteration's primary source
2. Default to **omission** rather than assertion if the current source can't be located
3. NEVER infer "it must still be the same" — it usually isn't, and when it is, you can verify in seconds

### Examples of what NOT to do

❌ "Galarian Stunfisk is banned from Jungle Cup" (based on October 2025 articles, not verified for May 2026)
❌ "GO Battle Thursday gives 4x Stardust" (based on a past season; check the current season)
❌ "Community Day move evolution window is 5 hours" (verify per event)
❌ "Mystery Box cooldown is reduced this week" (a past event reduced it; check current)

### Examples of what TO do

✓ Fetch the current iteration's official announcement, blog post, or LeekDuck event page
✓ If no source confirms, write around the claim or omit it
✓ Flag in research brief: `[UNVERIFIED: claim about X — needs source for current iteration]`

## This Policy Applies to the Verifier Too

When reviewing or correcting the agent's work, the same rules apply. Don't assert facts based on training data, past iterations, or community knowledge without primary-source verification. If you can't cite a specific URL for a claim, you don't have grounds to assert it as fact.

This is especially important during back-and-forth corrections: the verifier might "fix" something to a wrong value if working from stale data.

## Anti-Hallucination Reminders

- **Never paraphrase a "rule" from training data without verification.** Pokémon GO rules change frequently and your training data is months old.
- **Don't trust this repo as ground truth for volatile rules.** This repo's reference files are snapshots from when they were last updated.
- **The repo IS authoritative for** structure (newsletter format, framework angles, citation policies, writing rules) — these are decisions, not facts.
- **The repo is NOT authoritative for** specific bans, schedules, pricing, eligibility lists, or rate values — these are facts that change.

## Update Cadence Recommendation

The reference files in this repo should be reviewed periodically:
- `shiny-odds-reference.md` — review when major rate changes are reported
- `community-tips.md` (Memories in Motion section) — review at start of each new season
- `meta-data-sources.md` (any cached ban examples) — review whenever cited cup runs again
- `trainer-tips-framework.md` — angles describing mechanics should be reviewed if mechanics change
- `community-day-tips.md` — most content is stable, but verify post-event raid window patterns each CD
