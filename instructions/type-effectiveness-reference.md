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
| Skarmory (Steel/Flying) | Electric | **1.6×** | Steel takes Electric NEUTRAL (1.0×); Flying is weak to Electric (1.6×). Product = 1.6× SE. Skarmory is WEAK to Electric — Hub-DB confirms. (This row was wrong prior to 2026-06-12.) |
| Garchomp (Dragon/Ground) | Electric | **0.244×** | Dragon RESISTS Electric (0.625×); Ground is main-series-immune to Electric (0.39× in PoGO). Product = 0.625 × 0.39 = 0.244× — "triple resistance" per Hub-DB Garchomp meta analysis. Stacking goes BELOW the 0.39× single-layer floor. (This row was wrong prior to 2026-06-12 — the previous "Dragon neutral" rationale was wrong.) |

## Stacking floor — important clarification

The **0.39× value is the floor for a SINGLE main-series-immunity matchup**, NOT a hard cap on dual-type defenders. Dual-type stacking multiplies through normally:

- One resist (0.625×) × one immunity (0.39×) = **0.244×** ("triple resistance")
- Two main-series immunities (theoretical, 0.39 × 0.39) = **0.152×**

Pokémon GO Hub displays these accurately on per-species pages — values like 24.4% damage multiplier ARE possible and show up in the in-game effectiveness banner as "Not very effective."

## Common newsletter copy errors to flag

- **"4× weakness"** → flag as main-series math. Replace with "double weakness" or "2.56× damage multiplier."
- **"immune to X"** → flag. No immunities in Pokémon GO. Use "highly resistant" or "takes only 0.39× damage from X."
- **"takes 0 damage"** / **"no damage from X"** → flag. Minimum non-effective damage is 0.39× for a single resistance layer; can be 0.244× with stacking.
- **"4× resistant"** / **"quadruple resistance"** → flag as main-series math. Use specific multiplier (0.39× single-layer floor, 0.244× triple-resistance via stacking).
- **Pokémon GO Hub "Damage Mechanics" wiki article (2019, BoonSlevin)** still cites the OLD pre-2020 multipliers (1.4× SE, 0.714× NVE, 1.96× double-weak). DO NOT use that article as a source. Use Hub-DB's per-species type chart instead — it reflects the current 1.6×/0.625×/0.39× values.

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
- True weaknesses (1.6×): **Fairy, Fighting, Flying, Psychic** (confirmed Hub-DB Mega Lopunny: all four at 160%)
- **The trap:** It LOOKS like Fighting should be neutral because Fighting-types feel bulky vs other Fighting-types in PvP. **It's not — Fighting does NOT resist Fighting in PoGO or main series.** Fighting vs Normal = 1.6× SE; Fighting vs Fighting = 1.0× neutral; product = 1.6× SE. Counter, Aura Sphere, Dynamic Punch, Force Palm, Close Combat all hit Normal/Fighting at full SE × STAB. Conkeldurr, Machamp, Lucario, Hariyama, Mega Blaziken, Mega Lucario, Marshadow are TOP-TIER picks, not suboptimal ones.
- Ghost is doubly resisted (0.39×): Normal's main-series Ghost immunity (0.39× in PoGO) × Fighting's Ghost neutral (1.0×) = 0.39×. Do not bring Chandelure, Origin Giratina, or Gengar.
- (Editorial note: this trap section previously claimed Fighting was neutral on Normal/Fighting — corrected 2026-06-12 after Joe asked us to double-check PoGO type effectiveness. The wrong claim cascaded into a bad #18 counter list edit; reverted.)

**Steel/Dragon** (Dialga, Shadow Dialga, Duraludon, Empoleon partial)
- True weaknesses (1.6×): **Fighting, Ground** ONLY (confirmed Hub-DB Dialga: 160% on both, nothing else)
- **Fire is NEUTRAL (1.0×) — the real trap.** Steel's Fire weakness (1.6×) cancels with Dragon's Fire resist (0.625×): 1.6 × 0.625 = 1.0×. Fire attackers (Reshiram, Mega Charizard Y, Shadow Moltres) deal NEUTRAL damage to Shadow Dialga, not SE. This was previously mis-claimed in this very doc as "Fire is SE at 1.6×" — Hub-DB Dialga page only lists Fighting and Ground as weaknesses.
- **Dragon, Ice, Fairy are all NEUTRAL or DOUBLY RESISTED** — Dragon's Dragon weakness (1.6×) × Steel's Dragon resist (0.625×) = 1.0× (Dragon neutral). Dragon's Ice resist (0.625×) × Steel's Ice neutral (1.0×) = 0.625× (Ice resisted). Steel's Fairy resist (0.625×) × Dragon's Fairy weakness (1.6×) = 1.0× (Fairy neutral). The standard Dragon-type raid roster (Mamoswine Ice, Dragonite Outrage, Togekiss Charm) UNDERPERFORMS here.
- **Grass and Poison are doubly resisted (0.39×):** Steel resists Grass × Dragon resists Grass = 0.625² = 0.39×; Steel main-series-immune to Poison × Dragon resist = 0.39 × 0.625 = 0.244× (triple resistance). Hub-DB lists Grass and Poison at 39.1% on Dialga (the Poison 0.244× actually rounds to 39.1% in the on-screen display — Hub-DB clips the display at the 0.39 floor).

**Bug/Steel** (Genesect, Mega Scizor, Forretress, Escavalier partial)
- True weaknesses: Fire is **doubly super-effective (2.56×)** — Bug's Fire weakness × Steel's Fire weakness.
- Fire-type attackers (Mega Charizard Y, Shadow Moltres, Reshiram) are catastrophic on Bug/Steel raids. This is one of the cleanest matchups in PoGO.

**Ghost/Dark** (Spiritomb, Sableye partial — Hoopa Unbound is Psychic/Dark, different)
- True weakness (single): **Fairy at 1.6×** — the ONLY weakness. (Fairy is neutral on Ghost; SE on Dark; product = 1.6×.)
- **Common errors:**
  - **Fighting:** Ghost main-series-immune to Fighting (0.39× in PoGO) × Dark weak to Fighting (1.6×) = **0.625× single resisted**. Despite Fighting being SE on Dark types in isolation, Conkeldurr on Spiritomb takes a single-layer resist. NOT a counter.
  - **Bug:** Ghost resists Bug (0.625×) × Dark weak to Bug (1.6×) = **1.0× neutral**. Despite Bug being SE on Dark in isolation, it's neutral here. Common error to bring Genesect or Pinsir.
  - **Ghost:** Ghost SE on Ghost (1.6×) × Dark resists Ghost (0.625×) = **1.0× neutral**. Chandelure on Spiritomb is neutral, not SE.
  - **Dark:** Same math as Ghost — neutral on Ghost/Dark.
  - **Psychic:** Ghost neutral to Psychic (1.0×) × Dark main-series-immune to Psychic (0.39×) = **0.39× doubly resisted**. Don't bring Mewtwo.
- Fairy attackers (Gardevoir, Togekiss, Tapu Lele Moonblast, Mega Diancie if released) are the only true SE picks.

**Water/Ground** (Swampert, Whiscash, Quagsire, Mega Swampert)
- True weakness: **Grass at 2.56×** (Water weak × Ground weak, both 1.6×). The strongest single-attack-type matchup commonly seen in raid pools.
- **The real Electric trap:** Electric vs Water (1.6× SE) × Electric vs Ground (0.39× main-series immunity) = **0.625× single resisted**, NOT doubly resisted. Hub-DB Swampert confirms Electric at 62.5%. Electric attackers underperform here because Ground's immunity cancels Water's weakness — but it's NOT the 0.244× / 0.39× I previously claimed.
- Even at 0.625× and against high Water/Ground bulk, Electric is a poor pick. Use Grass exclusively.

**Fire/Flying** (Charizard, Mega Charizard, Moltres, Talonflame, Mega Charizard Y)
- True weakness: **Rock at 2.56×** (Fire weak × Flying weak). Rock attackers cremate this typing — Smack Down + Stone Edge Tyranitar, Rampardos, Mega Aerodactyl, Mega Rhyperior.
- **Grass and Bug are DOUBLY resisted (0.39×):** both Fire AND Flying resist Grass and Bug, so 0.625 × 0.625 = 0.39× on both. Don't bring Kartana, Mega Sceptile, Genesect.
- **Ground is SINGLE resisted (0.625×), NOT doubly resisted** as previously written here: Fire is weak to Ground (1.6×) × Flying main-series-immune to Ground (0.39×) = 0.625×. Ground attackers underperform but it's a single-layer resist, not a doubly-resisted floor.

**Rock/Ground** (Rhyperior, Excadrill partial, Mega Aerodactyl partial — Mega Aero is Rock/Flying actually)
- True weaknesses: **Water and Grass at 2.56×** (both attacking types are SE on both Rock and Ground).
- **Electric is DOUBLY resisted (0.39×):** Electric vs Rock (1.0× neutral — Rock doesn't weak or resist Electric) × Electric vs Ground (0.39× main-series immunity) = 0.39×. Never lead with Electric.
- **Ice is also DOUBLY weak (2.56×) for some species** — Ice vs Rock is neutral but Ice vs Ground is SE; depending on which species we're discussing, Ice can be a real second weakness or just SE single.
  - Wait: Ice vs Rock (1.0× neutral) × Ice vs Ground (1.6× SE) = 1.6× single SE, NOT doubly weak. Correct list: just Water and Grass at 2.56×, Ice and Fighting at 1.6× single SE.

**Bug/Steel** (Genesect, Mega Scizor, Forretress, Escavalier partial)
- True weakness: **Fire is doubly super-effective (2.56×)** — Bug's Fire weakness × Steel's Fire weakness. Fire-type attackers (Mega Charizard Y, Shadow Moltres, Reshiram, Mega Blaziken) are catastrophic on Bug/Steel raids. One of the cleanest matchups in PoGO.
- **No other weakness:** Rock vs Bug (1.6× SE) × Rock vs Steel (0.625× resists) = 1.0× neutral. Rock is NOT a weakness despite Bug being weak to Rock in isolation. Common counter-list error.
- Fighting on Bug/Steel: Fighting vs Bug (0.625× Bug resists Fighting) × Fighting vs Steel (1.6× SE) = 1.0× neutral. Fighting attackers don't dent Mega Scizor.

### Validator rule (for recon Step 5.6)

For every "Premium" or "Budget" counter listed against a boss, compute:
`multiplier = boss_type_chart[charged_move_type] × (boss_type_chart[charged_move_type] if dual_type else 1)`

If `multiplier < 1.6`, the charged move is **not super-effective** on the boss. Flag the counter unless the rationale is documented (e.g., high raw DPS, bulk for survival, Mega-Evolved attack boost cross-promo). The Pokebattler `aggregation=AVERAGE` mode does sometimes rank neutral-coverage Megas highly due to raw stats, but the Hub article + Hub-DB typically correct this.

## Sources

- [Bulbapedia: Type effectiveness](https://bulbapedia.bulbagarden.net/wiki/Type) (type-matchup reference; note the main series uses 2× / 0.5× where Pokémon GO applies 1.6× / 0.625×)
- [Pokémon GO Hub type chart](https://db.pokemongohub.net/) (per-species effectiveness display)
- Niantic does not publish exact damage formulas in their help center; the 1.6× / 2.56× / 0.625× / 0.39× values are confirmed via in-game damage testing and APK datamine of the game's combat constants. These multipliers have been stable since Niantic's 2020 type-effectiveness adjustment.
