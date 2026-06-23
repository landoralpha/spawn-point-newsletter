#!/usr/bin/env python3
"""Spawn Point readability + AI-tell auditor.

Four passes over a draft (markdown text from --file, --notion-page-id, or stdin):

  1. Grade-level scoring per section — FKGL, Gunning Fog, Coleman-Liau
     triangulated. Target: every section ≤ 6.0 grade level.

  2. Per-sentence worst-offender flagging — the 10 hardest sentences in
     the whole draft, quoted with the metric that flunks them.

  3. AI-tell regex sweep — patterns loaded from ai_slop_patterns.json
     in three tiers (hard / warn / structural). Hard tells are an
     immediate-action flag even though the run doesn't hard-stop.
     DEPRECATED as of 2026-06-17 — the harshaneel/humanize `ai-check`
     skill at ~/.claude/skills/ai-check is the canonical AI-detection
     layer now. Pass 3 still runs for backwards compatibility but the
     workflow docs (researcher.md Step 5.5, recon.md Category L) call
     ai-check as Phase B and treat its verdict as authoritative.

  4. Sourceless-claim detection — appeals to authority ("studies show",
     "most trainers", etc.) without a URL or citation within 300 chars.

The tool's own output is plain English with no AI tells. Quote the
offending sentence, name the metric that flunks it, suggest a fix.

Usage:
  ./readability_check.py --file draft.md
  ./readability_check.py < draft.md
  ./readability_check.py --file draft.md --strict   # exit 1 on any flag
  ./readability_check.py --file draft.md --target 6.0
  ./readability_check.py --file draft.md --only slop  # one pass only

Exit codes:
  0 — all sections ≤ target grade AND zero tier-1 AI tells
  1 — at least one section above target OR at least one tier-1 AI tell
  2 — argument error / file not readable

Joe's bar (2026-06-15):
  - Flat target ≤ 6.0 across every section (5th–6th grade)
  - Tier-1 AI tells are FLAG, not hard-stop, BUT need immediate fix
  - Tool output must be human readable
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PATTERNS_PATH = os.path.join(ROOT, "ai_slop_patterns.json")

# ----------------------------- text parsing -----------------------------

SECTION_HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'])")
WORD_RE = re.compile(r"\b[\w'-]+\b")
URL_RE = re.compile(r"https?://[^\s)\]]+")


def strip_markdown_chrome(text):
    """Remove markdown structure that isn't prose — code blocks, image refs,
    table syntax, list markers, bold/italic markers. Leaves the words behind.

    Bullet items get a terminal period added if they don't have one already,
    so the sentence splitter sees each bullet as its own sentence rather than
    merging them all together (a single 6-bullet 'Week at a Glance' would
    otherwise score as one mega-sentence in the 80+ word range)."""
    # Code blocks
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`[^`]+`", " ", text)
    # Image references
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    # Link syntax — keep link text, drop URL
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Bold / italic markers
    text = re.sub(r"\*\*|__|\*|_", "", text)

    # Bullet handling — strip the marker AND make sure each bullet ends in
    # punctuation so sentence splitting treats them individually.
    def normalize_bullet(match):
        body = match.group(1).rstrip()
        if not body:
            return ""
        if body[-1] not in ".!?":
            body += "."
        return body + "\n"

    text = re.sub(r"^[\s]*[-*+]\s+(.+)$", normalize_bullet, text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s+(.+)$", normalize_bullet, text, flags=re.MULTILINE)

    # Blockquote markers
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    # Pipe-tables — keep cell text
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"^[\s|:-]+$", "", text, flags=re.MULTILINE)
    # Trim
    return text.strip()


def split_into_sections(markdown):
    """Return [(heading_text, body_text), ...]. The intro before the first
    heading is captured as 'Intro' if non-empty."""
    sections = []
    matches = list(SECTION_HEADER_RE.finditer(markdown))
    if not matches:
        return [("Body", markdown)]
    if matches[0].start() > 0:
        intro = markdown[: matches[0].start()].strip()
        if intro:
            sections.append(("Intro", intro))
    for i, m in enumerate(matches):
        heading = m.group(2).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        body = markdown[body_start:body_end].strip()
        if body:
            sections.append((heading, body))
    return sections


def split_sentences(text):
    """Naive sentence splitter — good enough for editorial work.

    Treats newlines as a hard sentence boundary first (so bullets and short
    headed lines split cleanly even when the lookahead-on-capital wouldn't
    fire — emoji-prefixed bullets, for example), then runs the standard
    punctuation-based splitter inside each line."""
    if not text or not text.strip():
        return []
    out = []
    for line in re.split(r"\n+", text):
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line:
            continue
        parts = SENTENCE_END_RE.split(line)
        out.extend(p.strip() for p in parts if p.strip())
    return out


# ----------------------------- syllable counting -----------------------------

VOWELS = set("aeiouy")


def count_syllables(word):
    """Heuristic syllable counter — counts vowel groups, subtracts silent 'e',
    accounts for 'le' endings. Good enough for grade-level math at the
    ±0.3 grade-level tolerance we care about."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    count = 0
    prev_was_vowel = False
    for c in w:
        is_vowel = c in VOWELS
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    # Silent 'e' at end
    if w.endswith("e") and count > 1:
        count -= 1
    # 'le' ending preceded by consonant gets a syllable back
    if len(w) > 2 and w.endswith("le") and w[-3] not in VOWELS:
        count += 1
    return max(count, 1)


# ----------------------------- metrics -----------------------------

def metrics_for(text):
    """Return {grade_fkgl, grade_gunning_fog, grade_coleman_liau, words, sentences, syllables, complex_words, letters}."""
    sentences = split_sentences(text)
    words = WORD_RE.findall(text)
    n_sent = max(len(sentences), 1)
    n_words = max(len(words), 1)
    n_syll = sum(count_syllables(w) for w in words)
    n_complex = sum(1 for w in words if count_syllables(w) >= 3)
    n_letters = sum(len(re.sub(r"[^a-zA-Z]", "", w)) for w in words)

    asl = n_words / n_sent
    asw = n_syll / n_words
    pct_complex = n_complex / n_words

    fkgl = 0.39 * asl + 11.8 * asw - 15.59
    gunning_fog = 0.4 * (asl + 100 * pct_complex)
    # Coleman-Liau
    L = n_letters / n_words * 100  # letters per 100 words
    S = n_sent / n_words * 100      # sentences per 100 words
    coleman_liau = 0.0588 * L - 0.296 * S - 15.8

    return {
        "fkgl": fkgl,
        "gunning_fog": gunning_fog,
        "coleman_liau": coleman_liau,
        "words": n_words,
        "sentences": n_sent,
        "syllables": n_syll,
        "complex_words": n_complex,
    }


def grade_summary(m):
    """Average of the three metrics (rough triangulation), and the max."""
    vals = [m["fkgl"], m["gunning_fog"], m["coleman_liau"]]
    return {"avg": sum(vals) / 3, "max": max(vals)}


# ----------------------------- AI-tells -----------------------------

def load_patterns():
    if not os.path.exists(PATTERNS_PATH):
        print(f"WARNING: {PATTERNS_PATH} not found; skipping AI-tell pass.", file=sys.stderr)
        return {}
    with open(PATTERNS_PATH) as f:
        return json.load(f)


def find_tells(text, patterns):
    """Scan text for tier-1/2/3 AI tells. Returns [(tier, match_string, fix, span), ...]."""
    hits = []
    for tier in ("tier1_hard", "tier2_warn", "tier3_structural"):
        for entry in patterns.get(tier, []):
            pat = re.compile(entry["pattern"], re.IGNORECASE)
            for m in pat.finditer(text):
                hits.append((tier, m.group(0), entry["fix"], m.span()))
    return hits


def find_sourceless_claims(text, patterns):
    """Sourceless authority appeals — claims like 'studies show' without a URL nearby."""
    hits = []
    for entry in patterns.get("sourceless_claim_patterns", []):
        pat = re.compile(entry["pattern"], re.IGNORECASE)
        for m in pat.finditer(text):
            window = text[max(0, m.start() - 300):min(len(text), m.end() + 300)]
            if not URL_RE.search(window):
                hits.append((m.group(0), entry["fix"], m.span()))
    return hits


# ----------------------------- worst sentences -----------------------------

def per_sentence_grades(section_name, body):
    """Compute FKGL per sentence, return list of (section, sentence, fkgl, length)."""
    items = []
    for s in split_sentences(strip_markdown_chrome(body)):
        if len(WORD_RE.findall(s)) < 5:
            continue  # skip fragments — they tank the math
        m = metrics_for(s)
        items.append((section_name, s, m["fkgl"], m["words"]))
    return items


# ----------------------------- report -----------------------------

def truncate(s, n=90):
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def render_report(sections, target, slop_hits, sourceless_hits, worst_sentences):
    out = []
    out.append("=== Readability Check ===\n")

    # Section grades
    out.append(f"Section grades (target ≤ {target:.1f}):")
    out.append("")
    out.append(f"  {'':<2} {'Section':<28} {'FKGL':>6} {'Fog':>6} {'CL':>6} {'Worst':>6}")
    out.append("  " + "-" * 56)
    failed_sections = []
    for name, m in sections:
        s = grade_summary(m)
        flag = "✓" if s["max"] <= target else "⚠" if s["max"] <= target + 1.5 else "✗"
        if s["max"] > target:
            failed_sections.append((name, s["max"]))
        out.append(
            f"  {flag:<2} {truncate(name, 28):<28} "
            f"{m['fkgl']:>6.1f} {m['gunning_fog']:>6.1f} {m['coleman_liau']:>6.1f} "
            f"{s['max']:>6.1f}"
        )
    out.append("")

    # Worst sentences
    if worst_sentences:
        out.append("Hardest sentences (lower these first):")
        out.append("")
        for section, sent, grade, n_words in worst_sentences[:10]:
            out.append(f"  [{truncate(section, 22)} | FKGL {grade:.1f} | {n_words}w]")
            out.append(f"    \"{truncate(sent, 100)}\"")
            why = []
            if n_words > 25:
                why.append(f"too long ({n_words} words)")
            m = metrics_for(sent)
            poly_pct = m["complex_words"] / max(m["words"], 1) * 100
            if poly_pct > 20:
                why.append(f"polysyllable density {poly_pct:.0f}%")
            if not why:
                why.append("long sentence + abstract words")
            out.append(f"    why: {'; '.join(why)}")
            out.append("")

    # AI tells
    by_tier = {"tier1_hard": [], "tier2_warn": [], "tier3_structural": []}
    for tier, match, fix, span in slop_hits:
        by_tier[tier].append((match, fix))

    if by_tier["tier1_hard"]:
        out.append(f"AI tells — IMMEDIATE FIX ({len(by_tier['tier1_hard'])}):")
        for match, fix in by_tier["tier1_hard"]:
            out.append(f"  ✗ \"{match}\" — {fix}")
        out.append("")

    if by_tier["tier2_warn"]:
        out.append(f"AI tells — review ({len(by_tier['tier2_warn'])}):")
        for match, fix in by_tier["tier2_warn"]:
            out.append(f"  ⚠ \"{match}\" — {fix}")
        out.append("")

    if by_tier["tier3_structural"]:
        out.append(f"Structural tells — review ({len(by_tier['tier3_structural'])}):")
        for match, fix in by_tier["tier3_structural"]:
            out.append(f"  ⚠ \"{truncate(match, 60)}\" — {fix}")
        out.append("")

    # Sourceless claims
    if sourceless_hits:
        out.append(f"Sourceless claims ({len(sourceless_hits)}):")
        for match, fix, span in sourceless_hits:
            out.append(f"  ? \"{match}\" — {fix}")
        out.append("")

    # Verdict
    tier1_count = len(by_tier["tier1_hard"])
    if failed_sections or tier1_count:
        out.append("Result: FAILED")
        if failed_sections:
            details = ", ".join(f"{n} ({g:.1f})" for n, g in failed_sections)
            out.append(f"  - {len(failed_sections)} section(s) above target: {details}")
        if tier1_count:
            out.append(f"  - {tier1_count} tier-1 AI tell(s)")
    else:
        out.append("Result: PASSED")

    return "\n".join(out)


# ----------------------------- main -----------------------------

def parse_word_budget(s):
    """Parse '1400-1800' into (floor, ceiling). Returns (None, None) on 'off'."""
    if not s or s.lower() == "off":
        return (None, None)
    m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", s)
    if not m:
        raise ValueError(f"--word-budget must be 'floor-ceiling' or 'off', got: {s!r}")
    floor, ceil = int(m.group(1)), int(m.group(2))
    if floor > ceil:
        raise ValueError(f"--word-budget floor ({floor}) > ceiling ({ceil})")
    return (floor, ceil)


def count_body_words(raw):
    """Count words in the body prose, excluding scaffolding sections that
    don't reach the reader (Subject Line Options, Headline Options, Subtitle
    Options, Opening Paragraph Options, Pre-Publish Audit Results, Hundo CP
    Provenance Table) AND graphic-placeholder briefs (raid card placeholders
    are agent→Joe annotations that get replaced by the actual image at
    embed time). Uses the same chrome stripper as the readability passes so
    URLs / table syntax / bold markers don't inflate the count."""
    EDITORIAL_HEADINGS = (
        "subject line options", "title options", "headline options",
        "subtitle options", "opening paragraph options",
        "pre-publish audit results", "pre-publish audit",
        "hundo cp provenance", "editorial options",
        "selected for draft",
    )

    # Graphic-placeholder lines — these are briefs the drafting agent writes
    # for Joe (per instructions/graphics-brief.md). At publish time, the
    # placeholder text is replaced by the actual graphic, so the brief text
    # never reaches the reader and shouldn't inflate the body word count.
    GRAPHIC_PLACEHOLDER_RE = re.compile(
        r"^\s*>?\s*🎨\s+\*\*(?:RAID CARD|EVENT CARD|CUP CARD|MAX BATTLE CARD|HUNDO STRIP)",
        re.IGNORECASE,
    )

    def strip_placeholder_blocks(text):
        out_lines = []
        in_placeholder = False
        for line in text.splitlines():
            if GRAPHIC_PLACEHOLDER_RE.match(line):
                in_placeholder = True
                continue
            if in_placeholder:
                # Placeholder ends at the next blank line or non-blockquote line.
                if not line.strip() or not line.lstrip().startswith(">"):
                    in_placeholder = False
                    if line.strip():
                        out_lines.append(line)
                continue
            out_lines.append(line)
        return "\n".join(out_lines)

    body_chunks = []
    for name, body in split_into_sections(raw):
        if name and any(name.lower().startswith(h) for h in EDITORIAL_HEADINGS):
            continue
        body_chunks.append(strip_placeholder_blocks(body))

    if not body_chunks:
        body_chunks = [strip_placeholder_blocks(raw)]

    text = strip_markdown_chrome("\n\n".join(body_chunks))
    return len(WORD_RE.findall(text))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="Path to markdown file. If omitted, reads stdin.")
    ap.add_argument("--target", type=float, default=6.0, help="Max grade per section (default 6.0)")
    ap.add_argument("--strict", action="store_true", help="Exit 1 on any tier-2 or sourceless flag too")
    ap.add_argument("--only", choices=["grade", "slop", "claims", "budget"], help="Run only one pass")
    ap.add_argument("--word-budget", default="off", help="Body word range, e.g. '1400-1800'. 'off' disables. Default off so existing CI doesn't break; the newsletter workflow passes '1400-1800' explicitly (raised from 1400-1700 on 2026-06-23 to accommodate Spotlight Hour as a required H2 section).")
    args = ap.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        with open(args.file) as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()

    if not raw.strip():
        print("Error: input is empty.", file=sys.stderr)
        sys.exit(2)

    try:
        budget_floor, budget_ceiling = parse_word_budget(args.word_budget)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    patterns = load_patterns()
    sections = []
    all_sentences = []
    for name, body in split_into_sections(raw):
        prose = strip_markdown_chrome(body)
        if len(WORD_RE.findall(prose)) < 10:
            continue  # skip short sections like single-bullet glossary headings
        sections.append((name, metrics_for(prose)))
        all_sentences.extend(per_sentence_grades(name, body))

    worst = sorted(all_sentences, key=lambda t: -t[2])

    only = args.only
    slop_hits = find_tells(strip_markdown_chrome(raw), patterns) if only in (None, "slop") else []
    sourceless_hits = find_sourceless_claims(strip_markdown_chrome(raw), patterns) if only in (None, "claims") else []
    show_grade = only in (None, "grade")

    print(render_report(
        sections if show_grade else [],
        args.target,
        slop_hits,
        sourceless_hits,
        worst if show_grade else [],
    ))

    # Word-budget pass (always reports if --word-budget was set)
    budget_fail = False
    if budget_floor is not None and only in (None, "budget"):
        body_wc = count_body_words(raw)
        print()
        print("=== Word-Budget Check ===")
        print(f"  Body word count: {body_wc}")
        print(f"  Target range:    {budget_floor}–{budget_ceiling}")
        if body_wc < budget_floor:
            print(f"  ✗ Under floor by {budget_floor - body_wc} words. Section may feel thin — add depth in Trending Topic or Trainer Tips, not in reference-data sections.")
            budget_fail = True
        elif body_wc > budget_ceiling:
            print(f"  ✗ Over ceiling by {body_wc - budget_ceiling} words. Cut reference data first (counter lists, spawn lists, GO Pass tiers) — those should move to embedded graphics per instructions/graphics-brief.md. Daily Discoveries and Don't Miss are the next-biggest bulk offenders.")
            budget_fail = True
        else:
            print(f"  ✓ Within target range.")

    # Exit code
    failed_sections = [(n, grade_summary(m)["max"]) for n, m in sections if grade_summary(m)["max"] > args.target]
    tier1_hits = [h for h in slop_hits if h[0] == "tier1_hard"]
    fail = bool(failed_sections) or bool(tier1_hits) or budget_fail
    if args.strict:
        fail = fail or any(h[0] == "tier2_warn" for h in slop_hits) or bool(sourceless_hits)
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
