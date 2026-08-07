#!/usr/bin/env python3
"""
Aixwim News — Static News Site Builder
=======================================
Membangun portal berita statis dari data/articles.json:
  index.html, artikel/*.html, kategori/*.html, cari/index.html,
  search_index.json, sitemap.xml, rss.xml, robots.txt, 404.html,
  favicon.svg, assets/css/style.css

Desain: HTML murni + CSS/JS inline (1 request per halaman) => Pagespeed 100.
Python stdlib only — berjalan di Termux maupun GitHub Actions.

Fitur: navbar sticky + burger mobile, hero, cards, pencarian real-time
(search_index.json + overlay + halaman /cari/), tema 3-mode (light/dark/auto),
share buttons, breadcrumb + JSON-LD, reading time, artikel terkait,
pagination kategori, back-to-top, fade-in, dark mode otomatis.
"""

import json
import math
import re
import shutil
import urllib.parse
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "articles.json"
OUT = ROOT / "public"
SUBWEB_SRC = ROOT / "subwebs"

BASE = "https://aixwim.github.io/aixwim/"


# ---------------------------------------------------------------- helpers
def load_data() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


data = load_data  # alias


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def fmt_date(iso: str, fmt: str = "%d %B %Y") -> str:
    dt = datetime.fromisoformat(iso)
    months = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember",
    }
    if fmt == "%d %B %Y":
        return f"{dt.day} {months[dt.month]} {dt.year}"
    if fmt == "%B %Y":
        return f"{months[dt.month]} {dt.year}"
    return dt.strftime(fmt)


def iso_to_rfc822(iso: str) -> str:
    dt = datetime.fromisoformat(iso)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return (f"{days[dt.weekday()]}, {dt.day:02d} {months[dt.month-1]} "
            f"{dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} +0700")


def cat_by_slug(data: dict, slug: str) -> dict:
    return next((c for c in data["categories"] if c["slug"] == slug), {"slug": slug, "name": slug})


def build_head(title: str, desc: str, url: str, kind: str = "article") -> str:
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0a2540">
<link rel="icon" href="{BASE}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="Aixwim News">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}favicon.svg">
<meta property="og:locale" content="id_ID">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{BASE}favicon.svg">
"""


# ================================================================ CSS
CSS = """:root{--navy:#0a2540;--blue:#1565c0;--red:#c62828;--gold:#ffd166;--ink:#1a1a1a;--mut:#5f6b7a;--line:#e4e8ee;--bg:#f6f8fb;--card-bg:#fff;--navy-soft:rgba(10,37,64,.08)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans",Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;font-size:17px}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
.skip-link{position:absolute;left:-999px;top:0;background:var(--navy);color:#fff;padding:.6rem 1rem;z-index:99}
.skip-link:focus{left:0}
.topbar{background:var(--navy);color:#fff;font-size:.8rem;padding:.35rem 0;text-align:center}
.topbar span{opacity:.85}
header.site{background:var(--navy);color:#fff;padding:1.1rem 1.25rem;position:sticky;top:0;z-index:50;box-shadow:0 2px 12px rgba(10,37,64,.25)}
header.site .wrap{max-width:1080px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:.6rem;font-size:1.35rem;font-weight:800;letter-spacing:-.02em;color:#fff}
.brand .logo{width:34px;height:34px;border-radius:8px;background:var(--gold);color:var(--navy);display:grid;place-items:center;font-weight:900;font-size:1.15rem}
nav.main{display:flex;gap:.25rem;flex-wrap:wrap}
nav.main a{color:#cdd9e8;font-size:.92rem;font-weight:600;padding:.4rem .7rem;border-radius:6px}
nav.main a:hover{background:rgba(255,255,255,.12);color:#fff;text-decoration:none}
nav.main a.active{background:rgba(255,209,102,.16);color:var(--gold)}
.nav-actions{display:flex;gap:.4rem;align-items:center}
.icon-btn{background:rgba(255,255,255,.14);border:0;color:#fff;width:36px;height:36px;border-radius:10px;cursor:pointer;font-size:1rem;display:grid;place-items:center;transition:background .15s}
.icon-btn:hover{background:rgba(255,255,255,.28)}
.burger{display:none;background:none;border:0;cursor:pointer;padding:.45rem;flex-direction:column;gap:5px}
.burger span{display:block;width:24px;height:2.5px;background:#fff;border-radius:2px;transition:transform .25s,opacity .25s}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.25rem}
.breaking{background:var(--card-bg);border-bottom:1px solid var(--line);font-size:.85rem}
.breaking .wrap{display:flex;gap:.5rem;align-items:center;padding-top:.5rem;padding-bottom:.5rem;overflow-x:auto;white-space:nowrap}
.breaking b{background:var(--red);color:#fff;padding:.12rem .5rem;border-radius:4px;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em}
.breaking a{color:var(--ink);font-weight:600}
.breaking a:hover{color:var(--red)}
.hero{background:linear-gradient(135deg,#0a2540 0%,#123f6e 60%,#1565c0 100%);color:#fff;padding:2.2rem 0;margin-bottom:1.75rem}
.hero .wrap{display:grid;grid-template-columns:1fr;gap:.25rem}
.hero .kicker{display:inline-block;background:var(--gold);color:var(--navy);font-weight:800;font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;padding:.22rem .65rem;border-radius:4px;margin-bottom:.8rem}
.hero h1{font-size:clamp(1.6rem,4vw,2.5rem);line-height:1.2;font-weight:800;letter-spacing:-.02em;max-width:20em}
.hero h1 a{color:#fff}
.hero p.lead{margin-top:.8rem;font-size:1.08rem;color:#cdd9e8;max-width:42em}
.hero .meta{margin-top:1rem;color:#9fb3c8;font-size:.85rem;display:flex;gap:1rem;flex-wrap:wrap}
.hero .meta b{color:var(--gold);font-weight:700}
section.block{background:var(--card-bg);border:1px solid var(--line);border-radius:12px;padding:1.5rem;margin-bottom:1.75rem}
h2.sect{font-size:1.15rem;font-weight:800;color:var(--navy);display:flex;align-items:center;gap:.6rem;margin-bottom:1.1rem;padding-bottom:.6rem;border-bottom:2px solid var(--gold)}
h2.sect::before{content:"";width:6px;height:20px;background:var(--red);border-radius:3px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.25rem}
.card{background:var(--card-bg);border:1px solid var(--line);border-radius:10px;padding:1.15rem;display:flex;flex-direction:column;gap:.55rem;transition:box-shadow .15s ease,transform .15s ease}
.card:hover{box-shadow:0 6px 20px rgba(10,37,64,.12);transform:translateY(-3px)}
.card .cat{align-self:flex-start;font-size:.7rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;color:var(--blue);background:var(--navy-soft);padding:.18rem .6rem;border-radius:4px}
.card h3{font-size:1.06rem;line-height:1.35;font-weight:700}
.card h3 a{color:var(--ink)}
.card h3 a:hover{color:var(--blue)}
.card p{font-size:.9rem;color:var(--mut)}
.card time{font-size:.78rem;color:var(--mut)}
.article-body{max-width:720px;margin:0 auto;background:var(--card-bg);border:1px solid var(--line);border-radius:12px;padding:2.2rem 2rem;margin-top:1.75rem}
.breadcrumb{font-size:.8rem;color:var(--mut);margin-bottom:1.1rem;display:flex;gap:.4rem;flex-wrap:wrap}
.breadcrumb a{color:var(--mut)}
.breadcrumb a:hover{color:var(--blue)}
.article-body h1{font-size:clamp(1.5rem,3.5vw,2.1rem);line-height:1.25;font-weight:800;letter-spacing:-.02em;color:var(--navy)}
.byline{display:flex;gap:1.2rem;flex-wrap:wrap;font-size:.85rem;color:var(--mut);margin:1rem 0 1.4rem;padding-bottom:1rem;border-bottom:1px solid var(--line)}
.byline b{color:var(--ink)}
.article-body p{margin-bottom:1.15rem;font-size:1.04rem}
.article-body p:first-of-type{font-size:1.13rem;color:#2b3a4a}
.share{display:flex;gap:.45rem;flex-wrap:wrap;margin:1.3rem 0 0;padding-top:1rem;border-top:1px solid var(--line);align-items:center}
.share .lbl{font-size:.78rem;color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-right:.2rem}
.share a{font-size:.75rem;font-weight:700;padding:.35rem .7rem;border-radius:20px;color:#fff;text-decoration:none}
.share a:hover{opacity:.85;text-decoration:none}
.share .wa{background:#25d366}.share .x{background:#111}.share .fb{background:#1877f2}.share .li{background:#0a66c2}.share .tg{background:#229ed9}
.tags{display:flex;gap:.5rem;flex-wrap:wrap;margin:1.4rem 0 0;padding-top:1rem;border-top:1px solid var(--line)}
.tags span{font-size:.72rem;background:#eef2f7;color:var(--navy);font-weight:600;padding:.25rem .7rem;border-radius:20px}
.related{margin-top:2rem}
.related h3{font-size:.95rem;color:var(--mut);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.8rem}
.pagination{display:flex;gap:.4rem;justify-content:center;margin-top:1.4rem;flex-wrap:wrap}
.pagination a,.pagination span{display:grid;place-items:center;min-width:36px;height:36px;padding:0 .6rem;border-radius:8px;background:var(--card-bg);border:1px solid var(--line);color:var(--navy);font-weight:700;font-size:.9rem;text-decoration:none}
.pagination a:hover{background:var(--blue);color:#fff;border-color:var(--blue);text-decoration:none}
.pagination .cur{background:var(--navy);color:var(--gold);border-color:var(--navy)}
footer.site{background:var(--navy);color:#9fb3c8;margin-top:2.5rem;padding:2rem 0 1.2rem;font-size:.85rem}
footer.site .wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem}
footer.site h4{color:#fff;font-size:.95rem;margin-bottom:.6rem}
footer.site ul{list-style:none}
footer.site li{margin-bottom:.35rem}
footer.site a{color:#9fb3c8}
footer.site a:hover{color:var(--gold)}
.copy{text-align:center;margin-top:1.5rem;border-top:1px solid rgba(255,255,255,.12);padding-top:1rem;font-size:.78rem}
.notfound{text-align:center;padding:4rem 1rem;max-width:560px;margin:0 auto}
.notfound h1{font-size:4rem;color:var(--navy)}
.to-top{position:fixed;right:1.1rem;bottom:1.1rem;width:44px;height:44px;border-radius:50%;border:0;background:var(--navy);color:var(--gold);font-size:1.25rem;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.3);z-index:80;transition:transform .15s}
.to-top:hover{transform:translateY(-3px)}
.search-overlay{position:fixed;inset:0;background:rgba(8,18,32,.74);backdrop-filter:blur(5px);z-index:90;display:flex;flex-direction:column;align-items:center;padding:9vh 1rem 2rem}
.search-box{width:min(640px,100%);display:flex;gap:.5rem;background:#fff;border-radius:14px;padding:.55rem .7rem;box-shadow:0 10px 40px rgba(0,0,0,.4)}
.search-box input{flex:1;border:0;outline:0;font-size:1.05rem;background:transparent;color:#111}
.search-box input::placeholder{color:#889}
.search-box button{border:0;background:var(--navy);color:#fff;border-radius:10px;padding:.42rem .85rem;cursor:pointer;font-size:.95rem;font-weight:700}
.search-results{width:min(640px,100%);margin-top:.8rem;background:#fff;border-radius:14px;padding:.6rem;max-height:55vh;overflow:auto;box-shadow:0 10px 40px rgba(0,0,0,.4)}
.s-item{display:block;padding:.7rem .8rem;border-radius:10px;text-decoration:none;color:inherit}
.s-item:hover{background:#f0f4f9;text-decoration:none}
.s-cat{font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:var(--blue);background:rgba(21,101,192,.08);padding:.15rem .5rem;border-radius:4px}
.s-title{display:block;font-weight:700;color:#111;margin:.25rem 0;line-height:1.35}
.s-title mark{background:var(--gold);border-radius:3px;padding:0 .1rem}
.s-meta{font-size:.75rem;color:#667}
.s-hint,.s-none{color:#667;font-size:.9rem;padding:.6rem .8rem}
.cari-input{width:100%;border:1px solid var(--line);border-radius:12px;padding:.75rem 1rem;font-size:1.05rem;outline:0;background:var(--card-bg);color:var(--ink)}
.cari-input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(21,101,192,.15)}
main{animation:fadeIn .45s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media(max-width:720px){.burger{display:flex}nav.main{display:none}nav.main.open{display:flex;flex-direction:column;position:absolute;top:100%;left:0;right:0;background:var(--navy);padding:.6rem 1rem 1rem;box-shadow:0 10px 24px rgba(0,0,0,.35)}nav.main.open a{padding:.6rem .7rem}}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#e8ecf1;--mut:#9aa7b6;--line:#2a3444;--bg:#0f1620;--card-bg:#16202e;--navy-soft:rgba(255,255,255,.08)}body{background:var(--bg)}.card h3 a{color:#f0f4f8}.tags span{background:#223044;color:#cdd9e8}.pagination a,.pagination span{background:var(--card-bg);color:#e8ecf1}}
:root[data-theme="dark"]{--ink:#e8ecf1;--mut:#9aa7b6;--line:#2a3444;--bg:#0f1620;--card-bg:#16202e;--navy-soft:rgba(255,255,255,.08)}
:root[data-theme="dark"] .card h3 a{color:#f0f4f8}
:root[data-theme="dark"] .tags span{background:#223044;color:#cdd9e8}
:root[data-theme="dark"] .pagination a,:root[data-theme="dark"] .pagination span{background:var(--card-bg);color:#e8ecf1}
:root[data-theme="light"]{--ink:#1a1a1a;--mut:#5f6b7a;--line:#e4e8ee;--bg:#f6f8fb;--card-bg:#fff;--navy-soft:rgba(10,37,64,.08)}
"""


# ================================================================ JS
APP_JS = """(function(){
var BASE="__BASE__";
function $(id){return document.getElementById(id)}
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML}
/* ---------- tema 3-mode ---------- */
var th=localStorage.getItem('aixwim-theme')||'auto';
function applyTheme(t){document.documentElement.setAttribute('data-theme',t);
var b=$('themeBtn');if(b){b.textContent=t==='dark'?'☀️':(t==='light'?'🌙':'🌓');b.setAttribute('aria-label','Tema: '+t);b.title='Tema: '+t;}}
applyTheme(th);
var tb=$('themeBtn');
if(tb){tb.addEventListener('click',function(){var o=['light','dark','auto'];var i=o.indexOf(th);th=o[(i+1)%3];localStorage.setItem('aixwim-theme',th);applyTheme(th);});}
/* ---------- burger mobile ---------- */
var burger=$('burgerBtn'),nav=$('mainNav');
if(burger&&nav){burger.addEventListener('click',function(){var open=nav.classList.toggle('open');burger.setAttribute('aria-expanded',open?'true':'false');});}
/* ---------- back to top ---------- */
var topBtn=$('toTop');
if(topBtn){window.addEventListener('scroll',function(){topBtn.hidden=window.scrollY<400;},{passive:true});
topBtn.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});}
/* ---------- pencarian ---------- */
var overlay=$('searchOverlay'),inp=$('searchInput'),res=$('searchResults'),closeBtn=$('searchClose');
var idxCache=null;
function loadIdx(){if(idxCache)return Promise.resolve(idxCache);
return fetch(BASE+'search_index.json').then(function(r){return r.json();}).then(function(d){idxCache=d;return d;}).catch(function(){return [];});}
function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
function runSearch(q){
q=norm(q.trim());
if(!res)return;
if(q.length<2){res.innerHTML='<p class="s-hint">Ketik minimal 2 huruf untuk mencari…</p>';return;}
loadIdx().then(function(idx){
var out=[];
idx.forEach(function(a){
var s=0,t=norm(a.title),x=norm(a.excerpt),c=norm(a.category_name),tg=norm((a.tags||[]).join(' '));
if(t.indexOf(q)>=0)s+=10;
if(c.indexOf(q)>=0)s+=6;
if(tg.indexOf(q)>=0)s+=4;
if(x.indexOf(q)>=0)s+=1;
if(s>0)out.push({a:a,s:s});
});
out.sort(function(x,y){return y.s-x.s;});
var top=out.slice(0,10);
if(!top.length){res.innerHTML='<p class="s-none">Tidak ditemukan untuk “'+esc(q)+'”. Coba kata kunci lain.</p>';return;}
res.innerHTML=top.map(function(o){
var a=o.a,t=a.title,i=norm(t).indexOf(q);
if(i>=0)t=t.slice(0,i)+'<mark>'+esc(t.slice(i,i+q.length))+'</mark>'+esc(t.slice(i+q.length));
return '<a class="s-item" href="'+BASE+'artikel/'+a.slug+'.html"><span class="s-cat">'+esc(a.category_name)+'</span><span class="s-title">'+t+'</span><span class="s-meta">'+esc(a.date.split('T')[0])+' · '+esc(a.reading_time)+' baca</span></a>';
}).join('');
}).catch(function(){res.innerHTML='<p class="s-none">Gagal memuat indeks pencarian.</p>';});
}
function openSearch(){if(!overlay)return;overlay.hidden=false;if(inp)inp.focus();if(inp&&inp.value.length>=2)runSearch(inp.value);}
function closeSearch(){if(overlay)overlay.hidden=true;}
var sBtn=$('searchBtn');
if(sBtn)sBtn.addEventListener('click',openSearch);
if(closeBtn)closeBtn.addEventListener('click',closeSearch);
if(overlay)overlay.addEventListener('click',function(e){if(e.target===overlay)closeSearch();});
if(inp){inp.addEventListener('input',function(){runSearch(inp.value);});
inp.addEventListener('keydown',function(e){if(e.key==='Escape')closeSearch();});}
document.addEventListener('keydown',function(e){
if((e.ctrlKey||e.metaKey)&&e.key==='/'){e.preventDefault();openSearch();}
if(e.key==='Escape'&&overlay&&!overlay.hidden)closeSearch();});
/* ---------- mode halaman /cari/ ---------- */
var page=$('searchPage');
if(page){var p=new URLSearchParams(window.location.search);var qp=p.get('q');
if(qp){if(inp)inp.value=qp;runSearch(qp);}}
})();
"""


# ================================================================ komponen
def page_shell(title: str, desc: str, url: str, body: str, kind: str = "article",
               include_search: bool = True) -> str:
    overlay = ""
    if include_search:
        overlay = f"""<div class="search-overlay" id="searchOverlay" hidden role="dialog" aria-label="Pencarian">
<div class="search-box"><input id="searchInput" type="search" placeholder="Cari berita… (Esc untuk tutup)" autocomplete="off" aria-label="Kata kunci pencarian"><button id="searchClose" type="button">Tutup</button></div>
<div class="search-results" id="searchResults"></div>
</div>"""
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
{build_head(title, desc, url, kind)}
<style>{CSS}</style>
</head>
<body>
<a class="skip-link" href="#main">Langsung ke konten</a>
{body}
<button class="to-top" id="toTop" aria-label="Kembali ke atas" hidden>↑</button>
{overlay}
<script>{APP_JS.replace("__BASE__", BASE)}</script>
</body>
</html>
"""


def header_html(active: str = "") -> str:
    d = data()
    cats = "".join(
        f'<a href="kategori/{c["slug"]}.html"{" class=active" if active==c["slug"] else ""}>{escape(c["name"])}</a>'
        for c in d["categories"]
    )
    return f"""<div class="topbar"><span>🔥 Berita terpercaya sejak 2026 · Independen & Akurat</span></div>
<header class="site"><div class="wrap">
<a class="brand" href="index.html"><span class="logo">A</span><span>Aixwim <em style="font-style:normal;color:var(--gold)">News</em></span></a>
<nav class="main" id="mainNav" aria-label="Kategori"><a href="index.html">Beranda</a>{cats}</nav>
<div class="nav-actions">
<button class="icon-btn" id="searchBtn" type="button" aria-label="Cari berita" title="Cari (Ctrl+/)">🔍</button>
<button class="icon-btn" id="themeBtn" type="button" aria-label="Ganti tema">🌓</button>
</div>
<button class="burger" id="burgerBtn" type="button" aria-label="Buka menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>"""


def footer_html() -> str:
    d = data()
    cats = "".join(f'<li><a href="kategori/{c["slug"]}.html">{escape(c["name"])}</a></li>' for c in d["categories"])
    hubs = subweb_links()
    return f"""<footer class="site"><div class="wrap">
<div><h4>{escape(d["site"]["name"])}</h4><p>{escape(d["site"]["tagline"])}</p></div>
<div><h4>Kategori</h4><ul>{cats}</ul></div>
<div><h4>Hub</h4><ul>{hubs}</ul></div>
<div><h4>Tentang</h4><ul>
<li><a href="index.html">Beranda</a></li>
<li><a href="cari/index.html">Pencarian</a></li>
<li><a href="rss.xml">RSS Feed</a></li>
<li><a href="sitemap.xml">Sitemap</a></li>
</ul></div>
</div>
<div class="copy">© {d["site"]["established"]} {escape(d["site"]["name"])} · {escape(d["site"]["editor"])} · Semua konten dilindungi hak cipta.</div>
</footer>"""


def subweb_links() -> str:
    """Tautan ke halaman hub subweb (dari staging root/subwebs/)."""
    if not SUBWEB_SRC.is_dir():
        return ""
    links = []
    for f in sorted(SUBWEB_SRC.glob("*.html")):
        slug = f.stem
        name = slug.replace("hub-", "").replace("-", " ").title() or slug
        links.append(f'<li><a href="subwebs/{escape(slug)}.html">{escape(name)}</a></li>')
    return "".join(links)


def subweb_urls() -> list[str]:
    """Daftar URL subweb untuk sitemap (dari staging root/subwebs/)."""
    if not SUBWEB_SRC.is_dir():
        return []
    return [f"{BASE}subwebs/{f.name}" for f in sorted(SUBWEB_SRC.glob("*.html"))]


def hero_block(art: dict) -> str:
    url = f'artikel/{art["slug"]}.html'
    return f"""<section class="hero"><div class="wrap">
<span class="kicker">Berita Utama</span>
<h1><a href="{url}">{escape(art["title"])}</a></h1>
<p class="lead">{escape(art["excerpt"])}</p>
<div class="meta"><span><b>Kategori:</b> {escape(cat_by_slug(data(), art["category"])["name"])}</span><span><b>Waktu baca:</b> {art["reading_time"]}</span><span><b>Update:</b> {fmt_date(art["date"])}</span></div>
</div></section>"""


def card_html(art: dict) -> str:
    cat = cat_by_slug(data(), art["category"])
    return f"""<article class="card">
<span class="cat">{escape(cat["name"])}</span>
<h3><a href="artikel/{art["slug"]}.html">{escape(art["title"])}</a></h3>
<p>{escape(art["excerpt"])}</p>
<time datetime="{art["date"]}">{fmt_date(art["date"])}</time>
</article>"""


def share_html(url: str, title: str) -> str:
    u = urllib.parse.quote(url, safe="")
    t = urllib.parse.quote(title)
    return f"""<div class="share"><span class="lbl">Bagikan:</span>
<a class="wa" rel="noopener" target="_blank" href="https://wa.me/?text={t}%20{u}">WhatsApp</a>
<a class="x" rel="noopener" target="_blank" href="https://twitter.com/intent/tweet?url={u}&text={t}">X</a>
<a class="fb" rel="noopener" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u={u}">Facebook</a>
<a class="li" rel="noopener" target="_blank" href="https://www.linkedin.com/sharing/share-offsite/?url={u}">LinkedIn</a>
<a class="tg" rel="noopener" target="_blank" href="https://t.me/share/url?url={u}&text={t}">Telegram</a>
</div>"""


def breadcrumb_ld(crumbs: list) -> str:
    items = ",".join(
        f"""{{"@type":"ListItem","position":{i+1},"name":{json.dumps(n, ensure_ascii=False)},"item":{json.dumps(u, ensure_ascii=False)}}}"""
        for i, (n, u) in enumerate(crumbs)
    )
    return f"""<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{items}]}}</script>"""


# ---------------------------------------------------------------- renderers
def render_index(d: dict) -> str:
    arts = sorted(d["articles"], key=lambda a: a["date"], reverse=True)
    hero = hero_block(arts[0])
    rest = arts[1:]
    latest = "".join(card_html(a) for a in rest[:6])
    blocks = []
    for cat in d["categories"]:
        items = [a for a in arts if a["category"] == cat["slug"]][:3]
        if not items:
            continue
        cards = "".join(card_html(a) for a in items)
        blocks.append(f"""<section class="block"><h2 class="sect">{escape(cat["name"])}</h2><div class="grid">{cards}</div></section>""")
    body = f"""{header_html()}
{hero}
<main id="main"><div class="wrap">
<section class="block"><h2 class="sect">Berita Terbaru</h2><div class="grid">{latest}</div></section>
{"".join(blocks)}
</div></main>
{footer_html()}"""
    website_ld = (
        '<script type="application/ld+json">{"@context":"https://schema.org",'
        '"@type":"WebSite","name":"' + d["site"]["name"] + '",'
        '"alternateName":"Aixwim News Indonesia","url":"' + BASE + '",'
        '"description":"' + d["site"]["description"] + '",'
        '"inLanguage":"id",'
        '"publisher":{"@type":"Organization","name":"' + d["site"]["name"] + '",'
        '"logo":{"@type":"ImageObject","url":"' + BASE + 'favicon.svg"}},'
        '"potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint",'
        '"urlTemplate":"' + BASE + 'cari/?q={search_term_string}"},'
        '"query-input":"required name=search_term_string"}}'
        "</script>")
    body += website_ld
    return page_shell(
        f"{d['site']['name']} — {d['site']['tagline']}",
        d["site"]["description"],
        BASE,
        body,
        kind="website",
    )


def render_article(d: dict, art: dict) -> str:
    cat = cat_by_slug(d, art["category"])
    url = f"{BASE}artikel/{art['slug']}.html"
    paras = "".join(f"<p>{escape(p)}</p>" for p in art["content"])
    tags = "".join(f"<span>#{escape(t)}</span>" for t in art.get("tags", []))
    related = []
    seen = {art["slug"]}
    for rslug in art.get("related", []):
        r = next((a for a in d["articles"] if a["slug"] == rslug), None)
        if r and r["slug"] not in seen:
            related.append(r)
            seen.add(r["slug"])
    for a in sorted(d["articles"], key=lambda x: x["date"], reverse=True):
        if len(related) >= 2:
            break
        if a["slug"] not in seen:
            related.append(a)
            seen.add(a["slug"])
    rel_cards = "".join(card_html(a) for a in related[:2]) if related else ""
    rel_block = f"""<div class="related"><h3>Berita Terkait</h3><div class="grid">{rel_cards}</div></div>""" if rel_cards else ""
    jld = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": art["title"],
        "description": art["excerpt"],
        "datePublished": art["date"],
        "dateModified": art["date"],
        "inLanguage": "id",
        "author": {"@type": "Organization", "name": art["author"]},
        "publisher": {"@type": "Organization", "name": d["site"]["name"], "logo": {"@type": "ImageObject", "url": f"{BASE}favicon.svg"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "articleSection": cat["name"],
        "keywords": ", ".join(art.get("tags", [])),
        "wordCount": sum(len(p.split()) for p in art["content"]),
    }
    bread = f"""<nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Beranda</a><span>›</span><a href="kategori/{cat['slug']}.html">{escape(cat["name"])}</a><span>›</span><span aria-current="page">Artikel</span></nav>"""
    bld = breadcrumb_ld([
        ("Beranda", BASE),
        (cat["name"], f"{BASE}kategori/{cat['slug']}.html"),
        (art["title"], url),
    ])
    body = f"""{header_html(active=cat["slug"])}
<main id="main"><div class="wrap">
<article class="article-body">
{bread}
<h1>{escape(art["title"])}</h1>
<div class="byline"><span>Oleh <b>{escape(art["author"])}</b></span><span><time datetime="{art["date"]}">{fmt_date(art["date"])}</time></span><span>{art["reading_time"]} baca</span></div>
{paras}
{share_html(url, art["title"])}
<div class="tags">{tags}</div>
{rel_block}
</article>
</div></main>
<script type="application/ld+json">{json.dumps(jld, ensure_ascii=False)}</script>
{bld}
{footer_html()}"""
    return page_shell(art["title"], art["excerpt"], url, body, kind="article")


def render_category(d: dict, cat: dict, page: int = 1, per_page: int = 6) -> str:
    arts = [a for a in d["articles"] if a["category"] == cat["slug"]]
    arts.sort(key=lambda a: a["date"], reverse=True)
    total = len(arts)
    pages = max(1, math.ceil(total / per_page))
    page = min(max(1, page), pages)
    slice_arts = arts[(page - 1) * per_page: page * per_page]
    url = f"{BASE}kategori/{cat['slug']}.html" if page == 1 else f"{BASE}kategori/{cat['slug']}-{page}.html"
    cards = "".join(card_html(a) for a in slice_arts)
    # pagination
    pag = ""
    if pages > 1:
        links = []
        for i in range(1, pages + 1):
            href = f"kategori/{cat['slug']}.html" if i == 1 else f"kategori/{cat['slug']}-{i}.html"
            if i == page:
                links.append(f'<span class="cur" aria-current="page">{i}</span>')
            else:
                links.append(f'<a href="{href}">{i}</a>')
        pag = f"""<nav class="pagination" aria-label="Halaman kategori">{''.join(links)}</nav>"""
    bld = breadcrumb_ld([
        ("Beranda", BASE),
        (cat["name"], url),
    ])
    body = f"""{header_html(active=cat["slug"])}
<main id="main"><div class="wrap">
<section class="block" style="margin-top:1.75rem">
<h2 class="sect">Kategori: {escape(cat["name"])}</h2>
<p style="color:var(--mut);margin-bottom:1.2rem">{escape(cat.get("description", ""))}</p>
<div class="grid">{cards}</div>
{pag}
</section>
</div></main>
{bld}
{footer_html()}"""
    return page_shell(
        f"{cat['name']} — {d['site']['name']}",
        cat.get("description", f"Berita kategori {cat['name']} di {d['site']['name']}"),
        url,
        body,
        kind="website",
    )


def render_search_page(d: dict) -> str:
    url = f"{BASE}cari/"
    body = f"""{header_html()}
<main id="main"><div class="wrap">
<section class="block" style="margin-top:1.75rem" id="searchPage">
<h2 class="sect">Pencarian</h2>
<input class="cari-input" id="searchInput" type="search" placeholder="Ketik kata kunci… (mis. ekonomi, bank, teknologi)" autocomplete="off" aria-label="Kata kunci pencarian">
<div class="search-results" id="searchResults" style="width:100%;margin-top:.9rem;box-shadow:none;border:1px solid var(--line);max-height:none"></div>
</section>
</div></main>
{footer_html()}"""
    return page_shell(
        f"Pencarian — {d['site']['name']}",
        f"Cari berita di {d['site']['name']}.",
        url,
        body,
        kind="website",
        include_search=False,
    )


def render_search_index(d: dict) -> str:
    idx = []
    for a in d["articles"]:
        idx.append({
            "slug": a["slug"],
            "title": a["title"],
            "excerpt": a["excerpt"],
            "category": a["category"],
            "category_name": cat_by_slug(d, a["category"])["name"],
            "date": a["date"],
            "reading_time": a["reading_time"],
            "tags": a.get("tags", []),
        })
    return json.dumps(idx, ensure_ascii=False)


def render_sitemap(d: dict) -> str:
    arts = sorted(d["articles"], key=lambda a: a["date"], reverse=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"""  <url><loc>{BASE}</loc><lastmod>{now}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>"""]
    urls.append(f"""  <url><loc>{BASE}cari/</loc><lastmod>{now}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>""")
    for u in subweb_urls():
        urls.append(f"""  <url><loc>{u}</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>""")
    for c in d["categories"]:
        urls.append(f"""  <url><loc>{BASE}kategori/{c['slug']}.html</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>""")
    for a in arts:
        urls.append(f"""  <url><loc>{BASE}artikel/{a['slug']}.html</loc><lastmod>{a['date'][:10]}</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""


def render_rss(d: dict) -> str:
    arts = sorted(d["articles"], key=lambda a: a["date"], reverse=True)
    items = "".join(f"""    <item>
      <title>{escape(a["title"])}</title>
      <link>{BASE}artikel/{a["slug"]}.html</link>
      <guid isPermaLink="true">{BASE}artikel/{a["slug"]}.html</guid>
      <pubDate>{iso_to_rfc822(a["date"])}</pubDate>
      <category>{escape(cat_by_slug(d, a["category"])["name"])}</category>
      <description>{escape(a["excerpt"])}</description>
    </item>""" for a in arts)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{escape(d["site"]["name"])}</title>
  <link>{BASE}</link>
  <description>{escape(d["site"]["description"])}</description>
  <language>id-id</language>
  <lastBuildDate>{iso_to_rfc822(arts[0]["date"] if arts else "2026-08-01T00:00:00+07:00")}</lastBuildDate>
  <atom:link href="{BASE}rss.xml" rel="self" type="application/rss+xml"/>
{items}
</channel>
</rss>
"""


def render_404(d: dict) -> str:
    body = f"""{header_html()}
<main id="main"><div class="notfound">
<h1>404</h1>
<p style="font-size:1.1rem;color:var(--mut)">Halaman yang Anda cari tidak ditemukan atau telah dipindahkan.</p>
<p style="margin-top:1rem"><a href="index.html" style="display:inline-block;color:var(--blue);font-weight:700">← Kembali ke Beranda</a></p>
</div></main>
{footer_html()}"""
    return page_shell(
        "Halaman Tidak Ditemukan — Aixwim News",
        "Halaman yang Anda cari tidak ditemukan.",
        f"{BASE}404.html",
        body,
        kind="website",
    )


ROBOTS = f"""User-agent: *
Allow: /

Sitemap: {BASE}sitemap.xml
"""


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#0a2540"/><text x="50" y="68" font-size="52" font-family="Arial" font-weight="bold" fill="#ffd166" text-anchor="middle">A</text></svg>"""




def sync_to_root() -> None:
    """Salin isi public/ ke root repo (GitHub Pages serve dari root, bukan public/)."""
    # Bersihkan file situs lama di root yang sudah tidak ada di public/
    # (mis. artikel yang dihapus) agar tidak tertinggal & ter-index Google.
    managed = {"artikel", "kategori", "cari", "subwebs", "assets"}
    for name in managed:
        src = OUT / name
        dst = ROOT / name
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            for item in src.rglob("*"):
                if item.is_file():
                    rel = item.relative_to(src)
                    dest = dst / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(item.read_bytes())
            # hapus file di dst yang tidak ada di src
            for item in dst.rglob("*"):
                if item.is_file() and not (src / item.relative_to(dst)).exists():
                    item.unlink(missing_ok=True)
        elif dst.exists():
            shutil.rmtree(dst, ignore_errors=True)
    for rel in ("index.html", "search_index.json", "sitemap.xml", "rss.xml",
                "robots.txt", "404.html", "favicon.svg", "perf-report.json",
                "analytics-report.json"):
        src = OUT / rel
        if src.exists():
            (ROOT / rel).write_bytes(src.read_bytes())
    print("✅ public/ disinkronkan ke root (Pages serve dari root)")


def copy_subwebs() -> None:
    """Salin staging subweb (root/subwebs/) ke public/subwebs/ sebelum sitemap."""
    if SUBWEB_SRC.is_dir():
        dst = OUT / "subwebs"
        dst.mkdir(parents=True, exist_ok=True)
        for f in SUBWEB_SRC.glob("*.html"):
            (dst / f.name).write_bytes(f.read_bytes())


# ---------------------------------------------------------------- build
def build() -> None:
    d = load_data()
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "artikel").mkdir(parents=True)
    (OUT / "kategori").mkdir(parents=True)
    (OUT / "cari").mkdir(parents=True)
    (OUT / "assets" / "css").mkdir(parents=True)

    (OUT / "index.html").write_text(render_index(d), encoding="utf-8")
    for a in d["articles"]:
        (OUT / "artikel" / f"{a['slug']}.html").write_text(render_article(d, a), encoding="utf-8")
    for c in d["categories"]:
        (OUT / "kategori" / f"{c['slug']}.html").write_text(render_category(d, c), encoding="utf-8")
        n_pages = max(1, math.ceil(sum(1 for a in d["articles"] if a["category"] == c["slug"]) / 6))
        for p in range(2, n_pages + 1):
            (OUT / "kategori" / f"{c['slug']}-{p}.html").write_text(render_category(d, c, page=p), encoding="utf-8")
    (OUT / "cari" / "index.html").write_text(render_search_page(d), encoding="utf-8")
    (OUT / "search_index.json").write_text(render_search_index(d), encoding="utf-8")
    copy_subwebs()
    (OUT / "sitemap.xml").write_text(render_sitemap(d), encoding="utf-8")
    (OUT / "rss.xml").write_text(render_rss(d), encoding="utf-8")
    (OUT / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (OUT / "404.html").write_text(render_404(d), encoding="utf-8")
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (OUT / "assets" / "css" / "style.css").write_text(CSS, encoding="utf-8")

    sync_to_root()

    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"✅ Build selesai: {len(d['articles'])} artikel, {len(d['categories'])} kategori, "
          f"{sum(1 for _ in OUT.rglob('*.html'))} halaman HTML, total {total/1024:.1f} KB")


if __name__ == "__main__":
    build()
