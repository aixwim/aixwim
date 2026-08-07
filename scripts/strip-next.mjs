/* Pasca-proses build Next.js: hapus runtime JS, RSC payload, dan duplikat.
   Halaman sudah server-render penuh → semua ini tidak diperlukan. */
import fs from 'node:fs';
import path from 'node:path';

const dir = path.join(process.cwd(), 'docs');
const files = [];
(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith('.html')) files.push(p);
  }
})(dir);

let total = 0;
for (const f of files) {
  let html = fs.readFileSync(f, 'utf8');
  const before = html.length;
  html = html.replace(/<script\s+src="[^"]*\/_next\/[^"]*"[^>]*>\s*<\/script>/g, '');
  html = html.replace(/<link[^>]*href="[^"]*\/_next\/[^"]*"[^>]*\/?>/g, '');
  // blok RSC payload: self.__next_f.push(...) — dengan atau tanpa kurung awal
  html = html.replace(/<script>\(?self\.__next_f[^]*?<\/script>/g, '');
  fs.writeFileSync(f, html);
  total += before - html.length;
}
// hapus index.txt (RSC payload) & folder duplikat 404/
(function clean(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) {
      if (e.name === '404') { fs.rmSync(p, { recursive: true, force: true }); console.log('🗑️ hapus', p); continue; }
      clean(p);
    } else if (e.name === 'index.txt') {
      const s = fs.statSync(p).size;
      fs.unlinkSync(p);
      total += s;
      console.log(`🗑️ hapus ${path.relative(dir, p)} (-${s}B)`);
    }
  }
})(dir);
const nextDir = path.join(dir, '_next');
if (fs.existsSync(nextDir)) { fs.rmSync(nextDir, { recursive: true, force: true }); console.log('🗑️ docs/_next dihapus'); }
console.log(`✅ Strip: ${files.length} html, -${(total / 1024).toFixed(1)}KB`);
