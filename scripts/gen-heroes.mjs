/**
 * Generate the Spawn Point themed hero library via fal Flux (schnell).
 * Each result is a permanent fal.media URL (same store as the brand icons).
 * Writes assets/brand-heroes/urls.json (themeKey -> URL) into the spawn-point repo.
 */
import { writeFileSync, mkdirSync } from 'node:fs'

const FAL_KEY = process.env.FAL_KEY
if (!FAL_KEY) { console.error('FAL_KEY not set'); process.exit(1) }
const MODEL = 'fal-ai/flux/schnell'
const TEMPLATE = (theme) => `Minimal abstract editorial graphic, ${theme} motif, flowing geometric shapes and soft gradient bars, deep midnight navy #0A1628 background, crimson #E30B5C and indigo #3D52A0 gradient accents, ice white highlights, premium dark tech aesthetic, generous negative space, no text, no letters, no logos, no characters`

// themeKey -> prompt motif. Covers the recurring Spawn Point issue types.
const THEMES = {
  water:       'ocean wave',
  fire:        'ember and flame',
  electric:    'lightning storm',
  grass:       'forest canopy leaves',
  dark:        'shadow mist',
  steel:       'steel gears and plating',
  dragon:      'dragon scales sweep',
  psychic:     'aurora ribbons',
  ice:         'frost crystal shards',
  news:        'radio broadcast signal waves',
  recon:       'magnifying lens and grid',
  anniversary: 'confetti burst celebration',
  generic:     'flowing signal ribbons',
}

async function gen(theme) {
  const headers = { Authorization: `Key ${FAL_KEY}`, 'Content-Type': 'application/json' }
  const submit = await fetch(`https://queue.fal.run/${MODEL}`, {
    method: 'POST', headers,
    body: JSON.stringify({ prompt: TEMPLATE(theme), image_size: { width: 1200, height: 600 }, num_images: 1, enable_safety_checker: true }),
  })
  if (!submit.ok) throw new Error(`submit ${submit.status}: ${await submit.text()}`)
  const { status_url, response_url } = await submit.json()
  for (let i = 0; i < 45; i++) {
    await new Promise((r) => setTimeout(r, 2000))
    const s = await fetch(status_url, { headers })
    if (!s.ok) continue
    const st = (await s.json()).status
    if (st === 'COMPLETED') break
    if (st === 'FAILED') throw new Error('FAILED')
  }
  const out = await fetch(response_url, { headers })
  const url = (await out.json())?.images?.[0]?.url
  if (!url) throw new Error('no url')
  return url
}

const urls = {}
for (const [key, motif] of Object.entries(THEMES)) {
  try {
    urls[key] = await gen(motif)
    console.log(`${key.padEnd(12)} ${motif.padEnd(28)} -> ${urls[key]}`)
  } catch (e) {
    console.log(`${key.padEnd(12)} FAILED: ${e.message}`)
  }
}

const dir = '/Users/joelandor/Documents/spawn-point/assets/brand-heroes'
mkdirSync(dir, { recursive: true })
writeFileSync(`${dir}/urls.json`, JSON.stringify(urls, null, 2) + '\n')
console.log(`\nWrote ${Object.keys(urls).length} hero URLs to assets/brand-heroes/urls.json`)
