#!/usr/bin/env python3
"""Cross-reference Pokémon GO claims against the mgrann03/pokemon-resources data layer.

mgrann03 is the community-curated PoGO species/move database that powers DialgaDex.
Adds value over the raw GameMaster JSON by separating Elite-TM-only moves from
standard movepool, marking each species's raid tier, and tracking release status
with manual override files.

Subcommands:

  moveset "Species" "Fast Move/Charged Move"
    Verify a counter moveset is real (both moves learnable by the species) AND
    classify accessibility:
      ✓ STANDARD — both moves in regular movepool
      ⚠ ELITE — one or both moves require Elite TM / legacy event
      ✗ INVALID — the species can't learn one of the moves

  debut "Species" [--form "FormName"]
    Verify whether a claimed PoGO debut is genuinely new. Cross-references
    pogo_pkm.min.json (released species) and pogo_pkm_manual_announced.json
    (announced-but-not-released). Output:
      ✗ NOT A DEBUT — species already released (with raid_tier if any)
      ✓ DEBUT — confirmed in announced file with effective date
      ? UNKNOWN — not in either source; verify against Spawn Point archive

  tier "Species" [--form "FormName"]
    Look up the raid_tier field. Convention observed in mgrann03:
      1 → 1-Star raid eligibility
      3 → 3-Star raid eligibility
      4 → Mega raid eligibility
      5 → 5-Star Legendary raid eligibility
      6 → Super Mega Raid (current Mega Rayquaza class)
      8 → Super Mega Raid Day debut tier (Mega Skarmory class)

  shadow "Species" [--form "FormName"]
    Check Shadow availability. Returns:
      ✓ SHADOW_AVAILABLE — Shadow form is in the game
      ✗ NO_SHADOW — Shadow form not (yet) released for this species

  info "Species" [--form "FormName"]
    Print the full mgrann03 entry for a species/form.

The script caches mgrann03's JSON locally for 24 hours under tools/cache/mgrann03/
to keep fetches cheap. Override the cache TTL with --refresh to force re-pull.

Examples:
  ./mgrann03_check.py moveset "Mega Rayquaza" "Air Slash/Dragon Ascent"
  ./mgrann03_check.py debut "Mega Skarmory"
  ./mgrann03_check.py tier "Bombirdier"
  ./mgrann03_check.py shadow "Reshiram"

Exit codes:
  0 — all checks pass
  1 — verification fails
  2 — argument or data fetch error
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(ROOT, "cache", "mgrann03")
TTL_SECONDS = 24 * 60 * 60  # 24h freshness

ENDPOINTS = {
    "pkm": "https://raw.githubusercontent.com/mgrann03/pokemon-resources/main/pogo_pkm.min.json",
    "announced": "https://raw.githubusercontent.com/mgrann03/pokemon-resources/main/pogo_pkm_manual_announced.json",
}

REGIONAL_PREFIXES = {
    "alolan": "Alola",
    "alola": "Alola",
    "galarian": "Galarian",
    "galar": "Galarian",
    "hisuian": "Hisuian",
    "hisui": "Hisuian",
    "paldean": "Paldea",
    "paldea": "Paldea",
}


def fetch_cached(key, force_refresh=False):
    """Fetch JSON from mgrann03 with 24h local cache. Uses curl (Python's urllib hits SSL cert verify failures in some envs)."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    age = float("inf") if not os.path.exists(path) else (time.time() - os.path.getmtime(path))
    if force_refresh or age > TTL_SECONDS:
        url = ENDPOINTS[key]
        age_str = "fresh" if age == float("inf") else f"{age/3600:.1f}h old"
        print(f"Fetching {url} (cache {age_str})...", file=sys.stderr)
        try:
            subprocess.run(["curl", "-sSL", "-o", path, url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: failed to fetch {url}: {e}", file=sys.stderr)
            sys.exit(2)
    with open(path) as f:
        return json.load(f)


def normalize_species_input(raw):
    """Parse 'Mega Rayquaza' / 'Hisuian Growlithe' / 'Shadow Garchomp' / 'Paldean Tauros'.
    Returns (base_name, form_hint, kind) where kind ∈ {'mega', 'regional', 'shadow', 'normal'}.
    """
    s = raw.strip()
    low = s.lower()
    if low.startswith("mega "):
        return (s[5:].strip(), "Mega", "mega")
    if low.startswith("shadow "):
        return (s[7:].strip(), None, "shadow")
    parts = s.split(maxsplit=1)
    if parts and parts[0].lower() in REGIONAL_PREFIXES:
        return (parts[1] if len(parts) > 1 else "", REGIONAL_PREFIXES[parts[0].lower()], "regional")
    return (s, None, "normal")


def find_entries(data, species, form_hint=None):
    """Find entries in mgrann03 data matching the species name + optional form hint.

    Critical rule: when a form is requested (explicit --form OR inferred from prefix like 'Mega X'),
    only return entries that match the form. Don't fall back to the base form — that's a different
    Pokémon for the question being asked.
    """
    base, form_from_prefix, _ = normalize_species_input(species)
    hint = form_hint or form_from_prefix

    # 1. Direct name match (handles "Mega Venusaur" stored verbatim in either file)
    direct = [e for e in data if e["name"].lower() == species.lower()]
    if direct:
        # If a form hint was given, narrow to matching form
        if hint:
            narrowed = [e for e in direct if hint.lower() in e.get("form", "").lower()]
            return narrowed if narrowed else direct  # name-match wins if forms don't narrow
        return direct

    # 2. Base species + form filter (handles regional forms stored as form on the base species)
    if base != species:  # the input had a strippable prefix
        by_name = [e for e in data if e["name"].lower() == base.lower()]
        if hint:
            by_form = [e for e in by_name if hint.lower() in e.get("form", "").lower()]
            return by_form  # empty if no form match — DO NOT fall back to base
        return by_name

    # 3. Fuzzy substring fallback (last resort, only when no prefix and no direct match)
    return [e for e in data if species.lower() in e["name"].lower()]


def cmd_moveset(args, pkm_data, announced_data):
    species = args.species
    fast, _, charged = args.moveset.partition("/")
    fast, charged = fast.strip(), charged.strip()
    if not fast or not charged:
        print(f"Error: moveset must be 'Fast Move/Charged Move', got {args.moveset!r}", file=sys.stderr)
        return 2

    entries = find_entries(pkm_data, species, args.form) or find_entries(announced_data, species, args.form)
    if not entries:
        print(f"✗ Species not found in mgrann03: {species!r}")
        return 1

    print(f"Looking up {species} (best match: id={entries[0]['id']} form={entries[0].get('form', '?')})")

    # Check across all matched entries (e.g., Mega has its own learnset)
    found_fast, fast_kind = False, None
    found_charged, charged_kind = False, None
    for e in entries:
        if fast in e.get("fm", []):
            found_fast = True; fast_kind = "standard"
        elif fast in e.get("elite_fm", []):
            found_fast = True; fast_kind = "elite" if fast_kind != "standard" else fast_kind
        if charged in e.get("cm", []):
            found_charged = True; charged_kind = "standard"
        elif charged in e.get("elite_cm", []):
            found_charged = True; charged_kind = "elite" if charged_kind != "standard" else charged_kind

    print(f"  Fast: {fast} → " + (
        f"✓ standard" if fast_kind == "standard"
        else f"⚠ ELITE / LEGACY (requires Elite Fast TM)" if fast_kind == "elite"
        else f"✗ NOT in {species}'s movepool"
    ))
    print(f"  Charged: {charged} → " + (
        f"✓ standard" if charged_kind == "standard"
        else f"⚠ ELITE / LEGACY (requires Elite Charged TM)" if charged_kind == "elite"
        else f"✗ NOT in {species}'s movepool"
    ))

    if not (found_fast and found_charged):
        print(f"\n✗ INVALID — {species} cannot use this moveset as written.")
        return 1
    if fast_kind == "elite" or charged_kind == "elite":
        print(f"\n⚠ ELITE — moveset is real but requires an Elite TM / legacy access.")
        return 0
    print(f"\n✓ STANDARD — moveset is real and uses standard movepool.")
    return 0


def cmd_debut(args, pkm_data, announced_data):
    species = args.species
    entries_main = find_entries(pkm_data, species, args.form)
    entries_announced = find_entries(announced_data, species, args.form)

    if entries_main and any(e.get("released") for e in entries_main):
        e = next(iter(entries_main))
        tier = e.get("raid_tier", "none")
        print(f"✗ NOT A DEBUT — {species} is already released (form={e.get('form', '?')}, raid_tier={tier}).")
        print(f"  Use 'returns' or 'rotates back in' framing, not 'debuts' / 'new to GO'.")
        return 1

    if entries_announced:
        e = next(iter(entries_announced))
        eff = e.get("eff_date", "no effective date in announced file")
        tier = e.get("raid_tier", "none")
        print(f"✓ DEBUT — {species} is in mgrann03's announced pipeline.")
        print(f"  Effective date: {eff}")
        print(f"  Expected raid_tier: {tier}")
        print(f"  Form: {e.get('form', '?')}")
        return 0

    print(f"? UNKNOWN — {species} not in mgrann03 released list or announced file.")
    print(f"  Verify against Spawn Point newsletter-archive.md before claiming debut status.")
    return 1


def cmd_tier(args, pkm_data, announced_data):
    species = args.species
    entries = find_entries(pkm_data, species, args.form) or find_entries(announced_data, species, args.form)
    if not entries:
        print(f"✗ Species not found: {species!r}")
        return 1
    for e in entries:
        tier = e.get("raid_tier", "none")
        tier_label = {
            1: "1-Star",
            3: "3-Star",
            4: "Mega",
            5: "5-Star Legendary",
            6: "Super Mega (Mega Rayquaza class)",
            8: "Super Mega Raid Day debut",
        }.get(tier, f"tier {tier}" if tier != "none" else "no raid eligibility recorded")
        print(f"  {e['name']} ({e.get('form', '?')}): raid_tier={tier} ({tier_label})")
    return 0


def cmd_shadow(args, pkm_data, announced_data):
    species = args.species
    entries = find_entries(pkm_data, species, args.form)
    if not entries:
        print(f"✗ Species not found: {species!r}")
        return 1
    has_shadow = any(e.get("shadow") for e in entries)
    if has_shadow:
        forms = [e.get("form", "?") for e in entries if e.get("shadow")]
        print(f"✓ SHADOW_AVAILABLE — {species} can appear as Shadow (forms: {', '.join(forms)})")
        return 0
    print(f"✗ NO_SHADOW — {species} does not (yet) have a Shadow form in PoGO per mgrann03.")
    return 1


def cmd_info(args, pkm_data, announced_data):
    species = args.species
    entries_main = find_entries(pkm_data, species, args.form)
    entries_announced = find_entries(announced_data, species, args.form)
    if not entries_main and not entries_announced:
        print(f"✗ Species not found: {species!r}")
        return 1
    if entries_main:
        print(f"=== {species} in pogo_pkm.min.json ({len(entries_main)} match{'es' if len(entries_main) != 1 else ''}) ===")
        for e in entries_main:
            print(json.dumps(e, indent=2))
    if entries_announced:
        print(f"\n=== {species} in pogo_pkm_manual_announced.json ({len(entries_announced)} match{'es' if len(entries_announced) != 1 else ''}) ===")
        for e in entries_announced:
            print(json.dumps(e, indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="Force re-fetch from mgrann03 (bypass 24h cache)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("moveset", help="Verify counter moveset is real + classify accessibility")
    p.add_argument("species")
    p.add_argument("moveset", help="'Fast Move/Charged Move'")
    p.add_argument("--form", help="Restrict to a specific form name (e.g., 'Mega', 'Hisuian')")

    p = sub.add_parser("debut", help="Verify whether a species is a true PoGO debut")
    p.add_argument("species")
    p.add_argument("--form", help="Restrict to a specific form name")

    p = sub.add_parser("tier", help="Look up raid_tier for a species")
    p.add_argument("species")
    p.add_argument("--form", help="Restrict to a specific form name")

    p = sub.add_parser("shadow", help="Check Shadow availability for a species")
    p.add_argument("species")
    p.add_argument("--form", help="Restrict to a specific form name")

    p = sub.add_parser("info", help="Print full mgrann03 entry for a species")
    p.add_argument("species")
    p.add_argument("--form", help="Restrict to a specific form name")

    args = ap.parse_args()

    pkm_data = fetch_cached("pkm", args.refresh)
    announced_data = fetch_cached("announced", args.refresh)

    handler = {
        "moveset": cmd_moveset,
        "debut": cmd_debut,
        "tier": cmd_tier,
        "shadow": cmd_shadow,
        "info": cmd_info,
    }[args.cmd]
    sys.exit(handler(args, pkm_data, announced_data))


if __name__ == "__main__":
    main()
