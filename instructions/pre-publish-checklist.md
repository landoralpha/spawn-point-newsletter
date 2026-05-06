# Pre-Publish Self-Audit Checklist

After completing all section drafts but before pushing to Notion, run this audit pass. The goal is to catch cross-section inconsistencies, date/day mismatches, internal contradictions, and source-quality issues that section-by-section writing tends to miss.

## Audit Pass: Run These Checks in Order

### 1. Cross-Section Consistency

Search the assembled draft for the following and verify every instance is consistent:

- **Same Pokémon, same moveset:** If you mention "Mega Swampert (Water Gun / Hydro Cannon)" in the Raids section and "Mega Swampert" again in the Trainer Tips, both must use the same moveset. Common failure: one section copied an old article's moveset, another used Pokebattler's current data.
- **Same fact, same number:** Stardust costs, candy counts, IV thresholds, percentages, raid times, eligibility caps — every numeric claim must match across sections.
- **Same date, same day-of-week:** "Monday May 5" must agree with "Tuesday May 5" — they can't both appear. Run Python `date(year, month, day).strftime('%A')` to verify each date.
- **Same event, same window:** If the Lechonk CD is "Saturday May 9 2-5 PM," every reference to it across sections must use the same start/end times.

Flag any contradiction as `[INCONSISTENCY: Section A says X, Section B says Y]` and resolve before publish.

### 2. Date / Day-of-Week Verification

For every "[Day] [Month] [Date]" pattern in the draft:

```python
from datetime import date
# Example check
target = date(2026, 5, 5)
print(target.strftime('%A'))  # Should print "Tuesday" if you wrote "Tuesday May 5"
```

Common failures:
- "Monday May 5" when May 5 is Tuesday
- "Wednesday April 29: Nihilego arrives Wednesday May 6" — both are Wednesdays so the rotation header confuses
- Friendship Friday referenced as a specific date — verify it's actually Friday

### 3. Internal Pokemon Consistency

For every Pokémon mentioned more than once in the draft:
- Same form (Shadow / Mega / Gigantamax / regional / Hisuian — pick one and stick with it)
- Same moveset (verify against PvPoke or Pokebattler — whichever was the source for that section)
- Same role (don't list Excadrill as "Steel option" in one place and "Ground option" in another without acknowledging both types)

### 4. Cup / Format Eligibility Audit

If the newsletter covers a themed PvP cup:
- Every Pokémon recommended in the GBL section has a type matching the cup's eligibility list
- No banned Pokémon are in the recommendations (verify against the CURRENT iteration's ban list, not historical iterations)
- If bans exist, the newsletter mentions them explicitly

If Max Monday or Max Battles are featured:
- Every Pokémon recommended as Attacker/Defender/Healer is on the current Pokémon GO Hub Max Battle tier list (or has a tier explicitly cited)
- No Shadow Pokémon recommended for Max Battle roles
- Tier citations match the current month's tier list

### 5. Source Link Quality Audit

For every URL in every Sources line:
- **No homepage links.** `db.pokemongohub.net` is not acceptable; `db.pokemongohub.net/pokemon/793` is.
- **No /wiki/ index pages** when a specific article exists. `pokemongohub.net/post/wiki/go-battle-league/` is not acceptable; `pokemongohub.net/post/pvp/nifty-or-thrifty-great-league-jungle-cup-meta-analysis/` is.
- **Every link must support a specific claim** the section makes. Not just "related to the topic."
- **Test each link** if possible — broken links erode trust.

### 6. Citation Policy Audit

For every claim about PvP rankings, raid counters, or Max Battle tiers:
- Specific rank, score, or tier cited (per `meta-data-sources.md`)
- Source link present in the Sources line
- No generic phrases like "is a top pick" or "ranks well" without numbers

### 7. Anti-Pattern Check

Search the draft for these specific anti-patterns:

| Find | Replace with | Why |
|---|---|---|
| "Fast Attack" | "Fast Move" | Niantic's official terminology |
| "shiny available" | "with a chance to be shiny" | Writing rule |
| "Pokemon" (no accent) | "Pokémon" | Brand correctness |
| Generic "is a top pick" | Specific rank/score | Citation policy |
| `db.pokemongohub.net` (homepage) | Specific Pokémon URL | Source quality |

### 8. Volatile Claim Audit

For every claim that touches a volatile rule (per `rule-verification.md`):
- Was this verified against the CURRENT iteration's source during research, or inherited from cached/past-iteration knowledge?
- If cached, re-verify or flag as `[UNVERIFIED]`
- If contradicting a current authoritative source, trust the current source

Specifically check:
- Cup ban lists (don't infer from past iterations)
- GBL season name and end date
- Daily Discoveries schedule
- Dynamax-eligible list
- Mega Evolution roster
- Friendship Friday / event-specific bonuses

### 9. Hundo CP Audit (REQUIRED)

For every featured catchable Pokémon — every Five-Star raid boss, Mega raid boss, Shadow raid boss, the featured Max Monday Dynamax/Gigantamax Pokémon, and any Community Day featured Pokémon — verify the section includes BOTH:

1. **L20 hundo catch CP** (15/15/15 IVs, normal weather)
2. **L25 hundo catch CP** (15/15/15 IVs, weather-boosted)

For Community Day, these values are for the EVOLVED form (the form players evolve into during the bonus window).

**Why this matters:** trainers screen-check catch CPs immediately after raids and Max Battles. Knowing the exact hundo CP lets them identify a perfect IV catch on sight. A newsletter without these numbers fails its most practical function.

**Source:** `db.pokemongohub.net/pokemon/[dexNr]` lists pre-computed values. If hub-db is unavailable or the species isn't yet listed, compute from `pokedex.json` base stats using the GO CP formula (see `instructions/meta-data-sources.md`).

**Failure modes to fix:**
- Section names a raid boss but omits hundo CPs → ADD both L20 and L25 values.
- Only L20 is listed → ADD L25 weather-boosted.
- Wrong form (e.g., Tapu Lele's hundo CP cited for the Mega Banette section) → FIX to the section's actual featured Pokémon.
- Computed value differs from hub-db → trust hub-db unless hub-db is clearly stale.

### 10. The "I Might Be Wrong" Check

Before publishing, scan the draft and ask: "Which claims am I most confident about that I haven't actually verified this run?"

The most dangerous claims are the ones that *feel* obvious:
- "X has always been banned in this cup"
- "Y is the best counter for this raid type"
- "Z works the same way it always has"

These are the claims most likely to be wrong because they bypass verification. If a claim feels obvious, that's a flag to verify it anyway.

### 11. Subject Line A/B Audit

Verify the draft begins with the **Subject Line A/B Options** block per `newsletter-creation.md` Section 1. Check:
- Exactly 3 alternatives, each from a different headline pattern (subject-led, action-led, theme-led, hook)
- A "Selected for draft:" line naming one of the three
- None of the three pattern-matches the banned headline list ("This Week in Pokémon GO" / "Weekly Roundup" / "Updates: [date range]")

### 12. Notion Property Coverage Audit

Verify the agent populated these database properties (or noted any missing in the email summary):
- Issue Number, Date Range, Featured Community Day, Trending Topic, GBL Cup
- Mega Raid, 5-Star Raid, Shadow Raid, Max Monday
- Subject A/B Options, Has Month/Season Transition

If any property doesn't exist on the database, log to the email summary so Joe can add it.

## When to Run This Audit

Run after Step 5 (newsletter draft complete) but BEFORE Step 6 (push to Notion).

If any check fails:
1. Fix the issue in the draft
2. Re-run the relevant section of the audit
3. Don't push to Notion until all checks pass

## What to Flag in the Email Notification

Include audit results in the Step 7 email to Joe:
- Number of consistency issues found and resolved
- Any `[UNVERIFIED]` flags that remain in the draft (so he can resolve manually)
- Any `[STALE REFERENCE]` flags pointing to repo files that need updating
- Any `[ROTATION CONFLICT]` flags from raidboss.json cross-validation
- Any `[PENDING]` flags (e.g., monthly content post not yet published)
- **Audit-check failure history** — which checks fired this run and what was caught (running this surfaces which audits earn their keep)
- **Data source health** — flag any silent fallback (Pokebattler 502 → article fallback, db.pokemongohub.net 403 → computed CP, raidboss.json unavailable → ignored cross-validation)
- **Missing Notion properties** — if the agent tried to populate a property that doesn't exist on the database
- **Underused Trainer Tip angles surfaced in this run** — informational, helps Joe see variety drift over time

## Section Header Audit (CRITICAL — high-impact, easy to miss)

After writing each section, verify the **section header** matches the **section body**. Section-by-section writing makes it easy to leave a previous newsletter's header in place when reusing structure. Examples of this failure:

- Header says "Shadow Entei Raid Day" but body is about Lechonk Community Day
- Header says "Max Monday featuring Dynamax Shuckle" but body and image are Cottonee
- "Rotating in Wednesday April 29" carried from previous newsletter when actual rotation is May 6

### How to check
1. Read each section header out loud
2. Confirm the Pokémon/event named in the header matches the body content
3. Confirm any dates in the header match the actual newsletter week

Common failure points:
- Weekend Event header (the featured event name)
- Max Monday header (the featured Dynamax Pokémon)
- Raid Bosses subsection rotation date headers (the "Rotating in [Day, Date]" line)
- Trending Topic header (the topic name)

This is a top-priority check because a wrong header undermines reader trust immediately and is highly visible in tables of contents and previews.

## Required Sections Audit

Before publishing, verify every required section from `newsletter-creation.md` is present:

1. Title + Subtitle
2. Opening Paragraph
3. Week at a Glance
4. Events (Section 5 — for special/limited-time events; can be omitted if no qualifying events)
5. Raid Bosses (Section 6)
6. GO Battle League (Section 7)
7. Max Monday (Section 8)
8. Daily Discoveries (Section 9)
9. Trending Topic (Section 10)
10. **Don't Miss (Section 11)** — exactly 3 callouts. Often forgotten.
11. Sign-off

If a section is intentionally omitted (e.g., no Events for a slow week), note it in the research brief so it's a deliberate choice.

## Move Name Formatting Rules

Pokémon GO move names are NEVER hyphenated, even when they're two words:
- ✓ "Mud Slap" — ✗ "Mud-Slap"
- ✓ "Power Gem" — ✗ "Power-Gem"
- ✓ "Body Slam" — ✗ "Body-Slam"
- ✓ "Stone Edge" — ✗ "Stone-Edge"
- ✓ "Hydro Pump" — ✗ "Hydro-Pump"

Search the draft for hyphenated move names and de-hyphenate.

## Style and Grammar Polish

These are easy to fix and significantly raise the perceived quality of the newsletter:

### Date formatting
- **Always include a comma after weekday names:** "Saturday, May 9" not "Saturday May 9"
- **Date ranges use en-dash (–):** "May 4–May 10" not "May 4-May 10" (en-dash is `–`, not regular hyphen)
- **Times include AM/PM on both ends:** "6:00 PM to 7:00 PM" not "6:00 to 7:00 PM"

### Time formatting standard: AM/PM (caps, no periods)

The newsletter standard is **AM/PM** (capital letters, no periods). Apply this throughout every section:
- ✓ "6:00 AM to 9:00 PM"
- ✓ "Raid Hour is Wednesday, May 6 from 6:00 PM to 7:00 PM"
- ✗ "6:00 a.m. to 9:00 p.m." (don't use lowercase with periods)
- ✗ "6:00 am to 9:00 pm" (always capitalize)

Common drift point: Daily Discoveries section often gets written with lowercase a.m./p.m. — verify it matches the rest of the newsletter.

### Comma audit (date constructions)

Search the draft for these patterns and verify a comma follows the weekday:
- "Monday May" → "Monday, May"
- "Tuesday May" → "Tuesday, May"
- "Wednesday May" → "Wednesday, May"
- "Thursday May" → "Thursday, May"
- "Friday May" → "Friday, May"
- "Saturday May" → "Saturday, May"
- "Sunday May" → "Sunday, May"

(Adjust month names per the current newsletter's date range.)

When date includes a year, also add a comma before the year:
- ✓ "Saturday, May 9, 2026"
- ✗ "Saturday May 9 2026"

### Fractions
Pick one and use throughout:
- Symbol form: "¼ Egg Hatch Distance"
- Numeric form: "1/4 Egg Hatch Distance"
Recommend symbol form for cleaner display.

### Quotation marks
Curly vs straight should be consistent throughout. If using curly quotes (typographic), apply everywhere; same for straight.

## Lucky Friend vs Lucky Trade Distinction

**These are two distinct mechanics** and should be cited precisely:

- **Lucky Friend** — a *status* between two Best Friends, rolled at ~1.1% per first-of-day Best Friend interaction. The status guarantees the next trade between you produces Lucky Pokémon.
- **Lucky Trade** — a trade outcome that produces Lucky Pokémon. Triggered by Lucky Friend status, by trading pre-2017 catches (1.1% otherwise), or via Lucky Trinket (during specific events).

The properties **1/64 hundo odds** and **half Stardust to power up** are properties of Lucky Pokémon, not properties of "Lucky Friend trades."

### Phrasing
- ✓ "A Lucky Trade (guaranteed when trading with a Lucky Friend) gives 1/64 hundo odds and halves the power-up Stardust."
- ✓ "Trading with your Lucky Friend produces a Lucky Trade — both Pokémon become Lucky."
- ✗ "A Lucky Friend trade gives 1/64 hundo odds" (conflates the mechanics)

## Anti-Patterns Captured From Real Newsletter Tests

These specific errors have appeared in past newsletter tests and should be specifically watched for:

1. **Galarian Stunfisk recommended in a Jungle Cup top picks list** — verify ban status of this iteration before recommending
2. **"Mega Gengar: Shadow Claw / Shadow Ball"** — Pokebattler optimal is Lick / Shadow Ball
3. **"Shadow Gyarados: Waterfall / Hydro Cannon"** — Gyarados can't learn Hydro Cannon (it's Hydro Pump)
4. **Necrozma Dawn Wings missing from Cresselia counters** — was added via fusion mechanic; check current Pokebattler #1
5. **"Monday May 5" or similar date/day mismatch** — verify with Python
6. **Top Counter list contradicting Budget Picks list** for the same Pokémon
7. **XL Candy count differing between Trainer Tips and Daily Discoveries** sections
8. **"Scopely" vs "Niantic" mismatch** with the rest of the newsletter's voice
9. **Cup eligibility list missing or incorrect** for a themed PvP format
10. **Generic homepage links** in Sources sections instead of specific article URLs
