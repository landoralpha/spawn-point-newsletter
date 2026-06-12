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

### 1. Pull three sources in parallel via subagent

Spawn a `general-purpose` subagent with this prompt template. Wait for the structured report.

```
I need top raid counters for {boss_name} ({boss_typing}) from THREE sources:

1. Pokebattler JSON API — DPS-optimal:
   https://fight.pokebattler.com/raids/defenders/{POKEMON_ID}/levels/{raid_tier}/attackers/levels/40/strategies/CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC?sort=ESTIMATOR&weatherCondition=NO_WEATHER&dodgeStrategy=DODGE_REACTION_TIME&aggregation=AVERAGE&randomAssistants=-1&friendLevel=FRIENDSHIP_LEVEL_0
   - POKEMON_ID is the GameMaster ID, e.g., ZEKROM, LOPUNNY_MEGA, DIALGA. For Megas, try {NAME}_MEGA first, then MEGA_{NAME}, then {NAME} at RAID_LEVEL_MEGA.

2. Pokémon GO Hub article — accessibility-weighted human guide:
   Search pokemongohub.net for "{boss_name} Counters Guide" or "{boss_name} Raid Counters"

3. Pokémon GO Hub-DB — canonical counter list:
   https://db.pokemongohub.net/pokemon/{DEX_NUM} (use form suffix for Megas: {DEX}-Mega; for Shadows: {DEX}-Shadow)

Use mcp__claude_ai_Spawn_Point_Fetcher__fetch_url to bypass 403s. Bodies often >250 KB and saved to a temp path — use jq + python3+bs4 to extract counter sections.

Return a markdown table per source (top 10), then synthesize:
- **Premium (5)** — top-tier including Megas, Shadows, Legendaries with exclusive moves
- **Budget (5)** — commonly-owned, no exclusive moves required, accessible from raids/research/wild evolution

Apply the balance rule (memory: feedback-counter-source-balance): Pokebattler shows optimal DPS, Hub-DB shows accessibility. Premium leans Pokebattler ranking. Budget leans Hub-DB accessibility. Mark exclusive moves with [exclusive].

CRITICAL: For dual-type bosses, verify every charged move is super-effective using PoGO type-chart math (1.6 / 1.0 / 0.625 / 0.39, multiplicative). Cross-reference instructions/type-effectiveness-reference.md "Dual-type cancellation traps" section. Skip counters whose charged move is neutral or worse UNLESS the rationale is high raw DPS / bulk / Mega aura cross-promo (document the exception).

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
- **Hub article rank vs Pokebattler rank divergence** — usually a moveset/aggregation difference. The validator catches the most-common case (neutral-charged-move on a Mega).
- **GameMaster ID for Lopunny** — `LOPUNNY` at `RAID_LEVEL_MEGA` resolves; `LOPUNNY_MEGA` is the form ID used in Hub-DB URL pattern but not Pokebattler.
- **Hub-DB form URLs** — `{DEX}-Mega` (note hyphen + capital M); `{DEX}-Mega_X` / `{DEX}-Mega_Y` (underscore inside Mega X/Y); `{DEX}-Shadow`; `{DEX}-Primal`. See memory `reference_hub_db_form_conventions.md`.
