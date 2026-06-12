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
