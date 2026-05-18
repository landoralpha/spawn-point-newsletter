# Type Effectiveness Reference — Pokémon GO

Pokémon GO uses DIFFERENT multipliers than the main-series Pokémon games. "4×" weakness and "0×" immunity are MAIN-SERIES math — they do not exist in Pokémon GO. Always use the values below when verifying damage-multiplier claims in newsletter copy or Trainer Tips.

## Multiplier Table

| Effectiveness | Pokémon GO multiplier | Main series (FOR REFERENCE ONLY — DO NOT USE) |
|---|---|---|
| Doubly super-effective (stacked, e.g., Bug/Fighting vs Flying) | **2.56×** (1.6²) | 4× |
| Super-effective (single) | **1.6×** | 2× |
| Neutral | **1×** | 1× |
| Not very effective (single resistance) | **0.625×** (1/1.6) | 0.5× |
| Doubly resistant OR main-series immunity (e.g., Normal vs Ghost, Fairy vs Dragon, Skarmory vs Electric) | **0.39×** (0.390625, 1/1.6²) | 0.25× or 0× |

## Critical rules

- **There is NO 0× / true immunity in Pokémon GO.** Main-series immunities (Ghost vs Normal, Ground vs Flying, Dragon vs Fairy, etc.) become **0.39× resistance** in Pokémon GO — attacks still land for reduced damage.
- **Multipliers stack** for dual-typed defenders. If both types are weak to the attacking type, the multiplier is 1.6 × 1.6 = **2.56×**. If both types resist (including one main-series-immunity case), it's 0.625 × 0.625 = **0.39×**.
- A "4× weak" or "double weak" claim in Pokémon GO context means **2.56× damage multiplier**. "4×" is main-series shorthand and is technically incorrect for Pokémon GO copy — use "double Flying weakness" or "2.56× Flying damage multiplier" instead.

## Common examples for fact-check verification

| Defender | Attacking type | Multiplier | Notes |
|---|---|---|---|
| Buzzwole (Bug/Fighting) | Flying | **2.56×** | Double super-effective — Flying hits both Bug and Fighting |
| Pheromosa (Bug/Fighting) | Flying | **2.56×** | Same as Buzzwole |
| Xurkitree (Electric) | Ground | 1.6× | Single super-effective |
| Nihilego (Rock/Poison) | Ground | **2.56×** | Ground hits both Rock and Poison super-effectively |
| Cresselia (Psychic) | Dark / Ghost / Bug | 1.6× | Single super-effective |
| Dragonite (Dragon/Flying) | Ice | **2.56×** | Ice hits both Dragon and Flying |
| Skarmory (Steel/Flying) | Electric | 0.39× | Steel resists + Flying immune-in-main-series → 0.39× in PoGO (NOT 0×) |
| Garchomp (Dragon/Ground) | Electric | 0.39× | Ground immune-in-main-series + Dragon neutral → 0.39× in PoGO |

## Common newsletter copy errors to flag

- **"4× weakness"** → flag as main-series math. Replace with "double weakness" or "2.56× damage multiplier."
- **"immune to X"** → flag. No immunities in Pokémon GO. Use "highly resistant" or "takes only 0.39× damage from X."
- **"takes 0 damage"** / **"no damage from X"** → flag. Minimum non-effective damage is 0.39× of base.
- **"4× resistant"** / **"quadruple resistance"** → flag. Maximum resistance is 0.39× (double resistance).

## Sources

- [Pokémon GO Hub GamePress damage mechanics](https://pokemongo.gamepress.gg/damage-mechanics) (community-aggregated, derived from Niantic game data)
- [Pokémon GO Hub type chart](https://db.pokemongohub.net/) (per-species effectiveness display)
- Niantic does not publish exact damage formulas in their help center; the 1.6× / 2.56× / 0.625× / 0.39× values are confirmed via in-game damage testing and APK datamine of the game's combat constants. These multipliers have been stable since Niantic's 2020 type-effectiveness adjustment.
