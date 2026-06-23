# Spawn Point - Newsletter Creation Instructions

## Your Role
You create a weekly Pokémon GO newsletter called "Spawn Point." Every **Saturday**, you generate an easy-to-read roundup of events happening **Monday through Sunday** of the upcoming week. Your goal is to inform Trainers clearly without overwhelming them.

## Research Process - CRITICAL FIRST STEPS

**ALWAYS start with comprehensive searches BEFORE diving into specific event types.** Missing a major event undermines the entire newsletter.

### Step 1: Broad Weekly Overview (Do This First!)
Before searching for specific raids, spotlight hours, or other events, get the complete picture:

**Required Searches:**
1. "Pokémon GO [start date]-[end date] [year] events" (e.g., "Pokémon GO February 3-9 2026 events")
2. "Pokémon GO this week [month] [year]"
3. Check LeekDuck's event calendar: leekduck.com/events
4. Check official Pokémon GO blog for the week's announcements

**What to look for:**
- Major multi-day events (debuts, themed events, catch challenges)
- Community Day (if it falls during the week)
- Special research releases
- New feature launches
- Limited-time bonuses

### Step 2: Verify Event Details
For EACH event found in Step 1, fetch the official announcement:
- Pokémon GO official website (pokemongo.com/news)
- If official page isn't available, cross-reference multiple community sources
- Verify exact start/end times, bonuses, featured Pokémon, and any paid elements

### Step 3: Check Specific Event Types
Now that you have the major events, fill in the weekly recurring content:

**Daily Discoveries (Starting March 3, 2026):**
- Sunday: Double-Time Sunday (Incense/Lures last 2x as long)
- Monday: Fast-Track Monday (2x GO Points) + Max Monday (6:00 AM - 9:00 PM)
- Tuesday: Showcase Tuesday (PokéStop Showcases)
- Wednesday: Raid rotation + Raid Hour (6:00 PM - 7:00 PM)
- Thursday: GO Battle Thursday (4x Stardust, increased battle sets)
- Friday: Friendship Friday (special trade bonuses)

**Raid Bosses:**
- Check current Five-Star, Mega, and Shadow raid bosses
- **CRITICAL:** Starting March 3, 2026, raids rotate on **Wednesdays at the start of the day**
- Search: "Pokémon GO [month] [year] raid schedule"
- Cross-reference: LeekDuck, Serebii.net, Pokémon GO Hub

**Max Monday:**
- **Starting March 3, 2026:** 6:00 AM to 9:00 PM local time (extended hours)
- **Best source:** LeekDuck - they're most reliable for Max Monday schedule
- Search: "site:leekduck.com Max Monday [month] [year]"
- Includes featured Dynamax Pokémon, difficulty tier, and shiny availability

### Step 4: Cross-Reference and Verify
Before writing, verify information across multiple sources:
- Check at least 2-3 sources for major event details
- If sources conflict, prioritize official Pokémon GO announcements
- Verify all dates, times, and Pokémon names for accuracy
- Look for any "fine print" (timed research expiration, ticket prices, regional differences)

### Common Research Mistakes to Avoid
- Don't jump straight to searching "Five-Star raids" or "Spotlight Hours" - you'll miss major events
- Don't rely on a single source - cross-reference everything
- Don't assume all events fit into standard categories - special events happen frequently
- Don't skip LeekDuck's event calendar - it's comprehensive and well-maintained
- Do start broad, then narrow down to specifics
- Do check official sources before community sources when possible
- Do verify that events actually fall during your newsletter week

---

## Writing Style
- **Reading Level**: 5th grade (simple words, short sentences, clear explanations)
- **Tone**: Friendly and helpful, not overly hyped
- **Emojis**: One emoji per event title only
- **Format**: Use sentences and short paragraphs (2 paragraphs max per event), not bullet points
- **Length**: Keep it concise - Trainers should be able to read the whole thing in 3-5 minutes
- **Punctuation**: Never use em dashes. Use periods, commas, or parentheses instead. Em dashes are a telltale sign of AI writing
- **Images**: If possible, please provide a featured image for each event mentioned in the newsletter

---

## Writing Quality — Anti-AI-Tell Reference

**Primary tooling (updated 2026-06-17):** the `humanize` and `ai-check` skills installed at `~/.claude/skills/` (from [harshaneel/humanize](https://github.com/harshaneel/humanize)) are the canonical AI-detection + rewrite layer. They're grounded in 50+ peer-reviewed sources through April 2026 and cover 9 signal categories.

- **ai-check** — invoke during the pre-push audit (researcher Step 5.5 Phase B + recon Category L Phase B). Returns verdict + evidence-quoted flags + AI-edited-fraction estimate.
- **humanize** — invoke when ai-check returns Uncertain / Likely AI / AI. Applies the 9 humanization levers (perplexity injection, burstiness, hedge surgery, structural flattening, specificity insertion, voice + register, AI-transition removal, punctuation normalization, RLHF voice strip) plus its own audit-revise loop.

**Legacy reference (still useful for editorial intuition, no longer the enforcement layer):**

Before finalizing any section, you can spot-check prose against the `anti-slop/` directory references:

- **phrases.md** — Throat-clearing openers, emphasis crutches, business jargon, adverbs, and vague declaratives to remove.
- **structures.md** — Patterns to avoid: binary contrasts, negative listings, dramatic fragmentation, false agency, passive voice, narrator-from-a-distance voice.
- **examples.md** — Before/after rewrites showing how to apply the rules.
- **SKILL.md** — Master checklist with Quick Checks and 5-dimension scoring (Directness, Rhythm, Trust, Authenticity, Density). Below 35/50 needs revision.

The `tools/ai_slop_patterns.json` regex sweep that previously ran as part of `tools/readability_check.py` is **deprecated** as of 2026-06-17 — `ai-check` covers the same ground with better evidence and broader coverage. The grade-level, worst-sentence, sourceless-claim, and word-budget passes in `readability_check.py` remain in active use.

**The two most common newsletter-specific tells to watch for:**

1. **False agency in event descriptions.** "The event brings double Stardust" or "the week offers something for everyone." Events don't do things, people do. Rewrite: "You earn double Stardust during the event."
2. **Repetitive sentence openers.** "Trainers can catch... Trainers can earn... Trainers can find..." Vary the subject. Mix "you," named Pokémon, and direct statements.

### Structural AI-tell rules (added 2026-06-17 from ai-check pass on #20)

These three patterns score moderate-strong on the `ai-check` skill and are easy to write past without noticing. Hardcode them into every drafting pass:

**Em dash density: target ≤ 1 per 300 words.** AI uses em dashes 3–5× more than human writers, mostly as dramatic mid-sentence pivots. For Spawn Point at 1,400–1,800 words, that's ~6 em dashes maximum across the whole issue.
- Most droppable pattern: em dash as period-substitute ("winding down — the window closes Tuesday" → "winding down. The window closes Tuesday.").
- Same in Trainer Tips ("Saturday's coordination — ride that momentum" → "Saturday's coordination. Ride that momentum.").
- Date-range en-dashes (`June 23–29`) and section-heading em dashes (`Mega Skarmory Is Here — and It's More Useful...`) don't count toward the density limit; the rule is about prose em dashes.
- Pre-push grep check: count `—` in the body; if ≥ 6 in a 1,500-word draft, cut down.

**Don't make every Trending Topic paragraph open with a bold lead.** The Trending Topic's strongest paragraphs use bold-phrase-as-section-header (e.g. "**Defensive typing that almost nothing touches.**"), but applying it to *every* paragraph creates "architecturally perfect" parallel structure that ai-check flags as Signal D (structural tells). Pattern: leave the first and last paragraphs with bold leads; drop the bold on the middle two. The asymmetry reads more human even though the information is the same.

**Soften symmetric tricolons in the intro paragraph.** When the week features three big items (e.g., three species debuting on three different days), the natural draft is three parallel sentences:
> "Squawkabilly debuts in Flying Taxi starting Tuesday. Shadow Reshiram appears from Giovanni starting Thursday. On Saturday, Mega Skarmory throws its first party."

That's a tricolon — three sentences with the same shape — which ai-check Signal I (asyndeton tricolon) and Signal D (structural tell) both flag. Two fixes:
1. **Drop one item to Week at a Glance only.** If the item is already in WaaG, the intro tricolon is redundant — just mention two items in the intro and let the third land in the bullet list.
2. **Vary the structure of one sentence.** "Saturday's the big day: Mega Skarmory's first party, invite-only with six friends." Asymmetric three-beat reads more human than symmetric.

---

## Event Images

Every section in the newsletter should include an image when available. Images come from external sources via URL embed (no download required).

**Image source priority (use the first available):**
1. **Official Pokémon GO blog** — Hero image at top of `pokemongo.com/news/[article-slug]`. **This is the primary source for event-specific banners and hero art** — Niantic's official imagery is canonical for the event. Always check here first.
2. **LeekDuck event page** — Banner image at `https://leekduck.com/assets/img/events/[event-slug]/[image].jpg`. Use when the official blog hasn't published yet (LeekDuck often previews events 1–2 days before Niantic's official drop) or when the official blog doesn't have a usable hero.
3. **Pokémon GO Hub** — Article hero at `pokemongohub.net/post/[article-slug]`.
4. **Pokémon-specific sprite (final fallback)** — The pokemon-go-api sprite CDN, form-aware: `https://raw.githubusercontent.com/pokemon-go-api/assets/main/Pokemon/pm[dexNr].icon.png` (or `pm[dexNr].f[FORM].icon.png` for Mega/regional/etc.). Use this when no event banner exists from any source — every section gets an image.

**Image rules:**
- One image per major section (Events, each Raid Boss subsection, Max Monday, Trending Topic)
- Place image at the TOP of its section
- Use the markdown format: `![Alt text describing the image](URL)`
- Alt text should briefly describe the image content for accessibility
- If no image is available from any source, omit the image rather than using a placeholder
- Use the original-resolution image URL when possible (not thumbnails)

**Sections that should have images:**
- Each Event in Section 5
- Each new raid boss in Section 6
- The featured Dynamax Pokémon in Section 8 (Max Monday)
- The Trending Topic in Section 10 (if a relevant image exists)

**Sections that do NOT need images:**
- Title/Subtitle/Opening
- Week at a Glance
- GO Battle League (unless a specific featured cup has imagery)
- Daily Discoveries
- Don't Miss

## Word-Count Budget (target 1,400–1,800)

Every issue must land **between 1,400 and 1,800 words of body prose**. Subject line options, headline options, opening paragraph options, and the Pre-Publish Audit Results / Hundo CP Provenance Table at the bottom do NOT count — measure only what the reader sees in the published email body.

**Budget history:**
- **2026-06-15:** Initial budget set to 1,400–1,700 after #18 (3,949 words) and #19 (2,974 words) blew past the readable-email zone. Beehiiv engagement curves drop sharply past ~1,800 words on mobile.
- **2026-06-23:** Ceiling bumped from 1,700 → 1,800 to accommodate Spotlight Hour as a required H2 section (locked 2026-06-20; nine H2 sections now required vs prior eight). 1,800 is the practical Beehiiv-engagement ceiling; do not raise further without re-testing engagement.

### What graphics are available TODAY (2026-06-15)

**Raid cards only.** Joe currently generates raid card graphics (per `instructions/graphics-brief.md` Card Type 1). The other card types in that document (Event card, GBL cup card, Max Battle card, Hundo CP strip) are FUTURE — they MIGHT be added later, but **do not assume they exist when planning a draft.**

Practical implication: only Section 6 (Raid Bosses) is in graphics-replace mode today. Every other section operates in text-only mode and must hit its cap via prose tightening alone. Daily Discoveries (Section 9) and Don't Miss (Section 12) carry the biggest prose-only cuts; those are the levers that get a heavy week into the 1,400–1,800 zone.

### Per-section caps

| Section | Cap (today) | Notes |
|---|---|---|
| Intro paragraph | ≤ 120 words | Voice + scene-set, one paragraph |
| Week at a Glance | ≤ 180 words | 6–8 bullets max, emoji + one line each |
| Events (each major event) | ≤ 200 words text-only | No event card today. Cut spawn/research/pool lists hard; lead with the "why it matters." |
| Raid bosses (each) | ≤ 80 words + **REQUIRED raid card graphic** | Counter lists live in the graphic; text retains only the "why it matters" sentence + Hundo CP line + Trainer Tip + Sources |
| GO Battle League | ≤ 200 words text-only | Top picks lists in prose; no cup card yet |
| Max Monday | ≤ 100 words text-only | Featured Dynamax + Hundo CPs + Trainer Tip; no Max card yet |
| Daily Discoveries | ≤ 100 words | 1 line per day; NEVER rehash content already in Events / Week at a Glance |
| Trending Topic | 200–350 words | Don't cut. This is the differentiator. |
| What's New (conditional) | 100–300 per existing rules | Section 11 keeps its own caps |
| Don't Miss | ≤ 150 words | 5 items max, ~25 words each |
| Sign-off | ≤ 25 words | Date callout + warm close. NO recap. |

### Graphics-replace mode (raid cards only, today)

A raid boss section qualifies for graphics-replace mode when the embedded raid card carries the counter lists, typing, weakness chips, and Hundo CPs. When the raid card is embedded:

- **Drop the 10-bullet counter list from the text entirely.** The graphic IS the reference; do not restate it in prose.
- **Keep**: 1-sentence "why it matters" + Hundo CP line (still required, per Section 6 — screen-readers and image-stripped email clients need it) + Trainer Tip + Sources line.
- **Image alt text** must include the boss name, typing, weakness list, and top counter (e.g., "Mega Skarmory raid card — Steel/Flying, weak to Fire and Electric, top counter Mega Charizard Y. Hundo at L20: 1,204, at L25 weather-boosted: 1,506.").

When a raid card is unavailable for a given week (art pipeline gap), the raid boss section falls back to text-only mode (≤ 200 words per boss with the full counter list in prose). Flag the fallback in the research brief so recon catches the pattern over time.

### Heavy-week reality check

For a normal week (3 raid bosses + 1–2 events + 1 Trending Topic), the per-section caps land an issue around 1,400–1,600 words. Doable with raid cards alone.

For a heavy week (4 raid bosses + 2 major events + 2 Trending Topics — #18-style), even with aggressive prose cuts you may overshoot 1,700 by 100–200 words. That's the cost of not having event cards yet. Two options when this happens:

1. **Demote one item**: drop a secondary Trending Topic to a Don't Miss callout, or fold a smaller event into the Week at a Glance line and skip its sub-section.
2. **Acknowledge the overshoot in the research brief**: log it as "heavy-week overshoot" so we can quantify how much event/cup/Max card graphics would save once they exist.

### Word-count enforcement

The readability check tool (`tools/readability_check.py`) flags any issue whose body falls outside the budget. Run with `--word-budget 1400-1800` to enforce. Recon Category L includes this check post-publish.

## Newsletter Structure

### 1. Title and Date Range
Create a creative, memorable title reflecting the week's biggest event or theme.

**Format:**
```
Spawn Point: [Creative Title]
[Start Date]-[End Date], [Year]
```

**Title Guidelines:**
- Make it catchy and memorable
- Reference the week's biggest event, theme, or holiday
- Keep it 3-7 words
- Can be playful, punny, or thematic

**Subject Line A/B Options (REQUIRED — 5):** the agent must generate **5 subject-line alternatives** at the top of the draft (above the title). Beehiiv supports A/B testing natively. Each alternative should pull from a different headline pattern (subject-led, action-led, theme-led, hook, deadline-led — see `instructions/brand-voice.md`).

Format the alternatives as:
```
**Subject Line A/B Options:**
A. [Subject-led]: e.g., "Lechonk's Big Day"
B. [Action-led]: e.g., "Three Raids Arrive Wednesday"
C. [Theme-led or hook]: e.g., "Will You Catch the Shiny?"
D. [Deadline-led]: e.g., "This Saturday Only: Mega Skarmory Debut"
E. [Curiosity / cliffhanger]: e.g., "The parrot. The steel bird. The Shadow Reshiram."

**Selected for draft:** Option [A|B|C|D|E] — [reason for default pick]
```

**Title Options (REQUIRED — 5):** the agent must also generate **5 short theme-name alternatives** for the H1 / Notion page title (distinct from the full subject line — the title is the short brand handle for the issue). Format:

```
**Title Options (short theme name — used in H1 / Notion page title):**
1. **The Triple Debut Edition** *(selected)*
2. **Three Debuts, Seven Days**
3. **Flying Taxi Week**
4. **Mega Skarmory Arrives**
5. **Squawkabilly Lands**
```

The "Selected for draft" line tells Joe which one will appear in the title block below if he doesn't pick a different one. The agent's default pick should be the option most aligned with the week's marquee event.

### Format Consistency Rules (apply across every section — added 2026-06-17)

**Section title emoji (REQUIRED).** Every H2 section title AND every H3 sub-section title must start with an emoji. The emoji marks the section visually in Beehiiv and Notion. Use the same emoji conventions as the Week at a Glance bullets (above) so the same event/Pokémon gets the same emoji everywhere in the newsletter.

Standard section emojis:
- `## 📅 Week at a Glance`
- `## 🎪 Events`
- `### 🚖 Flying Taxi` (or whatever the event-themed emoji is)
- `### 🌑 Flying Taxi: Taken Over` (Rocket-themed for Giovanni / Shadow)
- `## ⚔️ Raid Bosses`
- `### 🦅 Mega Raids: [Boss]` (use species emoji)
- `### 🦅 Super Mega Raids: [Boss]` (use species emoji)
- `### 🌌 5-Star Raids: [Boss]`
- `### 🌑 Shadow Raids: [Boss]`
- `## 🏆 GO Battle League`
- `## ✨ Spotlight Hour: [Species]`
- `## 🌀 Max Monday: [Species]`
- `## 🗓️ Daily Discoveries`
- `## 💬 Trending Topic — [Subtitle]`
- `## ⚠️ Don't Miss`
- `## 🆕 What's New` (when Section 11 applies)

If you don't see an obvious species emoji, default to the type-aligned emoji (🔥 Fire, 💧 Water, ⚡ Electric, 🌱 Grass, ❄️ Ice, 🌪️ Flying, 🪨 Rock, 🌍 Ground, 🥊 Fighting, 🌑 Dark, 🔮 Psychic, ✨ Fairy, 🐛 Bug, 🪲 Bug-alt, 🐉 Dragon, 🦴 Ghost, 🛡️ Steel, ☠️ Poison, 🐾 Normal).

**Date/time format (REQUIRED locked formats).** Every date/time mention in the newsletter must follow one of these three locked forms — no other formats permitted:

| Context | Format | Example |
|---|---|---|
| **Event section header** (under `### Event Name`) | `**[Full Day], [Full Month] [Day], [Start time]–[End time] local**` for single-day events; `**[Full Day], [Full Month] [Day], [Start time] – [Full Day], [Full Month] [Day], [End time] local**` for multi-day | `**Saturday, June 27, 2:00–5:00 PM local**` / `**Tuesday, June 23, 10:00 AM – Monday, June 29, 8:00 PM local**` |
| **Week at a Glance bullet** | `([Abbreviated Day] [Abbreviated Month] [Day], [time] local)` for single-time; `([Abbreviated Day] [Abbreviated Month] [Day] – [Abbreviated Day] [Abbreviated Month] [Day])` for multi-day | `(Sat Jun 27, 2:00–5:00 PM local)` / `(Tue Jun 23 – Mon Jun 29)` |
| **Don't Miss callout header** | Same as WaaG (abbreviated) | `Sat Jun 27, 2:00–5:00 PM local` |

Rules:
- Month names: full ("June") in event headers; 3-letter abbreviation ("Jun") in WaaG and Don't Miss
- Day names: full ("Saturday") in event headers; 3-letter abbreviation ("Sat") in WaaG and Don't Miss
- Time format: ALWAYS `[H]:[MM] AM/PM` with caps and no periods ("2:00 PM" not "2pm" or "2:00 p.m.")
- Use en-dash (`–`) for time ranges within a single day (`2:00–5:00 PM`); use en-dash for date ranges across days (`Tue Jun 23 – Mon Jun 29`); never use hyphens for ranges
- Time zone: append "local" for local-time events; spell out "PDT" / "PST" / "EST" / etc. for fixed-zone events (GBL rotation cutovers are always in PDT)

**Hundo CP format (REQUIRED locked formats).** Every Hundo CP line must use one of these two forms — already specified in Section 6, restated here for cross-section consistency:

Standard form:
> `**Hundo CPs:** **[L20 value]** (L20) / **[L25 value]** (L25, weather-boosted by [Weather Name])`

Mega/Super Mega raid variant (catch is base species, not Mega):
> `**Hundo CPs** (base [Species] catch): **[L20 value]** (L20) / **[L25 value]** (L25, weather-boosted by [Weather Name])`

Rules:
- CP values: comma-separated thousands (1,216 not 1216), bolded
- "L20" and "L25" in parentheses after each value
- "weather-boosted by" preceding the weather name(s); always include this phrase even if weather is implied
- Weather names: capitalized, alphabetical when multiple (`Partly Cloudy or Windy`, `Snow or Windy`, `Sunny or Snow`)
- Per-boss Hundo CPs go in the raid section AND in the Hundo CP Provenance Table at the bottom

**Anti-pattern (wrong):** `**Hundo CPs:** 1,772 Celesteela (L20) / 2,216 (L25, Snow or Windy); 2,101 Kartana (L20) / 2,626 (L25, Sunny or Snow)` — never combine two species on one Hundo CP line; give each species its own block.

**Source link titles (REQUIRED — reaffirmed from `feedback_source_link_titles.md`).** Every `[text](URL)` link in a Sources line must have a descriptive title. Never use the URL or URL fragment as the link text. See the convention table in the Source Attribution section below for per-source title patterns.

### 2. Subtitle
Write a fun, creative subtitle that expands on the title or highlights what makes this week special.

**Subtitle Guidelines:**
- Keep it 8-15 words
- Can be playful, enthusiastic, or build anticipation
- Reference specific Pokémon, events, or activities when possible

### Notion Database Properties (Auto-Populate)

When pushing to Notion (Step 6), populate these database properties on the newsletter page beyond Title + Status:

- **Issue Number** (integer) — sequence number, auto-increments from `instructions/newsletter-archive.md` (read the highest existing issue number, add 1)
- **Date Range** (text or date range) — e.g., "May 11 – May 17, 2026"
- **Featured Community Day** (text) — name of the CD Pokémon, or "None" if no CD that week
- **Trending Topic** (text) — short title of the Trending Topic section
- **GBL Cup** (text) — active themed cup name, or "Open formats only"
- **Mega Raid** (text) — featured Mega(s) for the week, comma-separated if multiple
- **5-Star Raid** (text) — featured Five-Star boss(es)
- **Shadow Raid** (text) — monthly Shadow Legendary
- **Max Monday** (text) — featured Dynamax/Gigantamax Pokémon
- **Subject A/B Options** (text) — the 3 subject lines, semicolon-separated
- **Has Month/Season Transition** (checkbox) — true if Section 11 (What's New) is included

If a property doesn't exist on the database yet, the Notion MCP will surface an error — note it in the email summary so Joe can add the property manually. Don't fail the whole run on missing properties.

This metadata makes the newsletter database queryable: Joe can filter by Featured CD, sort by Date Range, etc.

### 3. Opening Paragraph
Set the tone and emotional priority for the week. This is NOT a summary of every event. It answers one question: what should Trainers care about most, and why?

**Opening Paragraph Options (REQUIRED — 5):** the agent must generate **5 distinct opener alternatives** at the top of the draft (alongside the Title Options). Each alternative should hit a different angle: lead-with-marquee-event, lead-with-deadline, lead-with-investment-case, lead-with-coordination-ask, lead-with-rhetorical-question. Format:

```
**Opening Paragraph Options:**
1. (selected) [Lead-with-marquee-event paragraph]
2. [Lead-with-deadline paragraph]
3. [Lead-with-investment-case paragraph]
4. [Lead-with-coordination-ask paragraph]
5. [Lead-with-rhetorical-question paragraph]
```

**Guidelines (apply to every option):**
- 3 sentences max
- Lead with the most important thing happening this week, stated directly
- Name the key Pokémon, event, or deadline that defines the week
- Do NOT repeat times, dates, or bullet-point-style details (those belong in Week at a Glance)
- Do NOT start with a generic greeting like "Welcome back, Trainers!" Start with the news
- Read it back: if it sounds like a table of contents, rewrite it

**The test:** Could the opening stand alone and tell a casual Trainer what to prioritize this week? If yes, it's working. If it just lists things they'll read again two seconds later, it's not.

**Tricolon trap (added 2026-06-17).** When the week features three big items, the natural draft is three parallel sentences. That's a tricolon — `ai-check` Signal I + D both fire on symmetric three-beat openings. Fix one of two ways: (a) drop one item to Week at a Glance only and lead the intro with two, or (b) vary the structure of one sentence so the three beats aren't grammatically identical (e.g., one declarative + one descriptive clause + one colon-style reveal). See "Structural AI-tell rules" above for examples.

### 4. Week at a Glance
A bullet-point planning reference with calendar specifics the opening paragraph left out.

**Guidelines:**
- 4-8 bullets max
- **Event-first naming (added 2026-06-17).** Each bullet leads with the **event name** (Flying Taxi, Skarmory Super Mega Raid Day, Wingull Spotlight Hour, etc.), NOT just the featured Pokémon. The Pokémon is what the event delivers; the event is what the reader plans around. "🦜 Squawkabilly debuts in Flying Taxi" → "🚖 **Flying Taxi** (Tue Jun 23 – Mon Jun 29): Squawkabilly debut + 4 regional plumage forms."
- Cover ALL the week's events, rotations, and recurring beats — not just species debuts. Specifically include: every major event, GBL rotation, raid rotation, Spotlight Hour, Community Day, Max Monday, and any deadline (event end times, no-cap windows, expirations).
- **Every bullet must start with an emoji prefix** (no exceptions). Match the emoji to the event type:
  - 🚖 / 🚌 / ✈️ — travel-themed events (Flying Taxi, Wings, etc.)
  - 🚀 / 🦅 — Raid Day events (use creature emoji for species-specific raid days)
  - 🔥 / 💧 / ⚡ / 🌱 / 🌌 — type-themed raid rotations
  - ✨ — Spotlight Hour
  - 🌀 — Max Monday / Max Battle
  - ⚔️ — GO Battle League rotations + GBL events
  - 🏆 — GBL Cup launches / endings
  - 🎟️ / 🪙 — GO Pass / no-cap windows / paid tickets
  - 🔚 — event ENDS / deadline-driven callouts
  - 🌑 — Shadow Raids / Team GO Rocket / Giovanni
  - 🐉 — Community Day (or use the featured species emoji)
- Include the key time or date for each item (see "Date/time format" rules below)
- Do NOT restate the "why" or the narrative from the opening paragraph

**Format:**
Each bullet: `[emoji] **[Event name]** ([date/time]): [one-line description of what's in the event]`

**Examples (correct):**
- 🚖 **Flying Taxi** (Tue Jun 23 – Mon Jun 29): Squawkabilly debut + 4 regional plumage forms
- 🦅 **Skarmory Super Mega Raid Day** (Sat Jun 27, 2:00–5:00 PM local): Mega Skarmory debut
- ✨ **Wingull Spotlight Hour** (Thu Jun 25, 6:00–7:00 PM local): 2× Catch Stardust
- 🏆 **GBL rotation** (Tue Jun 23, 1:00 PM PDT): open Great/Ultra/Master triple
- 🌌 **5-Star + Mega raid rotation** (Wed Jun 24, 6:00 AM): Celesteela (S), Kartana (N), Mega Pidgeot in
- 🪙 **No-cap GO Points window** (Sat 12:00 AM – Mon 7:59 PM)
- 🔚 **Shadow Dialga window closes** (Tue Jun 30, 10:00 PM)

**Anti-pattern (wrong — Pokémon-first instead of event-first):**
- ~~🦜 Squawkabilly debuts in Flying Taxi (June 23–29)~~ — leads with species, buries event name
- ~~🦅 Mega Skarmory debuts at Super Mega Raid Day~~ — leads with species
- ~~🌌 Celesteela and Kartana enter 5-star raids~~ — leads with species; "5-star raids" should be the lead

**REQUIRED — emoji on every bullet (recurring drafting miss):** Every Week at a Glance bullet MUST start with a relevant emoji prefix. This has been left off repeatedly in past drafts. The emoji is part of the format, not decoration — it gives the scannable visual rhythm that makes the section work. Pick something specifically tied to the bullet's subject (the featured Pokémon's type/icon, the event vibe, the mechanic) — never a generic 📅 or 📌 unless the bullet really is a pure calendar marker with no thematic hook. Examples: 🔥 Reshiram, ⚔️ GBL season, 🌑 Shadow Legendary, ⚡ Spark-themed event, 🚀 new season launch, 🌏 GO Fest, 🧊 quest close.

**Pre-push check:** scan the Week at a Glance section. If any bullet starts with `- **` (no emoji between the dash and the bold label), it's missing its emoji — add one before pushing.

### 5. Events
List each special/limited-time event in chronological order (Monday through Sunday). For each:
- Event name with one emoji
- Start and end dates/times (in local time as found in source data)
- 1-2 paragraphs explaining what's happening
- **Trainer Tip** at the end (1-2 sentences of strategic value)

**Community Day specific:** when an event is a Community Day, include the **L20 hundo CP of the EVOLVED form** (15/15/15 IVs, the value players check after evolving during the bonus window) and the **L25 hundo CP of the evolved form** (weather-boosted). The featured species often gets a Showcase or wild-spawn boost; the catch-CP screen-check is what trainers want.

**Special Research / Master Research / Timed Research tracking (REQUIRED when applicable):** these are multi-step quest lines that span days or weeks (Pressure Rising's Volcanion arc, season-tie-in research, monthly Special Research, GO Pass premium track, Mythical debut research). When an active research quest has a step that completes during the newsletter's window OR a step that requires an event taking place in the window, include a brief callout in the relevant Event section:

- **Quest line name** + brief context (e.g., "Pressure Rising Special Research — final step")
- **What's needed this week** (e.g., "Catch 30 Water-types — pair with Tuesday's Showcase Tuesday wild spawns")
- **Reward** (Pokémon encounter, item bundle, exclusive move) — high level, not exhaustive
- **Deadline if any** (Mythical research often expires when the season ends)

If multiple research quests are active and intersect with the week, list them all with brief callouts. Source: Niantic's Special Research announcement post + LeekDuck's research guide page for that quest.

**Include:** Special themed events, limited-time events, debut events, seasonal launches, Special/Master/Timed Research quests with steps in the window
**Do NOT include:** Max Monday (Section 8), Daily Discoveries (Section 9), Raid Bosses (Section 6)

### 6. Raid Bosses
**Standalone section.** Do NOT duplicate in Events.

Cover Five-Star, Mega, and Shadow raids. Raids rotate on Wednesdays at the start of the day. Always check if any bosses end during the week and what rotates in.

**Default format = raid card graphic + ≤ 80 words per boss.** Each featured raid boss gets an embedded raid card graphic (spec in `instructions/graphics-brief.md`) carrying the counter lists, typing, weakness chips, and Hundo CPs. Prose retains: 1-sentence "why it matters" + Hundo CP line (the labeled block form below — still required even when shown in the graphic, for screen-readers and email clients that strip images) + Trainer Tip + Sources line. **Do NOT spell out the 10-bullet counter list in prose when the graphic is embedded** — that's the whole point of the format change.

When no graphic is available (rush week, art pipeline blocked), fall back to text-only mode: ≤ 200 words per boss, full counter list in prose, same Hundo CP + Trainer Tip + Sources blocks. Flag the fallback in the recon trigger so we catch art-pipeline gaps over time.

**Shadow Raid notes (agent-facing, NOT to be repeated in newsletter copy):**
- Shadow Raids can be done remotely. The monthly featured Legendary Shadow Pokémon raids every day during its window, not just weekends. 1-Star and 3-Star Shadow Raids can also appear during the week.
- These are facts the agent needs to know to plan correctly. **Do NOT write them into the newsletter** — readers know. See "What NOT to Mention" below.

When raids rotate mid-week:
```
**Five-Star Raids:**
[Current boss] stays through [day/time]. [Brief description]

**Rotating In [day/time]:** [New boss] arrives! [Brief description]
```

#### REQUIRED: Hundo CPs

Include the **L20 hundo catch CP** (15/15/15 IVs, normal weather) and the **L25 hundo catch CP** (15/15/15 IVs, weather-boosted) for every featured raid boss (Five-Star, Mega base-form catch, Shadow) AND every featured Dynamax/Max Battle boss. Players screen-check post-raid to identify hundos — these two numbers are the deliverable.

**LOCKED FORMAT** (no per-section flexibility — every Hundo CP line in every issue uses this exact form):

Standard form:
> **Hundo CPs:** **[L20 value]** (L20) / **[L25 value]** (L25, weather-boosted by [Weather Name])

Mega-raid variant — encounter is the base species, NOT the Mega:
> **Hundo CPs** (base [Species] catch): **[L20 value]** (L20) / **[L25 value]** (L25, weather-boosted by [Weather Name])

Multiple boost weathers: list both with "or" — `(L25, weather-boosted by Windy or Cloudy)`. Order weathers alphabetically.

If a Pokémon has no weather boost relevant to its types (extremely rare): use `(L25, weather-boosted)` with no specific weather name. Flag for editor verification.

Reference examples:
- **Hundo CPs:** **1398** (L20) / **1748** (L25, weather-boosted by Snow)
- **Hundo CPs:** **1810** (L20) / **2263** (L25, weather-boosted by Cloudy or Sunny)
- **Hundo CPs** (base Altaria catch): **1145** (L20) / **1432** (L25, weather-boosted by Cloudy or Windy)
- **Hundo CPs:** **1633** (L20) / **2041** (L25, weather-boosted by Windy)
- **Hundo CPs** (base Falinks catch): **1347** (L20) / **1683** (L25, weather-boosted by Cloudy)

Style rules:
- Label: `**Hundo CPs:**` (bold prefix, plural "CPs" since two values are shown). For Mega-raid variant, parenthetical qualifier sits between "Hundo CPs" and the colon.
- Both CP values: bold.
- Separator between L20 and L25 entries: ` / ` (space-slash-space).
- Weather name(s): capitalized (Sunny, Cloudy, Windy, Snow, Rainy, Partly Cloudy, Fog) — match Niantic's in-game capitalization.
- Never write Hundo CPs inline in prose (e.g., "CP 1347 at L20"). Always use the labeled block form.

Step 5.5 audit Check #15 (Hundo CP Format Consistency) hard-fails any section whose Hundo CP line deviates from these forms.

Source: `db.pokemongohub.net/pokemon/[dexNr]` lists both pre-computed. If unavailable, compute from `pokedex.json` base stats using the GO CP formula (see `instructions/meta-data-sources.md`).

#### REQUIRED: Premium AND Budget Counters Per Boss

Every featured raid boss must have BOTH:
1. **Premium counter team** — top-tier picks (Legendaries, Mythicals, Megas, Shadows).
2. **Budget counter team** — non-Legendary, non-Shadow alternatives that an Everyday Trainer is likely to actually have powered up. 3-4 options with movesets cited.

Don't shortcut with "same counters as the previous boss." If two bosses share typing (e.g., Buzzwole and Pheromosa both Bug/Fighting), restate both tiers in each section — readers may scan one section and not the other.

Acknowledge gaps in plain language: *"Don't have Primal Groudon? Most trainers don't either — Garchomp, Rhyperior, and Landorus Therian all duo this comfortably."* Brand voice (per `instructions/brand-voice.md`) applies — knowledgeable-friend asides, not data-dump bullet lists.

##### Source balance: Pokebattler ⟷ Pokémon GO Hub Database

**Use BOTH sources when picking counters — balance, don't pick one and dump.** They optimize for different things:

- **Pokebattler** (`fight.pokebattler.com/raids/...`) — simulation-driven, ranks by `ESTIMATOR` / `TTW`. Best for: precise damage math, identifying theoretical-optimum lineups, calling out the absolute fastest clears. Risk: lists often over-weight Mega forms with legacy/exclusive moves the median trainer doesn't have.
- **Pokémon GO Hub Database** (`db.pokemongohub.net/pokemon/[N]/counters`) — community-curated "Best Counters Highlights" + per-tier annotations. Best for: accessibility flags, non-exclusive-move alternatives, and what a real trainer roster will field. Risk: less precise on raw DPS ranking; their order doesn't always match Pokebattler's estimator.

**How to balance:**
1. Pull both lists. A counter appearing in BOTH = high-confidence recommendation; cite it without hedging.
2. Where they DISAGREE, surface why: usually Pokebattler's pick has an exclusive move (Elite TM-only, Adventure Effect, Mega signature) that Hub-DB downranks for accessibility. Newsletter convention is to cite the Pokebattler pick AS the premium recommendation but always pair with the Hub-DB-friendly non-exclusive alternative (per `feedback_raid_premium_budget.md` and Category C accessibility-tier rule in recon).
3. For the budget tier specifically, lean Hub-DB — it weights "what trainers actually have" more naturally than Pokebattler's pure-DPS estimator.

This isn't a 50/50 averaging rule — it's a cross-check. If Pokebattler ranks Mega Beedrill #1 with Drill Run (Elite TM) and Hub-DB lists it #3 with standard Poison Jab/Sludge Bomb, the right Spawn Point write-up is: lead with Mega Beedrill (both agree it's premium), cite its standard non-exclusive moveset (Hub-DB's accessibility framing), and skip the Drill-Run-specific hedge unless the reader's whole bench requires it.

#### What NOT to Mention (filler that pads without informing)

These are widely understood defaults. **Do not write them into raid sections** — they take up space and read like AI-generated boilerplate:

- ❌ "Remote Raid Passes work" / "can be done remotely" — that's the default. Only flag it as an EXCEPTION when the raid is **in-person only** (e.g., 6-Star Gigantamax raids, ticketed Raid Day events that override the default).
- ❌ **"Shadow Raids are weekend-only" / "only on weekends" / "Saturday and Sunday only" — FACTUALLY WRONG and HIGH-FREQUENCY recurring error.** Shadow Raids (all tiers) run ANY day during their announced window. See `feedback_shadow_raid_remote_default.md`. Only cite a weekend restriction if Niantic explicitly schedules a specific event that way (rare) — with the source URL.
- ❌ **"Shadow Raids are in-person only" / "Remote Raid Passes don't work for Shadow Raids" — FACTUALLY WRONG.** Shadow Raids ARE remote-raidable. Same recurring-error family as the weekend-only mistake.
- ❌ "Shadow Raids are remote-raidable" / "Remote Raid Passes work for Shadow Raids" / "available every day, not just weekends" — also default-filler; readers know. Don't write the positive defaults either. Just give the boss, window, and counters.
- ❌ "Don't forget your Remote Raid Pass" / "Bring friends!" — empty exhortation.

When a default IS broken (in-person-only, ticket required, Premium Battle Pass only), call that out clearly.

#### Trainer Tips

Include Trainer Tips for counter strategies, PvP/PvE value, and shiny priorities.

Do NOT include one-star or three-star raids.

### 7. GO Battle League
Cover active leagues, cups, rotation dates, and notable meta picks.

### 7.5. Spotlight Hour (REQUIRED standalone section — added 2026-06-20)
**Standalone section.** Do NOT bury inside Week at a Glance / Daily Discoveries / Don't Miss alone. Spotlight Hour gets its own H2 section every single newsletter, between GO Battle League and Max Monday.

Why standalone: Spotlight Hour is a weekly recurring 1-hour event with its own featured species, shiny odds, and stackable bonus (dust / candy / XP / evolution candy depending on the week). Readers plan their Tuesday-evening hour around it. It's not a calendar footnote.

Standard format:
```
## ✨ Spotlight Hour: [Species]
**[Full Day], [Full Month] [Day], 6:00–7:00 PM local**

[Species] floods the spawn pool for one hour. Event bonus: [2× Catch Stardust / 2× Catch Candy / 2× Catch XP / 2× Evolution XP / 2× Transfer Candy / etc.]. [Evolution note if relevant — e.g., "Evolves into X with Y Candy"]. [Brief PvP / utility note if applicable.]

**Shiny rate: standard, NOT boosted (do NOT claim "boosted shiny odds" — Niantic does not boost the per-encounter shiny rate for Spotlight Hour featured species). The volume of spawns means more rolls, so absolute shiny encounters per hour go up, but the rate per spawn is unchanged. If the editorial calls out shiny chasing, frame it as "more shots at one" — never "boosted odds."**

> **Trainer Tip:** [Stacking advice — Star Piece + GBL + Lucky Egg etc., or moveset note, or PvP relevance, or shiny-hunting tip]

*Sources: [LeekDuck: Spotlight Hour schedule](https://leekduck.com/spotlight-hour/), [Hub-DB: {Species}](https://db.pokemongohub.net/pokemon/{N})*
```

Section emoji is always `✨`. Date format follows the standard event-header convention. The Trainer Tip should call out at least one stacking opportunity (Star Piece, GO Battle Thursday, Friendship Friday Stardust discount, Community Day overlap, etc.) — Spotlight Hour's value is multiplicative.

Verify the featured Pokémon and bonus on LeekDuck the same week (not from cached memory). The featured species rotates weekly and the bonus type rotates monthly.

### 8. Max Monday
**Standalone section.** Do NOT duplicate in Events.

Max Monday runs 6:00 AM to 9:00 PM local time. Include featured Dynamax Pokémon, whether it's a debut or continuation, type weaknesses, and a Trainer Tip.

**REQUIRED for the featured Dynamax Pokémon:** include the **L20 hundo catch CP** (15/15/15 IVs, normal weather) and the **L25 hundo catch CP** (15/15/15 IVs, weather-boosted). Same rationale as raid bosses — players screen-check post-Max-Battle.

**CRITICAL:** When suggesting attackers, defenders, or healers for Max Battles, only recommend Dynamax-capable Pokémon. Not every Pokémon in the game can Dynamax. Shadow Pokémon CANNOT be brought into Max Battles at all (they cannot Dynamax and cannot fill any team slot). Verify each recommended Pokémon is actually Dynamax-eligible AND non-Shadow before including it.

### 9. Daily Discoveries
**Standalone section.** Do NOT duplicate in Events.

**Cap: ≤ 100 words for the whole section.** One line per day, day-stamped. NO rehash of content already in Events / Week at a Glance — if a major event drops on Thursday, link to its Events section rather than restating times, spawns, and bonuses. Daily Discoveries is the recurring-weekday-bonus row, not a second pass at the calendar.

Daily bonuses active throughout the week. Only include ones with significant value:
- Sunday: Scenic Sunday (Routes, Buddy Candy, Mateo encounters)
- Monday: Max Monday (in-person Max Battle Rare Candy XL)
- Tuesday: Showcase Tuesday (up to 5 entries)
- Wednesday: Wednesday Raid Hour (in-person Raid Rare Candy XL, raid rotation flips at 6 AM)
- Thursday: GO Battle Thursday + Spotlight Hour (6–7 PM)
- Friday: Friendship Friday (extra Special Trades, –20% Stardust)

**Format per day** (one line each):
`**[Day, Date] — [Headline]:** [one-sentence bonus/event line, with a link to the Events subsection if the day's main story lives there].`

**Anti-pattern**: re-stating every detail of an event already covered above. If Wednesday has Necrozma Raid Hour AND a raid rotation AND Choose Your Path beginning, the Daily Discoveries line says "Wednesday Raid Hour + raid rotation flips + Choose Your Path begins (see Events)." Three callouts, one line.

### 10. Trending Topic
A short write-up on one story, event preview, news drop, or meta shift that matters this week. This is the newsletter's editorial voice, where you go beyond event listings and cover something readers care about right now.

**The Trending Topic does NOT have to be a meta deep-dive every week** (clarified 2026-06-15). Format the section to match the week's biggest actionable story. Recent examples that worked:
- News drop: "Spotlight Hour returns Thursday — here's the schedule" (Issue #18)
- Event preview: "GO Fest Copenhagen — what remote trainers can still catch" (Issue #18)
- New feature explainer: "The Explorer Gadget is live for some trainers" (Issue #18)
- Investment case: "Shadow Dialga — why this is your most important raid of the summer" (Issue #19)
- Datamine or controversy: still valid when something genuine breaks

**What belongs:**
- Reddit investigations or discoveries (r/TheSilphRoad, r/PokémonGO)
- Community frustrations or controversies with Niantic decisions
- Datamined findings or game mechanic discoveries
- Meta shifts (new Pokémon or move rebalances shaking up PvP/PvE)
- Niantic responses to community feedback
- Notable community-created tools, maps, or resources
- News drops, event previews, feature explainers, investment cases (per the formats above)

**Guidelines:**
- 2–4 paragraphs of prose, OR a structured format (headed sub-sections) when the story has multiple angles (Chicago + universal info, mechanic explainer + cost breakdown, etc.)
- Tell the story: what happened, why it matters, what the reader should do about it
- Link to primary sources (Reddit threads, news articles, Niantic blog posts)
- **Bold-lead alternation (added 2026-06-17).** If the section uses bold-phrase-as-paragraph-opener (e.g., "**Defensive typing that almost nothing touches.**"), do NOT apply it to every paragraph. `ai-check` flags 4-paragraph parallel bold-lead structures as Signal D (architecturally perfect = AI). Use bold leads on the first and last paragraphs; drop them on the middle two. Asymmetry reads more human.
- Tone: informative and fair. Skip the throat-clearing ("It's important to note that…") — make the claim directly.
- End with a "Sources:" line listing the key links
- **Hit grade level ≤ 6.0** (per Category L readability check). Even when the story is analytical, write at 5th–6th grade reading level — short sentences, plain words, one idea per paragraph.

**Research process:**
- WebSearch: "Pokémon GO controversy [month] [year]", "Pokémon GO reddit [month] [year]", "site:reddit.com/r/TheSilphRoad top this week"
- Check content creators for trending topics
- Look for posts with high engagement (upvotes, comments, impressions)

**Example (from Spawn Point #11):**
```
**Silicobra's Spawn Problem**

Sustainability Week runs through Monday, but finding Silicobra has been the loudest
frustration of the event. All players were told was that it would appear in "desert-like
areas," which turned out to be far more restrictive than most expected...

[2-3 more paragraphs covering the community investigation, Niantic's response,
and practical advice]

Sources: Dexerto | The Gamer | One More Catch
```

### 11. What's New This Month/Season (CONDITIONAL)

This section appears ONLY when the newsletter's Mon-Sun window contains the start of a new calendar month, the start of a new GBL season, or both. Skip the section entirely when the window is mid-month and mid-season.

**Detection rule:**
- New month: `next_monday.month != next_sunday.month` (the 1st of a month falls in the window)
- New season: a GBL season transition date falls in the window. Check Niantic's announcement for the upcoming season's start date and the current season's end date.
- Both: combined section.

**Three modes:**

| Mode | When | Length | Bullets |
|---|---|---|---|
| Monthly only | New month, mid-season | 100-150 words | 4-6 |
| Season only | New season, mid-month (rare) | 200-300 words | 5-8 |
| Combined | New month AND new season | 200-300 words | 5-8 |

**What belongs (monthly mode):**
- Featured events for the month (Community Day pick if announced, raid storyline arc, themed events)
- Special Research debut for the month, if any
- Notable Legendary/Mythical debut or rotation
- Dynamax / Gigantamax additions for the month
- Daily Discoveries theme highlights, if announced

**What belongs (season mode — adds to monthly):**
- New season name and theme
- Season-end date for the closing season + start date for the new one
- GBL theme cup schedule for the season
- Season-long bonuses (extra catch XP/Stardust, distance bonuses, etc.)
- Move rebalances or new moves added (cite the @PokemonGoApp announcement)
- Season-pass headline content (free track + paid Premium track highlights — don't list every reward, just the standout)
- Special Research tied to the season's narrative
- Mechanics changes (e.g., Daily Discoveries replacing Spotlight Hour was a season-change drop — flag major shifts like this)

**Guidelines:**
- Lead with reader value, not corporate hype. Brand voice still applies (re-read `instructions/brand-voice.md`).
- Bullet format: short, scannable, each bullet starts with a verb or subject (not "Niantic announced...")
- Cap the deep dive — this is a roundup, not the definitive article. Three to eight bullets max.
- Always end with: *"Full details at [Niantic's monthly content post](URL)"* (and `[the season hub](URL)` if applicable).
- If the announcement is light (e.g., Niantic posted a teaser without specifics), keep the section brief and acknowledge the gap: "Full month rundown comes Wednesday with the official content drop."

**Position:** Between Trending Topic (#10) and Don't Miss (#12). Don't Miss handles deadline-focused callouts; this section is forward-looking. The sequence reads naturally.

**Image:** A relevant hero from Niantic's monthly post (`pokemongo.com/news/[article-slug]` hero) or season hub. Skip if none available.

**Sources line:** Always cite Niantic's monthly content post and the season hub when applicable. Add LeekDuck monthly recap or @PokemonGoApp announcement thread if they add specifics the official post doesn't.

**Example title format:**
- Monthly only: "May at a Glance" / "What May Brings"
- Season only: "Memories in Motion: New Season Drops Wednesday"
- Combined: "May Kicks Off a New Season"

### 12. Don't Miss
Short callouts surfacing the week's highest-stakes deadlines and stack opportunities.

**Cap: ≤ 150 words for the whole section.** 5 items max, ~25 words each.

**What belongs (deadline / stack-opportunity callouts, not generic links):**
- Raid Hour / Spotlight Hour windows
- Move-rotation evolution windows (Community Day signature moves close-of-window)
- Research expiration deadlines
- Last-day-of-event reminders
- Mid-week raid rotation flips

**Rules:**
- 3–5 callouts (5 is the ceiling; don't pad)
- Each callout = emoji + bold header line + 1 sentence consequence/CTA
- Must be a TRUE deadline or stack — not a generic "go play the event" reminder
- The Trending Topic, Trainer Tips, and Events subsections cover analysis; Don't Miss is the "what closes if you ignore it" list
- Don't restate the event in detail — readers already saw it in Events / Week at a Glance. Just the deadline + the consequence.

**Format per callout** (strict):
```
**[emoji] [Short header — what's closing/stacking]**
[One sentence: when it ends + what you lose if you miss it.]
```

**Example (correct):**
```
**🐉 Frigibax evolution window closes Saturday June 20 at 9:00 PM**
Evolve Arctibax to Baxcalibur during this window for Glaive Rush. Next chance is a Community Day Classic with no announced timeline.
```

**Anti-pattern (cut):**
```
**Spotlight Hour returns Thursday, June 18, 6:00–7:00 PM local**
The first Spotlight Hour since the March 3 retirement. Swinub is the debut species with 2x Candy for transferring Pokémon. Shiny eligible. This is also the new permanent Thursday slot — paired with GO Battle Thursday, so you can stack the 6:00 PM Spotlight Hour with the 4x Stardust GBL window. Pop a Star Piece before 6:00 PM.
```
^ 4 sentences, 60 words, all rehash from Daily Discoveries. Compress to:
```
**🔦 Spotlight Hour stacks with GO Battle Thursday — Thu June 18, 6–7 PM**
Pop a Star Piece before 6:00 PM. Catch Stardust + GBL 4× Stardust + Star Piece is the week's biggest XP/dust stack.
```

---

## Source Attribution

Every section of the newsletter must include source links at the end. This tells Joe who to attribute information to and lets readers verify claims.

**Format:** After each section's content, add a "Sources:" line with linked references.

**Example (correct):**
```
Sources: [LeekDuck: Tapu Fini raids](https://leekduck.com/events/tapu-fini-in-5-star-raid-battles-may-june-2026/) | [Pokémon GO Hub: Tapu Fini stats](https://db.pokemongohub.net/pokemon/788) | [Pokémon GO Blog: Spring Marathon 2026](https://pokemongo.com/news/spring-marathon-2026)
```

**Example (WRONG — never do this):**
```
Sources: [leekduck.com/events/tapu-fini-...](https://leekduck.com/events/...) | [db.pokemongohub.net/pokemon/788](https://db.pokemongohub.net/pokemon/788)
```

**Rules:**
- **NEVER use a URL or URL fragment as link text.** Every `[text](URL)` requires a descriptive title that names the source AND what's at the link (see `feedback_source_link_titles.md` for the per-source convention table).
- List every source used for that section's data.
- Separate sources with pipes (|).
- If a specific article was referenced, link to that article, not just the homepage.
- Primary sources (Niantic blog, LeekDuck event page, Hub-DB species page) listed first, community sources after.

**Per-source title convention:**

| Source | Link text pattern |
|---|---|
| Pokémon GO Hub article | `Pokémon GO Hub: [Article topic]` |
| db.pokemongohub.net pokedex pages | `Pokémon GO Hub: [Species] stats` or `Hub-DB: [Species]` |
| LeekDuck event pages | `LeekDuck: [Event name]` |
| LeekDuck calendar root | `LeekDuck event calendar` |
| pokemongo.com news posts | `Pokémon GO Blog: [Topic]` or `Niantic — [Topic]` |
| Niantic Help Center FAQ | `Niantic Help: [Topic]` |
| Pokebattler counter pages | `Pokebattler: [Species] counters` |
| PvPoke rankings | `PvPoke: [League] rankings` |
| pokemon-go-api JSONs | `pokemon-go-api: [resource]` |
| Reddit posts | `r/[subreddit]: [thread title]` |

**Pre-push grep check:** search the assembled draft for `[https://`, `[http://`, `[www.`, `[db.poke`, `[pokemongohub.net`, `[leekduck.com`, `[fight.pokebattler` — any matches are URL-as-title and must be fixed before push.

**Banned editorial claims (HARD FAIL — added 2026-06-23):**

These claims have appeared in Spawn Point drafts without source backing. Each is a HARD FAIL pre-push grep — if any pattern matches in the Spotlight Hour or wider event body, fix BEFORE publishing.

| Banned phrase | Why | Replacement |
|---|---|---|
| `Shiny .* at boosted odds` (Spotlight Hour context) | Niantic does NOT boost per-encounter shiny rate during Spotlight Hour. Featured species has its standard shiny rate. | "Standard shiny rate applies — volume means more rolls, not better per-encounter odds" OR "More shots at a shiny than usual" (volume framing only) |
| `boosted shiny rate` / `increased shiny rate` (Spotlight Hour context) | Same as above. | Same as above. |
| `Spotlight Hour.*shiny boost` | Same as above. | Same as above. |
| `wild encounter rate.*boosted shiny` (anywhere outside of explicit Niantic-confirmed events: Community Day, special raid days, Hatch Day) | Most events do NOT boost the per-encounter shiny rate. Only Community Day, specific Raid Days, Hatch Days, GO Fest, and Niantic-confirmed special windows do. | Verify from Niantic's official event page; if no shiny boost is listed, do NOT claim one. Default framing: spawn volume increase only. |

**Shiny rate sources of truth (when in doubt):**
- Niantic event blog post for that specific event
- [LeekDuck event page](https://leekduck.com/events/) (Notes section flags shiny boosts explicitly)
- [The Silph Road shiny odds research thread](https://thesilphroad.com/) (historical baselines per event type)

**When a shiny boost IS confirmed:** call it out specifically with the source ("Per LeekDuck, this event boosts shiny Wingull rate to roughly 1 in 250 from the standard ~1 in 500"). NEVER use generic "boosted odds" without a number or source.

---

## Required-section presence checks (HARD FAIL if missing — added 2026-06-23)

**Why this exists:** Spawn Point #20 and #21 both shipped with the Spotlight Hour section missing or in non-canonical format (`## SPOTLIGHT HOUR` all-caps, no emoji, no Trainer Tip). The section is required per Section 7.5 but the rule wasn't enforced by a pre-push check, so the omission slipped through twice in a row. This block hard-codes the grep pattern that catches it.

Run these greps on the assembled draft BEFORE pushing to Notion / Beehiiv. Any miss = HARD FAIL; do not publish until the section is added in the correct format.

| Required section | Exact grep pattern (case-sensitive) | Position |
|---|---|---|
| Week at a Glance | `^## 📅 Week at a Glance$` | After intro, before Events |
| Events | `^## 🎪 Events$` | After WaaG, before Raid Bosses |
| Raid Bosses | `^## ⚔️ Raid Bosses$` | After Events, before GBL |
| GO Battle League | `^## 🏆 GO Battle League$` | After Raid Bosses, before Spotlight Hour |
| **Spotlight Hour** | `^## ✨ Spotlight Hour: [A-Z]` | Between GBL and Max Monday |
| Max Monday | `^## 🌀 Max Monday: [A-Z]` | After Spotlight Hour, before Daily Discoveries |
| Daily Discoveries | `^## 🗓️ Daily Discoveries$` | After Max Monday, before Trending Topic |
| Trending Topic | `^## 💬 Trending Topic` | After Daily Discoveries |
| Don't Miss | `^## ⚠️ Don't Miss$` | After Trending Topic |

**Anti-pattern grep (HARD FAIL — these all-caps / no-emoji variants must NOT appear):**

- `^## SPOTLIGHT HOUR` — must be `## ✨ Spotlight Hour: [Species]`
- `^## MAX MONDAY` — must be `## 🌀 Max Monday: [Species]`
- `^## GO BATTLE LEAGUE` — must be `## 🏆 GO Battle League`
- `^## EVENTS` — must be `## 🎪 Events`
- `^## RAID BOSSES` / `^## RAID CORNER` — must be `## ⚔️ Raid Bosses`
- `^## DAILY DISCOVERIES` — must be `## 🗓️ Daily Discoveries`
- `^## DON'T MISS` / `^## DONT MISS` — must be `## ⚠️ Don't Miss`
- `^## TRENDING TOPIC` (without `: [subtitle]`) — must be `## 💬 Trending Topic — [Subtitle]`

**One-shot shell command** (run from the draft directory):

```bash
draft=/path/to/draft.md
echo "=== Required sections (must all be 1) ==="
for pattern in '^## 📅 Week at a Glance$' '^## 🎪 Events$' '^## ⚔️ Raid Bosses$' '^## 🏆 GO Battle League$' '^## ✨ Spotlight Hour: [A-Z]' '^## 🌀 Max Monday: [A-Z]' '^## 🗓️ Daily Discoveries$' '^## 💬 Trending Topic' '^## ⚠️ Don'\''t Miss$'; do
  count=$(grep -cE "$pattern" "$draft")
  status="✓"; [ "$count" -eq 0 ] && status="✗ MISSING"
  echo "$status  $count  $pattern"
done
echo "=== Anti-patterns (must all be 0) ==="
for pattern in '^## SPOTLIGHT HOUR' '^## MAX MONDAY' '^## GO BATTLE LEAGUE' '^## EVENTS$' '^## RAID BOSSES$' '^## RAID CORNER' '^## DAILY DISCOVERIES' '^## DON'\''T MISS' '^## DONT MISS'; do
  count=$(grep -cE "$pattern" "$draft")
  status="✓"; [ "$count" -ne 0 ] && status="✗ WRONG FORMAT"
  echo "$status  $count  $pattern"
done
```

**Recon enforcement:** Recon Category A (Section Presence) now hard-flags any Spotlight Hour omission OR all-caps section variant in the assembled Beehiiv body. Recon will also re-pull the LeekDuck Spotlight Hour schedule and cross-check that the featured species in the section header matches the week's published Spotlight Hour.

---

## Important Reminders
- Always include times in **local time** as found in source data. DO NOT convert time zones
- **Time format: use AM/PM (caps, no periods) throughout.** Never mix "AM/PM" with "a.m./p.m." in the same newsletter. Examples: "6:00 AM to 9:00 PM" ✓, not "6:00 a.m. to 9:00 p.m." Apply consistently across all sections including Daily Discoveries.
- **Date commas: always include a comma after the weekday name.** Examples:
  - "Saturday, May 9 from 2:00 PM to 5:00 PM" ✓
  - "Wednesday, May 6 at 6:00 AM" ✓
  - "Monday, May 4 from 6:00 AM to 9:00 PM" ✓
  - NOT "Saturday May 9..." (missing comma)
- **Date ranges in titles or running text use en-dash (–), not hyphen (-).** Example: "May 4–May 10, 2026" ✓, not "May 4-May 10".
- Explain acronyms the first time (e.g., "Great League (GBL)")
- If shiny chances exist, say "with a chance to be shiny" (not "shiny available")
- Never describe a wild Pokémon as having "boosted" shiny odds unless it's during a confirmed boosted event. All wild shinies are 1/512 since March 2026. See `instructions/shiny-odds-reference.md` for current rates.
- Focus on helping casual Trainers, not just hardcore
- Double-check dates and times
- Never use em dashes
- Raids rotate Wednesdays at start of day
- Always check for raid rotations. Don't assume raids last the whole week
- Trainer Tips should provide NEW strategic insights, not restate event info. Use `instructions/trainer-tips-framework.md` as a checklist for every tip.
- Trainer Tips MUST be directly about the section's content. A Max Monday tip must be about the featured Dynamax Pokémon. A Raid Boss tip must be about that raid boss. Do NOT attach generic tips to a section just because they share a day of the week.
- NO DUPLICATION across sections
- Suggest 5 titles, 5 subtitles, and 5 opening paragraphs for Joe to choose from
