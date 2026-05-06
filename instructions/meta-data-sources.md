# Meta Data Sources Reference

When citing PvP rankings or raid counter info, ALWAYS pull from PvPoke and Pokebattler directly. Do NOT lean on outdated articles. Articles often lag the current meta by months.

For raid boss rotation and Pokémon base data (stats, types, movesets, form availability), the `pokemon-go-api.github.io` JSON endpoints replace HTML scraping. See the dedicated section near the bottom of this file.

## CRITICAL: PvP Cup Bans Are NOT in PvPoke JSON

**PvPoke's cup-specific JSON includes Pokémon that are officially banned from that cup.** PvPoke ranks them by theoretical performance regardless of ban status.

**Example (verified May 2026):** Jungle Cup officially bans Galarian Stunfisk and Gligar (per Niantic's announcement). But PvPoke's `jungle/overall/rankings-1500.json` lists Galarian Stunfisk at rank 6 (score 93) and Gligar at rank 31 (score 88.8). If the agent cites PvPoke without checking bans, it will recommend Pokémon that aren't legal for the cup.

### Required workflow for cup-specific PvP

1. **Fetch the official ban list FIRST** from one of these sources:
   - Official Pokémon GO Twitter/X account (`@PokemonGoApp`) when the cup is announced
   - LeekDuck event page for the cup
   - pokemongo.com/news for the season/cup announcement
   - Pokémon GO Hub "Nifty or Thrifty" meta analysis (`pokemongohub.net/post/pvp/nifty-or-thrifty-...`) - usually states the ban list explicitly
2. **Fetch PvPoke JSON** for the cup
3. **Filter the rankings**: skip any entry whose `speciesId` matches a banned species (account for Shadow variants too — if Gligar is banned, Shadow Gligar is also banned)
4. **Cite from the filtered list**: "Piloswine is the cup's top legal pick at #1 (PvPoke 96.4)..."

### Cup bans CHANGE between iterations
**Do NOT cache or trust historical ban lists.** Niantic adjusts bans between iterations of the same cup name. A Pokémon banned in last year's Jungle Cup may be allowed in this year's. Always re-verify each newsletter run.

**Historical reference (NOT to be trusted as current):**
- October 2025 Jungle Cup banned Galarian Stunfisk and Gligar
- May 2026 Jungle Cup banned Galarian Stunfisk and Gligar (per @PokemonGoApp announcement)

These are examples of past iterations. The current iteration's bans MUST be verified against the current Niantic announcement before each newsletter.

### Cup ban patterns
Cup bans typically target Pokémon that are oppressive in the format:
- Open formats (`all`): no cup bans, only the standard "no Mythicals/Legendaries above CP cap" rules baked into the league
- Themed cups (Jungle, Retro, Fantasy, Kingdom, Holiday, Willpower, Love, etc.): often have 1-3 banned Pokémon
- See `instructions/rule-verification.md` for the broader policy on rule changes over time

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

## Adventure Effects, Mega/Primal, Dynamax References

For mechanics-heavy questions about these systems, consult the dedicated reference files:

- `instructions/adventure-effects-reference.md` — Adventure Effects (the 9 confirmed Charged-Attack-based outside-battle abilities)
- `instructions/mega-evolution-reference.md` — Mega Evolution and Primal Reversion mechanics, levels, costs, auras, 2026 changes
- `instructions/dynamax-reference.md` — Dynamax/Gigantamax mechanics, Max Particles, tier costs, G-Max roster, role composition

These three references replace the older condensed coverage in framework angles 12 (Mega) and 21 (Dynamax). The framework angles point to these files for full detail.

**Critical distinction repeated for emphasis:**
- Mega/Primal Pokémon do NOT have Adventure Effects. Adventure Effects are a separate mechanic tied to Charged Attacks on a small Legendary roster.
- The only Adventure Effect that interacts with Dynamax/Gigantamax is Eternatus's Dynamax Cannon.

## Pokémon GO Hub Max Battle Tier Lists

For Max Battle (Dynamax/Gigantamax) attacker, defender, and healer recommendations — and for verifying whether a Pokémon is even Dynamax-capable — use the Pokémon GO Hub tier lists. These are updated monthly by community contributors.

### Current URLs (verify each iteration)

| Role | URL Pattern | Notes |
|---|---|---|
| Max Attackers | `https://pokemongohub.net/post/guide/max-attackers-tier-list/` | S/A/B/C/D/E tiers; Gigantamax forms cluster at top |
| Max Defenders | `https://pokemongohub.net/post/guide/max-defenders-tier-list/` | S through F tiers; F tier = "no 0.5s fast move" (unusable) |
| Max Healers | `https://pokemongohub.net/post/guide/max-healers-tier-list-june-2025/` (URL versions monthly — search if 404) | S Tier is Blissey alone; A tier includes Wailord, Snorlax, Lapras, etc. |

If the static URL 404s, search `site:pokemongohub.net max [attackers|defenders|healers] tier list` for the current iteration.

### Tier interpretation

- **Attackers:** S = Gigantamax forms with super-effective coverage. A = strong Gigantamax + top Dynamax. B-C = solid options. D = niche. E = essentially unviable.
- **Defenders:** S-A = Steel-types with Lock-On / Metal Claw resistances. B-C = situational. D-E = poor stats. F = no 0.5s fast move (cannot generate Max Energy fast enough).
- **Healers:** Blissey is alone at S due to massive HP. A tier = high-HP picks. B-C-D ranked by HP and longevity.

### Citation rules

When recommending Max Battle counters:
1. Verify the suggested Pokémon appears in the relevant tier list (Attacker / Defender / Healer)
2. Cite specific tier when relevant: "Gigantamax Inteleon (S Tier Attacker per Pokémon GO Hub)"
3. **Do NOT recommend any Pokémon in F Tier as a defender** — they are mechanically incapable of the role
4. **Skip Shadow Pokémon entirely** — they cannot Dynamax; they are not in any of these tier lists
5. If a Pokémon is absent from all three lists, it is likely not Dynamax-eligible. Verify before recommending.

### Negative claims (worth citing)

For Trainer Tips that note a Pokémon is NOT a strong Max Battle pick, citing the tier lists adds credibility. Example: "Whimsicott sits in E Tier (Attacker), F Tier (Defender), D Tier (Healer) per Pokémon GO Hub — not worth investing for Max Battles, but its Whimsicott form has GL play."

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
2. **For themed cups (Jungle, Retro, etc.): fetch the official ban list FIRST** from Niantic's announcement, LeekDuck, or Pokémon GO Hub's Nifty or Thrifty article
3. Fetch the relevant PvPoke JSON
4. **Filter rankings against the ban list** — PvPoke includes banned Pokémon
5. Cite specific rank, score, and recommended moveset for the featured Pokémon (from the filtered list)
6. Reference matchups and counters from the JSON, not from articles

Example tip phrasing:
- "Lechonk's evolved form Oinkologne sits at #14 in Great League with a Mud Slap / Body Slam / Play Rough moveset (PvPoke score: 87)."
- "In Jungle Cup (G-Stunfisk and Gligar banned), Piloswine is the runaway #1 pick (PvPoke 96.4) with Powder Snow / Icicle Spear / Stone Edge."
- NOT: "Lechonk is a top Great League pick this season."
- NOT: Citing G-Stunfisk as a top Jungle Cup pick when it's banned.

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

## pokemon-go-api JSON Endpoints (Community-Maintained)

Two endpoints from `pokemon-go-api.github.io` provide JSON for data that previously required HTML scraping. Both are stable, free, and work reliably with WebFetch.

### Raid boss rotation (CURRENT ONLY — not a schedule)

```
https://pokemon-go-api.github.io/pokemon-go-api/api/raidboss.json
```

Returns the lineup spawning RIGHT NOW across all tiers (1-Star, 3-Star, 5-Star, Mega, Shadow, Gigantamax). Updates within minutes of in-game rotation changes. **It is a snapshot of live state, not a forward schedule. It cannot tell you what rotates in next week.**

**The newsletter covers a future Monday-Sunday window.** When the trigger fires on Monday and the agent drafts for the following Mon-Sun, raidboss.json shows THIS week's lineup, not the newsletter's week. So treat this endpoint carefully:

**Correct uses:**
- **"Ending soon" Don't Miss callouts.** If raidboss.json shows Tornadus is currently spawning AND a Niantic announcement says Tornadus rotates out Wednesday, the agent flags Tornadus as a deadline in the Don't Miss section ("Catch your last Tornadus before Wednesday's rotation swap").
- **Cross-validation against announcements.** If LeekDuck or Niantic announced "Lechonk raids return Saturday May 9" but raidboss.json on the trigger run day already shows Lechonk in the live rotation, that contradicts the announcement. Flag as `[ROTATION CONFLICT: ...]`.
- **Filling gaps when announcements are vague.** If Niantic says "new Mega rotates in mid-week" without naming the species, raidboss.json a few days later (manual re-run or the next cycle) is the source of truth.

**Wrong uses:**
- Drafting next week's raid section using only this JSON. The live state on trigger-run-day is THIS week's lineup, not next week's.

**Where the FUTURE rotation actually comes from:**
- Niantic news posts (`pokemongo.com/news/...`) — the canonical source for upcoming rotation announcements
- LeekDuck event pages and season previews
- @PokemonGoApp Twitter/X
- Pokémon GO Hub previews

These primary sources publish the rotation schedule before it goes live. raidboss.json is the verification layer — it confirms the rotation is in fact what was announced, once it goes live.

### Pokémon pokedex (stats, types, moves, forms)

```
https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex.json
```

Returns an array of every Pokémon. Each entry includes:
- `id` (e.g., `TAPU_LELE`)
- `dexNr` (e.g., 786)
- `formId` (form key string)
- `stats.attack`, `stats.defense`, `stats.stamina` (base stats)
- `primaryType`, `secondaryType`
- `quickMoves[]`, `cinematicMoves[]`, `eliteQuickMoves[]`, `eliteCinematicMoves[]`
- Form data nested under: `megaEvolutions{}`, `regionForms{}`, `tempEvolutions{}` (each with own stats/moves/form key)

**How to use:**
- Verify base stats, available movesets, mega/region/temp form availability.
- The form keys under `megaEvolutions{}` etc. become the `{FORM}` substring in the sprite URL pattern.
- 1-hour cache recommended.

### Hundo CP computation from base stats

For published L20/L25/L40/L50 hundo CPs, `db.pokemongohub.net/pokemon/[number]` is still primary because the values are pre-computed.

If the agent needs to verify or compute a hundo CP from base stats (e.g., hub-db is unavailable, or a brand-new Pokémon isn't yet listed), use the standard GO CP formula:

```
CP = floor((Atk * sqrt(Def) * sqrt(Sta) * cpm^2) / 10)
```

With CP multipliers (cpm):
- L20 hundo: 0.5974
- L25 hundo (weather-boosted L20): 0.6679
- L40 hundo: 0.7903
- L50 hundo (XL Candy max): 0.8403

Atk/Def/Sta = `base + 15` (for hundo IVs of 15/15/15).

### Pokémon sprite CDN

```
https://raw.githubusercontent.com/pokemon-go-api/assets/main/Pokemon/pm{dexNr}.icon.png            # base form
https://raw.githubusercontent.com/pokemon-go-api/assets/main/Pokemon/pm{dexNr}.s.icon.png          # base form, shiny
https://raw.githubusercontent.com/pokemon-go-api/assets/main/Pokemon/pm{dexNr}.f{FORM}.icon.png    # form-specific
https://raw.githubusercontent.com/pokemon-go-api/assets/main/Pokemon/pm{dexNr}.f{FORM}.s.icon.png  # form-specific, shiny
```

**Form suffixes:** `MEGA`, `MEGA_X`, `MEGA_Y`, `PRIMAL`, `DAWN_WINGS`, `DUSK_MANE`, `ULTRA`, `ORIGIN`, `BLACK`, `WHITE`, `CROWNED_SWORD`, `CROWNED_SHIELD`, `THERIAN`, `HERO`, plus regional form keys from pokedex.json's `regionForms{}` (e.g., `ALOLA`, `GALARIAN`, `HISUIAN`, `PALDEAN`).

**Why this is the canonical Pokémon image source:**
- GitHub raw has no hotlink protection (unlike LeekDuck / pokemongohub).
- Stable URLs (the assets repo doesn't get reorganized).
- Form-aware out of the box — no separate URL pattern per form.
- Free, no rate limits.

**Use this CDN for Pokémon-specific sprites** (raid boss images, featured Pokémon images, counter sprites in Trainer Tips, etc.). For event banners and event hero art (Community Day banner, special event keyart), the priority order is:

1. **Official Pokémon GO blog** (`pokemongo.com/news/[article-slug]` hero) — primary source for event-specific imagery; Niantic's official banner is canonical for the event.
2. **LeekDuck event page banner** — use when the official blog hasn't published yet (LeekDuck often previews 1–2 days early) or when the official blog doesn't have a usable hero.
3. **Pokémon GO Hub article hero** — third-line fallback.
4. **Pokémon sprite from this CDN** — final fallback when no event banner exists from any source. Every newsletter section gets an image; if no banner, use the featured Pokémon's sprite.

**Examples:**
- Tapu Lele (#786): `pm786.icon.png`
- Mega Camerupt (#323, mega): `pm323.fMEGA.icon.png`
- Necrozma Dusk Mane (#800): `pm800.fDUSK_MANE.icon.png`
- Shiny Lechonk (#915): `pm915.s.icon.png`

## When to Fall Back to Articles

**Default:** PvPoke JSON and Pokebattler JSON are the authoritative source for PvP rankings and raid counters. Always try them first.

**Fallback to articles if:**
- The JSON endpoint returns an error (4xx, 5xx)
- The Pokémon isn't found in the JSON (e.g., a brand-new species not yet in PvPoke's data)
- The data appears stale or doesn't reflect a recent rebalance
- You need context the data can't provide (community sentiment, narrative around a meta shift)

When falling back to articles, flag it: note `[fallback: source]` in the research brief so Joe can verify.

**Always use articles for:**
- **Event details** (LeekDuck, official blog) - times, dates, featured Pokémon, bonuses
- **Recent meta shifts** (Reddit, content creators) for the Trending Topic section
- **Community sentiment** that PvPoke/Pokebattler can't capture (which Pokémon "feels" overpowered, etc.)
