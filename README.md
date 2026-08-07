# Aixwim News

Portal berita Indonesia — ekonomi, teknologi, nasional, bisnis, dan pendidikan.
Statis, cepat, SEO-friendly. Dibangun dengan **Jekyll** + **GitHub Pages**.

## 🌐 Live

https://aixwim.github.io/aixwim/

## ⚡ Fitur

- 100% statis: 1 request per halaman (CSS/JS inline), tanpa framework
- SEO: JSON-LD (NewsArticle, WebSite, BreadcrumbList), sitemap, RSS, canonical
- Pencarian real-time (Ctrl+/), tema 3-mode (light/dark/auto), dark mode otomatis
- Share buttons (WA, X, FB, LinkedIn, Telegram), artikel terkait, back-to-top
- Responsif + aksesibel (skip-link, aria, semantic HTML)

## 📁 Struktur

```
_config.yml          → konfigurasi (url, baseurl, plugin)
_layouts/            → default, home, post, kategori, cari, 404
_includes/           → head, nav, footer, card + style.css + script.js
_posts/*.md          → artikel (markdown + frontmatter)
kategori/*.md        → halaman kategori
cari/index.md        → halaman pencarian
pages.yml            → konfigurasi Pages CMS
```

## ✍️ Kelola Konten

### Via Pages CMS (mudah)
1. Buka https://pagescms.org → Connect with GitHub → login manual
2. Pilih repo `aixwim` → menu **Artikel**
3. Buat/edit post → setiap publish otomatis commit → situs langsung update

### Via git (manual)
```bash
# Tambah artikel baru
nano _posts/YYYY-MM-DD-judul-slug.md   # frontmatter: layout, title, categories, date, author, excerpt, reading_time, tags

# Build lokal (opsional, perlu ruby/jekyll)
jekyll build

# Publish
git add -A && git commit -m "artikel baru: ..." && git push
```

## 🏗️ Build Lokal

```bash
gem install jekyll jekyll-sitemap
jekyll serve   # → http://localhost:4000/aixwim/
```

## 📄 Lisensi

MIT © 2026 Aixwim News
