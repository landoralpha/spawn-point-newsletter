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
4. Joel can update the reference file based on the flag

### What to flag in the Attention Items

At the top of the research brief, flag any rule changes detected:
- `[RULE CHANGE: GBL Thursday cap changed from 50 to N battles]`
- `[RULE CHANGE: Jungle Cup ban list now includes [new ban]]`
- `[RULE CHANGE: New season started: [name], schedule changes affect Daily Discoveries section]`
- `[POSSIBLE RULE CHANGE: shiny rate for X seems different from reference, needs verification]`

This lets Joel update the repo's reference files if a real change occurred.

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
