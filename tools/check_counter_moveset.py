#!/usr/bin/env python3
"""Verify that a list of raid counter movesets are super-effective on a boss.

PoGO multipliers: 1.6 (SE), 1.0 (neutral), 0.625 (resisted), 0.39 (doubly resisted).
For dual-type defenders, the multiplier on each attack-type is the PRODUCT of the
single-type effectiveness against each of the defender's types.

Usage:
  ./check_counter_moveset.py \\
      --boss "Mega Lopunny:Normal/Fighting" \\
      "Mega Latios:Zen Headbutt/Aura Sphere" \\
      "Mega Rayquaza:Air Slash/Dragon Ascent" \\
      "Blaziken:Counter/Aura Sphere"

Output: per-counter table marking whether the listed Charged Move is super-effective
(or at least 1.6×) on the boss's typing. Plus a summary line.

If the FAST move is also of an attacking type that's super-effective, it gets a
"fast-also-SE" note; if neither move is SE, the counter is flagged as POSSIBLY
SUBOPTIMAL (acceptable rationale: raw DPS, bulk, Mega aura — must be documented).

The script reads its move→type mapping from a small bundled JSON (`moves.json`).
For moves not in the bundle, pass `--unknown-ok` to skip the move silently, or
add the move to `moves.json` (preferred for repeat species).
"""

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MOVES_PATH = os.path.join(ROOT, "moves.json")

# PoGO type chart: attacker → defender → multiplier
# Built from Niantic's 2020 type-effectiveness constants.
# 1.6 = super-effective; 0.625 = resisted; 0.39 = doubly resisted (main-series immunity).
SE, NE, RE, DRE = 1.6, 1.0, 0.625, 0.39

TYPE_CHART = {
    "Normal":   {"Rock": RE, "Ghost": DRE, "Steel": RE},
    "Fire":     {"Fire": RE, "Water": RE, "Grass": SE, "Ice": SE, "Bug": SE, "Rock": RE, "Dragon": RE, "Steel": SE},
    "Water":    {"Fire": SE, "Water": RE, "Grass": RE, "Ground": SE, "Rock": SE, "Dragon": RE},
    "Electric": {"Water": SE, "Electric": RE, "Grass": RE, "Ground": DRE, "Flying": SE, "Dragon": RE},
    "Grass":    {"Fire": RE, "Water": SE, "Grass": RE, "Poison": RE, "Ground": SE, "Flying": RE, "Bug": RE, "Rock": SE, "Dragon": RE, "Steel": RE},
    "Ice":      {"Fire": RE, "Water": RE, "Grass": SE, "Ice": RE, "Ground": SE, "Flying": SE, "Dragon": SE, "Steel": RE},
    "Fighting": {"Normal": SE, "Ice": SE, "Poison": RE, "Flying": RE, "Psychic": RE, "Bug": RE, "Rock": SE, "Ghost": DRE, "Dark": SE, "Steel": SE, "Fairy": RE},
    "Poison":   {"Grass": SE, "Poison": RE, "Ground": RE, "Rock": RE, "Ghost": RE, "Steel": DRE, "Fairy": SE},
    "Ground":   {"Fire": SE, "Electric": SE, "Grass": RE, "Poison": SE, "Flying": DRE, "Bug": RE, "Rock": SE, "Steel": SE},
    "Flying":   {"Electric": RE, "Grass": SE, "Fighting": SE, "Bug": SE, "Rock": RE, "Steel": RE},
    "Psychic":  {"Fighting": SE, "Poison": SE, "Psychic": RE, "Dark": DRE, "Steel": RE},
    "Bug":      {"Fire": RE, "Grass": SE, "Fighting": RE, "Poison": RE, "Flying": RE, "Psychic": SE, "Ghost": RE, "Dark": SE, "Steel": RE, "Fairy": RE},
    "Rock":     {"Fire": SE, "Ice": SE, "Fighting": RE, "Ground": RE, "Flying": SE, "Bug": SE, "Steel": RE},
    "Ghost":    {"Normal": DRE, "Psychic": SE, "Ghost": SE, "Dark": RE},
    "Dragon":   {"Dragon": SE, "Steel": RE, "Fairy": DRE},
    "Dark":     {"Fighting": RE, "Psychic": SE, "Ghost": SE, "Dark": RE, "Fairy": RE},
    "Steel":    {"Fire": RE, "Water": RE, "Electric": RE, "Ice": SE, "Rock": SE, "Steel": RE, "Fairy": SE},
    "Fairy":    {"Fire": RE, "Fighting": SE, "Poison": RE, "Dragon": SE, "Dark": SE, "Steel": RE},
}

DEFAULT_MOVES = {
    # Fast moves
    "Counter": "Fighting", "Force Palm": "Fighting", "Low Kick": "Fighting", "Karate Chop": "Fighting",
    "Confusion": "Psychic", "Zen Headbutt": "Psychic", "Psycho Cut": "Psychic", "Psywave": "Psychic",
    "Dragon Tail": "Dragon", "Dragon Breath": "Dragon",
    "Mud Shot": "Ground", "Mud-Slap": "Ground", "Bullet Punch": "Steel", "Metal Claw": "Steel",
    "Wing Attack": "Flying", "Gust": "Flying", "Air Slash": "Flying", "Peck": "Flying",
    "Fire Spin": "Fire", "Fire Fang": "Fire", "Incinerate": "Fire", "Ember": "Fire",
    "Charm": "Fairy", "Fairy Wind": "Fairy",
    "Snarl": "Dark", "Bite": "Dark",
    "Hex": "Ghost", "Lick": "Ghost", "Shadow Claw": "Ghost",
    "Thunder Shock": "Electric", "Spark": "Electric",
    "Rollout": "Rock", "Smack Down": "Rock",
    "Fury Cutter": "Bug", "Bug Bite": "Bug",
    "Ice Fang": "Ice", "Frost Breath": "Ice", "Powder Snow": "Ice",
    "Vine Whip": "Grass", "Razor Leaf": "Grass", "Magical Leaf": "Grass",
    "Water Gun": "Water", "Waterfall": "Water",
    "Tackle": "Normal", "Quick Attack": "Normal", "Sucker Punch": "Dark",
    "Drum Beating": "Grass", "Volt Switch": "Electric", "Acid": "Poison", "Poison Jab": "Poison",
    "Sand Attack": "Ground",

    # Charged moves
    "Aura Sphere": "Fighting", "Close Combat": "Fighting", "Dynamic Punch": "Fighting",
    "Focus Blast": "Fighting", "Sacred Sword": "Fighting", "Cross Chop": "Fighting",
    "Brick Break": "Fighting", "Secret Sword": "Fighting",
    "Psystrike": "Psychic", "Psychic": "Psychic", "Future Sight": "Psychic",
    "Mist Ball": "Psychic", "Luster Purge": "Psychic", "Nature's Madness": "Grass",
    "Earth Power": "Ground", "Earthquake": "Ground", "Precipice Blades": "Ground",
    "Drill Run": "Ground", "Bulldoze": "Ground", "Scorching Sands": "Ground",
    "Sandsear Storm": "Ground",
    "Dragon Claw": "Dragon", "Outrage": "Dragon", "Draco Meteor": "Dragon",
    "Breaking Swipe": "Dragon", "Dragon Energy": "Dragon", "Roar of Time": "Dragon",
    "Spacial Rend": "Dragon", "Dragon Ascent": "Flying",
    "Dazzling Gleam": "Fairy", "Play Rough": "Fairy", "Moonblast": "Fairy", "Disarming Voice": "Fairy",
    "Sky Attack": "Flying", "Fly": "Flying", "Brave Bird": "Flying", "Hurricane": "Flying",
    "Oblivion Wing": "Flying",
    "Blast Burn": "Fire", "Overheat": "Fire", "Flamethrower": "Fire", "Fusion Flare": "Fire",
    "Heat Wave": "Fire", "Magma Storm": "Fire",
    "Hydro Cannon": "Water", "Hydro Pump": "Water", "Surf": "Water", "Sparkling Aria": "Water",
    "Aqua Tail": "Water", "Water Pulse": "Water",
    "Frenzy Plant": "Grass", "Solar Beam": "Grass", "Leaf Blade": "Grass", "Grass Knot": "Grass",
    "Crunch": "Dark", "Foul Play": "Dark", "Dark Pulse": "Dark", "Payback": "Dark",
    "Shadow Ball": "Ghost", "Shadow Punch": "Ghost", "Moongeist Beam": "Ghost",
    "Sludge Bomb": "Poison", "Sludge Wave": "Poison", "Gunk Shot": "Poison",
    "Wild Charge": "Electric", "Thunder": "Electric", "Thunderbolt": "Electric",
    "Discharge": "Electric", "Thunder Punch": "Electric", "Fusion Bolt": "Electric",
    "Rock Wrecker": "Rock", "Stone Edge": "Rock", "Rock Slide": "Rock", "Power Gem": "Rock",
    "X-Scissor": "Bug", "Megahorn": "Bug",
    "Avalanche": "Ice", "Ice Beam": "Ice", "Ice Burn": "Ice", "Blizzard": "Ice", "Freeze Shock": "Ice",
    "Hyper Beam": "Normal", "Body Slam": "Normal", "Giga Impact": "Normal",
    "Iron Head": "Steel", "Meteor Mash": "Steel", "Behemoth Blade": "Steel",
    "Behemoth Bash": "Steel", "Gigaton Hammer": "Steel", "Sunsteel Strike": "Steel",
    "Dynamax Cannon": "Dragon",
    "Twister": "Dragon",
}


def load_moves():
    """Load moves.json, falling back to defaults if missing."""
    moves = dict(DEFAULT_MOVES)
    if os.path.exists(MOVES_PATH):
        try:
            with open(MOVES_PATH) as f:
                moves.update(json.load(f))
        except Exception as e:
            print(f"Warning: failed to load {MOVES_PATH}: {e}", file=sys.stderr)
    return moves


def lookup_multiplier(attack_type, defender_types):
    """Compute attacker type vs defender's full typing (multiplicative)."""
    mult = 1.0
    for t in defender_types:
        mult *= TYPE_CHART.get(attack_type, {}).get(t, 1.0)
    return mult


def parse_boss(s):
    """Parse 'Mega Lopunny:Normal/Fighting' → (name, [Normal, Fighting])."""
    if ":" not in s:
        raise ValueError(f"Boss must be 'Name:Type' or 'Name:Type1/Type2', got {s!r}")
    name, types_raw = s.split(":", 1)
    types = [t.strip().capitalize() for t in types_raw.split("/")]
    for t in types:
        if t not in TYPE_CHART:
            raise ValueError(f"Unknown type {t!r}. Valid: {sorted(TYPE_CHART)}")
    return name.strip(), types


def parse_counter(s):
    """Parse 'Mega Latios:Zen Headbutt/Aura Sphere' → (name, fast, charged)."""
    if ":" not in s:
        raise ValueError(f"Counter must be 'Name:Fast/Charged', got {s!r}")
    name, moves_raw = s.split(":", 1)
    if "/" not in moves_raw:
        raise ValueError(f"Counter moves must be 'Fast/Charged', got {moves_raw!r}")
    fast, charged = moves_raw.split("/", 1)
    return name.strip(), fast.strip(), charged.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--boss", required=True, help="e.g., 'Mega Lopunny:Normal/Fighting'")
    ap.add_argument("counters", nargs="+", help="Each: 'Name:Fast/Charged'")
    ap.add_argument("--unknown-ok", action="store_true", help="Skip counters whose moves aren't in moves.json")
    ap.add_argument("--strict", action="store_true", help="Exit 1 if any counter is suboptimal")
    args = ap.parse_args()

    moves = load_moves()
    boss_name, boss_types = parse_boss(args.boss)

    print(f"Boss: {boss_name} ({'/'.join(boss_types)})")
    print()
    header = f"{'Counter':<28} {'Fast (type)':<24} {'Charged (type)':<26} {'CM mult':>8}  Verdict"
    print(header)
    print("-" * len(header))

    fails = 0
    for raw in args.counters:
        name, fast, charged = parse_counter(raw)
        fast_type = moves.get(fast)
        charged_type = moves.get(charged)
        if fast_type is None or charged_type is None:
            unknown = [m for m, t in (("Fast", fast_type), ("Charged", charged_type)) if t is None]
            if args.unknown_ok:
                print(f"{name:<28} (skipped — unknown move: {fast if fast_type is None else charged})")
                continue
            print(f"{name:<28} ERROR — unknown {unknown[0]} move ({fast if fast_type is None else charged})")
            fails += 1
            continue

        fast_mult = lookup_multiplier(fast_type, boss_types)
        cm_mult = lookup_multiplier(charged_type, boss_types)

        if cm_mult >= 1.6:
            verdict = "✓ SE charged"
            if fast_mult >= 1.6:
                verdict += " + SE fast"
        elif cm_mult >= 1.0:
            verdict = "⚠ NEUTRAL charged"
            if fast_mult >= 1.6:
                verdict += " (fast SE — borderline OK)"
            else:
                verdict += " — SUBOPTIMAL"
                fails += 1
        else:
            verdict = "✗ RESISTED charged — DROP"
            fails += 1

        print(
            f"{name:<28} {f'{fast} ({fast_type})':<24} "
            f"{f'{charged} ({charged_type})':<26} {cm_mult:>7.2f}×  {verdict}"
        )

    print()
    total = len(args.counters)
    ok = total - fails
    print(f"{ok}/{total} counters use SE moves" + (f"  ({fails} flagged)" if fails else ""))

    if args.strict and fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
