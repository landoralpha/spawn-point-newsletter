# Meta Data Sources Reference

When citing PvP rankings or raid counter info, ALWAYS pull from PvPoke and Pokebattler directly. Do NOT lean on outdated articles. Articles often lag the current meta by months.

## PvPoke (PvP Rankings)

### Direct JSON endpoints (preferred)

PvPoke publishes raw JSON ranking data at:
```
https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/{cup}/overall/rankings-{cap}.json
```

Where:
- `{cup}` = `all` for standard format, OR a specific cup name (`jungle`, `retro`, `fantasy`, `kingdom`, `holiday`, `remix`, etc.)
- `{cap}` = `1500` (Great League), `2500` (Ultra League), `10000` (Master League)

### Examples

| URL | Purpose |
|---|---|
| `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/all/overall/rankings-1500.json` | Great League (open) |
| `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/all/overall/rankings-2500.json` | Ultra League (open) |
| `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/all/overall/rankings-10000.json` | Master League |
| `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/jungle/overall/rankings-1500.json` | Jungle Cup GL |
| `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/retro/overall/rankings-1500.json` | Retro Cup GL |

### JSON structure

Each entry contains:
- `speciesId` (e.g., "piloswine")
- `speciesName` (display name)
- `rating` (overall rating)
- `score` (0-100 score)
- `moveset` (recommended fast move + 2 charged moves, all uppercase IDs)
- `matchups` (top 5 favorable matchups)
- `counters` (top 5 unfavorable matchups)
- `moves.fastMoves` and `moves.chargedMoves` (usage stats)
- `stats.product` (stat product, the bulk × attack × defense efficiency metric)

### Tier mapping (from score)

| Score | Tier |
|---|---|
| 90+ | S |
| 80-89 | A |
| 70-79 | B |
| 60-69 | C |
| 50-59 | D |
| <50 | F |

The first entry in the JSON array = rank 1. Index + 1 = rank.

### Fallback URL pattern

PvPoke website URL (for human reference, not fetch):
```
https://pvpoke.com/rankings/{cup}/{cap}/overall/
```

Examples:
- `https://pvpoke.com/rankings/all/1500/overall/` (GL open)
- `https://pvpoke.com/rankings/jungle/1500/overall/` (Jungle GL)

## Pokebattler (Raid Counters)

### Direct JSON endpoint

```
https://fight.pokebattler.com/raids/defenders/{POKEMON_ID}/levels/{TIER}/attackers/levels/40/strategies/CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC?sort=ESTIMATOR&weatherCondition=NO_WEATHER&dodgeStrategy=DODGE_REACTION_TIME&aggregation=AVERAGE&includeLegendary=true&includeShadow=true&includeMegas=true&attackerTypes=POKEMON_TYPE_ALL
```

### Pokemon ID format

Convert Pokémon name to Pokebattler ID:
- Uppercase
- Replace spaces and hyphens with underscores
- Remove apostrophes and special characters

Examples:
- "Rayquaza" → `RAYQUAZA`
- "Mega Charizard X" → `CHARIZARD_MEGA_X`
- "Shadow Mewtwo" → `MEWTWO_SHADOW_FORM`
- "Necrozma Dusk Mane" → `NECROZMA_DUSK_MANE_FORM`
- "Gigantamax Gengar" → `GENGAR_GIGANTAMAX`

### Tier values

| Raid Type | TIER value |
|---|---|
| Tier 1 (1-Star) | `RAID_LEVEL_1` |
| Tier 3 (3-Star) | `RAID_LEVEL_3` |
| Tier 5 (Five-Star Legendary) | `RAID_LEVEL_5` |
| Mega | `RAID_LEVEL_MEGA` |
| Gigantamax | `RAID_LEVEL_6_MAX` |
| Shadow Tier 1 | `RAID_LEVEL_1_SHADOW` |
| Shadow Tier 3 | `RAID_LEVEL_3_SHADOW` |
| Shadow Tier 5 | `RAID_LEVEL_5_SHADOW` |

### JSON response structure

`data.attackers[0].randomMove.defenders` is the array of attackers, sorted. Each entry has:
- `pokemonId` (uppercase Pokémon ID)
- `byMove[]` (each fast/charged move combo with results)
- `total.estimator` (lower = better, time-to-win metric)
- `total.tdo` (total damage output)

### Sort modes

- **By Estimator** (default): best raw DPS attackers
- **By TDO**: highest total damage output (good for "tankier" attackers)
- **By HP**: highest HP (healer/defender role for Max Battles)

For Max Battle context, use this multi-role split:
- Top 2 by Estimator = Attackers
- Top 2 by TDO (excluding attackers) = Defenders
- Top 2 by HP (excluding above) = Healers

### Filtering rules

- Skip Eternamax forms (game-unavailable)
- Skip Frustration/Return as charged moves (these are Shadow/Purified-only moves not relevant to non-Shadow attackers)
- For Max Battles specifically: filter out Shadow Pokémon entirely (they cannot be brought into Max Battles)

## How the Agent Should Use These

### When writing PvP meta tips

1. Identify which league(s) and cup(s) are active for the week
2. Fetch the relevant PvPoke JSON
3. Cite specific rank, score, and recommended moveset for the featured Pokémon
4. Reference matchups and counters from the JSON, not from articles

Example tip phrasing:
- "Lechonk's evolved form Oinkologne sits at #14 in Great League with a Mud Slap / Body Slam / Play Rough moveset (PvPoke score: 87)."
- NOT: "Lechonk is a top Great League pick this season."

### When writing raid counter tips

1. Fetch Pokebattler counter data for the specific raid boss
2. Cite top 3-5 attackers with their best moveset (from `byMove[0]`)
3. Note budget non-Legendary, non-Shadow alternatives
4. Skip Shadow Pokémon when writing Max Battle (Dynamax/Gigantamax) counters

Example tip phrasing:
- "Rayquaza's top counters: Shadow Salamence (Dragon Tail / Outrage), Shadow Garchomp (Dragon Tail / Outrage), Shadow Dragonite (Dragon Breath / Draco Meteor). Budget: regular Garchomp (Dragon Tail / Outrage)."
- NOT: "Use strong Dragon-types to counter Rayquaza."

### When data conflicts between PvPoke/Pokebattler and an article

PvPoke and Pokebattler are authoritative. Articles are secondary. If they disagree, cite the data source.

### Caching guidance for the agent

- PvPoke rankings update with seasons / patches. Re-fetch each newsletter run.
- Pokebattler estimator data updates with game balance changes. Re-fetch each run.
- Both sources are JSON, so WebFetch should work without 403s (raw GitHub for PvPoke, fight.pokebattler.com for Pokebattler).

## When to Fall Back to Articles

**Default:** PvPoke JSON and Pokebattler JSON are the authoritative source for PvP rankings and raid counters. Always try them first.

**Fallback to articles if:**
- The JSON endpoint returns an error (4xx, 5xx)
- The Pokémon isn't found in the JSON (e.g., a brand-new species not yet in PvPoke's data)
- The data appears stale or doesn't reflect a recent rebalance
- You need context the data can't provide (community sentiment, narrative around a meta shift)

When falling back to articles, flag it: note `[fallback: source]` in the research brief so Joel can verify.

**Always use articles for:**
- **Event details** (LeekDuck, official blog) - times, dates, featured Pokémon, bonuses
- **Recent meta shifts** (Reddit, content creators) for the Trending Topic section
- **Community sentiment** that PvPoke/Pokebattler can't capture (which Pokémon "feels" overpowered, etc.)
