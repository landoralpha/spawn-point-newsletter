# Social Media Copy Generation

The Spawn Point newsletter ships every Monday for the upcoming week. Each week the agent also generates social-media copy adapted for four platforms so the same content can flow across the entire social pipeline. **This file covers the COPY ONLY.** Carousel slides, image rendering, and visual layout are handled by a separate Landoralpha project — the agent does not generate carousel JSON, slide content, or visual specs.

Each weekly run produces a "social pack" with four pieces:

1. **Instagram caption** — 200–300 words, used as the caption for the IG carousel post or as a standalone IG feed post.
2. **Twitter/X** — either a single tweet (≤280 chars) OR a short thread (3–5 tweets) depending on content density.
3. **TikTok/Reels caption** — 100–150 chars, optimized for TikTok's truncated caption display and hashtag-driven discovery.
4. **Facebook post** — 200–400 words, more conversational, hashtags optional.

Brand voice rules from `instructions/brand-voice.md`, the no-default-filler rule, and the gap-acknowledgment principle all apply across every platform.

**Publish day:** Spawn Point ships Saturday. When social copy references when readers will see the new issue, say **Saturday** — e.g., "Out this Saturday" / "New Spawn Point hits Saturday." Don't say "Monday" or any other day. The cron fires Monday for the agent's research/writing window; that's internal, not reader-facing.

## Brand voice still applies

The social copy uses Spawn Point's voice (`brand-voice.md`), the no-default-filler rule (don't say "Remote Raid Passes work" — readers know), and the gap-acknowledgment principle. Stop-slop quick checks apply: cut adverbs, no passive voice, no em dashes, vary sentence rhythm, trust the reader.

Social copy is **shorter and louder** than the newsletter prose. Every sentence pulls weight. Be punchy, not preachy.

## Source content

The social pack summarizes the SAME week as the newsletter. Reference your own newsletter draft (`output/newsletter-draft-[YYYY-MM-DD].md`) for the source-of-truth content. Pick the highest-priority items:

1. Community Day or top-of-week feature event (if any)
2. The week's headline raid swap
3. Max Monday Pokémon (if notable)
4. GBL cup feature (if notable)
5. Don't Miss deadline callout
6. Trending Topic teaser (curiosity gap, not the full story)

A "quiet" week might surface only 2 items. A "busy" week (CD + Mega rotation + new GBL season + Trending Topic) earns the full multi-platform treatment with longer Twitter threads and richer Facebook posts.

## 1. Instagram Caption (200–300 words)

Used as the caption for the carousel post (rendered by the separate carousel project) or as a standalone IG feed post.

**Structure:**
- **Hook (1–2 sentences):** different from the newsletter title — the caption is independent context for non-carousel viewers. Lead with the most magnetic event of the week.
- **Body (3–4 highlights):** concise lines for the week's top items. Use line breaks, not bullet points (IG strips them visually).
- **CTA:** `Full weekly breakdown in Spawn Point — link in bio.`
- **Hashtags:** 5–10 tags after a line break.

**Hashtag set (rotate 5–10 per post):**
- `#PokemonGO` (always)
- `#PokemonGOCommunity` (always)
- `#LandorAlpha` (always — brand)
- `#SpawnPoint` (always — newsletter)
- `#[FeaturedPokemon]` (e.g., `#Lechonk` — pick the week's headline species)
- `#PokemonGOEvents`
- `#PokemonGORaids`
- `#PokemonGOFriends`
- `#PokemonGOCommunityDay` (when CD falls in the week)
- `#GoBattleLeague` (when a notable cup runs)
- `#MaxBattles` (when Max Monday or 6-Star is notable)

**Length:** 800–1,500 characters total (well under IG's 2,200 limit). Most readers don't scroll past the third line on mobile, so front-load the hook.

## 2. Twitter/X — Single Tweet OR Short Thread

Pick ONE per week based on content density.

### Single tweet (≤280 chars, default for quiet weeks)

When the week has 1–2 standout items, pack into a single tweet with one hashtag.

Example:
```
Lechonk Community Day lands Saturday May 9, 2–5 PM local. Evolve Oinkologne (Family of Three) in-window for Mud Slap. Mega Camerupt rotates out Wednesday too. Full breakdown ↓ landoralpha.beehiiv.com #PokemonGO
```

### Short thread (3–5 tweets, for busy weeks)

When 3+ items deserve attention, thread it. Each tweet is self-contained but threads naturally.

- Tweet 1: hook + first highlight (link to newsletter at end)
- Tweet 2: second highlight
- Tweet 3: third highlight
- Tweet 4 (optional): Trending Topic teaser
- Tweet 5 (optional): Don't Miss callout + close

Each tweet ≤280 chars. **Don't number tweets** ("1/4") — wastes characters; the thread visualizes itself.

**Hashtag rules:** Twitter/X favors 0–2 hashtags per tweet. Use `#PokemonGO` once in the thread (usually tweet 1) and the species hashtag (e.g., `#Lechonk`) once if relevant. No hashtag walls.

## 3. TikTok/Reels Caption (100–150 chars)

TikTok's caption box truncates aggressively — the first 60–70 chars are what most viewers see. Lead with the hook.

**Structure:**
- 1 short sentence hook
- 5–8 hashtags (TikTok hashtags are heavily weighted for discovery)

**Hashtag set (rotate 5–8):**
- `#PokemonGO` (always)
- `#PokemonGOCommunity` (always)
- `#PokemonGOTikTok`
- `#PokemonGOTrainer`
- `#[FeaturedPokemon]` (e.g., `#Lechonk`)
- `#PokemonGOFYP` / `#fyp`
- `#PokemonGOEvents`
- `#PokemonGORaids`

Example (143 chars):
```
Lechonk Community Day Saturday — and yes, Oinkologne IS worth evolving 🐷 #PokemonGO #PokemonGOCommunity #Lechonk #PokemonGOFYP #PokemonGOEvents
```

## 4. Facebook Post (200–400 words)

Facebook's algorithm rewards longer, conversational posts. Hashtags carry less weight than on IG/Twitter; treat them as optional flair.

**Structure:**
- **Opener (1–2 sentences):** conversational, friendlier than IG. "Big week ahead for Pokémon GO trainers" tone.
- **Body (3–5 paragraphs):** more detail than IG, paragraph-style not list-style. Cover the same 3–5 weekly highlights with a sentence or two of context per item.
- **Direct link to newsletter:** include `https://landoralpha.beehiiv.com/p/[issue-slug]` inline (Facebook allows clickable links).
- **Hashtags:** optional. If used, keep to 2–3 max (`#PokemonGO`, `#LandorAlpha`).

**Tone difference from IG:** more storyteller-friendly, full sentences, paragraph breaks. Facebook readers expect more context up front before clicking through.

## What NOT to Write (across all platforms)

Same banned-phrases list as the newsletter (`brand-voice.md`), plus social-specific:

- ❌ "Don't miss out!" / "Don't sleep on..." (overused, AI-default)
- ❌ "You won't believe..." (clickbait)
- ❌ "Drumroll please..." (filler)
- ❌ "Let's dive in" (forbidden in any context)
- ❌ Default-filler: "Remote Raid Passes work" / "every day not just weekends"
- ❌ "Tag a friend who..." / "Comment below if..." (engagement bait)
- ❌ More than 10 hashtags on Twitter (looks like spam)
- ❌ Hashtag walls on Facebook (treats FB like Instagram)
- ❌ Numbering thread tweets like "1/4" (wastes characters)

## Output Format

Write to `output/social-pack-[YYYY-MM-DD].md` with this structure:

```markdown
# Social Pack: [Newsletter Monday] – [Newsletter Sunday]

## Instagram Caption

[200–300 word caption with line breaks and hashtags]

---

## Twitter/X

**Format used:** [single tweet | thread]

[the tweet, OR each thread tweet on its own line]

---

## TikTok/Reels Caption

[100–150 char caption with hashtags]

---

## Facebook Post

[200–400 word post with optional hashtags]

---

## Notes (optional)

[Any creative latitude flags, e.g., "Used Twitter thread because four standout items this week" or "Skipped Facebook hashtags — busier post"]
```

This file gets pushed to Notion as a child page under the newsletter (Step 6 Phase 3). Each section becomes a Notion code block so Joel can copy-paste verbatim with formatting intact.

## Pre-Publish Audit (social-specific)

After generating the pack, verify:

1. **Hook test:** read each platform's opening sentence cold. Does it grab? Or does it sound like a press release?
2. **Length checks:**
   - IG caption: 800–1,500 chars
   - Twitter single tweet: ≤280 chars
   - Twitter thread: each tweet ≤280 chars
   - TikTok caption: 100–150 chars
   - Facebook: 200–400 words
3. **Hashtag rules per platform.** IG: 5–10 including the four "always" tags. Twitter: 0–2 per tweet. TikTok: 5–8 with `#PokemonGOFYP` or `#fyp`. Facebook: 0–3, optional.
4. **Link inclusion:** newsletter link present where appropriate (Facebook inline, IG "link in bio", Twitter direct URL, TikTok "link in bio" if mentioned).
5. **Default-filler scan:** no "Remote Raid Passes work" / "every day not just weekends".
6. **Banned-phrases scan** (full list above).
7. **Voice check:** read aloud. Sounds like Spawn Point, or like a brand account?
8. **Cross-platform de-duplication:** the four pieces should NOT be near-identical text. Each platform has its own structure, length, and tone. If the IG caption and Facebook post are 90% the same words, rewrite the Facebook to be more storyteller-style.
