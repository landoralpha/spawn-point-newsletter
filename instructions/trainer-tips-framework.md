# Trainer Tips Framework

For every event, raid rotation, or feature in the newsletter, run through this checklist to find the best strategic tips. Not every angle applies to every event. Pick the 1-2 most valuable tips per section.

## Checklist: Angles to Evaluate

### 1. Stardust Optimization
**Bonus Stardust Pokémon** - These Pokémon give extra Stardust when caught (base values before bonuses):
- 750 Stardust: Staryu, Meowth (all forms), Paras, Parasect, Shellder
- 500 Stardust: Trubbish, Audino, Chimecho, Combee
- Weather-boosted catches add 25% more Stardust

**Star Piece Stacking** - When to recommend Star Pieces:
- Any event with Stardust multiplier (2x, 3x catch Stardust)
- GO Battle Thursday (4x Stardust from wins) + Star Piece = 6x
- Raid Day events with multiple raids
- Community Day last-hour push
- Stack: Star Piece + event bonus + weather boost + bonus Stardust Pokémon = massive returns
- Star Piece lasts 30 minutes. Time it around peak activity.

**Stardust Event Math** - Show readers the multiplier:
- Base catch = 100 Stardust
- 2x event bonus = 200
- Star Piece (1.5x) on top = 300
- Weather boost (1.25x) = 375
- Bonus Pokémon (e.g., Staryu at 750 base) with all multipliers = significantly more

### 2. XP Optimization
**Lucky Egg Stacking** - When to recommend Lucky Eggs:
- Friendship level-ups (Best Friend = 100,000 XP base, 200,000 with Lucky Egg)
- Community Day (evolving sprees during 2x evolve XP)
- Raid Hour (multiple raids in sequence)
- Any event with XP multiplier
- Stack: Lucky Egg + event XP bonus + Excellent throws

**XP Sources by Value:**
- Best Friend level-up: 100,000 XP (200K with Lucky Egg)
- Ultra Friend level-up: 50,000 XP
- Legendary raid catch: 10,000 XP
- Excellent curve throw: ~2,000 XP (with bonuses)
- Evolving: 1,000 XP per evolution (2,000 with Lucky Egg)
- Tip: Coordinate friendship level-ups during XP events for maximum value

### 3. Item Strategy
**What to use when:**
- **Pinap Berry**: When candy is the bottleneck (rare spawns, raid bosses you need candy for)
- **Silver Pinap Berry**: Rare Pokémon with shiny chance (better catch rate + double candy)
- **Golden Razz Berry**: Shiny Legendary in raids, high-IV targets
- **Incense**: During boosted Incense events (Double-Time Sunday, specific events)
- **Lure Modules**: Friendship Friday (attract others for trades), Community Day
- **Remote Raid Passes**: Save for Legendary rotations you need, not common bosses
- **Premium Battle Pass**: GO Battle Thursday for 4x Stardust per set

**Resource Management Tips:**
- Don't burn Rare Candy on Pokémon available in the wild. Save for Legendaries.
- Poffins double buddy walking distance. Time them for Adventure Sync reward windows.
- Elite TMs: only use on confirmed meta picks, never speculative.

### 4. PvP Meta Relevance
For any Pokémon featured in events, raids, or spawns, pull data from PvPoke directly. See `instructions/meta-data-sources.md` for the JSON endpoints. Do NOT rely on articles for rankings - they go stale fast.

**Data source:** `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/{cup}/overall/rankings-{cap}.json`

**Is it relevant in Great League (1500 CP)?**
- Pull PvPoke JSON, find by `speciesId`. Top 50 = worth mentioning.
- Cite specific rank, score, and recommended moveset
- IV priority for GL: 0/15/15 or similar (low attack, high defense/HP)

**Is it relevant in Ultra League (2500 CP)?**
- Top 30 = worth mentioning
- IV priority: 0/15/15 for most, 15/15/15 for some Legendaries that max below 2500

**Is it relevant in Master League (no CP cap)?**
- Legendaries and pseudo-Legendaries dominate
- IV priority: 15/15/15 (hundos matter here)
- Mention if the raid boss is a ML pick

**Current Cup/Special Format:**
- If a special cup is running (Fantasy Cup, Retro Cup, Jungle Cup, etc.), swap the cup slug into the JSON URL
- Note type restrictions and which featured spawns fit

**Tip phrasing rule:** Cite specifics from PvPoke. "Oinkologne sits at #14 in Great League with a Mud Slap / Body Slam / Play Rough moveset (PvPoke score: 87)" beats "Lechonk is a top GL pick."

### 5. Raid & PvE Meta Relevance
Pull counter data from Pokebattler directly. See `instructions/meta-data-sources.md` for JSON endpoint patterns. Do NOT rely on articles for counter recommendations.

**Data source:** `https://fight.pokebattler.com/raids/defenders/{POKEMON_ID}/levels/{TIER}/...`

For raid bosses and event Pokémon, check:
- **Raid attacker ranking**: Pull Pokebattler JSON, sort by `total.estimator` (lower = better). Top 10 attackers from `data.attackers[0].randomMove.defenders`.
- **Shadow variant**: Is the Shadow version a top-tier attacker? (Skip Frustration/Return movesets)
- **Mega evolution**: Does Mega energy drop from Mega raids this week?
- **Future relevance**: Will this Pokémon get a Community Day move or signature move later? (flag "might be worth holding candy")

**Tip phrasing rule:** Cite specifics from Pokebattler. "Top counters: Shadow Salamence (Dragon Tail / Outrage), Shadow Garchomp (Dragon Tail / Outrage)" beats "Use strong Dragon-types."

### 6. Type Effectiveness for Raids/Max Battles
For every new raid boss or Max Monday Pokémon:
- List the boss's weaknesses (super effective types)
- Name the top 3 counters with specific moves
- Name 2-3 budget counters (non-Legendary, non-Shadow, commonly available)
- Note double weaknesses if applicable (e.g., Tyranitar is double-weak to Fighting)

### 7. Medal & Badge Progress
**Type Medals** - Catching Pokémon of a specific type contributes to that type's medal:
- Catch thresholds: Bronze: 10, Silver: 50, Gold: 200, Platinum: 2,500
- **Catch rate multiplier (community-derived from datamining; Niantic doesn't publish exact values):** Bronze 1.1x, Silver 1.2x, Gold 1.3x, Platinum 1.4x
- **Dual-type Pokémon:** Average of the two medal multipliers (e.g., Bronze Water + Platinum Ground on Quagsire = 1.25x)
- The "+1/+2/+3/+4" community shorthand approximates these multiplier-based bonuses; cite "multiplier" framing for accuracy
- If an event floods spawns of a specific type, mention the medal grind opportunity
- Example: Steel-type event = good time to push the Steel medal, which helps catch future Steel-types

**Other Medals to Watch:**
- Collector: total Pokémon caught
- Scientist: total Pokémon evolved
- Battle Legend: GBL wins
- Champion: raids completed
- Successor: Dynamax wins
- Best Buddy: buddy distance + interactions
- Pilot: trade distance (Friendship Friday = good time for long-distance trades)
- Lucky Trade medal: track Lucky Trades on Friendship Friday

### 8. Bonus Stacking Combinations
These are the high-value combinations to flag:

**Stardust Stack:**
- Event Stardust bonus + Star Piece + GO Battle Thursday + weather boost
- Example: "Pop a Star Piece before your GO Battle Thursday sets. With the event's 2x Stardust and Thursday's 4x win bonus, each win reward hits hard."

**XP Stack:**
- Event XP bonus + Lucky Egg + Excellent throws + friendship level-up
- Example: "Coordinate a Best Friend level-up during this event's 2x XP window with a Lucky Egg running for 400,000 XP from a single interaction."

**Candy Stack:**
- Event candy bonus + Pinap Berry + transfer during 2x transfer candy
- Example: "Catch with Pinap, then transfer during the event's 2x transfer candy window for 9 candy per catch instead of 3."

**Catch Stack (Community Day):**
- Incense + Lure + Star Piece + Lucky Egg + Pinap/Silver Pinap
- Time these for the featured move window

### 9. Event-Specific Timing
- **Frustration removal windows**: TM away Frustration from Shadow Pokémon during specific events. Always flag when this is available.
- **Exclusive/Legacy moves**: Community Day moves, event-exclusive moves. Note the deadline.
- **GO Pass deadlines**: When do free/paid pass rewards expire?
- **Special Trade windows**: Events with extra Special Trades (normally 1/day, some events give 2-3)
- **Remote Raid changes**: Events that increase the daily Remote Raid limit

### 10. Resource Prep Reminders
For big upcoming events, remind readers to:
- Clear Pokémon storage before Community Day
- Stock up on Pinap Berries or Star Pieces
- Walk buddy for candy before evolution events
- Save Rare Candy for incoming Legendary raid boss
- Open gifts to get close to friendship level-ups (but don't trigger them until Lucky Egg is ready)

### 11. Shiny Hunting Efficiency
Know the current shiny rate tiers (post-Memories in Motion flattening, March 2026). See `instructions/shiny-odds-reference.md` for the full table.

**Rates safe to cite (well-established data):**
- Community Day: ~1/25
- Raid Day / Research Day / Hatch Day: ~1/10
- Legendary/Mythical/Ultra Beast raids (Five-Star): 1/20
- Non-Five-Star raids (1-4 Star): 1/64
- Egg hatches: 1/64
- Wild (all species): 1/512

**Rates NOT to cite (say "boosted shiny odds" instead):**
- GO Fest / Safari Zone, standard event boosts, Catch Mastery, Rocket Leaders, Mega raids
- These rates are community-estimated. Niantic could vary them. Never guess a number.

**Critical change:** As of March 3, 2026, all wild shiny rates were flattened to 1/512. The old perma-boost system (1/64 for species like Onix, Scyther, Rockruff, Sandile, etc.) no longer applies to wild encounters. Raids and eggs were standardized to 1/64, which only mattered for common species (rare species were already 1/64). Previously raid/egg-locked species no longer carry their boosted rate into the wild during events.

**Tip implications:**
- Stop recommending wild shiny hunting for formerly perma-boosted species as if they have better odds. They don't.
- Raids and eggs are now the best non-event shiny hunting methods for rare species (1/64 vs 1/512 wild).
- At paid events, previously perma-boosted species no longer carry their old premium rate. Say "boosted shiny odds for ticket holders" without citing a number.
- When an event says "increased shiny odds," write "boosted shiny odds during the event." Do not guess a rate.

**Quick-catch technique** nearly doubles encounters per hour by skipping the catch animation. Recommend it for time-limited events like Community Day or Raid Day.
- Example: "Community Day is 3 hours. Use quick-catch to hit 300+ encounters instead of 150. That's roughly 12 shinies at the 1/25 rate."

### 12. Mega Evolution & Primal Reversion

For complete mechanics, Mega Levels (Base / High / Max / Super Max), rest periods, Mega Energy sources, the Mega-Evolved attack boost (Niantic FAQ #3334; do NOT write "aura" in newsletter copy), Super Mega Raid Day catch bonuses, the spend-to-level mechanic, and Primal Reversion details, see `instructions/mega-evolution-reference.md`. The reference now includes a **consolidated benefits-per-Mega-Level cheat sheet** (added 2026-06-24).

Quick reference (Mega Level benefits):

| Mechanic | Base | High | Max | Super Max |
|---|---|---|---|---|
| Same-type catch Candy | +1 | +2 | +3 | >+3 |
| Same-type catch XP | none | +50 | +100 | greater |
| Same-type Candy XL chance | 0% | +10% | +25% | greater |
| Rest period after 8-hr active | ~7 days | ~5 days | ~3 days | **24 hrs** |
| Mega-Evolved attack boost (party bonus in raids) | +30% type-match / +10% other (does NOT scale by level) ||||

- **Mega active duration:** 8 hours per use
- **One Mega/Primal active** per trainer at a time
- **Mega-Evolved attack boost** (raid bonus, per Niantic FAQ #3334 — Niantic does NOT use "aura"; do not write "Mega aura" / "type aura" in newsletter copy): +30% type-matched / +10% other types to OTHER trainers in lobby. Bringer is EXCLUDED unless another trainer also has an active Mega/Primal. Attack boosts do NOT stack — only the highest boost applies per attack type.
- **Mega Levels progress only ONCE per individual per day via free Evolution.** Reaching Max = 30+ days minimum on the free path.

**Spend-to-level (live May 23, 2026):** Trainers can spend that species' Mega Energy to push the Mega Level at ANY level — Base → High, High → Max, or Max → Super Max. Cost scales DOWN with prior Mega Evolution count for that species (the more times you've already Mega Evolved it, the cheaper each level becomes). Specific costs not published by Niantic. Mega Energy is per-species, NOT generic — Beedrill Energy only levels Mega Beedrill.

**Super Mega Raid Day catch bonus (standing rule since Falinks, May 23, 2026):** Every catch from a Super Mega Raid Day comes with **Mega Level 1 already unlocked**. Trainers do NOT pay the initial Mega Energy cost for their first Mega Evolution of that species. Confirmed across Falinks, Mewtwo X/Y (GO Fest 2026 Global), Skarmory. Treat as standing mechanic for ALL future Super Mega Raid Day events — do not call it "new" for each one after Falinks.

**Primal Reversion (Groudon and Kyogre only):**
- Same 8-hour duration, separate Primal Energy resource
- Primal Groudon boosts Fire/Grass/Ground at +30% (other types +10%)
- Primal Kyogre boosts Water/Electric/Bug at +30% (other types +10%)
- Primal Energy NOT earned from buddy walking (only Mega Energy is)
- Primal attack boost is strictly stronger than Mega-Evolved attack boost for its boosted types

**2026 changes (Pokémon GO Tour: Kalos, Feb 28 – March 1, 2026):**
- New Super Max Mega Level
- Super Mega Raids (require ≥7 trainers)
- Link Charges + Link Holder system
- Mega Energy storage cap raised to 10,000 (Primal still 9,999)
- Mega Mewtwo X/Y debut at GO Fest 2026 Global (July 11–12, 2026, free)

- Example: "Grass-type event? Mega Evolve Venusaur (or Primal Groudon if you have one) before your catching session. Mega gets +1/+2/+3 Candy on Grass catches at Base/High/Max levels. Primal Groudon goes harder, boosting Fire/Grass/Ground catches with both Candy AND XL chance — best for the long-term level grind."

### 13. Candy XL Farming
296 XL Candy needed to max a Pokémon from L40 to L50. Key sources:
- Catching L31+ Pokémon (weather-boosted spawns guaranteed L31+)
- Trading gives a passive XL chance (higher at greater distance)
- Walking buddy earns XL at 1 per walk distance at L31+
- Converting 100 regular Candy = 1 XL Candy
- Mega Evolution bonus increases XL drop rate on same-type catches

- Example: "Weather-boosted Machop spawns at L31+, giving passive XL drops. Mega Evolve a Fighting-type and trade extras before transferring for max XL yield."

### 14. Weather Boost Awareness
Weather-boosted Pokémon:
- Spawn at L25-35 (vs normal L1-30)
- Have a 4/4/4 IV floor
- Give 25% more Stardust per catch
- Give passive XL Candy chance at L31+

Check which event spawns align with local weather. Weather-boosted catches during a Stardust event with Star Piece = massive returns.
- Example: "Rainy weather during the Water Festival? Water-types spawn at higher levels with better IVs and 25% bonus Stardust. Prioritize those over non-boosted spawns."

### 15. PvP IV Optimization (Stat Product)
For Great League and Ultra League, ideal IVs are LOW Attack / HIGH Defense / HIGH HP (e.g., 0/15/15). Attack inflates CP faster, so low-attack Pokémon fit more total stats under the CP cap.
- Wild catches: 0/0/0 IV floor (best for PvP IVs)
- Trades by friendship level: No hearts 0/0/0, Good 1/1/1, Great 2/2/2, Ultra 3/3/3, Best 5/5/5
- Research/raids/eggs: 10/10/10 floor (bad for PvP IVs)
- Good/Great Friend trades give the lowest IV floors and best PvP IV odds

- Example: "Stunfisk in event research has a 10/10/10 IV floor, too high for good PvP IVs. Trade your extras with a Good Friend instead. Good Friend trades re-roll from 1/1/1, giving you a real shot at rank 1."

### 16. Trading Strategy & Lucky Coordination
- Lucky Friends: ~1.1% per daily Best Friend interaction. Guaranteed 12/12/12 IVs, half Stardust to power up. Hundo odds: 1/64.
- Best Friend trades (non-Lucky): 5/5/5 IV floor, hundo odds 1/669 (with 5% Lucky chance factored in)
- Lucky guarantee: Trade a Pokémon caught before August 2016 (45 lifetime limit)
- Special Trades: 1/day normally, 2-3 during events or Friendship Friday
- Distance trades: bonus Candy based on catch distance + Pilot Medal progress
- **Shadow Pokémon CANNOT be traded.** Only Purified Pokémon can be traded. Never suggest trading Shadow Pokémon.
- See `instructions/hundo-odds-reference.md` for complete hundo odds by trade friendship level.

- Example: "Dialga leaves raids next week. Lucky Friend trades give 1/64 hundo odds vs 1/216 from raids. Coordinate a Lucky trade before the rotation for your best shot at a perfect Dialga."

### 17. Egg Pool & Hatch Strategy
Event-specific egg pools change what hatches from 2km, 5km, 7km, and 10km eggs. Key tactics:
- Clear egg slots the night before an event to fill with event eggs
- Super Incubators (1.5x speed) only on 10km/12km eggs. Regular incubators on 2km.
- Adventure Sync 50km reward eggs have an exclusive pool (Riolu, Goomy, Dreepy)
- Keep 2 egg slots open before Monday 9am for Adventure Sync rewards

- Example: "New 7km egg pool drops Tuesday with Frigibax. Clear your egg slots Monday night. Pick up 7km eggs from gifts during the event window."

### 18. Research Encounter Stacking
Complete Field Research tasks but flee the encounter to "stack" rewards (up to 100). Claim them during bonus Stardust/Candy/XP events for amplified rewards.
- High-value stack targets: Audino (2,100 Stardust), Chansey, Combee (750 Stardust)
- Stack throughout the week, claim during weekend events with Star Piece running

- Example: "Double Stardust event starts Saturday. Stack Audino and Combee research encounters this week, then claim them all Saturday with a Star Piece running."

### 19. Collection Challenges & Dex Completion
Events often include Collection Challenges with deadlines and rewards (Elite Collector medal, Stardust, Rare Candy). Also watch for:
- Region-locked Pokémon appearing globally during GO Fest or special events
- New shiny releases (first day = highest community excitement and trading value)
- Pokedex-first catches that should be prioritized before the event window closes

- Example: "Torkoal and Pachirisu spawn globally during GO Fest. These are normally region-locked. Catch multiples and stock Candy now."

### 20. Buddy & Best Buddy Optimization
- Best Buddy gives a +1 level CP boost (can hit critical PvP breakpoints)
- Poffin doubles hearts earned and halves walking distance for 6 hours
- Match your buddy to the current event type for Mega Energy via walking
- Excited mood (feed, play, snapshot, battle, walk) doubles hearts for the day

- Example: "Your PvP Medicham is 2 hearts from Best Buddy. The CP boost pushes it past a key Ultra League breakpoint. Prioritize buddy activities today."

### 21. Dynamax & Max Particle Management

For complete mechanics, particle math, Max Move tier costs, and Gigantamax roster, see `instructions/dynamax-reference.md`.

Quick reference:
- Max Particle daily soft cap: 800 (resets 5:00 AM local). Storage cap: 1,500.
- Walking: 300 MP per 2 km. Power Spots: 120 MP first interaction, 100 MP/spot/day after.
- Battle costs: 250 MP (1-star), 400 MP (3-star), 800 MP (5-star, 6-star Gigantamax). Particles consumed only on victory.
- Team roles: Attacker (typed Max Move), Defender (Max Guard), Healer (Max Spirit). Niantic-recommended 4-player split: 2/1/1 (attackers/healer/tank).
- 17 Gigantamax species in Pokémon GO as of May 2026. G-Max moves outclass standard Max Moves; prioritize G-Max forms.
- Eternatus Dynamax Cannon Adventure Effect can push Max Moves to Lvl 4 (above the normal cap of 3).

**CRITICAL: Only Dynamax-capable Pokémon can participate in Max Battles.**
- Not every Pokémon in the game can Dynamax. Only Pokémon released as Dynamax-eligible can fill any team slot (attacker, defender, or healer).
- **Shadow Pokémon CANNOT be brought into Max Battles at all.** They cannot Dynamax and cannot fill any team slot. Do not consider Shadow Pokémon when suggesting Max Battle teams.
- Before suggesting Max Battle counters, verify against current Pokémon GO Hub Max Battle tier lists (Attackers, Defenders, Healers).
- A Pokémon being strong against the featured type is NOT enough. It must be Dynamax-capable AND non-Shadow.

**Note on Adventure Effects:** Adventure Effects are a SEPARATE mechanic from Dynamax. They are tied to specific Charged Attacks on a small Legendary roster (Origin Formes, Fusions, Crowned Forms, Necrozma, Eternatus). Mega and Primal Pokémon do NOT have Adventure Effects. The only Adventure Effect that interacts with Dynamax is Eternatus's Dynamax Cannon. See `instructions/adventure-effects-reference.md` for the full list.

- Example: "Gigantamax Gengar this weekend. Farm particles all week (walk + Power Spot visits) to enter 3-4 battles on event day. If you have Eternatus, run Dynamax Cannon (5,000 Stardust + 30 Candy) before entering to push your Max Moves to Lvl 4."

### 22. Shadow Pokémon Triage (Keep vs. Purify)
Shadow Pokémon deal 20% more damage but take 20% more damage. Decision tree:
- **Keep Shadow**: Top raid attackers (Shadow Mewtwo, Shadow Machamp, Shadow Metagross). The 20% attack bonus outweighs any IV improvement from purifying.
- **Purify**: Species with Mega Evolutions (Shadow can't Mega Evolve). Pokémon with 13/13/13+ IVs that become hundos when purified (+2 to each stat). Pokémon you want for PvP where bulk matters more than attack (Return is a solid PvP charge move).
- **Shadow Pokémon CANNOT be traded.** Only Purified Pokémon can be traded. If you want to trade a Shadow Pokémon, you must purify it first.
- **Shadow Pokémon CANNOT be brought into Max Battles at all.** They cannot Dynamax and cannot fill any team slot. Never consider Shadow Pokémon for Max Battles.

**Shadow IV Floors & Purification Hundo Odds:**
- Grunt/Leader Shadows: 0/0/0 IV floor (1/4,096 hundo). Purifying 13+ IVs = 1/152 hundo chance.
- Giovanni Shadows: 6/6/6 IV floor (1/1,000 hundo). Purifying 13+ IVs = 1/37 hundo chance.
- Shadow Raids: 6/6/6 IV floor (1/1,000 hundo). With IV Boost: 7/7/7 (1/729 hundo).
- Shadow Raid with IV Boost, purifying 13+ = 1/27 hundo chance (tied for best odds in the game).

- Example: "Shadow Mewtwo from Giovanni has a 6/6/6 IV floor, so 1/1,000 hundo odds. Keep it Shadow even with bad IVs. The 20% attack bonus outweighs perfect IVs. But that 14/14/14 Shadow Beedrill from a Grunt? Purify it for a hundo and Mega eligibility."

### 23. Post-Event Transfer Timing
Don't mass-transfer immediately after events. Hold catches for:
- 2x Transfer Candy events (often tied to Spotlight Hours or special events)
- Tag catches during events for easy sorting later
- Use `@special` search filter before transferring to avoid deleting exclusive-move Pokémon
- Evolve before transferring when you need Candy for later evolutions

- Example: "Caught 400 Tepig on Community Day? Tag them and wait for next week's 2x Transfer Candy window. You'll double your Candy return on every transfer."

### 24. Adventure Sync Weekly Rewards
Hitting walking thresholds before Monday 9am:
- 25km: 3,000 Stardust, 500 XP, assorted items
- 50km: 10,000 Stardust, 1,500 XP, exclusive 10km egg pool (Riolu, Goomy, Dreepy)
- Keep 2 egg slots open before Monday morning to receive reward eggs
- Disable battery saver / low power mode if steps aren't counting

- Example: "Walk 50km this week for the exclusive egg pool. Make sure you have 2 open egg slots before Monday 9am or you'll miss the reward eggs."

### 25. Mystery Box / Meltan Timing
Transferring to Pokémon HOME opens a Mystery Box (60-minute Meltan spawns, 3-day cooldown).
- Shiny Meltan only available during specific limited events
- Melmetal is a top Master League pick. XL grinding during shiny windows is efficient.
- Reduced cooldown during special events (can open more frequently)

- Example: "Steeled Resolve event activates Shiny Meltan and reduces Mystery Box cooldown. Open your box during the event. At ~1/125 shiny rate with 60 minutes of spawns, you have a solid shot."

### 26. Raid Catch Optimization
Circle-lock technique: hold the ball, wait for the attack animation, release during a small circle window. Maximizes Excellent throw rate on Legendaries.

Catch probability stacking:
- Golden Razz Berry: highest catch rate multiplier
- Excellent Curve Throw: ~2x catch rate
- Type Medal multiplier (community-derived): Bronze 1.1x, Silver 1.2x, Gold 1.3x, Platinum 1.4x
- All three combined gives the best possible catch odds per ball

Type medals matter. If a new Legendary raid boss arrives and you don't have a Platinum medal for its type, flag the gap.
- Example: "Tapu Koko is Electric/Fairy. Your Electric and Fairy type medals directly boost your catch rate. Platinum gives +4 per throw. If either medal is below Gold, prioritize catching those types this week."

### 27. GO Pass & Ticket Value Assessment
For every ticketed event or monthly GO Pass, evaluate:
- What does the free tier give? (Always list this first)
- What does the paid tier add? (Exclusive encounters, items, bonuses)
- Is the paid version worth it for casual players? Hardcore?
- GO Pass deadlines: when do rewards expire?

- Example: "The free GO Pass gives an Entei encounter and basic tasks. The Deluxe Pass ($4.99) adds a Lucky Trinket, extra Rare Candy, and a second encounter. If you raid regularly, the Rare Candy alone covers the value."

### 28. Special Evolution Methods
Many Pokémon have non-standard evolution paths. Flag these when featured Pokémon have them:
- **Trade evolutions** (0 Candy after trading): Machoke, Haunter, Kadabra, Boldore, Gurdurr, Phantump, Pumpkaboo, Shelmet/Karrablast
- **Lure evolutions**: Glacial Lure (Glaceon), Mossy Lure (Leafeon), Magnetic Lure (Magnezone, Probopass), Rainy Lure (Sliggoo to Goodra)
- **Walking evolutions**: Feebas (20km + 100 Candy), Eevee (10km for Espeon/Umbreon)
- **Eevee naming tricks**: one-time-use name trick for each Eeveelution

- Example: "Machop spawns boosted this event. Trade your Machokes with friends before evolving. Traded Machokes evolve to Machamp for 0 Candy instead of 100."

### 29. Photobomb Encounters
GO Snapshot during events can trigger photobomb encounters with featured Pokémon:
- Some events give 5+ photobombs per day with shiny chance
- Daily Smeargle photobomb (1 per day outside events)
- Takes 10 seconds per attempt. Free encounters.

- Example: "During GO Fest, open GO Snapshot 5 times for bonus encounters with event Pokémon. Each one can be shiny. Ten seconds per photobomb, so there's no reason to skip it."

### 30. Elite TM Priority
Elite Fast TMs and Elite Charged TMs unlock legacy or Community Day moves. These are rare (1-2 per season from GBL). Don't waste them.
- **Worth an Elite TM**: Metagross (Meteor Mash), Swampert (Hydro Cannon), Mewtwo (Psystrike or Shadow Ball), Salamence (Outrage)
- **Not worth an Elite TM**: Anything not in the PvP or PvE top tier, or anything returning to raids/events soon
- If a Community Day move was missed, check whether the Pokémon is meta-relevant before using an Elite TM

- Example: "Missed Hydro Cannon on your Swampert during Community Day? Swampert is a top-5 Great League pick. That's one of the few Pokémon worth an Elite Charged TM."

### 31. Raid Lobby Strategy
Splitting into smaller groups by team color earns more Premier Balls:
- Team Damage Bonus: +1 to +3 balls based on your team's % of total damage
- Gym Control Bonus: +2 balls if your team controls the gym
- More balls = more catch attempts = more Candy per raid

Triggers during Raid Hour, Raid Day, and any event with bonus raids.
- Example: "During Raid Hour, split lobbies by team color. A 6-person Valor group deals more team damage than 18 mixed players, earning you 2-3 extra Premier Balls per raid."

### 32. Gym Coin & Berry Strategy
50 coins/day max from gym defenders. Passive Stardust and Candy from feeding berries:
- Feed a berry to a gym defender: 20 Stardust per berry, ~1/85 chance of Candy for that species
- Burn excess Nanab and Razz berries here
- Golden Razz fully restores motivation (save for defending during EX Raid invites or contests)
- Gym badge progress: higher badge level = more items from spinning that gym

- Example: "Sitting on 200 Nanab Berries? Feed them to gym defenders for 4,000 Stardust and a chance at rare Candy drops. It clears bag space and earns passive rewards."

### 33. Remote Raid Coordination
- Poke Genie, Campfire, and community Discords connect you with raid groups worldwide
- Remote Raid daily limit: 10 (doubles to 20 during some events)
- Prioritize remote passes for Legendaries leaving soon over ones staying another week
- Remote raids deal slightly less damage than in-person, so groups need to be slightly larger
- **Shadow Raids are remote-raidable.** [INTERNAL REFERENCE ONLY — DO NOT include this in newsletter copy. Per `feedback_shadow_raid_remote_default.md`, treat remote-raidability as silent default; mentioning it is default-filler. Only flag the exception when a specific Shadow Raid event is explicitly in-person only per Niantic's announcement.]
- **The monthly featured Legendary Shadow Pokémon raids EVERY DAY during its window**, not just on weekends.
- **1-Star and 3-Star Shadow Raids can also appear during the week**, not just weekends. Always check the current rotation for active Shadow Raids on any tier.

- Example: "Tapu Koko leaves raids Tuesday. If you still need a shiny or high-IV catch, use Poke Genie to join remote raids this weekend before the rotation."

### 34. Lure Module Types
Different lure types attract different spawns and enable specific evolutions:
- **Standard Lure**: general spawns, 30 minutes (60 on Double-Time Sunday)
- **Glacial Lure**: Ice-types + Glaceon evolution
- **Mossy Lure**: Grass/Bug-types + Leafeon evolution
- **Magnetic Lure**: Electric/Steel-types + Magnezone, Probopass evolution
- **Rainy Lure**: Water/Bug-types + Goodra evolution (Sliggoo)
- **Golden Lure**: rarer spawns + chance for Coin Bag (Gimmighoul)

Double-Time Sunday doubles lure duration. Stack event bonuses with the right lure type.
- Example: "Double-Time Sunday + Glacial Lure = 60 minutes of boosted Ice-type spawns. If you need Glaceon, evolve your Eevee near the lure instead of spending 25 Candy on a random Eeveelution."

### 35. Breakpoints & Power-Up Efficiency
A breakpoint is the level where a fast move deals +1 extra damage to a specific raid boss. Powering up past the breakpoint wastes Stardust for zero extra damage.
- Most Pokémon hit a key breakpoint around L30-35 (about 75% of max damage for 25% of the cost)
- L40 is the soft cap. L40 to L50 costs more Stardust/Candy than L1 to L40 combined.
- For raid counters, L30 is usually "good enough." L35 for frequent raiders. L40+ for short-person or solo attempts.

- Example: "Powering up Shadow Machamp to L30 costs roughly 120,000 Stardust. Going from L30 to L40 costs another 150,000 for only ~10% more damage. For most players, L30 is the sweet spot."

### 36. Hundo Hunting Strategy
Know where to invest time based on hundo odds (see `instructions/hundo-odds-reference.md` for full table):
- Mighty Pokémon: 1/27 (best odds in the game)
- Lucky Friend trades: 1/64
- Research/Raids/Eggs: 1/216
- Best Friend trades: 1/669 (with 5% Lucky chance)
- Weather-boosted wild: 1/1,728
- Standard wild: 1/4,096

When a rare Pokémon appears in raids AND is tradeable, compare: raid for 1/216 odds, or save Lucky trades for 1/64. For Pokémon you plan to max out (Legendaries, ML picks), Lucky trades also halve the power-up Stardust cost.

- Example: "Rayquaza in Five-Star raids gives 1/216 hundo odds per catch. If you're sitting on a Lucky Friend trade, that's 1/64 odds and half the Stardust to power up. Save your Lucky trade for Rayquaza before it leaves."

### 37. Team GO Rocket Balloon Schedule
Rocket balloons appear on a fixed schedule. The schedule changes during Takeover events.

**Normal schedule (every 6 hours):**
- 12:00 AM, 6:00 AM, 12:00 PM, 6:00 PM local time
- Each balloon stays for ~20 minutes after spawning
- Open the game during these windows or you'll miss the balloon

**Takeover event schedule (every 2 hours):**
- 12:00 AM, 2:00 AM, 4:00 AM, 6:00 AM, 8:00 AM, 10:00 AM
- 12:00 PM, 2:00 PM, 4:00 PM, 6:00 PM, 8:00 PM, 10:00 PM
- 12 balloons per day instead of the normal 4

**When to flag this:**
- Any Team Rocket Takeover event (balloons rotate every 2 hours)
- Events featuring new Shadow Pokémon or Giovanni encounters
- Frustration TM removal windows (always tied to Rocket events)
- Shadow raid weekends

- Example: "Taken Over runs through Sunday. Balloons appear every 2 hours instead of 6, giving you 12 chances per day to battle Leaders and farm Shadow Pokémon. Log in at 12:00, 2:00, 4:00, 6:00, 8:00, and 10:00 (AM and PM) for each balloon."

### 38. Pokédex Search Operators
Power-user search strings for cleanup, evolves, and PvP triage. See `instructions/community-tips.md` section 1 for the full list.

Key operators:
- `&` (AND), `,` (OR), `!` (NOT)
- IV stars: `0*` (trash), `4*` (hundo), `3*` (93%+)
- `@special` finds untradeable move sets - run BEFORE bulk-TMing
- `@2dragon` finds every Dragon-type charged attacker
- `cp-1500&3*&!legacy` = high-IV GL candidates excluding Pokémon with legacy moves
- Tag filters: `legendary`, `lucky`, `shiny`, `shadow`, `purified`, `xxs`, `xxl`

Mass evolve speedup: rename evolve candidates to `a` or `1` so they cluster at the top of the list. Saves 8-12 evolves per Lucky Egg.

- Example: "Before mass-TMing your Charizards, run `dragon&@special` to filter out anything with Dragon Breath you might want to keep. Legacy moves are gone forever once TM'd over."

### 39. Friend, Gift & Postcard Strategy
- 30 gifts opened/day cap. 1 sent/friend/day. No receive cap.
- Friend list cap: 650 (raised from 450 in 2026)
- Postcard Book holds 350. Pinned postcards from international friends are the only path to Vivillon's 18 patterns.
- Bag capacity unlocks: L43/53/63/73 add +5 gift bag capacity each (max 40)

Strategy:
- Stockpile gifts on weekends, open the daily max of 20/day during friendship XP boost events (the open cap is 20/day, not 30)
- Use international friends specifically for Vivillon postcard patterns
- L31+ players: in-person trades give 1 guaranteed XL Candy + 1 regular candy

- Example: "Friendship Friday this week. Stockpile gifts now and open your 20 Friday with a Lucky Egg active to compound the friendship XP boost."

### 40. Daily Streak Bonuses
**7-day PokéStop streak:** 2,500 XP + bonus items, day 7 guaranteed Evolution Item
**7-day catch streak:** 2,500 XP + 3,000 Stardust, plus 500 XP / 600 Stardust on first daily catch

Mechanics:
- Multiple spins/catches in same day count as one streak day
- Day rolls over at 12:00 AM local
- Missing a day breaks streak

Stack with Lucky Egg before day 7 catch to double the streak XP.

- Example: "Hit a Lucky Egg before your 7th-day catch tomorrow. The 2,500 XP streak bonus doubles to 5,000, plus you get the 600 Stardust first-catch bonus."

### 41. PokéCoin & Gym Defender Optimization
- 1 coin per 10 minutes, 50 coin daily cap
- 8 hours 20 minutes is the threshold for the full 50 coins
- Multiple gyms don't stack the cap - 6 gyms ≠ 300 coins
- Pokémon must return defeated to claim coins

Strategy:
- Place defenders in evening so they flip overnight = full 50 coins next morning
- Coordinate timing: let one return, place in next
- Variety bonus: different species in same gym drain motivation slower

S-tier defenders (2026): Blissey, Chansey, Snorlax, Metagross. Place Blissey + Snorlax for the "fat wall" combo.

- Example: "Drop a Blissey in your local gym tonight before bed. By morning you'll have flipped through 8+ hours of defending and earned the full 50 coins."

### 42. AR Power-Up PokéStops
Tier system based on AR scans contributed by the community:
- 5 scans = Level 1
- 10 scans = Level 2
- 25 scans = Level 3

Higher tier = more items per spin AND longer powered-up duration.

AR Mapping tasks live in their own slot (don't take regular Field Research slots). Reward: typically Stardust + Rare Candy.

- Example: "Your local park has 3 stops sitting at Level 1. Coordinate a community scan day to push them to Level 3 - everyone benefits from the boosted item drops."

### 43. PokéStop Showcase Tactics
Showcase scoring formula: Score = (Scaled Height × 800/Max) + (Scaled Weight × 150/Max) + (IV Sum × 50/45) + Bonus

Height carries the most weight. **XXL Pokémon dominate size showcases.** A 0% XXL beats a hundo XS.

- Furfrou Trim swaps: 25 candy + 10K dust per swap, 9 trims total. Each trim = separate Showcase eligibility.
- Vivillon: 18 patterns via international postcard pins (only path).
- One Pokémon, one active Showcase - have multiple high-IV/XXL specimens of the same species ready.

Pokédex search `xxs&!shiny` finds every micro-form for size-XS Showcases.

- Example: "Showcase Tuesday features XXL [species] this week. Filter your storage for `xxl&[species]` and enter your largest. Pure size beats IVs in size showcases."

### 44. Memories in Motion Season Changes (2026)
The Spring 2026 season (Mar 3 - Jun 2) introduced major structural changes. Key shifts:

- **Spotlight Hours retired for the Spring 2026 season** - replaced by Daily Discoveries day-of-week structure. NOTE: Spotlight Hour RETURNED June 18, 2026 with the Forever Forward season and is now a required newsletter section; Daily Discoveries runs alongside it.
- **Wild evolved Pokémon can be shiny** - new shiny pool to hunt for any species with shiny base form released
- **L31+ in-person trades give 1 guaranteed XL Candy + 1 regular candy** - reframes trading from "lucky chase" to "candy guarantee"
- **GO Battle Thursday: 4x Stardust win rewards, daily set cap raised from 5 to 10 (50 battles)** - the dust farming day
- **Weekend events shift to Saturdays** - plan Saturday play sessions
- **Event GO Passes replace paid tickets** - stack pass tasks on Mondays (2x GO Points)

Volcanion Special Research "Pressure Rising" is free for all trainers since Mar 3, 2026. Many returning players don't know it's free.

- Example: "GO Battle Thursday gives 50 battles at 4x Stardust this season. With Star Piece running, that's the highest dust-per-hour activity in the game. Schedule your grind for Thursday."

### 45. Necrozma Fusion (New Mechanic)
Fusion costs:
- **Dusk Mane Necrozma:** 1,000 Solar Fusion Energy + 30 Necrozma Candy + 30 Cosmog Candy + Solgaleo
- **Dawn Wings Necrozma:** 1,000 Lunar Fusion Energy + 30 Necrozma Candy + 30 Cosmog Candy + Lunala

Energy from raids during fusion events. Stockpile during the event window.

Important: Necrozma Dusk Mane is NOT Dynamax-capable (it never may be). Reference for Trainer Tips when Necrozma raids appear.

- Example: "Solgaleo raids return this week. If you have an Ultra Necrozma in storage, save 1,000 Solar Fusion Energy from the Cosmog raids to fuse Dusk Mane Necrozma later."

### 46. GO Plus+ Auto-Catch
- Auto-Throw ball selection (2026): choose Poké Ball, Great Ball, or Ultra Ball
- Set Ultra for high-CP zones
- Auto-catches work during raid lobbies (background spawns)

Sleep tracking integration:
- 1,700 Stardust + 2 Buddy Hearts daily (basic)
- 2,500 Stardust if you sleep 7+ hours
- Automatic Best Buddy progress while you sleep

- Example: "Your GO Plus+ auto-catches background spawns while you're in raid lobbies. Set ball preference to Ultra for raid hour - you'll catch the Pokémon that spawn under your foot during the 5-minute lobby waits."

### 47. Special Evolution Methods (Hisuian/Paldean)
Beyond Pokédex completion, these often lock unique strategic value behind specific evolution requirements:

- **Sneasler:** Hisuian Sneasel + 100 Candy + 7 km buddy walking + DAYTIME (easy to miss)
- **Ursaluna:** Ursaring + 100 Candy + real-world full moon (once a month only)
- **Wyrdeer / Kleavor / Hisuian Samurott:** NOT evolvable in Pokémon GO - only via 3-star raids
- **Annihilape:** Primeape + 100 Candy + defeat 30 Ghost/Psychic Pokémon as buddy. Rage Fist locked to Mankey CD evolutions.
- **Gholdengo:** Roaming Gimmighoul + 999 Gimmighoul Coins (consumed). Lucky Trade Gimmighoul to skip months of grind.

Track moon phase calendar for Ursaluna events. Plan walking routes for Sneasler around daytime hours.

- Example: "Full moon falls on Wednesday. If you've been walking Hisuian Ursaring, evolve Wednesday night for Ursaluna. The full moon window is 3 hours either side of peak."

### 48. Niantic Wayfarer & S2 Cell Logic
- 1 Upgrade per 100 Agreements (Upgrades fast-track your nominations)
- Agreement = your nomination decision matched the consensus

S2 cell mechanics determine spawns and gyms:
- Level 17 cells = spawn points
- Level 14 cells = gym/PokéStop assignment
- One Wayspot in an empty L14 cell becomes a gym; later additions don't displace it

For local communities pushing for new gyms or stops, getting first nomination in an empty L14 cell is high-leverage.

- Example: "Your local park has stops but no gym. Check the S2 cell map - if a stop sits alone in its L14 cell, nominating an additional Wayspot in the same cell will likely promote it to a gym."

### 49. Steel Box Strategy & XL Trade Bonus (2026)
The Memories in Motion season's L31+ in-person trade bonus is significant:
- 1 guaranteed XL Candy on every in-person trade
- +1 regular candy
- Stacks with Lucky chance and trade re-roll IVs

Strategy: Trade meetups for grinding XL Candy on level-50 power-up targets. 100 trades = 100 XL Candy (more than walking buddy 100 km).

For Mystery Box / Meltan grinding: standard 7-day cooldown, but events reduce it. Stack openings around event windows. Shiny Meltan ~1/125 in events.

- Example: "Need XL Candy for Garchomp's L50 grind? Plan an in-person Garchomp trade meetup with 5 friends. Five trades = 5 XL Candy + 5 regular Candy + IV re-roll chances. Faster than walking 5 km × 5 = 25 km of buddy walking."

## How to Apply

For each newsletter section:
1. **The tip MUST be directly about the section's content.** A Max Monday tip must be about the featured Dynamax Pokémon (counters, type strategy, tier ranking). A Raid Boss tip must be about that specific boss. Do NOT attach a generic game tip to a section just because it happens on the same day. If the tip works equally well pasted into any other section, it's not specific enough.
2. Scan this checklist against the event/feature
3. Pick the 1-2 most impactful angles (don't overwhelm readers with every possible tip)
4. Write the tip in 1-2 sentences
5. Be specific with numbers (multipliers, CP thresholds, medal counts, shiny rates)
6. If a tip involves stacking bonuses, show the math or the multiplier chain
7. Prioritize tips that are time-sensitive or event-exclusive over general knowledge

## Angle Drift Tracking (Variety Surveillance)

Variety matters. The same 4–5 angles get over-used while 30+ remain dormant. Each newsletter run, the agent should:

1. **Cross-reference `instructions/newsletter-archive.md` "Trainer Tip Angles Used" fields** for the past 8 issues.
2. **Surface underused angles** in the research brief: list 3–5 angles that haven't appeared in 8+ issues but COULD fit the upcoming week's content.
3. **Flag heavily-reused angles** in the research brief: list angles used in 4+ of the past 8 issues. Default AWAY from these unless the week's content makes them the obvious right call.

Heavily-reused (as of May 2026, per archive analysis):
- XP/Stardust farming combos
- Lucky Egg / Star Piece / Pinap stacking
- Mega-Evolved attack boost synergy
- Raid counter recommendations

Underused (rotate in when content allows):
- Field Research stacking (multiple research tasks for the same target)
- TM cycling (re-roll bad movesets during free-TM events)
- Buddy Adventure hearts (efficient heart-stacking for candy/walk distance)
- Routes / Zygarde Cells (path strategy)
- Gym defending Stardust (50 Stardust per 10 min coin)
- Party play multipliers (group-bonus efficiency)
- Shadow purification math (Stardust/candy break-even calc)
- Postcard book bonuses (gift-related XP/items)
- Adventure Sync milestones (weekly distance rewards)

This tracking is informational — the goal is variety, not strict rotation. If the week's content makes a heavily-reused angle the obvious right call, use it.
