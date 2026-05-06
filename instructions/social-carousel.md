# Social Carousel + Caption Generation

The Spawn Point newsletter ships every Monday for the upcoming week. Each week the agent also generates social-media copy so the same content can be reposted as an Instagram carousel + caption (and optionally other formats). This file is the playbook for that copy — adapted from the Landoralpha Carousel Content Intelligence guide.

The carousel is **content only** — no rendering. The agent outputs:
1. A 10-slide carousel as JSON matching the local renderer schema (`/Users/joelandor/Claude-Master/my-carousel-system/`)
2. An Instagram caption with hashtags
3. Alt text suggestions for each slide's background

Joel pastes the JSON into his local carousel renderer to produce the final 1080×1440 images.

## Brand voice still applies

The carousel uses Spawn Point's voice (`instructions/brand-voice.md`), the no-default-filler rule, and the gap-acknowledgment principle. Stop-slop quick checks apply: cut adverbs, no passive voice, no em dashes, vary sentence rhythm, trust the reader.

The carousel is **shorter and louder** than the newsletter prose — every slide is one idea. Be punchy, not preachy.

## Triple Hook Framework

Instagram gives carousels three separate chances to hook each viewer. When someone doesn't engage with slide 1, the algorithm shows them slide 2 next time, then slide 3.

**Core rule:** Slides 1, 2, and 3 must each work as a standalone hook for a cold scroller with zero context. They are three separate entry points into the same week — not a sequence.

**Progression rule:** Each hook should "progress things without progressing too much." A new angle on the same week, not a continuation. If slide 2 only makes sense after reading slide 1, rewrite it.

**Headline limit:** 10 words max per hook headline.

| Slide | Role | Requirement |
|-------|------|-------------|
| Slide 1 | Primary hook | Cold entry, no context needed |
| Slide 2 | Secondary hook | Fresh angle, still standalone |
| Slide 3 | Tertiary hook | Another entry point, same week |

## Spawn Point Hook Formulas

Adapted from the general carousel formulas to weekly Pokémon GO content. Pull two or three from this list per carousel — don't reuse the same formula across all three hook slides.

1. `[N] things you can't miss in Pokémon GO this week`
2. `[Featured Pokémon]'s Big Day is [Day]`
3. `[Mega/Legendary] arrives Wednesday — here's what to bring`
4. `Stop hoarding [resource] before [event]`
5. `If you've been waiting on [Pokémon/event], this is the week`
6. `[Number] hours of bonuses you didn't know about`
7. `The [adjective] guide to this week in Pokémon GO`
8. `What to plan around before Monday`

**Don't use:**
- ❌ "This week in Pokémon GO" (generic, AI-default)
- ❌ "Your weekly roundup" (corporate)
- ❌ "Get ready Trainers" (banned phrase per brand voice)
- ❌ "Buckle up" / "Without further ado" / "Don't miss out"

## Content Arc: Listicle (default for Spawn Point)

Spawn Point's weekly content is news-driven, not "5 tips." The Listicle arc fits best:

```
Slide 1–3   Triple Hook (three standalone entries into the week)
Slide 4     Community Day OR top-of-week feature event
Slide 5     Raid rotation (the week's big raid swap)
Slide 6     Max Monday Pokémon
Slide 7     GBL cup or PvP feature
Slide 8     Trending Topic teaser (curiosity gap, not the full story)
Slide 9     Don't Miss — deadline callout (one specific thing ending soon)
Slide 10    CTA — "Save this for when you need it" or "DM me 'WEEK' for the full breakdown"
```

If a week has no Community Day, replace slide 4 with the headline event of the week (Raid Day, themed event launch, season opener, etc.). If no Max Monday is featured (rare), replace slide 6 with the raid counter tip for the week's top boss.

## Content Arc: Myth-Busting (when a Trending Topic carries the week)

When the week's most magnetic story is a controversy or community myth (Firestar73 DQ, Spotlight Hour return debates, datamined surprise), the Myth-Busting arc beats Listicle:

```
Slide 1–3   Triple Hook (each teases the controversy from a different angle)
Slide 4     Common Belief — what most players think
Slide 5–7   Why It's Wrong / What Actually Happened (evidence, dates, sources)
Slide 8     Better Approach / What This Means For You
Slide 9     Quick week-in-review (events, raids, one-liner each — high density)
Slide 10    CTA
```

Use Listicle by default. Switch to Myth-Busting only when the Trending Topic is unambiguously the week's lead story.

## Writing Rules (per slide)

### Hook slides (1–3)
- Max 10 words per headline
- Must work with zero prior context
- No pronouns referencing previous slides ("this", "it", "that")
- No "Trainers!" / "Hey trainers!" openers
- Specific Pokémon names beat generic phrasing ("Lechonk's Big Day" > "A new Community Day")

### Content slides (4–9)
- **One idea per slide** — never two
- Max 8 words for the headline
- Max 25 words for the body
- Grade 6 reading level — short words, short sentences
- Lead with a verb or subject, not "Niantic announced..."
- Cite specifics: dates, times, CPs, percentages — same standard as the newsletter

### CTA slide (10)
- One action only — never two options
- Always include the handle: `@landoralpha`
- Make the benefit explicit: `Save this for when you need it` > `Like if you enjoyed`
- Standard rotation:
  - "Save this for when you need it" (default)
  - "Send this to your raid group" (when raid-heavy week)
  - "Follow @landoralpha for daily Pokémon GO tips" (rotation use)
  - "Subscribe to Spawn Point for the full weekly breakdown" (newsletter cross-promo — use sparingly, maybe 1× per month)

## JSON Output Schema

The agent outputs the carousel as a JSON code block matching `/Users/joelandor/Claude-Master/my-carousel-system/`'s schema:

```json
{
  "slug": "spawn-point-week-of-[YYYY-MM-DD]",
  "template": "story",
  "handle": "@landoralpha",
  "global_background": "",
  "slides": [
    {
      "number": 1,
      "type": "hook",
      "headline": "Lechonk's Big Day is Saturday",
      "subtext": "",
      "body": "",
      "image": "",
      "background": "",
      "alt_text_suggestion": "Wide shot of a player using Pokémon GO on a sunny park trail, Lechonk overlay"
    },
    {
      "number": 2,
      "type": "hook",
      "headline": "Three new raid bosses arrive Wednesday",
      "subtext": "",
      "body": "",
      "image": "",
      "background": "",
      "alt_text_suggestion": "Phone screen with raid lobby UI, glowing"
    },
    ...
    {
      "number": 10,
      "type": "cta",
      "headline": "Save this for when you need it",
      "subtext": "",
      "body": "",
      "image": "",
      "background": "",
      "alt_text_suggestion": "Spawn Point logo on dark background"
    }
  ]
}
```

`alt_text_suggestion` is a Spawn Point-specific extension — it tells Joel what kind of background photo to source for each slide. Joel sources the actual images and updates the `background` field before rendering.

`global_background` and `background` fields stay empty in the agent's output — Joel fills them locally after picking images.

## Instagram Caption

After the JSON, output a single Instagram caption that:

- Opens with a 1–2 sentence hook (different from slide 1's headline — the caption is independent context for non-carousel viewers).
- Lists the week's top 3–4 highlights as concise lines (no bullet points — IG strips them; use line breaks).
- Closes with: `Full weekly breakdown in Spawn Point — link in bio.`
- Adds 5–10 hashtags after a line break.

**Hashtag set (rotate 5–10 of these per post):**
- `#PokemonGO` (always)
- `#PokemonGOCommunity` (always)
- `#LandorAlpha` (always — brand)
- `#SpawnPoint` (always — newsletter)
- `#[FeaturedPokemon]` (e.g., `#Lechonk` — pick the week's headline species)
- `#PokemonGOEvents`
- `#PokemonGORaids`
- `#PokemonGOFriends`
- `#PokemonGOCommunityDay` (when a CD falls in the week)
- `#GoBattleLeague` (when a notable cup runs)
- `#MaxBattles` (when Max Monday or 6-Star is notable)

**Caption length:** 800–1,500 characters total (well under IG's 2,200 limit). Hooks and highlights skim well; nobody reads past the third line on mobile.

## What NOT to write in the carousel

Same banned-phrases list as the newsletter (`brand-voice.md`), plus:

- ❌ "Don't miss out!" / "Don't sleep on..." (overused, AI-default)
- ❌ "You won't believe..." (clickbait)
- ❌ "Drumroll please..." (filler)
- ❌ "Let's dive in" (forbidden in any context)
- ❌ Default-filler: "Remote Raid Passes work" / "every day not just weekends" — same rule as raid sections
- ❌ Two CTAs on the same slide
- ❌ Body text on hook slides 1–3
- ❌ Pronouns on hook slides ("this is huge", "it's the best")

## Pre-Publish Audit (carousel-specific)

After generating, verify:

1. **Triple Hook standalone test:** read slide 1 alone — does it land cold? Read slide 2 alone — does it land cold? Slide 3 too. If any hook references "this", "that", "the above", or implies prior context, rewrite.
2. **Headline word count:** every headline ≤ 10 words (hooks) or ≤ 8 words (content).
3. **Body word count:** every body ≤ 25 words.
4. **Grade 6 reading level:** scan for compound words and long sentences. Break or simplify.
5. **No banned phrases.**
6. **CTA single-action:** slide 10 has one action, includes `@landoralpha`.
7. **Caption length:** 800–1,500 characters total.
8. **Hashtag count:** 5–10 (always include the four "always" tags).
9. **Voice check:** read the carousel aloud as if texting a friend — does it sound like Spawn Point or like a brand account?

## Algorithm Signal Priority (for content judgment)

When deciding what makes the carousel vs what gets cut, optimize for:

1. **Saves** — strongest signal. Will a casual player save this to reference Saturday morning? If not, the carousel is too forgettable.
2. **Shares to DMs** — viral coefficient. Is there one slide a player would DM to their raid group?
3. **Swipe-through rate** — does each slide hook into the next? No filler middle.
4. **Dwell time** — are slides scannable in 1–2 seconds each, with one slide deserving a 5-second pause?
5. **Comments** — is there a question or hot take that invites response?
6. **Likes** — weakest signal; ignore.

A carousel that nails saves and shares beats one with a clever hook but no save-worthy content.
