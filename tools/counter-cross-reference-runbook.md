# Counter Cross-Reference Runbook

A reusable subagent procedure for pulling raid counters from Pokebattler + Pokémon GO Hub article + Hub-DB, synthesizing into balanced Premium/Budget lists, and validating against the PoGO type chart. Used by **recon Step 5.6** and by manual pre-publish fact-checks.

## When to invoke

- Recon Step 5.6: for every raid boss that has a Premium/Budget list in the draft (typically 3 per issue: Five-Star, Mega, Shadow).
- Manual: Joe says "run the counters for [boss] again." Pass the boss name + raid tier.

## Inputs

- `boss_name` — e.g., `Zekrom`, `Mega Lopunny`, `Shadow Dialga`
- `raid_tier` — `RAID_LEVEL_5`, `RAID_LEVEL_MEGA`, `RAID_LEVEL_5_SHADOW`, `RAID_LEVEL_3`
- `boss_typing` — e.g., `Electric/Dragon`, `Normal/Fighting`

## Procedure

### 1. Pull three sources in parallel via subagent (UPDATED 2026-06-15: tri-source equal-weight)

Spawn a `general-purpose` subagent with this prompt template. Wait for the structured report.

```
I need top raid counters for {boss_name} ({boss_typing}) from THREE sources, weighted EQUALLY:

1. Pokebattler JSON API:
   https://fight.pokebattler.com/raids/defenders/{POKEMON_ID}/levels/{raid_tier}/attackers/levels/40/strategies/CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC?sort=ESTIMATOR&weatherCondition=NO_WEATHER&dodgeStrategy=DODGE_REACTION_TIME&aggregation=AVERAGE&randomAssistants=-1&friendLevel=FRIENDSHIP_LEVEL_0
   
   CRITICAL — Pokebattler ID format (confirmed empirically 2026-06-15; wrong format = 404 on every boss):
   - Base: {POKEMON} (e.g., ZEKROM, DIALGA, CELESTEELA)
   - Mega: {POKEMON}_MEGA — SUFFIX, NOT prefix (SKARMORY_MEGA ✓, MEGA_SKARMORY ✗)
   - Mega X/Y: {POKEMON}_MEGA_X / {POKEMON}_MEGA_Y (MEWTWO_MEGA_X ✓)
   - Primal: {POKEMON}_PRIMAL (GROUDON_PRIMAL ✓, PRIMAL_GROUDON ✗)
   - Shadow Legendary 5-Star: use BASE {POKEMON} at tier RAID_LEVEL_5_SHADOW (NOT _SHADOW_FORM suffix)
   
   Tier constants:
   - 5-Star: RAID_LEVEL_5
   - Mega (and Super Mega + Primal): RAID_LEVEL_MEGA
   - Shadow 5-Star: RAID_LEVEL_5_SHADOW (NOT RAID_LEVEL_5_LEGENDARY — deprecated)
   - 3-Star: RAID_LEVEL_3
   - 1-Star: RAID_LEVEL_1

2. Pokémon GO Hub-DB — canonical curated counter list:
   https://db.pokemongohub.net/pokemon/{DEX_NUM}/counters
   Form keys: {N}-Mega (single Mega), {N}-Mega_X / {N}-Mega_Y (underscore inside Mega X/Y), {N}-Shadow, {N}-Primal
   Parse the BestCountersHighlights_highlights__O4EAQ section (top 7 picks).

3. DialgaDex — third-party calculator (third-source tiebreaker):
   https://www.dialgadex.com/?p={DEX_NUM}&f={FORM_CODE}
   FORM_CODE: S=Shadow, M=Mega, P=Primal; omit &f= for base form.
   Example: https://www.dialgadex.com/?p=483&f=S for Shadow Dialga.
   JS-rendered SPA — use fetch_url MCP mode="text" to extract rankings.
   DialgaDex provides Baseline / Budget / ESpace tiers — map cleanly to Spawn Point's Premium / Budget editorial standard.

Use mcp__claude_ai_Spawn_Point_Fetcher__fetch_url to bypass 403s. Bodies often >250 KB and saved to a temp path — use jq + python3+bs4 to extract counter sections.

Return a markdown table per source (top 10), then synthesize:
- **Premium (5)** — top-tier including Megas, Shadows, Legendaries with exclusive moves
- **Budget (5)** — commonly-owned, no exclusive moves required, accessible from raids/research/wild evolution

**EQUAL-WEIGHT rule (updated from prior "Pokebattler primary, Hub-DB accessibility-weighted" framing):** Pokebattler and Hub-DB are BOTH first-class sources. When they agree on a counter, high confidence. When they disagree, DialgaDex breaks the tie — note `[tiebreaker: dialgadex sided with <source>]`. For challenging matchups (debuts, Super Mega Raid Day, low-meta bosses), pull DialgaDex proactively rather than only as a tiebreaker.

Mark exclusive moves with [exclusive]. Cite the source(s) supporting each pick: `[both]`, `[pokebattler+dialgadex]`, `[hub-db+dialgadex]`, etc.

CRITICAL: For dual-type bosses, verify every charged move is super-effective using PoGO type-chart math (1.6 / 1.0 / 0.625 / 0.39, multiplicative). Cross-reference instructions/type-effectiveness-reference.md "Dual-type cancellation traps" section. Skip counters whose charged move is neutral or worse UNLESS the rationale is high raw DPS / bulk / Mega-Evolved attack boost coordination (document the exception).

Return under 1500 words.
```

### 2. Validate the synthesis with the type-chart tool

Pass the candidate Premium + Budget list to:

```bash
python3 tools/check_counter_moveset.py \
  --boss "{boss_name}:{boss_typing}" \
  --strict \
  "Pokemon Name:Fast Move/Charged Move" \
  ...
```

Any `⚠ NEUTRAL` or `✗ RESISTED` verdict on the charged move is a recon FLAG — either drop the counter from the list OR replace the moveset with a SE alternative.

### 3. Output format for recon

For each boss, the recon report includes:

```markdown
### {Boss} counter audit
- **Pokebattler top 5 (ESTIMATOR):** [list with estimator values]
- **Hub article top 5:** [list with rationale]
- **Hub-DB top 5:** [list]
- **Type-chart validator:** N/M counters use SE charged moves
- **Synthesis vs draft delta:** [what's in the draft that shouldn't be / what's missing]
- **Recommended swaps:** [explicit before→after for any FLAGs]
```

## Cached results

If `--cached` is passed AND the boss + raid tier + week was checked in the past 48 hours, return the cached file from `tools/cache/counter-{boss}-{tier}-{date}.md` instead of re-pulling. Otherwise refresh.

## Common pitfalls

- **Mega Mewtwo X/Y** — in PoGO since GO Fest 2026 in-person events; broadly available post-July 12. Before then, exclude from "broadly available" Premium lists OR caveat with "GO Fest ticket-holder only this week."
- **Eternatus** — accessible only via Eternamax Max Battles. List in Premium only if many trainers have it.
- **Pokebattler ID format vs Hub-DB URL — DIFFERENT conventions:**
  - Pokebattler: `LOPUNNY_MEGA` at `RAID_LEVEL_MEGA` (form SUFFIX, all caps, underscore-separated)
  - Hub-DB URL: `/pokemon/428-Mega` (form SUFFIX, hyphen-separated, capital-first letters)
  - Common confusion: Pokebattler does NOT accept `MEGA_LOPUNNY` (prefix order) — must be `LOPUNNY_MEGA`.
- **Hub-DB form URL conventions** — `{DEX}-Mega`, `{DEX}-Mega_X` / `{DEX}-Mega_Y` (underscore inside Mega X/Y), `{DEX}-Shadow`, `{DEX}-Primal`. See memory `reference_hub_db_form_conventions.md`.
- **Pokebattler Shadow tier** — `RAID_LEVEL_5_SHADOW` (NOT `RAID_LEVEL_5_LEGENDARY` — deprecated). Confirmed 2026-06-15.
- **DialgaDex URL form codes** — single-letter: `S` Shadow, `M` Mega, `P` Primal. Different from Hub-DB's word-suffix convention.
- **All-bosses 404 on Pokebattler** — symptom of ID format error (MEGA_ prefix, RAID_LEVEL_5_LEGENDARY tier) — NOT a sandbox 403, NOT a Pokebattler outage. fetch_url MCP escalation won't help; fix the URL format.
- **Hub article rank vs Pokebattler rank divergence** — usually a moveset/aggregation difference. The validator catches the most-common case (neutral-charged-move on a Mega). DialgaDex is the third-source tiebreaker per the equal-weight rule.
