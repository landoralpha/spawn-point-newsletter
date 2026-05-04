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

### 9. The "I Might Be Wrong" Check

Before publishing, scan the draft and ask: "Which claims am I most confident about that I haven't actually verified this run?"

The most dangerous claims are the ones that *feel* obvious:
- "X has always been banned in this cup"
- "Y is the best counter for this raid type"
- "Z works the same way it always has"

These are the claims most likely to be wrong because they bypass verification. If a claim feels obvious, that's a flag to verify it anyway.

## When to Run This Audit

Run after Step 5 (newsletter draft complete) but BEFORE Step 6 (push to Notion).

If any check fails:
1. Fix the issue in the draft
2. Re-run the relevant section of the audit
3. Don't push to Notion until all checks pass

## What to Flag in the Email Notification

Include audit results in the Step 7 email to Joel:
- Number of consistency issues found and resolved
- Any `[UNVERIFIED]` flags that remain in the draft (so he can resolve manually)
- Any `[STALE REFERENCE]` flags pointing to repo files that need updating

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
