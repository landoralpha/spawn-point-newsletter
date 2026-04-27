# Spawn Point Newsletter Instructions Redesign — Spec

**Date:** 2026-04-20
**Status:** Draft
**Author:** Joel + Claude (brainstorm session)

---

## Problem Statement

The current newsletter instructions produce drafts with incomplete data, requiring significant manual fact-checking and backfilling after generation. The writing quality pipeline (anti-slop files: phrases.md, structures.md, examples.md, SKILL.md) works well. The sourcing, verification, and data accuracy pipeline does not go far enough, leading to repeated manual corrections for shiny availability, event times, raid rotations, move names, and debut status.

## Goal

Rewrite the Spawn Point newsletter instructions with a three-phase pipeline (Research, Verify, Write) that front-loads all data gathering and verification before any writing begins. Incorporate a source routing table with explicit URL patterns and fallback chains. Restructure the newsletter sections for better reader flow. Keep the existing anti-slop infrastructure intact.

## Target Model

Claude Opus 4.6 (`claude-opus-4-6`) — strongest reasoning and writing judgment for quality-first newsletter work.

---

## Architecture: Three-Phase Pipeline

```
RESEARCH (gather all data)
    | gate: all sections have sourced data or flagged gaps
    v
VERIFY (cross-reference and flag conflicts)
    | gate: all high-risk data points checked against 2+ sources
    v
WRITE (draft the newsletter)
    | gate: anti-slop check, structure check, source citations
    v
DELIVER (draft with flags and attention items)
```

Each phase has a gate. The model cannot proceed to the next phase until the current gate is satisfied. No writing happens until all data is gathered and verified.

---

## Phase 1: Research

### Source Routing Table

Every data type maps to a primary source, URL pattern, fallback, and last resort.

| Data Needed | Primary Source | URL Pattern | Fallback | Last Resort |
|---|---|---|---|---|
| Event calendar/schedule | LeekDuck | `leekduck.com/events/` | Official blog (`pokemongo.com/news`) | Flag inline |
| Raid boss schedule | LeekDuck | `leekduck.com/events/` | pokemongohub.net | Flag inline |
| Raid counters (new boss) | db.pokemongohub.net | `db.pokemongohub.net/pokemon/[pokedexnumber]/counters` | Pokebattler (see URL patterns below) | Pause-and-prompt |
| PvP rankings — Great League | pvpoke.com | `pvpoke.com/rankings/all/1500/overall/[name]/` or `[name_forme_name]/` | db.pokemongohub.net | Pause-and-prompt |
| PvP rankings — Ultra League | pvpoke.com | `pvpoke.com/rankings/all/2500/overall/[name]/` or `[name_forme_name]/` | db.pokemongohub.net | Pause-and-prompt |
| PvP rankings — Master League | pvpoke.com | `pvpoke.com/rankings/all/10000/overall/[name]/` or `[name_forme_name]/` | db.pokemongohub.net | Pause-and-prompt |
| Max Battle tier lists — Attack | pokemongohub.net | `pokemongohub.net/post/guide/max-attackers-tier-list/` | pokebase.app (overall only) | Pause-and-prompt |
| Max Battle tier lists — Defense | pokemongohub.net | `pokemongohub.net/post/guide/max-defenders-tier-list/` | pokebase.app (overall only) | Pause-and-prompt |
| Max Battle tier lists — Healers | pokemongohub.net | `pokemongohub.net/post/guide/max-healers-tier-list-june-2025/` (if 404, search `site:pokemongohub.net max healers tier list` for updated URL) | pokebase.app (overall only) | Pause-and-prompt |
| Dynamax overall rankings | pokebase.app | `pokebase.app/pokemon-go/tier-lists/dynamax-tier-list` | pokemongohub.net tier lists | Flag inline |
| Max Monday schedule | LeekDuck | `leekduck.com/events/` | pokemongohub.net | Flag inline |
| Shiny availability | db.pokemongohub.net | `db.pokemongohub.net/pokemon/[pokedexnumber]` | LeekDuck shiny checklist | Flag inline |
| CP charts / hundo values | db.pokemongohub.net | `db.pokemongohub.net/pokemon/[pokedexnumber]` | pokebattler.com | Flag inline |
| GBL rotation schedule | LeekDuck | `leekduck.com/events/` | Official blog | Flag inline |

### db.pokemongohub.net URL Patterns

| Form Type | URL Pattern | Example |
|---|---|---|
| Standard | `db.pokemongohub.net/pokemon/[pokedexnumber]` | `/pokemon/383` (Groudon) |
| Standard counters | `db.pokemongohub.net/pokemon/[pokedexnumber]/counters` | `/pokemon/383/counters` |
| Gigantamax | `db.pokemongohub.net/pokemon/[pokedexnumber]-Gigantamax` | `/pokemon/6-Gigantamax` (Charizard) |
| Shadow | `db.pokemongohub.net/pokemon/[pokedexnumber]-Shadow` | `/pokemon/381-Shadow` (Latios) |
| Alternate forme | `db.pokemongohub.net/pokemon/[pokedexnumber]-[FormeName]` | `/pokemon/999-Chest` (Gimmighoul), `/pokemon/999-Roaming` |

Counters page: append `/counters` to any of the above (e.g., `/pokemon/381-Shadow/counters`).

### Pokebattler URL Patterns

All Pokebattler URLs share a common base and query string:

**Base:** `https://www.pokebattler.com/raids/defenders/`
**Query string (appended after the path):** `?sort=ESTIMATOR&weatherCondition=NO_WEATHER&dodgeStrategy=DODGE_REACTION_TIME&aggregation=AVERAGE&includeLegendary=true&includeShadow=true&includeMegas=true&attackerTypes=POKEMON_TYPE_ALL&primalAssistants=&numParty=1`

| Raid Type | Path Pattern | Example |
|---|---|---|
| Five-Star | `NAME/levels/RAID_LEVEL_5/attackers/levels/40/strategies/CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC` | `GROUDON/levels/RAID_LEVEL_5/...` |
| Five-Star (alternate forme) | `NAME_FORME_FORM/levels/RAID_LEVEL_5/...` | `KYUREM_BLACK_FORM/levels/RAID_LEVEL_5/...` |
| Five-Star (crowned forme) | `NAME_CROWNED_DESCRIPTOR_FORM/levels/RAID_LEVEL_5/...` | `ZAMAZENTA_CROWNED_SHIELD_FORM/levels/RAID_LEVEL_5/...` |
| Shadow | `NAME_SHADOW_FORM/levels/RAID_LEVEL_5_SHADOW/...` | `LATIOS_SHADOW_FORM/levels/RAID_LEVEL_5_SHADOW/...` |
| Mega | `NAME_MEGA/levels/RAID_LEVEL_MEGA/...` | `ALAKAZAM_MEGA/levels/RAID_LEVEL_MEGA/...` |
| Gigantamax | `NAME_GIGANTAMAX/levels/RAID_LEVEL_6_MAX/...` | `BLASTOISE_GIGANTAMAX/levels/RAID_LEVEL_6_MAX/...` |

**Naming convention:** Pokebattler uses ALL_CAPS with underscores. Forme names follow `NAME_FORMENAME_FORM`. Crowned formes include the full descriptor (e.g., `ZAMAZENTA_CROWNED_SHIELD_FORM`).

### pvpoke.com URL Patterns

| League | URL Pattern |
|---|---|
| Great League (1500 CP) | `pvpoke.com/rankings/all/1500/overall/[name]/` or `pvpoke.com/rankings/all/1500/overall/[name_forme_name]/` |
| Ultra League (2500 CP) | `pvpoke.com/rankings/all/2500/overall/[name]/` or `pvpoke.com/rankings/all/2500/overall/[name_forme_name]/` |
| Master League (10000 CP) | `pvpoke.com/rankings/all/10000/overall/[name]/` or `pvpoke.com/rankings/all/10000/overall/[name_forme_name]/` |

### Raid Counter Depth

When a new raid boss rotates in during the newsletter week:
- Pull top 3-5 counters with fast and charged move names
- Include 2-3 budget-friendly alternatives for newer players
- Format as a short list, not a table
- Only pull fresh counter data for new rotations, not continuing bosses

### Routing Flow

```
Need data → Check primary source URL
    |
    v
Primary returns data? → YES → Use it
    |
    NO
    v
Check fallback source URL
    |
    v
Fallback returns data? → YES → Use it
    |
    NO
    v
Last resort = "Flag inline"? → Flag: [UNCONFIRMED: ...]
Last resort = "Pause-and-prompt"? → Stop drafting, prompt Joel with what's missing and where you looked
```

### Research Steps (in order)

1. **Broad weekly overview** — search for all events in the newsletter date range using multiple sources. Start with LeekDuck events calendar and official Pokémon GO blog.
2. **Event details** — for each event found, fetch the official announcement. Cross-reference with community sources.
3. **Raid boss rotation** — check if any raid bosses (Five-Star, Mega, Shadow) rotate during the week. If a new boss rotates in, pull counter data using the routing table.
4. **GBL rotation** — check what leagues and cups are active or rotating during the week.
5. **Max Monday** — check LeekDuck for the featured Dynamax Pokémon.
6. **Weekly bonuses** — confirm Daily Discoveries schedule (recurring, but verify no changes).
7. **Don't Miss research** — actively search Reddit, content creators, and community sources for tools, meta shifts, and community discoveries (see Don't Miss section below).

### Research Gate

All sections have sourced data or flagged gaps. No section is left empty without an inline flag explaining what's missing and where to look.

---

## Phase 2: Verify

After all data is gathered, run a dedicated verification pass before writing.

### High-Risk Data Points Checklist

Each must be confirmed against 2+ sources:

| Data Point | What to verify | Sources to cross-check |
|---|---|---|
| Shiny availability | Can this Pokémon be shiny in GO right now? | db.pokemongohub.net + LeekDuck shiny checklist |
| Event start/end times | Exact times in local time, no timezone conversion | Official announcement + LeekDuck |
| Raid boss rotation dates | When does current boss leave, when does new boss start? | LeekDuck + official blog + pokemongohub.net |
| Move names/movesets | Correct fast/charged move names for counters and PvP | db.pokemongohub.net + pvpoke.com |
| Debut status | Is this Pokémon appearing in GO for the first time, or returning? | Official announcement + LeekDuck + db.pokemongohub.net |
| Raid counter accuracy | Are these still the current top counters? | db.pokemongohub.net + pokebattler.com |

### Verification Rules

- **Two sources agree** — data is verified, proceed
- **Sources conflict** — check official Pokémon GO announcement as tiebreaker
- **Official doesn't cover it** — flag inline: `[UNCONFIRMED: Source A says X, Source B says Y — verify before publishing]`
- **Data not posted yet** — flag inline: `[NOT YET ANNOUNCED: Check [source URL] closer to publication]`
- **Wider net** — after checking established sources, search `"Pokémon GO [event/boss name] [month] [year]"` and check r/TheSilphRoad and @PokémonGoApp on X for last-minute changes, corrections, or details the primary sources haven't updated yet

### Verify Gate

Every high-risk data point is either verified or flagged. No unverified data enters the draft without a visible flag.

---

## Phase 3: Write

### Lead Options (Present First)

Before drafting the full newsletter, present:
- **5 title options** — each reflecting the week's biggest theme from a different angle
- **5 subtitle options** — can mix and match with any title
- **5 opening paragraph options** — each leading with a different priority or framing

Present all options together. Joel picks or requests revisions. The model drafts the remaining sections only after the title/subtitle/opening combination is selected.

### Newsletter Structure (10 Sections)

#### 1. Title + Date Range
Creative, memorable title reflecting the week's biggest event or theme.

**Format:**
```
Spawn Point: [Creative Title]
[Start Date]-[End Date], [Year]
```

**Guidelines:**
- 3-7 words
- Reference the week's biggest event, theme, or holiday
- Can be playful, punny, or thematic

#### 2. Subtitle
Fun, creative subtitle expanding on the title or highlighting what makes the week special.

**Guidelines:**
- 8-15 words
- Reference specific Pokémon, events, or activities when possible
- Match the energy of the week

#### 3. Opening Paragraph
Sets the tone and emotional priority. Answers: what should Trainers care about most, and why?

**Guidelines:**
- 3 sentences max
- Lead with the most important thing happening this week
- Name the key Pokémon, event, or deadline
- Do NOT repeat times, dates, or bullet-point details (those go in Week at a Glance)
- Do NOT start with a generic greeting
- If it reads like a table of contents, rewrite it

#### 4. Week at a Glance
Bullet-point planning reference. Calendar specifics the opening paragraph left out.

**Guidelines:**
- 4-6 bullets max
- Each bullet: one event, rotation, deadline, or feature
- Include key time or date
- Complementary to the opening paragraph, never overlapping
- Format: `[emoji] **[Label]** — [one-line with time/date]`

#### 5. Events
Special/limited-time events in chronological order (Monday through Sunday).

**Includes:** Themed events, Community Day, limited-time events, seasonal launches, debut events
**Excludes:** Max Monday, Weekly Bonuses, Raid Bosses, GBL (each has its own section)

**Per event:**
- Event name with one emoji
- Start and end dates/times (local time, no timezone conversion)
- 1-2 paragraphs explaining what's happening
- Trainer Tip (1-2 sentences, strategic value only)

#### 6. Raid Bosses + Counters
Five-Star, Mega, and Shadow raids only. No one-star or three-star.

**When raids rotate mid-week:**
```
**Five-Star Raids:**
[Current boss] stays through [day/time]. [Brief description]

**Rotating In [day/time]:** [New boss] arrives. [Description + counter breakdown]
```

**Counter breakdown (new rotations only):**
- Top 3-5 counters with fast/charged moves
- 2-3 budget-friendly alternatives for newer players
- Formatted as a short list

**Continuing bosses:** Brief note, no counter refresh.

**Mega raid note:** Trainers catch the standard (non-Mega) form after defeating a Mega Raid boss. Include hundo CP when available.

**Shadow raids:** Note full duration (typically month-long). Shadow raids are available throughout the week, not just weekends.

**Trainer Tip:** Strategic insight (PvP/PvE investment value, optimal timing, type advantages).

**Max Battle mechanics (never get these wrong):**
- Mega Pokémon CANNOT boost ally attacks in Max Battles (only in standard Raids)
- Eternatus' Dynamax Cannon adds bonus damage in Max Battles
- Crowned Forme Zacian's Behemoth Blade strengthens attack in Raids and Max Battles
- Crowned Forme Zamazenta's Behemoth Bash strengthens defense in Raids and Max Battles

#### 7. GBL / PvP
Weekly league rotation and cup format.

**Includes:**
- What leagues/cups are active this week
- Rotation date if it changes mid-week
- One quick meta note when relevant (e.g., a featured event Pokémon that's strong in the current cup)

**Guidelines:**
- Keep it brief unless a major rotation or new cup warrants more detail
- Link to pvpoke.com for deeper meta analysis when relevant

#### 8. Max Monday
Featured Dynamax Pokémon for the week.

**Schedule:** 6:00 AM to 9:00 PM local time. Power Spots refresh more frequently with additional Power Spots active. Note that Power Spot availability is limited outside of Max Monday and Max Battle Day windows.

**Per Max Monday:**
- Featured Dynamax Pokémon, difficulty tier, shiny availability
- Type weaknesses
- Whether it's a debut or continuation
- Trainer Tip if strategic value exists

**Primary source:** LeekDuck

#### 9. Weekly Bonuses
Recurring daily bonuses. Renamed from "Daily Discoveries" for reader clarity.

**Schedule:**
- **Sunday:** Double-Time Sunday (Incense/Lures last 2x as long)
- **Monday:** Fast-Track Monday (2x GO Points from Pass Tasks)
- **Tuesday:** Showcase Tuesday (PokeStop Showcases)
- **Wednesday:** Raid Hour 6:00-7:00 PM (covered in Raid Bosses section, just reference it here)
- **Thursday:** GO Battle Thursday (4x Stardust from wins, 10 battle sets)
- **Friday:** Friendship Friday (2 Special Trades, increased Lucky chance, reduced Stardust cost, 2 guaranteed Candy XL)

**Guidelines:**
- Brief (1-2 sentences each)
- Focus on high-impact days (Friendship Friday, GO Battle Thursday, Double-Time Sunday)
- Skip or briefly mention lower-impact days (Showcase Tuesday, Fast-Track Monday)

#### 10. Don't Miss
Three callouts surfacing things NOT covered elsewhere in the newsletter.

**Content categories (pick 3 total, at least 2 categories represented):**

| Category | What to look for | Where to search |
|---|---|---|
| Tools & Resources | Apps, websites, trackers, IV calculators, infographics the community is using | Reddit (r/TheSilphRoad, r/PokémonGO), X/Twitter creators, LeekDuck tools |
| Meta & Strategy | Rising/falling PvP picks, underrated raid attackers, niche builds, move update impacts | pvpoke.com meta, GO Hub analysis, content creators |
| Community & Upcoming | Leaked/teased events, community discoveries, QoL changes in updates, datamine highlights | Pokeminers, r/TheSilphRoad, content creators, official social accounts |

**Research instructions:**
- Do NOT write from leftover event info — must be genuinely new content
- Search Reddit for top posts from the past 7 days
- Check content creators' recent posts
- Search for timely-but-not-event-tied content
- Every callout links to a source

**Flag behavior:** If fewer than 3 strong callouts found, flag: `[DON'T MISS: Only found [X] strong callouts — need [Y] more. Suggested search: [specific query]]`

**Format:**
```
**[emoji] [Short label]**
One or two sentences. [Link text](URL)
```

### Source Citations

At the end of each section, list sources used:
*Sources: [source name](URL) | [source name](URL)*

### Writing Style

- **Reading level:** 5th grade (simple words, short sentences)
- **Tone:** Conversational but tight. Short paragraphs, personality without fluff. Expand where the content warrants it.
- **Emojis:** One emoji per event title only
- **Format:** Sentences and short paragraphs (2 max per event), not bullet points (except Week at a Glance and Weekly Bonuses)
- **Length:** Readable in 3-5 minutes
- **Punctuation:** Never use em dashes. Use periods, commas, or parentheses.
- **Times:** Always local time as found in source data. Never convert time zones.
- **Shiny phrasing:** "with a chance to be shiny" (not "shiny available")
- **Acronyms:** Explain on first use (e.g., "Great League (GBL)")
- **Audience:** Casual and hardcore Trainers both

### Anti-Slop Infrastructure

Cross-reference all prose against existing project files before finalizing:
- **phrases.md** — throat-clearing openers, emphasis crutches, jargon, adverbs, vague declaratives
- **structures.md** — binary contrasts, negative listings, dramatic fragmentation, false agency, passive voice
- **examples.md** — before/after rewrites
- **SKILL.md** — master checklist and scoring (Directness, Rhythm, Trust, Authenticity, Density — must hit 35/50)

**Newsletter-specific tells:**
1. False agency: "The event brings double Stardust" — rewrite as "You earn double Stardust during the event"
2. Repetitive openers: "Trainers can catch... Trainers can earn..." — vary subjects

### Quality Gates (Run Before Delivery)

**Gate 1: Anti-slop** — Run SKILL.md Quick Checks. Score on five dimensions. Rewrite anything below 35/50.

**Gate 2: Accuracy** — Confirm every date, time, and Pokémon name was verified in Phase 2. Confirm all inline flags are still present.

**Gate 3: Structure** — No duplication across sections. Opening paragraph and Week at a Glance are complementary. Don't Miss is genuinely new. Trainer Tips add strategic value.

**Gate 4: Tone and length** — Conversational, no filler, no hype. Sections appropriately sized. Full newsletter 3-5 minutes. Counters include budget alternatives.

### Delivery Format

Draft delivered with:
- All `[UNCONFIRMED]` and `[NOT YET ANNOUNCED]` flags visible
- Source citations at the end of each section
- Summary at the top listing items needing Joel's attention (unconfirmed data, missing sources, pause-and-prompt items)

---

## Information Sources

### Official Sources
- Pokémon GO official website & Niantic blog (`pokemongo.com/news`)
- @PokémonGoApp on X
- @NianticHelp on X

### Community/Data Sources
- LeekDuck (`leekduck.com`) — events, raid schedule, Max Monday, shiny checklist
- Pokémon GO Hub (`pokemongohub.net`) — news, analysis, tier lists
- Pokémon GO Hub Database (`db.pokemongohub.net`) — counters, CP charts, PvP tiers, moves, shiny status
- PvPoke (`pvpoke.com`) — PvP rankings and movesets
- Pokebattler (`pokebattler.com`) — raid counter simulations
- PokeBase (`pokebase.app`) — overall Dynamax rankings
- Serebii.net — Pokémon GO section
- r/TheSilphRoad (Reddit)
- r/PokémonGO (Reddit)
- Pokeminers — datamines and leaks

### Content Creators
- LeekDuck, FlareBlazeArt, G47ix, ShinyHundo, PKMNLens, PogoHub, landoralpha, Dittobase

---

## Out of Scope

- Changes to anti-slop files (phrases.md, structures.md, examples.md, SKILL.md) — these work as-is
- Beehiiv template/formatting — this spec covers content instructions only
- Automation or scheduling of the newsletter generation
