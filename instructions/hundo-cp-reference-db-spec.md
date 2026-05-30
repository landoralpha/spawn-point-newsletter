# Hundo CP Reference Database — Spec & Rollout

The **`Spawn Point Hundo CP Reference`** Notion database is the master, persistent source for every featured Pokémon's hundo catch CPs (L20 base, L25 weather-boosted) plus the base stats they derive from. The Research Agent trigger queries it first every run; only species/forms that have never been featured before trigger a Hub-DB fetch (which is then written back so the next run is a lookup).

This file documents:
1. The database schema (properties + types + allowed values).
2. The rollout sequence (create DB → seed → wire trigger → verify).
3. The one-time pre-population playbook (so the DB is "100% solid" out of the gate, not just organically grown).
4. Verification / re-verification policy.

---

## 1. Schema

**Database name:** `Spawn Point Hundo CP Reference`
**Parent:** under the same Spawn Point Notion workspace that already houses the News & Updates DB and the Run Log DB. A "Reference" sub-page is the natural home.

| Property | Type | Required | Notes |
|---|---|---|---|
| **Species** | Title | yes | Display name. Match the catalog convention: `Garchomp`, `Mega Garchomp`, `Mega Garchomp Z`, `Primal Kyogre`, `Zacian Crowned Sword`, `Black Kyurem`, etc. (NOT slug — humans read this.) |
| **Form** | Select | yes | `base` for the standard form. Allowed values: `base`, `mega`, `mega_x`, `mega_y`, `mega_z`, `primal`, `gigantamax`, `dynamax`, `shadow`, `alolan`, `galarian`, `hisuian`, `paldean`, `origin`, `altered`, `therian`, `incarnate`, `crowned_sword`, `crowned_shield`, `hero`, `dawn_wings`, `dusk_mane`, `ultra`, `white`, `black`. (Mirrors the pogo-card-generator `PokemonForm` enum so the two systems stay aligned.) |
| **Dex** | Number | yes | National dex number (integer). Form variants share the base species' dex. |
| **Base ATK** | Number | yes | Pokemon GO base attack from `pokemon-go-api/pokedex.json` (or Hub-DB if pokedex.json is stale on a brand-new release). |
| **Base DEF** | Number | yes | Pokemon GO base defense. |
| **Base STA** | Number | yes | Pokemon GO base stamina. |
| **Hundo CP @ L15** | Number | yes | Research encounter CP (level 15, 15/15/15). |
| **Hundo CP @ L20** | Number | yes | Raid catch + Egg hatch CP (level 20, 15/15/15). Same level for both — one column covers both encounter contexts. |
| **Hundo CP @ L25** | Number | yes | Weather-Boosted Raid catch CP (level 25, 15/15/15). |
| **Hundo CP @ L50** | Number | yes | Fully maxed-out CP (level 50 via XL candy, 15/15/15). Doesn't include the Best Buddy in-battle bump. |
| **Source** | URL | yes | Either the Hub-DB URL (e.g. `https://db.pokemongohub.net/pokemon/445-Mega`) OR the literal string `pokedex.json (computed)` for compute-only fallback. |
| **Method** | Select | yes | `hub-db-fetched` or `pokedex.json-computed`. (Defines the verification path. `hub-db-fetched` rows are higher trust because Hub-DB renders the actual GAME value, not a formula.) |
| **First Recorded** | Date | yes | The run that first added the row. |
| **Last Verified** | Date | yes | Most recent re-verification (Hub-DB re-fetch or recompute match). Equal to First Recorded for fresh rows. |
| **Verification Notes** | Rich text | no | Free-form. Use for "Niantic rebalanced 2026-04 — re-verified" or "Hub-DB still shows old stats; flagged." |

**Uniqueness:** the **(Species, Form)** pair is the natural key. Before creating a new row, the trigger MUST query by Species + Form and refuse to insert a duplicate (it should update the existing row instead).

---

## 2. Rollout

In order:

1. **Joe (in Notion UI):** Create the database under the Spawn Point workspace with the schema above. Set Select options for `Form` and `Method` exactly as listed. Get the **data source URL** (`collection://...`) from Notion's database menu.

2. **Joe (in this repo):** Open `triggers/researcher.md`, find the placeholder `[FILL_IN_AFTER_DB_CREATED]` (in the Step 2 Hundo flow), and replace it with the actual `collection://...` URL. Commit + push.

3. **One-time pre-population** (optional but recommended for "100% solid out of the gate" — see §3 below). Run the seeder script in `pogo-card-generator` against the new DB to fill it with the standard featured set (all legendaries / mythicals / megas / GO-released Ultra Beasts — ~250–300 rows). After this, the trigger's normal run only fetches the genuinely-new species each week (typically 0–2 per run).

4. **First production run after wiring:** the trigger's first run with the DB live will hit it for every featured species in that week's research. New species miss → fetch → write row → use. Existing species hit immediately. Joe can spot-check the brief snapshot's "From master DB?" column to confirm the lookup-first path engaged.

5. **Until step 1 is done:** the trigger falls back to the legacy per-run fetch-and-record-to-brief flow (graceful degradation; no run failures). The snapshot's "From master DB?" column shows `[no master DB this run — direct fetch]` so the regression is visible in the run summary.

---

## 3. One-time pre-population playbook

Goal: seed every species + form variant in one rate-limited pass so weekly runs do near-zero new-row creation. Scope: **all Pokémon** in `pokemon-go-api/pokedex.json` (base species + every form: megaEvolutions, regionForms, tempEvolutions) + the speculative Legends Z-A backfills from `pogo-card-generator/src/data/overrides/megaRoster.ts` — roughly **1,200–1,500 rows**.

**Computation, not fetching.** For the four levels we care about (L15 / L20 / L25 / L50), the canonical GO CP formula `floor((Atk+15) * sqrt(Def+15) * sqrt(Sta+15) * cpm^2 / 10)` matches Hub-DB exactly — the L34–L36 boundary where the formula and Hub-DB diverge is not touched by these levels. So the seeder reads pokedex.json base stats and computes; no Hub-DB fetches required for the bulk seed, which keeps the run polite and deterministic. The trigger's on-miss path still goes Hub-DB-first for any species the seeder didn't cover (genuinely new releases between pokedex.json updates).

**CPM constants (canonical):**
- L15: `0.51739395`
- L20: `0.5974`
- L25: `0.667934`
- L50: `0.84029999`

**Seeder script:** `pogo-card-generator/scripts/seed-hundo-cp-master.ts`. Three modes:

- `--dry` (default): walks pokedex.json + the mega roster, computes all four hundo CPs per row, writes `scripts/.hundo-cp-seed.json` for Joe to review. No Notion writes.
- `--create-db --parent-page-id=<id>`: creates the DB in Notion with the schema above (uses `NOTION_TOKEN`). Prints the new database URL.
- `--push --db-id=<id>`: bulk-inserts every row from `.hundo-cp-seed.json` into the DB via raw Notion API. Rate-limited (~3 req/sec). Idempotent: queries by (Species, Form) before insert and skips existing rows, so re-runs after schema/data changes are safe.

Joe's full rollout sequence:

1. Create a Notion Integration at <https://www.notion.so/my-integrations>. Save the secret to `pogo-card-generator/.env.local` as `NOTION_TOKEN=secret_...`.
2. Decide where the DB lives (under the Spawn Point workspace's Reference page) and copy that parent page's ID.
3. `cd pogo-card-generator && npm run seed-hundo-master -- --create-db --parent-page-id=<id>` → prints the new DB's URL + `data_source_url`.
4. `npm run seed-hundo-master -- --push --db-id=<id>` → ~7-minute bulk insert.
5. Paste the `data_source_url` into `triggers/researcher.md`'s `[FILL_IN_AFTER_DB_CREATED]` slot. Commit + push spawn-point.

After step 5 the researcher trigger runs in lookup-first mode against a fully-seeded DB.

---

## 4. Verification / re-verification policy

- **Fresh rows** (First Recorded = today): trust the source path. Method `hub-db-fetched` is canonical; `pokedex.json-computed` is acceptable but flag in `Verification Notes` if Hub-DB was checked and missing.

- **Aging rows** (Last Verified > 90 days ago): the next research run that touches the row should re-fetch and recompute as a sanity pass. If values match, update `Last Verified = today`. If they DIFFER (rare — Niantic rebalance, Hub-DB correction), update Hundo CP @ L20/L25 + Base stats + `Verification Notes` with a one-line `Re-verified [date]: <old L20>/<old L25> → <new L20>/<new L25> (suspected Niantic rebalance)`.

- **Niantic rebalance announcement:** if a stat change ships, Joe (or a one-off script) re-fetches the affected species' rows wholesale rather than waiting for the 90-day pass. This is rare (a few per year).

- **Form additions:** when a new mega tier ships (e.g. Legends Z-A's Mega Z), the seeder script handles bulk creation; or the first weekly research run that features one creates the row organically.

---

## 5. Why this DB lives in Notion (not a JSON file in the repo)

The repo would be simpler (just commit `instructions/hundo-cp-table.json` and read it via raw.githubusercontent), BUT the triggers don't have repo write access — they can only edit the markdown snapshots Joe pushes manually. A Notion DB is the only persistent store the triggers can write to mid-run. The trade-off is one Notion query per featured species per run, which is negligible compared to the Hub-DB fetch + LLM extract it replaces.
