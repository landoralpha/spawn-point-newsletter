# Pokémon GO Seasons Reference

**Single source of truth for season-scoped facts.** Anything that's bound to a specific season (Daily Discovery rotation, themed Community Days, season-specific GO Pass structure, debut pipelines, themed Research Breakthrough pools, Egg pools, GBL cup rotation, season-themed Special Research) lives in THIS file under the appropriate season section.

System-level mechanics that persist across seasons (Mega Evolution rules, Dynamax mechanics, Link Charges, Stardust formulas, raid pass economics) belong in their own `*-reference.md` files. Once a season-debut mechanic is confirmed to persist post-season, it gets promoted from here to the appropriate general reference.

## How to use this file

For any newsletter / recon / monitor activity:

1. **FIRST** identify the date range being worked on (newsletter date range, recon target post date, monitor scan window).
2. **THEN** look up overlapping season(s) in the Date Range Index below.
3. **APPLY** only the data from season(s) overlapping that range.
4. **NEVER** pull future-season facts into a newsletter fully contained in an older season.

## Date Range Index

| Season | Start | End | Status |
|---|---|---|---|
| Season of Memories in Motion | 2026-03-03 10:00 AM local | 2026-06-02 10:00 AM local | HISTORICAL |
| Season of Forever Forward | 2026-06-02 10:00 AM local | 2026-09-08 10:00 AM local | CURRENT (active) / UPCOMING (pre-June 2) |

## Season-application rule (CRITICAL)

For a newsletter spanning [Monday] – [Sunday]:
- **Both dates within one season** → apply that season's data only.
- **Range straddles a season boundary** → apply EACH season's data ONLY to the days within that season's window. Be explicit in copy: "Through Tuesday (Memories in Motion era)..." / "Starting Wednesday (Forever Forward season opens)..."
- **NEVER apply future-season info to a newsletter fully contained in an older season.** A recon on Spawn Point #15 (May 18-24, entirely within MIM) must not flag Forever Forward facts.

---

## Memories in Motion (HISTORICAL — 2026-03-03 to 2026-06-02)

**Season window:** March 3, 2026 at 10:00 AM local → June 2, 2026 at 10:00 AM local.

**Theme:** Nostalgia — Pokémon GO's pre-anniversary look-back on the game's history.

### Daily Discovery rotation (MIM era)

| Day | Bonus |
|---|---|
| Monday | **Fast-Track Monday** — 2× GO Points earned all day + Max Monday (Dynamax featured boss, 6:00 AM–9:00 PM, Power Spot refresh boost) |
| Tuesday | **Showcase Tuesday** — PokéStop Showcases active (one entry per Showcase) |
| Wednesday | **Raid rotation flips at 6:00 AM** (new Mega + new 5-Star bosses; previous bosses ended Tuesday 10:00 PM) + featured Raid Hour 6:00–7:00 PM |
| Thursday | **GO Battle Thursday** — 4× Stardust from GBL win rewards + daily set cap raised from 5 to 10 (50 battles total) |
| Friday | **Friendship Friday** — standard trade bonuses active (verify specific values per event — they vary) |
| Saturday | **Spotlight Saturday** — featured Pokémon spotlight + bonus per event |
| Sunday | **Catch-Up Sunday** + **Double-Time Sunday** — Incense and Lures last 2× their normal duration |

### Season-specific mechanics

- **Wild shiny rate flattened to 1/512** (March 3 onward). Raid/egg perma-boost removed from wild encounters. Raids/eggs standardized to 1/64 baseline (5-Star Legendary at 1/20). See `shiny-odds-reference.md`.
- **GO Pass: Memories in Motion** — free track + Deluxe ($4.99 standard / $6.99 with +6 Ranks).
- **Pressure Rising Special Research** — season-themed quest leading to Volcanion encounter. **Persistent** — stays in quest log after the season transitions (see `feedback_verify_research_expirations.md`).

### Notable in-season events (selected)

- **Mega Falinks Super Mega Raid Day** — May 23, 2026 (also marks the Mega Energy spend-to-level system going live)
- **Dynamax Registeel debut** — May 18, 2026 (first Steel-type Tier 5 Max Battle)
- **Tapu rotation closed this season** — Tapu Koko (April), Tapu Lele (late April), Tapu Bulu (May 20-26), Tapu Fini (May 27 – June 2)
- **Blanche's Quest for Knowledge** — May 26 – June 1, 2026 (Team Mystic research event)

### GBL cups featured this season

- Catch Cup: Memories in Motion (Great League Edition) — themed cup limiting entries to Pokémon caught during the season
- Plus rotation through GL / UL / ML open formats

### Mega Raid debut pipeline (during MIM)

- Mega Victreebel, Mega Malamar, Mega Dragonite (Kalos Tour Global, Feb 28-Mar 1)
- Mega Mewtwo X, Mega Mewtwo Y (planned for GO Fest Global July 11-12 — debuts STRADDLE the MIM/FF boundary)

---

## Forever Forward (CURRENT — 2026-06-02 to 2026-09-08)

**Season window:** June 2, 2026 at 10:00 AM local → September 8, 2026 at 10:00 AM local.

**Theme:** Future-of-Pokémon-GO + 10-year anniversary celebrations (GO Fest 2026 Global is the centerpiece).

### Daily Discovery rotation (Forever Forward — CHANGES from MIM)

| Day | Bonus | Change from MIM |
|---|---|---|
| Sunday | **Scenic Sunday** — more Pokémon spawn while following a Route; Incense attracts even more on Routes; faster Buddy Candy progress on Routes; encounter Mateo up to 3×/day on Routes | **CHANGED** — Catch-Up Sunday → Scenic Sunday. Routes-focused. |
| Monday | **Max Monday** — Power Spots refresh more frequently; additional Power Spots active; Max Battles 6:00 AM–9:00 PM local rotate featured Dynamax Pokémon | **CHANGED** — Fast-Track Monday REMOVED. Only Max Monday remains. |
| Tuesday | **Expanded Showcase Tuesday** — Trainers can enter up to **5** PokéStop Showcases | **CHANGED** — Showcase Tuesday expanded from 1 entry to 5. |
| Wednesday | Presumed continuation: raid rotation flips at 6:00 AM + featured Raid Hour 6:00–7:00 PM | UNCHANGED (verify on first FF newsletter) |
| Thursday | Presumed continuation: GO Battle Thursday (4× Stardust + 10 sets) | UNCHANGED (verify) |
| Friday | Presumed continuation: Friendship Friday | UNCHANGED (verify) |
| Saturday | Presumed continuation: Spotlight Saturday | UNCHANGED (verify) |

**Note:** Daily Discoveries pause during weeks of global GO Fest, GO Wild Area, and GO Tour events.

### GO Pass: Forever Forward — NEW Major Milestone Bonus tier system

Free track + Deluxe paid version. The NEW feature is persistent rank-tier bonuses that **last until the current GO Pass ends** (not just per-rank one-time rewards):

| Tier | Rank | Persistent Bonus |
|---|---|---|
| Tier 1 | Rank 1 | +1 additional Candy for trading Pokémon |
| Tier 2 | Rank 25 | Increased limits on opening / receiving / storing Gifts |
| Tier 3 | Rank 50 | 2× Daily Adventure Incense duration |
| Tier 4 | Rank 75 | Increased XP and Stardust from hatching Eggs |

### Community Day schedule (Forever Forward)

| Date | Event | Featured |
|---|---|---|
| June 20 | June Community Day | TBA |
| July 4 | July Community Day | TBA |
| August 16 | August Community Day | TBA |

### Notable in-season events (announced)

- **Pokémon GO Fest 2026: Tokyo** — May 29 – June 1, 2026 (in-person ticketed; **straddles MIM/FF boundary** — citywide ticket-holder features active May 25 – June 1)
- **Pokémon GO Fest 2026: Global** — July 11–12, 2026 (FREE for all trainers worldwide; 10-year anniversary)
- **Pokémon GO Fest 2026: Chicago** — June 4–7, 2026 (in-person ticketed)
- **Pokémon GO Fest 2026: Copenhagen** — June 11–14, 2026 (in-person ticketed)

### Mega debut pipeline (during Forever Forward)

- **Mega Mewtwo X and Mega Mewtwo Y** — debut at GO Fest Global (July 11-12). Psychic/Fighting and Psychic respectively.
- **Mega Skarmory** — Super Mega Raid debut during the season (Steel/Flying — date TBA)
- **Mega Raichu X and Mega Raichu Y** — both debut for the first time as Super Mega Raids (date TBA)

### Dynamax debut pipeline (during Forever Forward)

- **Dynamax Electabuzz**
- **Dynamax Magikarp**
- **Dynamax Feebas**
- "More throughout the Season" per Niantic — TBA additions expected.

### Research Breakthrough Encounters (Forever Forward pool)

Dragonite, Axew, Honedge, Jangmo-o, Indeedee, Klawf. All shiny-possible except Klawf (pending Niantic confirmation on Klawf shiny status).

### Egg pool (Forever Forward)

| Tier | Featured |
|---|---|
| 2 km | Exeggcute, Corphish, Wynaut, and more |
| 5 km | Riolu, Mantyke, Flittle, and more |
| 5 km Adventure Sync | Tyrogue, Sableye, Budew, and more |
| 7 km | Alolan Diglett, Galarian Corsola, Galarian Darumaka, and more |
| 7 km from Mateo's Gift Exchange | Hisuian Growlithe, Hisuian Sneasel, White-Striped Form Basculin, and more |
| 10 km | Mawile, Absol, Frigibax, and more |
| 10 km Adventure Sync | Bagon, Druddigon, Drampa, and more |

### GBL cups featured this season

- North American International Championships 2026 Cup
- Fantasy Cup
- Sunshine Cup
- More TBA per Niantic GBL schedule

---

## Upcoming seasons (post-Forever Forward)

No season announced past Forever Forward (September 8, 2026). Update this file when Niantic publishes the next season.

---

**Last verified against Niantic Forever Forward page:** 2026-05-27 (`https://pokemongo.com/en/seasons/forever-forward`)
**Memories in Motion source:** historical, from Spawn Point archive references and `https://pokemongo.com/news/welcome-to-memories-in-motion`
