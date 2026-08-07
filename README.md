# Aixwim News

Portal berita Indonesia — dibangun dengan **Next.js 15** (static export), tanpa autopilot.

## Stack
- Next.js (App Router, `output: 'export'`) → HTML statis di `docs/`
- GitHub Pages (source: `main` branch, folder `/docs`)
- Konten: `data/articles.json` (file-based CMS)

## Perintah
```bash
npm install          # install dependencies
npm run dev          # dev server
npm run build        # generate rss.xml + next build + strip runtime JS → docs/
npm run article -- "Topik berita"   # (opsional) tulis artikel via TERAI lalu append data
```

## Tambah Artikel (manual)
1. Edit `data/articles.json` (ikuti skema artikel yang ada) **atau**
2. `npm run article -- "judul topik"` → TERAI menulis → otomatis di-append
3. `npm run build && git add -A && git commit -m "feat: artikel baru" && git push`

## Fitur
- 10 artikel, 5 kategori, pencarian real-time (tanpa JS eksternal)
- JSON-LD: NewsArticle, BreadcrumbList, WebSite+SearchAction
- RSS, sitemap, robots.txt, 404 custom, dark mode, share buttons
- **1 request per halaman** (CSS/JS inline, tanpa dependensi eksternal) → Pagespeed optimal
