/**
 * One-time uploader: pushes assets/brand-icons/*.png to fal.storage and writes
 * assets/brand-icons/urls.json (semantic name -> public fal.media URL).
 *
 * These URLs are embedded into instructions/email-format.md as the locked icon set.
 * Re-run only if the icon art changes (URLs are permanent per upload).
 *
 * Usage:
 *   FAL_KEY=xxxx node scripts/upload-brand-icons.mjs
 *   node scripts/upload-brand-icons.mjs --env /path/to/.env.local   (reads FAL_KEY= line)
 *
 * No dependencies — raw fal storage REST, same auth style as the card-generator scripts.
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ICON_DIR = join(__dirname, '..', 'assets', 'brand-icons')

// --- resolve FAL_KEY ---
let FAL_KEY = process.env.FAL_KEY
const envArgIdx = process.argv.indexOf('--env')
if (!FAL_KEY && envArgIdx !== -1 && process.argv[envArgIdx + 1]) {
  const line = readFileSync(process.argv[envArgIdx + 1], 'utf8')
    .split('\n')
    .find((l) => l.trim().startsWith('FAL_KEY='))
  if (line) FAL_KEY = line.split('=').slice(1).join('=').trim().replace(/^["']|["']$/g, '')
}
if (!FAL_KEY) {
  console.error('FAL_KEY not set. Pass FAL_KEY=... or --env /path/to/.env.local')
  process.exit(1)
}

const INITIATE = 'https://rest.alpha.fal.ai/storage/upload/initiate'

async function uploadOne(name, bytes) {
  // 1. initiate: ask fal for a signed upload target + the eventual public URL
  const init = await fetch(`${INITIATE}?content_type=image/png&file_name=${encodeURIComponent(name)}`, {
    method: 'POST',
    headers: { Authorization: `Key ${FAL_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ content_type: 'image/png', file_name: name }),
  })
  if (!init.ok) throw new Error(`initiate ${name}: ${init.status} ${await init.text()}`)
  const { upload_url, file_url } = await init.json()
  // 2. PUT the bytes to the signed target
  const put = await fetch(upload_url, {
    method: 'PUT',
    headers: { 'Content-Type': 'image/png' },
    body: bytes,
  })
  if (!put.ok) throw new Error(`put ${name}: ${put.status} ${await put.text()}`)
  return file_url
}

const files = readdirSync(ICON_DIR).filter((f) => f.endsWith('.png'))
const only = process.argv.includes('--one') ? files.slice(0, 1) : files
const urls = {}
for (const f of only) {
  const bytes = readFileSync(join(ICON_DIR, f))
  const url = await uploadOne(f, bytes)
  urls[f.replace(/\.png$/, '')] = url
  console.log(`${f}  ->  ${url}`)
}
if (!process.argv.includes('--one')) {
  writeFileSync(join(ICON_DIR, 'urls.json'), JSON.stringify(urls, null, 2) + '\n')
  console.log(`\nWrote ${Object.keys(urls).length} URLs to assets/brand-icons/urls.json`)
}
