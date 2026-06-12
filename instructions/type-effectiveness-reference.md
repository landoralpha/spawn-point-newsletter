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

## Dual-type cancellation traps — common counter-list errors

When a defender's two types react oppositely to the same attacking type, multipliers MULTIPLY (not stack additively). The result can be **exactly neutral** even when one half looks like a weakness. Check the math before listing a "weakness."

### The math
`Final multiplier = (Type A reaction) × (Type B reaction)`

| Pattern | Example | Math | Net |
|---|---|---|---|
| Weak + Resist (same factor) | Fighting vs Normal/Fighting | 1.6 × 0.625 | **1.0× neutral** |
| Weak + Doubly resist | Ground vs Ground/Steel | 1.6 × 0.39 | 0.625× resisted |
| Doubly-weak | Flying vs Bug/Fighting | 1.6 × 1.6 | 2.56× |
| Resist + Resist | Fairy vs Steel/Dragon | 0.625 × 0.625 | 0.39× doubly resisted |

### Common-error dual-types — verify counters against these

These dual-typings recur in raid rotations AND have type-chart traps that produce frequent counter-list errors. Always check before recommending a "weakness" counter.

**Normal/Fighting** (Mega Lopunny, Diggersby, Greedent partial)
- True weaknesses (1.6×): **Flying, Psychic, Fairy**
- **Fighting is NEUTRAL (1.0×)** — Normal's Fighting weakness (1.6×) cancels Fighting's Fighting resist (0.625×). Conkeldurr, Machamp, Lucario, Hariyama, Mega Blaziken, Mega Lucario, Marshadow with Fighting movesets all hit NEUTRAL, not super-effective. Common counter-list error.
- Ghost is doubly resisted (0.39×): Normal's main-series Ghost immunity (0.39× in PoGO) × Fighting's Ghost neutral (1.0×) = 0.39×. Do not bring Chandelure, Origin Giratina, or Gengar.

**Steel/Dragon** (Dialga, Shadow Dialga, Duraludon, Empoleon partial)
- True weaknesses (1.6×): **Fighting, Ground**
- **Fire is NEUTRAL (1.0×)** — Steel's Fire weakness (1.6×) cancels Dragon's Fire neutral (1.0×) — wait, this is actually 1.6×. Let me recompute: Steel's Fire weakness = 1.6×, Dragon's Fire neutral = 1.0×, product = 1.6×. So Fire IS super-effective on Steel/Dragon at 1.6×. **Hub-DB confirms Fire is a weakness on Shadow Dialga.** ⚠️ This was previously mis-flagged in Spawn Point — Fire is genuinely 1.6× here.
- **Dragon, Ice, Fairy are all NEUTRAL or RESISTED** — Dragon's Dragon weakness (1.6×) × Steel's Dragon resist (0.625×) = 1.0× (Dragon neutral). Dragon's Ice resist (0.625×) × Steel's Ice neutral (1.0×) = 0.625× (Ice resisted). Steel's Fairy resist (0.625×) × Dragon's Fairy weakness (1.6×) = 1.0× (Fairy neutral). The standard Dragon-type raid roster (Mamoswine, Dragonite Outrage, Togekiss) UNDERPERFORMS here.

**Bug/Steel** (Genesect, Mega Scizor, Forretress, Escavalier partial)
- True weaknesses: Fire is **doubly super-effective (2.56×)** — Bug's Fire weakness × Steel's Fire weakness.
- Fire-type attackers (Mega Charizard Y, Shadow Moltres, Reshiram) are catastrophic on Bug/Steel raids. This is one of the cleanest matchups in PoGO.

**Ghost/Dark** (Hoopa Unbound partial, Spiritomb, Sableye partial)
- True weakness (single): **Fairy** (1.6× — Dark side)
- **No weakness on Ghost side that isn't covered by Dark** — Ghost's Ghost weakness × Dark's Ghost neutral = 1.6×. Ghost attackers still work but only via the Ghost-half exposure.
- Fighting, Psychic, Bug are ALL resisted or doubly resisted (Dark resists all three). Common error to bring Conkeldurr/Mewtwo for Spiritomb.

**Water/Ground** (Swampert, Whiscash, Quagsire, Mega Swampert)
- True weakness: **Grass at 2.56×** (Water weak × Ground weak, both 1.6× = 2.56×). The single strongest single-type matchup in the game.
- Electric is DOUBLY RESISTED (Water resist × Ground immunity = 0.625 × 0.39 = 0.244×, effectively 0.39× per PoGO's floor). DO NOT lead with Electric.

**Fire/Flying** (Charizard, Mega Charizard, Moltres, Talonflame)
- True weakness: **Rock at 2.56×** (Fire weak × Flying weak, both 1.6×). Rock attackers cremate this typing.
- Grass, Bug, Ground are all DOUBLY resisted. Ground vs Flying main-series immunity becomes 0.39× in PoGO, stacked with Fire's Ground neutral (1.0×) = 0.39×.

**Rock/Ground** (Rhyperior, Excadrill partial, Mega Aerodactyl partial)
- True weakness: **Water and Grass at 2.56×**
- Electric is DOUBLY resisted (Ground immunity to Electric = 0.39× × Rock neutral × 1.0 = 0.39×). Never lead with Electric.

### Validator rule (for recon Step 5.6)

For every "Premium" or "Budget" counter listed against a boss, compute:
`multiplier = boss_type_chart[charged_move_type] × (boss_type_chart[charged_move_type] if dual_type else 1)`

If `multiplier < 1.6`, the charged move is **not super-effective** on the boss. Flag the counter unless the rationale is documented (e.g., high raw DPS, bulk for survival, Mega aura cross-promo). The Pokebattler `aggregation=AVERAGE` mode does sometimes rank neutral-coverage Megas highly due to raw stats, but the Hub article + Hub-DB typically correct this.

## Sources

- [Pokémon GO Hub GamePress damage mechanics](https://pokemongo.gamepress.gg/damage-mechanics) (community-aggregated, derived from Niantic game data)
- [Pokémon GO Hub type chart](https://db.pokemongohub.net/) (per-species effectiveness display)
- Niantic does not publish exact damage formulas in their help center; the 1.6× / 2.56× / 0.625× / 0.39× values are confirmed via in-game damage testing and APK datamine of the game's combat constants. These multipliers have been stable since Niantic's 2020 type-effectiveness adjustment.
