# Aixwim News — Portal Berita Indonesia Autopilot

Portal berita statis berbahasa Indonesia — **cepat (Pagespeed 100), SEO lengkap, dan dikelola otomatis**.

## Arsitektur

```
data/articles.json   ← Master data berita (engine autopilot menulis di sini)
build_site.py        ← Static site builder (Python stdlib, tanpa dependensi)
public/              ← Output build
/                    ← Root = output live (GitHub Pages serve dari root)
```

## Build

```bash
python3 build_site.py
# → public/index.html, artikel/*.html, kategori/*.html,
#   sitemap.xml, rss.xml, robots.txt, 404.html, favicon.svg
```

## Keunggulan

- **1 request per halaman** — CSS inline, tanpa JS, tanpa font eksternal
- **SEO penuh** — JSON-LD NewsArticle, OG/Twitter, canonical, sitemap dinamis, RSS
- **Semantik** — HTML5 `article/main/nav/time`, breadcrumb, aria-label
- **Dark mode** otomatis via `prefers-color-scheme`
- **Autopilot** — pipeline GitHub Actions menambah artikel → build → deploy otomatis

## Alur Autopilot

1. Engine generate artikel → tambah ke `data/articles.json`
2. `python3 build_site.py` → render ulang seluruh situs
3. Sync `public/` → root → commit → push
4. GitHub Pages rebuild otomatis

© 2026 Aixwim News — Berita Indonesia Terpercaya, Cepat, dan Akurat
