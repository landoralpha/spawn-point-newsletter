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

  rank "Species" [--form "FormName"] [--type Type] [--level 40|50]
    Compute DialgaDex-style PvE attacker rank using the comprehensive
    DPS / TDO / EER formula (Gamepress-derived, ported from DialgaDex's
    calc.js). Output is the species's rank within the released attacker
    pool plus its ±5 neighbors so the position reads in context.
    --type filters to one-type rankings (matches DialgaDex's "Strongest
    Psychic Attackers" page); omit for any-type.
    Default level 40 (standard raid attacker); 50 for XL-capped.

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
    # Move databases — only fetched when the rank subcommand runs.
    "fm": "https://raw.githubusercontent.com/mgrann03/pokemon-resources/main/pogo_fm.json",
    "cm": "https://raw.githubusercontent.com/mgrann03/pokemon-resources/main/pogo_cm.json",
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


# ────────────────────────────────────────────────────────────────────
# PvE rank calculation — ported from DialgaDex's calc.js + rankings.js.
#
# The PoGO PvE damage model follows Gamepress's well-documented formula
# (https://gamepress.gg/pokemongo/how-calculate-comprehensive-dps).
# DialgaDex layers on a "comprehensive DPS" that accounts for charged-
# move timing and incoming damage from the boss; we mirror that here so
# the ranking ordering matches DialgaDex's "Strongest of Any Type" page.
# Simplifications vs. the full DialgaDex JS:
#   - No "search string" / Suboptimal toggle (always best moveset only).
#   - No party-power boost (settings_party_size = 1).
#   - "Old raid system" durations (settings_pve_turns = false) — matches
#     DialgaDex's default + nearly all real PoGO raid contexts.
#   - One-bar charged-move penalty IS applied per the JS.
# These match DialgaDex's defaults; absolute DPS numbers + ranking order
# should land within a few percent of the live site.
# ────────────────────────────────────────────────────────────────────

# CPM at each level — Niantic-published. Only L40 / L50 needed for PvE
# (L40 is standard raid attacker, L50 is XL-candy capped).
CPM = {40: 0.7903, 50: 0.84029999}
STAB = 1.2
DEFAULT_ENEMY_DEF = 180  # Generic Tier-5 raid boss DEF baseline
EST_Y_NUMERATOR = 1340   # DialgaDex calc.js — incoming dps approximation
EST_CM_POWER = 11670     # DialgaDex calc.js — incoming charged-move power
SHADOW_ATK_MULT = 1.2
SHADOW_DEF_MULT = 0.8333333


def fetch_moves_indexed():
    """Returns (fm_by_name, cm_by_name) — dicts keyed by move display name."""
    fm = fetch_cached("fm")
    cm = fetch_cached("cm")
    return ({m["name"]: m for m in fm}, {m["name"]: m for m in cm})


def stat_at_level(base, iv, level):
    """ATK/DEF/HP formula: (base + iv) * cpm. HP gets floored later."""
    return (base + iv) * CPM[level]


def calc_dps(types, atk, defense, hp, fm, cm, shadow=False):
    """Comprehensive DPS — port of DialgaDex's GetDPS (calc.js:23).

    types: list of the attacker's types (for STAB check)
    atk/def/hp: effective stats (post-shadow multiplier, post-CPM)
    fm, cm: move dict entries from pogo_fm.json / pogo_cm.json
    """
    if not fm or not cm:
        return 0.0
    if shadow:
        atk = atk * SHADOW_ATK_MULT
        defense = defense * SHADOW_DEF_MULT

    y = EST_Y_NUMERATOR / defense
    in_cm_dmg = EST_CM_POWER / defense
    tof = hp / y

    x = 0.5 * -cm["energy_delta"] + 0.5 * fm["energy_delta"]

    fm_stab = STAB if fm["type"] in types and fm["name"] != "Hidden Power" else 1
    cm_stab = STAB if cm["type"] in types else 1

    fm_dur = fm["duration"] / 1000
    cm_dur = cm["duration"] / 1000

    fm_dmg = 0.5 * fm["power"] * (atk / DEFAULT_ENEMY_DEF) * fm_stab + 0.5
    fm_dps = fm_dmg / fm_dur
    fm_eps = fm["energy_delta"] / fm_dur

    cm_dmg = 0.5 * cm["power"] * (atk / DEFAULT_ENEMY_DEF) * cm_stab + 0.5
    cm_dps = cm_dmg / cm_dur
    cm_eps = -cm["energy_delta"] / cm_dur

    # One-bar charged-move penalty — energy lost during damage window
    if cm["energy_delta"] == -100:
        dws = cm["damage_window_start"] / 1000
        cm_eps = (-cm["energy_delta"] + 0.5 * fm["energy_delta"] + 0.5 * y * dws) / cm_dur

    if fm_dps > cm_dps:
        return fm_dps

    # Guard against degenerate moves (zero energy on either side) that
    # would zero out the cycle-DPS denominator. Real PoGO data has a few
    # structural / event moves with energy_delta == 0; falling back to
    # fast-move-only DPS keeps the ranking stable instead of crashing.
    if (cm_eps + fm_eps) == 0:
        return fm_dps

    dps0 = (fm_dps * cm_eps + cm_dps * fm_eps) / (cm_eps + fm_eps)
    dps = dps0 + ((cm_dps - fm_dps) / (cm_eps + fm_eps)) * (0.5 - x / hp) * y
    return max(fm_dps, dps if dps > 0 else 0)


def calc_tdo(dps, hp, defense, shadow=False):
    """Total damage output — port of DialgaDex's GetTDO (calc.js:98)."""
    if shadow:
        defense = defense * SHADOW_DEF_MULT
    y = EST_Y_NUMERATOR / defense
    tof = hp / y
    return dps * tof


def calc_metric(dps, tdo):
    """Equivalent Damage Rating — DialgaDex's EER (calc.js:721).
    DPS^3 × TDO weighted; higher = stronger overall attacker."""
    if dps <= 0 or tdo <= 0:
        return 0
    return (dps ** 3) * tdo  # matches DialgaDex's "Metric" power form


def best_moveset(entry, fm_lookup, cm_lookup, shadow, level, type_filter=None):
    """Returns (best_dps, best_tdo, best_metric, best_fm_name, best_cm_name, atk, defense, hp).

    Iterates every (fm × cm) combination including elite moves. When
    type_filter is set, only counts movesets where either the fast or
    charged move matches that type (mirrors DialgaDex's per-type rank).
    """
    types = entry["types"]
    base_atk = entry["stats"]["baseAttack"]
    base_def = entry["stats"]["baseDefense"]
    base_hp = entry["stats"]["baseStamina"]
    atk = stat_at_level(base_atk, 15, level)
    defense = stat_at_level(base_def, 15, level)
    hp = int(stat_at_level(base_hp, 15, level))

    fms = list(entry.get("fm", [])) + list(entry.get("elite_fm", []))
    cms = list(entry.get("cm", [])) + list(entry.get("elite_cm", []))

    best = (0.0, 0.0, 0.0, None, None)
    for fm_name in fms:
        fm = fm_lookup.get(fm_name)
        if not fm:
            continue
        for cm_name in cms:
            cm = cm_lookup.get(cm_name)
            if not cm:
                continue
            if type_filter and fm["type"] != type_filter and cm["type"] != type_filter:
                continue
            dps = calc_dps(types, atk, defense, hp, fm, cm, shadow=shadow)
            tdo = calc_tdo(dps, hp, defense, shadow=shadow)
            metric = calc_metric(dps, tdo)
            if metric > best[2]:
                best = (dps, tdo, metric, fm_name, cm_name)
    return best + (atk, defense, hp)


def cmd_rank(args, pkm_data, announced_data):
    """Rank a species among all PvE attackers using DialgaDex's calc.

    Examples:
      rank "Necrozma" --form Normal              # base Necrozma vs. all
      rank "Necrozma" --form Dawn_wings --type Ghost
      rank "Mewtwo" --form Mega_y --level 50
    """
    species = args.species
    target_type = args.type.capitalize() if args.type else None
    level = args.level
    if level not in CPM:
        print(f"Error: --level must be 40 or 50, got {level}", file=sys.stderr)
        return 2

    target_entries = find_entries(pkm_data, species, args.form)
    if not target_entries:
        print(f"✗ Species not found in mgrann03: {species!r}")
        return 1
    # When the user wants a specific form, narrow to it (find_entries already
    # does this when --form is set); otherwise pick the base "Normal" form.
    if len(target_entries) > 1:
        target = next((e for e in target_entries if e.get("form") == "Normal"), target_entries[0])
    else:
        target = target_entries[0]

    fm_lookup, cm_lookup = fetch_moves_indexed()

    print(f"Ranking against the released PoGO attacker pool "
          f"(L{level}, perfect IVs, neutral target, "
          f"{'type-filtered: ' + target_type if target_type else 'any-type'})...",
          file=sys.stderr)

    rankings = []
    for e in pkm_data:
        if not e.get("released"):
            continue
        # Skip pure HP/raid-boss entries that lack stats (defensive).
        if not e.get("stats") or not e.get("fm") or not e.get("cm"):
            continue
        dps, tdo, metric, fm_name, cm_name, atk, defense, hp = best_moveset(
            e, fm_lookup, cm_lookup, shadow=False, level=level, type_filter=target_type)
        if metric == 0:
            continue
        rankings.append({
            "name": e["name"], "form": e.get("form", "Normal"),
            "dps": dps, "tdo": tdo, "metric": metric,
            "fm": fm_name, "cm": cm_name,
        })
        # Also include the Shadow variant if mgrann03 marks it available.
        if e.get("shadow"):
            sdps, stdo, smetric, sfm, scm, *_ = best_moveset(
                e, fm_lookup, cm_lookup, shadow=True, level=level, type_filter=target_type)
            if smetric > 0:
                rankings.append({
                    "name": "Shadow " + e["name"], "form": e.get("form", "Normal"),
                    "dps": sdps, "tdo": stdo, "metric": smetric,
                    "fm": sfm, "cm": scm,
                })

    rankings.sort(key=lambda r: r["metric"], reverse=True)

    # Locate the target row.
    target_name = target["name"]
    target_form = target.get("form", "Normal")
    target_idx = next(
        (i for i, r in enumerate(rankings)
         if r["name"] == target_name and r["form"] == target_form),
        None,
    )
    if target_idx is None:
        print(f"✗ {target_name} ({target_form}) didn't produce a valid ranking "
              f"(no moveset matched the filter?). Try without --type.")
        return 1

    rank = target_idx + 1
    total = len(rankings)
    pct = 100 * (1 - target_idx / total)
    def pretty(form):
        """mgrann03 form names use underscore_lowercase ('Dawn_wings'); humanize."""
        return form.replace("_", " ").title() if form else ""
    label = f"{target_name}" + (f" ({pretty(target_form)})" if target_form != "Normal" else "")
    print()
    print(f"   {label}")
    print(f"   ─ Rank #{rank} of {total} ({pct:.1f} percentile)")
    print(f"   ─ Best moveset: {rankings[target_idx]['fm']} / {rankings[target_idx]['cm']}")
    print(f"   ─ DPS {rankings[target_idx]['dps']:.2f}  "
          f"TDO {rankings[target_idx]['tdo']:.0f}  "
          f"EER {rankings[target_idx]['metric']/1e6:.2f}M")
    print()

    # Show ±5 neighbors so the rank reads in context.
    lo = max(0, target_idx - 5)
    hi = min(total, target_idx + 6)
    print(f"   Neighbors:")
    for i in range(lo, hi):
        r = rankings[i]
        marker = " ▶" if i == target_idx else "  "
        name = r["name"] + (f" ({pretty(r['form'])})" if r["form"] != "Normal" else "")
        print(f"   {marker} #{i+1:>3d}  {name:<30s}  DPS {r['dps']:6.2f}  TDO {r['tdo']:6.0f}")
    print()
    return 0


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

    p = sub.add_parser(
        "rank",
        help="Compute DialgaDex-style PvE attacker rank (DPS/TDO/EER)",
    )
    p.add_argument("species")
    p.add_argument("--form", help="Specific form (e.g., 'Mega', 'Dawn_wings'). Defaults to Normal.")
    p.add_argument("--type", help="Filter rankings to a specific attacker type (e.g., 'Psychic'). "
                                  "Default: any-type ranking.")
    p.add_argument("--level", type=int, default=40, choices=[40, 50],
                   help="Attacker level (default 40 = standard raid attacker).")

    args = ap.parse_args()

    pkm_data = fetch_cached("pkm", args.refresh)
    announced_data = fetch_cached("announced", args.refresh)

    handler = {
        "moveset": cmd_moveset,
        "debut": cmd_debut,
        "tier": cmd_tier,
        "shadow": cmd_shadow,
        "info": cmd_info,
        "rank": cmd_rank,
    }[args.cmd]
    sys.exit(handler(args, pkm_data, announced_data))


if __name__ == "__main__":
    main()
