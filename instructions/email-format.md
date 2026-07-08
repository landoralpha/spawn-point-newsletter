# Spawn Point Email Format Standard (v3 — Landoralpha branded, editorial layout)

**Single source of truth for every email sent by any Spawn Point agent.**
Every researcher / recon / monitor email follows this format. Consistency means Joe knows what he's looking at at a glance, and the agent isn't reinventing structure every run.

**DO NOT DEVIATE.** The HTML blocks below are copy-paste literals. Agents fill the `[bracketed slots]` with content and NOTHING else changes: not colors, not fonts, not padding, not structure. If a run needs something the template can't express, use the "When to deviate" rules at the bottom and flag the deviation in the Run Log Notes.

**Triggers do NOT embed their own copies of this HTML.** Each trigger step that emails defines only (a) the subject, (b) the slot values, and (c) which sections to include, then renders per this file. This file wins over any HTML fragment that survives in a trigger.

This file is referenced by:
- `triggers/researcher.md` — Step 0.5 (degraded), Step 4.5 (research plan), Step 7 (Pipeline Complete)
- `triggers/recon.md` — Step 0.5 (degraded), Step 6 (result)
- `triggers/monitor.md` — Step 0.5 (degraded), Step 6b (major news), Step 6c (cleanup info)

## Tool call (locked)

- Always via Spawn-Point-Fetcher MCP `send_email` tool.
- `to="joelandor@gmail.com"` (unless explicitly stated otherwise per-step).
- `body_format="html"` — NEVER plain text. The MCP auto-generates a plain-text fallback from the HTML for clients that need one.
- `subject` per the subject prefix convention below.
- `body` per the branded master template below.

## Subject prefix convention

Every subject line starts with a bracketed prefix tagging which agent fired the email:

| Prefix | Used by | When |
|---|---|---|
| `[Spawn Point]` | researcher Step 7 | Customer-facing milestone — Pipeline Complete |
| `[Spawn Point Research]` | researcher Step 0.5 / 4.5 | Research-specific operational (degraded, plan) |
| `[Spawn Point Recon]` | recon Step 0.5 / 6 | Recon-specific (result, degraded) |
| `[Spawn Point Monitor]` | monitor Step 0.5 / 6b / 6c | Monitor-specific (major news, degraded, cleanup) |

**Subject format:** `[<prefix>] <SCREAMING TYPE IF ALERT — e.g., DEGRADED RUN>: <human-readable headline>`

The archive-gap escalation string from `instructions/newsletter-archive.md` still injects into the subject when gap ≥ 2 — that rule is unchanged.

## Brand tokens (locked — Landoralpha "Midnight Signal")

| Token | Hex | Email use |
|---|---|---|
| Midnight Navy | `#0A1628` | Page background (always the base) |
| Deep Space | `#060F1C` | Table header rows only |
| Ice White | `#F0F4FF` | All primary text; button text |
| Crimson | `#E30B5C` | Links, eyebrow label, button border, footer band — NEVER as text on Deep Space |
| Muted Slate | `#8A94AD` | Secondary text: status line, captions |
| Border Navy | `#24365A` | All table borders and hairlines |

Font stacks (web fonts don't load in Gmail; the fallbacks ARE the design):
- Wordmark + headings: `'Outfit',Arial,'Helvetica Neue',sans-serif` (semibold 600 wordmark, bold 700 headlines)
- Body: `'Outfit',Arial,'Helvetica Neue',sans-serif`
- Data/technical/eyebrow: `'Space Mono','Courier New',monospace`

No other colors or fonts, anywhere, ever. No `<style>` blocks (Gmail strips them) — every style is inline.

## Layout anatomy (top to bottom)

1. **Header** — `SPAWN POINT` wordmark, top-left, semibold. Never changes.
2. **Headline** — large bold display line (the email's subject, human form).
3. **Hero image** — Flux-generated, report emails only (see Hero image section).
4. **Status line** — mono key/value facts strip.
5. **Eyebrow + sections** — one crimson eyebrow (flat icon + ALL-CAPS label) naming the email type, then big section headers with prose, tables, and buttons.
6. **Footer band** — full-width crimson band, navy text. Never changes structure.

## Master HTML body skeleton (locked)

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#0A1628" style="background-color:#0A1628;">
<tr><td align="center" style="padding:24px 12px 0 12px;">
<table width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="#0A1628" style="background-color:#0A1628; max-width:600px; width:100%;">

<!-- HEADER (locked, identical in every email) -->
<tr><td style="padding:28px 32px 8px 32px;">
  <p style="margin:0; font-family:'Outfit',Arial,'Helvetica Neue',sans-serif; font-weight:600; font-size:18px; letter-spacing:2px; color:#F0F4FF;">SPAWN POINT</p>
</td></tr>

<!-- HEADLINE -->
<tr><td style="padding:24px 32px 0 32px;">
  <h1 style="margin:0; font-family:'Outfit',Arial,'Helvetica Neue',sans-serif; font-weight:700; font-size:34px; line-height:1.2; color:#F0F4FF;">[Headline, sentence case, no emoji]</h1>
</td></tr>

<!-- HERO IMAGE (report emails only — omit this whole <tr> on degraded/cleanup emails or if generation fails) -->
<tr><td style="padding:24px 32px 0 32px;">
  <img src="[fal.media URL]" alt="[Headline]" width="536" style="display:block; width:100%; height:auto; border-radius:12px;" />
</td></tr>

<!-- STATUS LINE -->
<tr><td style="padding:20px 32px 0 32px;">
  <p style="margin:0; font-family:'Space Mono','Courier New',monospace; font-size:13px; line-height:1.6; color:#8A94AD;"><strong style="color:#F0F4FF;">[Key 1]:</strong> [Value 1] &nbsp;|&nbsp; <strong style="color:#F0F4FF;">[Key 2]:</strong> [Value 2] &nbsp;|&nbsp; <strong style="color:#F0F4FF;">[Key 3]:</strong> [Value 3]</p>
</td></tr>

<!-- EYEBROW (once, above the first section) — flat icon + label, NO emoji -->
<tr><td style="padding:32px 32px 0 32px;">
  <table cellpadding="0" cellspacing="0" border="0"><tr>
    <td valign="middle" style="padding-right:8px;"><img src="[eyebrow icon URL from the Icon system map]" alt="" width="16" height="16" style="display:block;" /></td>
    <td valign="middle"><p style="margin:0; font-family:'Space Mono','Courier New',monospace; font-weight:bold; font-size:11px; letter-spacing:3px; color:#E30B5C;">[EMAIL TYPE LABEL, ALL CAPS]</p></td>
  </tr></table>
</td></tr>

<!-- SECTION (repeat one <tr> per section, in the required-sections order) -->
<tr><td style="padding:12px 32px 0 32px;">
  <h2 style="margin:0 0 12px 0; font-family:'Outfit',Arial,'Helvetica Neue',sans-serif; font-weight:600; font-size:24px; line-height:1.3; color:#F0F4FF;">[Section title]</h2>
  <p style="margin:0 0 12px 0; font-family:'Outfit',Arial,'Helvetica Neue',sans-serif; font-size:15px; line-height:1.7; color:#F0F4FF;">[prose]</p>
  [data table if the section is tabular — exact form below]
  [button if the section has a primary link — exact form below]
</td></tr>

<!-- FOOTER BAND (locked) -->
<tr><td style="padding:40px 0 0 0;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#E30B5C" style="background-color:#E30B5C;">
    <tr><td style="padding:20px 32px;">
      <p style="margin:0; font-family:'Outfit',Arial,'Helvetica Neue',sans-serif; font-weight:600; font-size:14px; letter-spacing:2px; color:#0A1628;">SPAWN POINT</p>
      <p style="margin:6px 0 0 0; font-family:'Space Mono','Courier New',monospace; font-size:11px; line-height:1.6; color:#0A1628;">[Agent Name] · Run date: [YYYY-MM-DD] · <a href="https://www.notion.so/e57321c855844e22b41285873853e26c" style="color:#0A1628; text-decoration:underline;">Run Log</a> · Run ID: [trigger run ID if known, else omit this segment]</p>
    </td></tr>
  </table>
</td></tr>

</table>
</td></tr></table>
```

`[Agent Name]` values (unchanged):
- `Spawn Point Research Agent`
- `Spawn Point Recon Agent`
- `Spawn Point News Monitor`

Footer separators are `·` (middot). Never em dashes, anywhere in any email. No emoji anywhere — the eyebrow uses a flat icon (Icon system section), the headline carries neither icon nor emoji.

## Buttons (primary links)

When a section's job is sending Joe somewhere (the Notion draft, the research brief, the Run Log entry), render a button after the prose instead of burying the link:

```html
<table cellpadding="0" cellspacing="0" border="0" style="margin:16px 0 4px 0;">
  <tr><td style="border:1px solid #E30B5C; border-radius:4px;">
    <a href="[URL]" style="display:inline-block; padding:12px 24px; font-family:'Outfit',Arial,'Helvetica Neue',sans-serif; font-weight:600; font-size:14px; color:#F0F4FF; text-decoration:none;">[Button label]</a>
  </td></tr>
</table>
```

Max two buttons per email. Secondary links stay inline: `<a href="..." style="color:#E30B5C; text-decoration:none;">descriptive title</a>` — descriptive titles only, never raw URLs as link text.

## Icon system (flat line icons — NO emoji anywhere)

Spawn Point emails use flat line icons, never emoji. The set is Lucide (2px geometric stroke, no fill — matches the Landoralpha "thin-line icons only" brand rule), recolored to brand hex and served as 64×64 transparent PNGs.

**Hosting:** Gmail blocks inline `data:` URIs and strips inline `<svg>`, so every icon must be a hosted raster referenced by absolute URL. The set is uploaded to fal.storage (same account as the Flux hero), which serves permanent per-file URLs on `fal.media`. Paste the exact URL from the map below into each `<img src>`. There is NO shared base path — each icon is its own URL. The source of truth is `assets/brand-icons/urls.json`; re-run `scripts/upload-brand-icons.mjs` only if the art changes (new upload = new URLs, then update this table).

Every `<img>` carries `width` + `height` + descriptive `alt` so an images-off client (Gmail default until the sender is trusted) degrades to readable alt text, never a broken box.

**Eyebrow icon per email type** (one 16×16 icon left of the ALL-CAPS label):

| Email type | Eyebrow label | Icon URL |
|---|---|---|
| Researcher Step 7 (Pipeline Complete) | `PIPELINE COMPLETE · ISSUE #[N]` | `https://v3b.fal.media/files/b/0aa15abe/Y36Kl559RTF5woRDl-ofR_badge-check.png` |
| Researcher Step 4.5 (Research Plan) | `PRE-RESEARCH PLAN · ISSUE #[N]` | `https://v3b.fal.media/files/b/0aa15abe/bM3DczTH6oCLSQAcHkDsh_clipboard-list.png` |
| Recon Step 6 (Fact-Check) | `FACT-CHECK REPORT · ISSUE #[N]` | `https://v3b.fal.media/files/b/0aa15ac9/4IQaUfceVv5W58ZWeN1yR_search.png` |
| Monitor Step 6b (Major news) | `MAJOR NIANTIC NEWS` | `https://v3b.fal.media/files/b/0aa15abe/k1n7GFQXTXSsjjBc28sb5_newspaper.png` |
| Monitor Step 6c (Cleanup) | `DUPLICATE CLEANUP` | `https://v3b.fal.media/files/b/0aa15abe/N2x0P2U-8FcwF0ruwXRzk_trash-2.png` |
| Any agent Step 0.5 (Degraded) | `DEGRADED RUN` | `https://v3b.fal.media/files/b/0aa15ac9/msziIiBBJFznDdh8ShjhZ_triangle-alert.png` |

All six eyebrow icons are crimson `#E30B5C`. The email THEME still varies per issue, but it lives in the Flux hero image, not the icon — the eyebrow icon is fixed per email type so the type is instantly recognizable.

**Status icons** (13×13, inline in table cells, `vertical-align:middle`), replacing the old ✅/❌/⚠️ unicode:

| Meaning | alt | Color | Icon URL |
|---|---|---|---|
| healthy / passed / complete | `OK` | Ice White | `https://v3b.fal.media/files/b/0aa15abe/mIb4_l_iDlyjbIgnmezGI_circle-check.png` |
| failed / blocked / missing | `FAIL` | Crimson | `https://v3b.fal.media/files/b/0aa15abe/6xuNCGizm-JXHmMt3r8zN_circle-x.png` |
| degraded / partial / attention | `WARN` | Muted Rose `#FF4D8D` | `https://v3b.fal.media/files/b/0aa15abe/3yT3zyMAbOXFynLMj-Fic_triangle-alert-warn.png` |

Icon source of truth: the recolored PNGs live in `assets/brand-icons/` (generated from Lucide: `badge-check`, `clipboard-list`, `search`, `newspaper`, `trash-2`, `triangle-alert`, `circle-check`, `circle-x`). Regenerate with `stroke="[brand hex]"`, rasterize at 64×64, and re-upload via `scripts/upload-brand-icons.mjs` if the set is ever rebuilt.

## Hero image (Flux via fal.ai)

**Report emails only:** researcher Step 7 (Pipeline Complete), researcher Step 4.5 (Research Plan), recon Step 6 (result), monitor Step 6b (major news). Degraded (Step 0.5) and cleanup (Step 6c) emails NEVER carry an image — alert paths stay fast and dependency-free.

Generation (one MCP call, before assembling the body): call the Spawn-Point-Fetcher MCP `generate_image` tool with a short `theme` word:

```
generate_image(theme="ocean wave")   → {"success": true, "url": "https://...fal.media/...png"}
```

The tool holds `FAL_KEY` server-side (never in the trigger), applies the locked brand prompt below, and returns a public `fal.media` URL. Put `result.url` straight into the hero `<img src>`. Optional args: `width` / `height` (default 1200×600), `prompt_override` (leave unset in normal use).

**Locked prompt formula** (baked into the MCP tool — shown here for reference; the tool fills the ONE theme slot):

> Minimal abstract editorial graphic, [THEME] motif, flowing geometric shapes and soft gradient bars, deep midnight navy #0A1628 background, crimson #E30B5C and indigo #3D52A0 gradient accents, ice white highlights, premium dark tech aesthetic, generous negative space, no text, no letters, no logos, no characters

`theme` examples: `ocean wave` (water-week issue), `lightning storm` (electric), `radio broadcast signal` (major news), `magnifying lens` (recon report). One or two words, drawn from the email's subject matter. Never Pokémon likenesses — abstract motifs only (IP safety).

**Failure = omit.** If `generate_image` returns `success: false` (FAL_KEY not set on the server, fal error, timeout, missing URL) or the tool is absent: drop the hero `<tr>` entirely and note `[hero image skipped: <error>]` in the Run Log Notes. Never retry more than once, never block the email on the image. The email is fully branded without it.

## Required sections per email type

| Email | Eyebrow | Hero | Status line | Notion Pages | Subject Lines | Audit Results | Hundo CPs | Source Health | Trending Topic | Trainer Tips | Archive Diff | Flags | Footer band |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Researcher Step 7 (Pipeline Complete) | badge-check · PIPELINE COMPLETE | ✅ | ✅ | ✅ | ✅ (5 options) | ✅ | ✅ | ✅ | ✅ (4 cands) | ✅ (4 cands) | ✅ | ✅ | ✅ |
| Researcher Step 4.5 (Research Plan) | clipboard-list · PRE-RESEARCH PLAN | ✅ | ✅ | — | — | — | — | — | ✅ (4 cands shortlist) | ✅ (4 cands shortlist) | — | ✅ | ✅ |
| Researcher Step 0.5 (Degraded) | triangle-alert · DEGRADED RUN | — | ✅ | — | — | — | — | ✅ (what's down) | — | — | — | ✅ (recovery checklist) | ✅ |
| Recon Step 6 (Result) | search · FACT-CHECK REPORT | ✅ | ✅ | — | — | ✅ (per-claim flags) | — | ✅ | — | — | — | ✅ | ✅ |
| Recon Step 0.5 (Degraded) | triangle-alert · DEGRADED RUN | — | ✅ | — | — | — | — | ✅ | — | — | — | ✅ (recovery) | ✅ |
| Monitor Step 6b (Major news) | newspaper · MAJOR NIANTIC NEWS | ✅ | ✅ | — | — | — | — | — | — | — | — | ✅ (news bullets) | ✅ |
| Monitor Step 6c (Cleanup info) | trash-2 · DUPLICATE CLEANUP | — | ✅ | — | — | — | — | — | — | — | — | ✅ (archived list) | ✅ |
| Monitor Step 0.5 (Degraded) | triangle-alert · DEGRADED RUN | — | ✅ | — | — | — | — | ✅ | — | — | — | ✅ (recovery) | ✅ |

(✅ = required, — = omitted. Order matches the master skeleton. Source Health tables must include rows for ScrapedDuck endpoints and hundo-cp-master.json wherever the table appears in researcher emails.)

## Data tables — universal style (locked)

Whenever data is tabular (Notion Pages, Hundo CP Provenance, Source Health, Pre-Publish Audit Results, Remaining Flags, etc.), use this exact form inside a SECTION block:

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse; font-family:'Outfit',Arial,'Helvetica Neue',sans-serif; font-size:13px; line-height:1.5;">
  <tr>
    <th align="left" bgcolor="#060F1C" style="background-color:#060F1C; color:#F0F4FF; padding:8px 10px; border:1px solid #24365A; font-weight:bold;">Column 1</th>
    <th align="left" bgcolor="#060F1C" style="background-color:#060F1C; color:#F0F4FF; padding:8px 10px; border:1px solid #24365A; font-weight:bold;">Column 2</th>
  </tr>
  <tr>
    <td style="color:#F0F4FF; padding:8px 10px; border:1px solid #24365A;">data</td>
    <td style="color:#F0F4FF; padding:8px 10px; border:1px solid #24365A;">data</td>
  </tr>
</table>
```

Rules:
- Header cells: `bgcolor="#060F1C"` + the exact inline style shown. Data cells: the exact inline style shown. Nothing else.
- No `<thead>` / `<tbody>` (Gmail-incompatible mobile rendering). No `border="1"` attribute — borders come from the inline cell styles.
- Crimson never appears as text inside header cells (Deep Space background). Links inside DATA cells are fine: `<a href="..." style="color:#E30B5C;">`.
- Numbers, dates, timestamps inside cells may use `<span style="font-family:'Space Mono','Courier New',monospace;">` — optional, only for genuinely technical values.
- **CP values in emails carry NO thousands comma** (`2286`, not `2,286`) — monospace columns align cleaner without it. (This is the email convention; the reader-facing Beehiiv newsletter body keeps its own locked comma format per `newsletter-creation.md`.)
- For empty/zero-count tables, render one row that says `<td colspan="N" style="color:#F0F4FF; padding:8px 10px; border:1px solid #24365A;">None this run.</td>` — never drop the section entirely.

## Status icons (use for at-a-glance scanning)

Use the flat status-icon PNGs (URLs in the Icon system status table) inline in cell content, NOT as a separate column. Each is 13×13, `vertical-align:middle`, with `alt`:

- `<img src="[circle-check URL]" alt="OK" width="13" height="13" style="vertical-align:middle;" />` healthy / passed / complete
- `<img src="[circle-x URL]" alt="FAIL" width="13" height="13" style="vertical-align:middle;" />` failed / blocked / missing
- `<img src="[triangle-alert-warn URL]" alt="WARN" width="13" height="13" style="vertical-align:middle;" />` degraded / partial / requires-attention

Examples:
- Data Source Health cell: `<img [circle-check] alt="OK"> 200 via fetch_url MCP` or `<img [circle-x] alt="FAIL"> 500 (Reddit transient)` or `<img [triangle-alert-warn] alt="WARN"> 200 but stale (newest article Feb 2026)`
- Pre-Publish Audit Results cell: `PASSED` or `FIXED (N findings)` or `HARD FAIL` (text + icon optional)

## Pre-send checklist (run before every send_email call)

Verify the assembled body against ALL of these. Any failure = fix before sending, never send-then-note:

1. Header wordmark is exactly `SPAWN POINT` at font-weight 600; footer band is the crimson table with navy text; both match the skeleton byte-for-byte apart from slot values.
2. Zero `<style>` blocks; zero fonts/colors outside the brand token table; the only `<img>` tags are the hero (report emails only, fal.media URL) and the flat icons (eyebrow + status), each `src` an exact fal.media URL from the Icon system map, and every one carrying `width`, `height`, and `alt`.
3. ZERO emoji anywhere in the body. Exactly one crimson eyebrow, ALL CAPS, led by the correct flat icon per the Icon system table. Headline has no icon and no emoji.
4. Every table cell (`<th>`/`<td>`) carries `border:1px solid #24365A`; header cells are Deep Space.
5. At most two buttons; every other link is inline crimson with a descriptive title, never a raw URL.
6. Zero em dashes in the entire body. Footer separators are `·`. CP values have no thousands comma.
7. All `<` / `>` inside content HTML-escaped (`&lt;` / `&gt;`) — they appear in regex patterns and code samples. All bare `&` escaped as `&amp;`.
8. Required sections for this email type (matrix above) are all present, in skeleton order.

## Plain-text fallback

The MCP `send_email` tool auto-generates a plain-text body from the HTML. **Never author a separate plain-text body.** The HTML structure IS the source of truth — tables degrade to text-grid in the plain-text fallback, which is fine.

## When to deviate

Deviate ONLY if a specific email type has unusual content that breaks the table grid (e.g., a long code block). In that case, fall back to a `<pre>` block styled `style="font-family:'Space Mono','Courier New',monospace; font-size:12px; color:#F0F4FF; background-color:#060F1C; padding:12px; border:1px solid #24365A; overflow-x:auto;"` inside the section, but keep the header, headline, status line, eyebrow, sections, and footer band intact. Note the deviation in the Run Log Notes.

---

**Last verified:** July 7, 2026 (v3 — editorial layout per Joe's reference: wordmark header, display headline, Flux hero image, crimson footer band. Required-sections matrix carried over from v1/v2; subject-line count corrected to 5 per newsletter-creation.md).
