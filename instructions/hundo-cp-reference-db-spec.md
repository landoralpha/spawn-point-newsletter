# Hundo CP Reference — Architecture & Rollout

The master Hundo CP table backs every catch-CP citation in Spawn Point's research brief and newsletter draft. It lives in two places:

1. **PRIMARY — Vercel static JSON.** A committed file in `pogo-card-generator/public/data/hundo-cp-master.json`, deployed to Vercel and served at:

   <https://pogo-card-generator.vercel.app/data/hundo-cp-master.json>

   This is what the Spawn Point research trigger fetches at runtime (one ≈500 KB GET per run, no auth, CDN-cached). It is the source of truth.

2. **MIRROR — Notion database.** Optional. Human-readable browsing and editing surface. The trigger NEVER reads from Notion. If the two stores diverge, the Vercel JSON wins; resolve by re-running the seeder + committing.

The seeder script `pogo-card-generator/scripts/seed-hundo-cp-master.ts` writes the JSON file on every run and optionally syncs the Notion mirror via `--mirror`.

---

## 1. Coverage

Every Pokémon (~1,400 rows): base species + all form variants from `pokemon-go-api/pokedex.json` (megaEvolutions, regionForms, tempEvolutions) + Legends Z-A backfills from `pogo-card-generator/src/data/overrides/megaRoster.ts`. Each row carries hundo (15/15/15) CPs at the four encounter levels Spawn Point cites:

| Level | Encounter context | CPM |
|---|---|---|
| **L15** | Research encounters | 0.51739395 |
| **L20** | Raid catches + Egg hatches (same level) | 0.5974 |
| **L25** | Weather-Boosted Raids | 0.667934 |
| **L50** | Fully maxed-out (XL candy ceiling) | 0.84029999 |

**Why formula and not Hub-DB scrape.** The canonical PoGO CP formula `floor((Atk+15) * sqrt(Def+15) * sqrt(Sta+15) * cpm^2 / 10)` matches Hub-DB exactly at L15/L20/L25/L50 — the L34–L36 boundary where the formula and Hub-DB diverge isn't relevant here. Pure computation is deterministic, fast, and avoids ~1,400 outbound Hub-DB requests.

---

## 2. Vercel JSON shape

```json
{
  "generatedAt": "2026-05-30T16:23:00.000Z",
  "count": 1389,
  "rows": [
    {
      "species": "Mewtwo",
      "form": "base",
      "dex": 150,
      "baseAtk": 300, "baseDef": 182, "baseSta": 214,
      "cpL15": 1791, "cpL20": 2387, "cpL25": 2984, "cpL50": 4724,
      "source": "https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex.json",
      "method": "pokedex.json-computed"
    },
    …
  ]
}
```

**Key:** `(species_lowercase, form)`. `form` is `base` for the standard form, else one of: `mega`, `mega_x`, `mega_y`, `mega_z`, `primal`, `gigantamax`, `dynamax`, `shadow`, `alolan`, `galarian`, `hisuian`, `paldean`, `origin`, `altered`, `therian`, `incarnate`, `crowned_sword`, `crowned_shield`, `hero`, `dawn_wings`, `dusk_mane`, `ultra`, `white`, `black`.

**Auth.** The pogo-card-generator app uses a login middleware, but `/data/` is explicitly exempt ([src/middleware.ts](https://github.com/landoralpha/pogo-card-generator/blob/main/src/middleware.ts)). The JSON is public by design.

---

## 3. Notion mirror schema (optional, parallel to the JSON)

**Database name:** `Spawn Point Hundo CP Reference`
**Parent:** Spawn Point Notion workspace, under a "Reference" sub-page.

| Property | Type | Notes |
|---|---|---|
| Species | Title | `Garchomp`, `Mega Garchomp Z`, `Primal Kyogre`, etc. |
| Form | Select | `base` for the standard form; same enum as the JSON. |
| Dex | Number | National dex. |
| Base ATK / DEF / STA | Number ×3 | From pokedex.json. |
| Hundo CP @ L15 | Number | Research encounters. |
| Hundo CP @ L20 | Number | Raid catch + Egg hatch. |
| Hundo CP @ L25 | Number | Weather-Boosted Raid. |
| Hundo CP @ L50 | Number | XL candy ceiling. |
| Source | URL | `pokemon-go-api pokedex.json` for seeded rows. |
| Method | Select | `pokedex.json-computed` or `hub-db-fetched`. |
| First Recorded | Date | First seed. |
| Last Verified | Date | Last successful sync. |
| Verification Notes | Rich text | Free-form (rebalance flags, etc.). |

**Uniqueness:** `(Species, Form)` — the seeder's `--mirror` mode queries before insert and skips existing rows.

---

## 4. Rollout

### Minimum viable (Vercel only)

```bash
cd ~/Claude-Master/pogo-card-generator
npm run seed-hundo-master                 # writes public/data/hundo-cp-master.json
git add public/data/hundo-cp-master.json
git commit -m "data(hundo): refresh master table"
git push                                  # Vercel deploys → live at /data/hundo-cp-master.json
```

After this, the next research-trigger fire reads the new master. Done.

### Add the Notion mirror (one-time setup)

1. Create a Notion integration at <https://www.notion.so/my-integrations>. Save the secret to `pogo-card-generator/.env.local` as `NOTION_TOKEN=secret_…`.
2. Pick a parent Notion page under the Spawn Point workspace. **Share that page with your integration** (Connections menu on the page) so the API can create databases inside it. Copy the page ID from its URL.
3. `npm run seed-hundo-master -- --create-db --parent-page-id=<page-id>` — creates the DB with the schema above, prints the new database URL + ID.
4. `npm run seed-hundo-master -- --mirror --db-id=<db-id>` — bulk-inserts every row from the JSON to Notion (~8 minutes at the polite 3 req/sec rate). Idempotent: re-runs skip existing `(Species, Form)` rows.

Subsequent refreshes:

```bash
npm run seed-hundo-master -- --mirror --db-id=<db-id>
git commit + push the updated JSON
```

The seeder updates Vercel (file write) AND Notion (API push) in one go.

---

## 5. Update / refresh policy

- **Routine refresh:** run the seeder when pokedex.json changes (new species/forms ship, Niantic rebalances). The script is fast (one fetch + compute + one file write); no harm in re-running monthly.
- **Mid-week miss:** if the research trigger encounters a featured species not yet in the master, it falls back to Hub-DB ad-hoc + flags `[hundo-master miss]` in the Run Log. Joe re-runs the seeder + commits to backfill.
- **Niantic rebalance:** when a stat change ships, re-run the seeder; the formula uses the new pokedex.json base stats automatically.
- **Mega Z / speculative roster placeholders:** the seeder uses base species stats as placeholders (autoDerive pattern) for Legends Z-A megas not yet in pokedex.json. Once Niantic ships real values, pokedex.json updates and the next seeder run replaces the placeholder.
- **GMax / DMax:** pokemon-go-api's pokedex.json does not currently carry tempEvolution stats, so the seeded rows for Gigantamax/Dynamax forms are absent. The trigger's on-miss path picks these up ad-hoc from Hub-DB; a future seeder revision can include them if Niantic ships them in pokedex.json.

---

## 6. Why Vercel-primary, not Notion-primary

| Concern | Notion-primary | Vercel-primary (current) |
|---|---|---|
| Per-run reads | 10–30 Notion API queries | 1 CDN GET (~500 KB) |
| Hot-path dependency | Notion API up + Notion MCP available | Vercel CDN up (essentially always) |
| Rate limits | Notion: 3 req/sec | Vercel CDN: effectively none |
| Sandbox reachability | Notion MCP availability gated by run env | Public HTTPS, fetch_url MCP-friendly |
| Human-readable browsing | Native | Via the Notion mirror |
| Mid-run writeback | Yes (write to Notion on miss) | No (static deploy artifact) |

The mid-run writeback was the only Notion-primary win, and it's modest — misses are rare (only genuinely-new species), and the seeder-then-commit backfill closes them deterministically.
