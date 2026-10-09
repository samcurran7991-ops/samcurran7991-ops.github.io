// Screenshots the first screen of each studio's tour (studio page, phone app and dashboard together)
// for the "All three pieces" email picture.
import { chromium } from 'playwright'
import { readFileSync, mkdirSync, existsSync } from 'fs'
if (!existsSync('tools/thumbs/show.json')) process.exit(0)
const people = JSON.parse(readFileSync('tools/thumbs/show.json', 'utf8'))
mkdirSync('tools/thumbs/out', { recursive: true })
const b = await chromium.launch()
const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 })
for (const o of people) {
  await p.goto(o.url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {})
  await p.waitForTimeout(9000)
  await p.evaluate(() => { window.scrollTo(0, 0); document.querySelectorAll('.show-cue,.fab').forEach(e => e.remove()) })
  await p.waitForTimeout(800)
  await p.screenshot({ path: `tools/thumbs/out/show-${o.slug}.png` })
  console.log('shot show', o.slug)
}
await b.close()
