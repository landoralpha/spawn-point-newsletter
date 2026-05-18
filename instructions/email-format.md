# Spawn Point Email Format Standard

**Single source of truth for every email sent by any Spawn Point agent.**
Every researcher / recon / monitor email follows this format. Consistency means readers know what they're looking at at a glance, and the agent isn't reinventing structure every run.

This file is referenced by:
- `triggers/researcher.md` — Step 0.5 (degraded), Step 4.5 (research plan), Step 7 (Pipeline Complete)
- `triggers/recon.md` — Step 0.5 (degraded), Step 6 (result)
- `triggers/monitor.md` — Step 0.5 (degraded), Step 6b (major news), Step 6c (cleanup info)

## Tool call (locked)

- Always via Spawn-Point-Fetcher MCP `send_email` tool.
- `to="joelandor@gmail.com"` (unless explicitly stated otherwise per-step).
- `body_format="html"` — NEVER plain text. The MCP auto-generates a plain-text fallback from the HTML for clients that need one.
- `subject` per the subject prefix convention below.
- `body` per the master HTML template below.

## Subject prefix convention

Every subject line starts with a bracketed prefix tagging which agent fired the email:

| Prefix | Used by | When |
|---|---|---|
| `[Spawn Point]` | researcher Step 7 | Customer-facing milestone — Pipeline Complete |
| `[Spawn Point Research]` | researcher Step 0.5 / 4.5 | Research-specific operational (degraded, plan) |
| `[Spawn Point Recon]` | recon Step 0.5 / 6 | Recon-specific (result, degraded) |
| `[Spawn Point Monitor]` | monitor Step 0.5 / 6b / 6c | Monitor-specific (major news, degraded, cleanup) |

**Subject format:** `[<prefix>] <SCREAMING TYPE IF ALERT — e.g., DEGRADED RUN>: <human-readable headline>`

Examples:
- `[Spawn Point] Issue #16 Pipeline Complete — Tapu Fini's Turn (May 30, 2026)`
- `[Spawn Point Research] DEGRADED RUN — fetch_url MCP unavailable`
- `[Spawn Point Recon] PRE-PUBLISH issues — Spawn Point #14 needs fixes`
- `[Spawn Point Monitor] Major Niantic news: Mega Mewtwo X/Y debut window confirmed`
- `[Spawn Point Monitor] Duplicate cleanup: 7 entries archived`

## Master HTML body skeleton

Every email body looks like this. Required sections vary per email type (table below), but the header banner + footer are universal.

```html
<h1>[emoji] [Title]</h1>

<p><strong>[Key 1]:</strong> [Value 1] | <strong>[Key 2]:</strong> [Value 2] | <strong>[Key 3]:</strong> [Value 3]</p>

[zero or more <h2> sections, each with prose + tables as needed]

<p style="margin-top: 24px; padding-top: 12px; border-top: 1px solid #ddd; color: #666; font-size: 0.9em;">
[Agent name] — [Run date YYYY-MM-DD] | [Run log: <a href="...">link</a>]
</p>
```

## Header banner — choose ONE emoji per email type

- 🚨 **Alert / Degraded mode** — anything that blocks a normal run (Step 0.5 across all agents)
- 📋 **Plan / pre-research** — the research plan email before drafting
- 🌊 / 🔥 / ⚡ / 🌳 / 🌙 / 🐝 / 🛡️ **Theme-of-the-week** — for the Pipeline Complete email, pick whatever fits the issue's flagship Pokémon / event type (water / fire / electric / grass / dark / bug / steel etc.)
- 🔍 **Fact-check / Recon** — for recon result emails
- 📰 **News / Monitor major-news** — when Niantic announces something
- 🧹 **Cleanup / housekeeping** — for monitor duplicate-cleanup info emails
- ✅ **Success-only milestone** — when used alone (rare; usually combined with theme emoji)

## Required sections per email type

| Email | Header banner | Status line | Notion Pages | Subject Lines | Audit Results | Hundo CPs | Source Health | Trending Topic | Trainer Tips | Archive Diff | Flags | Footer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Researcher Step 7 (Pipeline Complete) | 🌊/🔥/etc | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (4 cands) | ✅ (4 cands) | ✅ | ✅ | ✅ |
| Researcher Step 4.5 (Research Plan) | 📋 | ✅ | — | — | — | — | — | ✅ (4 cands shortlist) | ✅ (4 cands shortlist) | — | ✅ | ✅ |
| Researcher Step 0.5 (Degraded) | 🚨 | ✅ | — | — | — | — | ✅ (what's down) | — | — | — | ✅ (recovery checklist) | ✅ |
| Recon Step 6 (Result) | 🔍 | ✅ | — | — | ✅ (per-claim flags) | — | ✅ | — | — | — | ✅ | ✅ |
| Recon Step 0.5 (Degraded) | 🚨 | ✅ | — | — | — | — | ✅ | — | — | — | ✅ (recovery) | ✅ |
| Monitor Step 6b (Major news) | 📰 | ✅ | — | — | — | — | — | — | — | — | ✅ (news bullets) | ✅ |
| Monitor Step 6c (Cleanup info) | 🧹 | ✅ | — | — | — | — | — | — | — | — | ✅ (archived list) | ✅ |
| Monitor Step 0.5 (Degraded) | 🚨 | ✅ | — | — | — | — | ✅ | — | — | — | ✅ (recovery) | ✅ |

(✅ = required, — = omitted. Order matches the master skeleton.)

## Tables — universal style

Whenever data is tabular (Notion Pages, Hundo CP Provenance, Source Health, Pre-Publish Audit Results, Remaining Flags, etc.), use this exact form:

```html
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">
  <tr><th>Column 1</th><th>Column 2</th></tr>
  <tr><td>data</td><td>data</td></tr>
</table>
```

Rules:
- `border="1"` + `cellpadding="6"` + `cellspacing="0"` + `style="border-collapse:collapse;"` — the only styling. Gmail-safe.
- No CSS classes, no `<style>` blocks, no `<thead>` / `<tbody>` (Gmail-incompatible mobile rendering).
- For empty/zero-count tables, render one row that says `<td colspan="N">None this run.</td>` — never drop the section entirely.

## Status icons (use for at-a-glance scanning)

Use these unicode icons inline in cell content, NOT as a separate column:

- ✅ healthy / passed / complete / OK
- ❌ failed / blocked / missing / hard-fail
- ⚠️ degraded / partial / requires-attention / soft-flag

Examples:
- Data Source Health cell: `✅ 200 via fetch_url MCP` or `❌ 500 (Reddit transient)` or `⚠️ 200 but stale (newest article Feb 2026)`
- Pre-Publish Audit Results cell: `PASSED` or `FIXED (N findings)` or `HARD FAIL` (text + icon optional)

## Footer (universal)

Every email ends with this single-paragraph footer:

```html
<p style="margin-top: 24px; padding-top: 12px; border-top: 1px solid #ddd; color: #666; font-size: 0.9em;">
[Agent Name] — Run date: [YYYY-MM-DD] | <a href="https://www.notion.so/e57321c855844e22b41285873853e26c">Run Log</a> | Run ID: [trigger run ID if known, else omit this segment]
</p>
```

`[Agent Name]` values:
- `Spawn Point Research Agent`
- `Spawn Point Recon Agent`
- `Spawn Point News Monitor`

## Inline style rules

- All `<` / `>` inside content HTML-escaped (`&lt;` / `&gt;`) — they appear in regex patterns, code samples, and similar.
- All `&` HTML-escaped (`&amp;`) unless already an entity.
- URLs wrapped in `<a href="...">` so they're clickable in Gmail.
- Pokémon name accents (é, etc.) are fine as raw unicode — Gmail handles them.
- NO `<style>` blocks (Gmail strips them on inline mail).
- Inline `style="..."` attributes ONLY on the footer paragraph and the universal table style shown above. Don't add inline styles elsewhere.
- NO custom fonts or colors beyond the gray footer border. Default rendering is correct.

## Plain-text fallback

The MCP `send_email` tool auto-generates a plain-text body from the HTML. **Never author a separate plain-text body.** The HTML structure IS the source of truth — tables degrade to text-grid in the plain-text fallback, which is fine.

## When to deviate

Deviate ONLY if a specific email type has unusual content that breaks the table grid (e.g., a long code block). In that case, fall back to `<pre>` blocks inside the section, but keep the header banner, status line, sections, and footer intact.

---

**Last verified:** May 18, 2026 (when this file was first written from the Pipeline Complete email format Joe approved).
