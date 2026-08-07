#!/usr/bin/env node
/* Tool MANUAL (bukan autopilot): tulis artikel baru via TERAI lalu append ke data/articles.json */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const topic = process.argv.slice(2).join(' ');
if (!topic) {
  console.log('Gunakan: npm run article -- "Topik berita"');
  process.exit(1);
}
const dataFile = path.join(process.cwd(), 'data', 'articles.json');
const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));

const prompt = `Kamu adalah jurnalis berita Indonesia. Tulis artikel berita singkat (5-6 paragraf) tentang: "${topic}".
Balas HANYA dengan JSON valid (tanpa teks lain):
{"slug":"slug-url-berbahasa-indonesia","title":"Judul","excerpt":"Ringkasan 1 kalimat","category":"salah satu dari: ekonomi,teknologi,nasional,bisnis,pendidikan","author":"Tim Redaksi Aixwim","date":"ISO-8601 sekarang","reading_time":"N menit","tags":["tag1","tag2"],"content":["paragraf1","paragraf2","paragraf3","paragraf4","paragraf5"]}`;

const r = spawnSync('terai', ['ask', prompt], { encoding: 'utf8', timeout: 180000 });
if (r.status !== 0 || !r.stdout) {
  console.error('❌ TERAI tidak tersedia/gagal:', (r.stderr || '').slice(0, 300));
  process.exit(1);
}
let out = r.stdout.trim();
// ekstrak JSON dari fenced block bila ada
const m = out.match(/```(?:json)?\s*([\s\S]*?)```/);
if (m) out = m[1];
const jsonStart = out.indexOf('{');
const jsonEnd = out.lastIndexOf('}');
if (jsonStart < 0 || jsonEnd < 0) { console.error('❌ Output bukan JSON:', out.slice(0, 200)); process.exit(1); }
let art;
try { art = JSON.parse(out.slice(jsonStart, jsonEnd + 1)); }
catch (e) { console.error('❌ JSON tidak valid:', e.message); process.exit(1); }

if (!art.slug || !art.title || !art.content || !art.content.length) {
  console.error('❌ Artikel tidak lengkap:', JSON.stringify(art).slice(0, 200));
  process.exit(1);
}
if (data.articles.some((a) => a.slug === art.slug)) {
  console.error('⚠️ Slug sudah ada:', art.slug);
  process.exit(1);
}
data.articles.push(art);
fs.writeFileSync(dataFile, JSON.stringify(data, null, 1));
console.log(`✅ Artikel ditambahkan: ${art.title} (${art.category})`);
console.log('   Jalankan: npm run build && git add -A && git commit -m "feat: artikel baru" && git push');
