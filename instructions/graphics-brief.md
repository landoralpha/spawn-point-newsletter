# Spawn Point — Graphics Brief

Card specs for the embedded graphics that absorb reference data and let prose hit the 1,400–1,800 word target. Wired into `instructions/newsletter-creation.md` Section 6 (Raid Bosses) today; other sections aspirationally.

**Source of truth**: Joe generates these cards. The newsletter agent's job is to provide a brief specifying which datapoints the card must carry, then write the prose around the embedded image. If a graphic is missing or pipeline-blocked, the agent falls back to text-only mode per each section's text-only cap.

## Status (2026-06-15)

| Card type | Status | Use today? |
|---|---|---|
| **Raid card** | ✅ ACTIVE | YES — generate for every featured raid boss |
| Event card | 🚧 Future / aspirational | NO — Events stay text-only |
| GBL cup card | 🚧 Future / aspirational | NO — GBL stays text-only |
| Max Battle card | 🚧 Future / aspirational | NO — Max Monday stays text-only |
| Hundo CP strip | 🚧 Future / aspirational | NO — Provenance Table stays at bottom |

**Only raid cards are generated today.** Joe might add the others later. Until then, the per-section caps in `newsletter-creation.md` for Events, GBL, Max Monday, and the Hundo CP Provenance Table operate in text-only mode. Drafting agents should NOT brief or assume Event/Cup/Max/Strip cards exist — Card Types 2–5 in this doc are SPEC-ONLY, kept here so the format is ready when those pipelines come online.

## Brand context

- Brand palette, typography, and visual rules: `/Users/joelandor/Claude-Master/landoralpha-brand-deck`
- Mark: Segmented Arch (PNG in Alpha Logo Marks/) — see `reference_landoralpha_mark_files.md`
- Sprite source for Mega/Primal HOME sprites: `public/sprites/home/{normal,shiny}/{dex}.m.png` via `scripts/normalize-mega-sprites.mjs`

---

## Card Type 1: Raid Card

**Used for**: every featured raid boss (Five-Star, Mega, Super Mega, Shadow) in Section 6.

**Required datapoints on the card:**
1. **Boss name** + form designator (e.g., "Mega Skarmory", "Shadow Dialga")
2. **Sprite** (HOME-style; Mega/Primal use the Mega sprite, Shadow uses the Shadow purple flame outline)
3. **Typing chips** (1 or 2 type chips, in Niantic in-game order — primary first)
4. **Weakness chips** with multipliers (e.g., "Fire 1.6×", "Electric 1.6×"; double-weak shown as "2.56×")
5. **Top 5 Premium counters** with movesets, one line each
6. **Top 5 Budget counters** with movesets, one line each
7. **Hundo CPs** (L20 + L25 + weather boost types) — labeled
8. **Active window** (start date → end date, "Wed Jun 17 – Tue Jun 23")
9. **Raid tier badge** ("5-Star", "Mega", "Super Mega" [requires 7 in-person], "Shadow 5-Star")

**Optional callouts (when relevant):**
- "Shiny eligible" badge
- "Elite TM legacy move required" flag on counter entries
- "First Mega Level pre-unlocked" callout (for GO Fest-style debut catches)

**What to OMIT** (keep visual density readable):
- Movepool beyond top counter movesets — Hub-DB has it, link out
- IV distribution chart
- DPS bar charts

**Alt text requirement**: `[Boss name] raid card — [typing], weak to [weakness list], top counter [#1 counter name]. Hundo at L20: [value], at L25 weather-boosted: [value].`

### Agent brief format (what the writer hands Joe for each raid card)

```
Raid card brief — [Boss name] [Active window]
  Sprite slot: {normal | shiny | mega | shadow | primal}
  Typing: [primary] / [secondary or none]
  Weaknesses (with multipliers): [Type 1] 1.6×, [Type 2] 1.6×, [Type 3] 2.56× (if double-weak), ...
  Hundo L20: [value]
  Hundo L25 (weather): [value] ([weather list])
  Premium counters (top 5, one moveset each):
    1. [Counter] — [fast move] / [charged move] [legacy flag if any]
    ...
  Budget counters (top 5, one moveset each, no exclusive moves):
    1. [Counter] — [fast move] / [charged move]
    ...
  Special badges: [shiny eligible, in-person only, ticket required, ...]
```

---

---

# FUTURE CARD TYPES (NOT YET AVAILABLE — spec only)

The card types below are documented so the format is ready when each pipeline comes online. Until each is marked ✅ ACTIVE in the Status table above, **drafting agents must NOT brief these cards or assume they'll be embedded.** Sections that would use them stay in text-only mode per `newsletter-creation.md` Word-Count Budget.

## Card Type 2: Event Card 🚧

**Used for**: heavy event sections (Section 5 Events) that previously ate 400–700 words spelling out spawn lists, raid pools, GO Pass tiers, and bonus ladders. Replaces #18-style Copenhagen / Candela's Quest deep dives.

**Required datapoints on the card:**
1. **Event name** + window (e.g., "Flying Taxi — June 23–29")
2. **Wild spawn chips** (sprite icons or names; group by "Featured" vs "Regional" vs "Rare")
3. **Raid pool by tier** (1-Star / 3-Star / 5-Star icons + bosses)
4. **Field Research encounter pool** (small chip row)
5. **GO Pass tiers** (free milestones + Deluxe price + Deluxe + N Ranks price)
6. **Bonus ladder** (Tier 1 + Tier 2 bonuses with icons)
7. **Costumed encounter** flag if any
8. **Shiny eligibility** indicators per row

**Optional callouts:**
- "Ticket required" badge for paid in-person events
- "Remote-eligible" callout when the event includes Remote-friendly content
- LEGO collab / sponsor callouts (Copenhagen-style)

**Alt text requirement**: `[Event name] event card — [window]. Featured spawns include [top 3]. Key raids: [top 3]. GO Pass: free + Deluxe $X.XX.`

---

## Card Type 3: GBL Cup Card 🚧

**Used for**: Section 7 GO Battle League, specifically type-restricted cups (Sunshine Cup, NAIC Cup, themed cups).

**Required datapoints on the card:**
1. **Cup name** + CP cap
2. **Eligible types** (chip row)
3. **Banned Pokémon** (if any)
4. **Top 10 PvPoke picks** (sprite row with rank numbers)
5. **Active window** (start → end)

**Optional callouts:**
- "Move-eligible exception" notes (e.g., "Alolan Marowak via Fire secondary typing")

**Alt text requirement**: `[Cup name] card — [CP cap], [eligible types]. Top pick [Rank 1 name].`

---

## Card Type 4: Max Battle Card 🚧

**Used for**: Section 8 Max Monday + any in-week Max Battle feature.

**Required datapoints on the card:**
1. **Featured Dynamax Pokémon** + sprite
2. **Typing chips**
3. **Weakness chips** with multipliers
4. **Top Max Battle attackers** (top 5, Dynamax-capable only — Shadow Pokémon NEVER appear here)
5. **Hundo CPs** (L20 + L25 + weather)
6. **Window** (date + 6:00 AM – 9:00 PM local)
7. **Rare Candy XL callout** for in-person Monday Max Battles

**What to OMIT:**
- PvP usage notes (Max Battle ≠ PvP)
- Non-Dynamax counter suggestions

**Alt text requirement**: `[Featured Pokémon] Max Battle card — [typing], weak to [weakness], top Dynamax counter [#1].`

---

## Card Type 5: Hundo CP Quick-Reference Strip 🚧

**Used for**: the Hundo CP Provenance Table currently sitting at the bottom of every issue (which almost no reader scrolls to). Converts the table to a single visual strip pinned beneath the Week at a Glance.

**Required datapoints on the strip:**
1. Every featured raid / Max Battle / Community Day Pokémon for the week
2. L20 hundo + L25 hundo with weather flag
3. Sprite per row

**Layout**: horizontal scroll on mobile, full-width grid on desktop.

**Why this matters**: the Provenance Table is the highest-effort, lowest-engagement section. Visualizing it makes the data actually useful at screen-check time (when readers post-raid CP-check), AND removes ~200 words from every issue.

---

## Pipeline notes (agent side)

1. **When drafting**, the agent assembles each section's prose AS IF the graphic is embedded — text retains only the "why it matters" + Hundo CP line + Trainer Tip + Sources, per Section 6.
2. **The agent's research brief** (the Notion sub-page that recon reads) includes a "Graphics Briefs" block listing one brief per card type required for the week. Joe consumes the briefs, generates the cards, drops them in.
3. **Fallback rule**: if a card is missing at recon time, recon flags it under a new Category L-2 ("missing required graphic — switch to text-only mode for that section AND extend word budget ceiling by the section's text-only delta"). Recon does NOT block publish on missing graphic, but does flag the gap.
4. **Embed location**: each card sits immediately AFTER the section's H2/H3 header and BEFORE the prose. Reader sees the visual first, then the editorial framing.

---

## Per-issue graphics shopping list

**Today (raid cards only):**

| Card type | Count per issue | Always required? |
|---|---|---|
| Raid card | 3–4 (Five-Star, Mega, Super Mega, Shadow) | YES for each featured boss |

That's **3–4 cards per issue** today. The drafting agent only briefs raid cards.

**Future (when other pipelines come online):**

| Card type | Count per issue | Always required? |
|---|---|---|
| Event card | 1–3 (per major event sub-section) | Yes when an event has spawn/research/GO Pass data |
| GBL cup card | 0–1 (only for type-restricted cups) | No (skip for open rotations) |
| Max Battle card | 1 (Max Monday) | Yes |
| Hundo CP strip | 1 (under Week at a Glance) | Yes |

Once those become ACTIVE, the per-issue mix grows to **6–10 cards per issue** total.

---

## Versioning

Initial spec drafted 2026-06-15 by the newsletter agent after Joe's word-count audit. Update this brief when:
- A new card type is introduced (e.g., Special Research story-arc tracker)
- A datapoint requirement changes (e.g., new Niantic format adds a field)
- A card type is retired because its data moved elsewhere
