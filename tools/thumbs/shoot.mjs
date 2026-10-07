// Screenshots each studio's booking page (desktop, first screen) for email thumbnails.
import { chromium } from 'playwright'
import { readFileSync, mkdirSync } from 'fs'
const people = JSON.parse(readFileSync('tools/thumbs/people.json', 'utf8'))
mkdirSync('tools/thumbs/out', { recursive: true })
const b = await chromium.launch()
const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 })
for (const o of people) {
  await p.goto(o.url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {})
  await p.waitForTimeout(5000)
  await p.evaluate(() => { window.scrollTo(0, 0); document.querySelectorAll('.chat-fab,.ava-fab,.pswitch').forEach(e => e.remove()) })
  await p.waitForTimeout(500)
  await p.screenshot({ path: `tools/thumbs/out/${o.slug}.png` })
  console.log('shot', o.slug)
}
await b.close()
