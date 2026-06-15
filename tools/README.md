# tools/ — Standalone Spawn Point validators

CLI helpers for the recon trigger and for manual pre-publish checks.

## `check_counter_moveset.py`

Verify that a list of counter movesets are super-effective on a boss using PoGO type-chart math (1.6 / 1.0 / 0.625 / 0.39, multiplicative for dual-types). Catches the recurring drafting error where a counter is listed with a NEUTRAL charged move.

**Usage:**
```bash
./check_counter_moveset.py \
  --boss "Mega Lopunny:Normal/Fighting" \
  "Mega Rayquaza:Air Slash/Dragon Ascent" \
  "Mega Latios:Zen Headbutt/Aura Sphere" \
  "Blaziken:Counter/Aura Sphere"
```

**Output:**
```
Counter         Fast (type)              Charged (type)              CM mult  Verdict
Mega Rayquaza   Air Slash (Flying)       Dragon Ascent (Flying)        1.60×  ✓ SE charged + SE fast
Mega Latios     Zen Headbutt (Psychic)   Aura Sphere (Fighting)        1.00×  ⚠ NEUTRAL charged (fast SE — borderline OK)
Blaziken        Counter (Fighting)       Aura Sphere (Fighting)        1.00×  ⚠ NEUTRAL charged — SUBOPTIMAL
```

**Flags:**
- `--strict` — exit 1 if any counter is suboptimal (useful for recon to fail loudly)
- `--unknown-ok` — silently skip counters whose moves aren't in `moves.json` (otherwise an unknown move is an error)

**Extending the move list:**
Add new moves to `moves.json` as `{"Move Name": "Type"}`. The script merges this on top of its bundled defaults. Niantic-canonical move names only (verify in-game spelling).

**Use in recon Step 5.6:** Recon should run this against every counter in the published Premium and Budget lists for each raid boss section. Any ⚠ or ✗ verdict is a FLAG.

## `mgrann03_check.py`

Cross-reference counter movesets, debut claims, raid-tier assignments, and Shadow availability against the `mgrann03/pokemon-resources` data layer (the community-curated PoGO species database that powers DialgaDex). Adds value over raw GameMaster JSON by separating Elite-TM-only moves from standard movepool, marking each species's raid_tier, and tracking release status with a manual override file for announced-but-not-yet-released species.

**Subcommands:**
- `moveset "<Species>" "<Fast/Charged>"` — Verify counter moveset is real AND classify as STANDARD vs ELITE accessibility.
- `debut "<Species>"` — Verify whether a debut claim is genuine (NOT A DEBUT if already released; DEBUT if in announced file with eff_date; UNKNOWN otherwise).
- `tier "<Species>"` — Look up `raid_tier` (1, 3, 4=Mega, 5=Legendary, 6=Super Mega current, 8=Super Mega Raid Day debut).
- `shadow "<Species>"` — Check Shadow form availability.
- `info "<Species>"` — Print full entry for a species (debug / inspection).

**Examples:**
```bash
./mgrann03_check.py moveset "Mega Rayquaza" "Air Slash/Dragon Ascent"   # → ⚠ ELITE (Dragon Ascent)
./mgrann03_check.py moveset "Mega Skarmory" "Steel Wing/Brave Bird"     # → ✓ STANDARD
./mgrann03_check.py debut "Mega Skarmory"                                # → ✓ DEBUT, eff_date 2026-06-27, raid_tier 8
./mgrann03_check.py debut "Tapu Fini"                                    # → ✗ NOT A DEBUT (released)
./mgrann03_check.py tier "Bombirdier"                                    # → raid_tier=3 (3-Star)
```

**Caching:** mgrann03 JSON files cached locally under `tools/cache/mgrann03/` for 24h. Override with `--refresh`.

**Use in researcher:** Step 2 (Research Phase) Counter Recipe runs `moveset` on every cited counter for accessibility classification; Step 1.5 (Rule Verification Pass) runs `debut` on every species framed as a debut.

**Use in recon:** Category C runs `moveset` for accessibility-tier confidence; Category F runs `debut` to verify debut framing. Both are auto-patchable when the verdict is unambiguous.
