#!/usr/bin/env python3
"""Konversi data/articles.json + aset Next.js -> struktur Jekyll (GitHub Pages native).
Menghasilkan: _config.yml, _layouts/, _includes/, _posts/, kategori/, cari/, index.md,
robots.txt, rss.xml, 404.html, favicon.svg, pages.yml (Pages CMS).
"""
import json, re, pathlib, shutil, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'data' / 'articles.json').read_text('utf8'))
SITE, CATS, ARTS = DATA['site'], DATA['categories'], DATA['articles']
BASE = SITE['base_url'].rstrip('/')

def w(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, 'utf8')
    print('  OK', rel)

# ---------- CSS & JS dari aset Next.js ----------
css_js = (ROOT / 'lib' / 'css.js').read_text('utf8')
CSS = css_js.split('`')[1]
layout_jsx = (ROOT / 'app' / 'layout.jsx').read_text('utf8')
m = re.search(r'const SCRIPTS = String\.raw`([\s\S]*?)`;', layout_jsx)
SCRIPTS = m.group(1) if m else ''
EXTRA_CSS = """
/* ===== tambahan Jekyll ===== */
.byline{display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--muted);font-size:.9rem;margin:12px 0 24px}
.article p{color:var(--text);font-size:1.04rem;line-height:1.8;margin-bottom:1.1em}
.article p.lead{font-size:1.15rem;font-weight:500;color:#1e293b}
.tags{margin:26px 0;display:flex;flex-wrap:wrap;gap:8px}
.tag{background:var(--bg);border:1px solid var(--border);border-radius:999px;padding:4px 12px;font-size:.8rem;color:var(--muted)}
.share{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0;padding-top:20px;border-top:1px solid var(--border)}
.share a{font-size:.8rem;font-weight:700;padding:8px 14px;border-radius:8px;color:#fff;text-decoration:none}
.share a:hover{opacity:.85}
.share .wa{background:#25d366}.share .x{background:#111}.share .fb{background:#1877f2}
.share .li{background:#0a66c2}.share .tg{background:#229ed9}
.related{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-top:30px}
.related h3{font-size:1rem;margin-bottom:12px}
.related ul{list-style:none;display:grid;gap:10px}
.related li a{font-weight:600}
.related .rmeta{display:block;font-size:.78rem;color:var(--muted)}
.breadcrumb{font-size:.85rem;color:var(--muted);margin-bottom:16px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.breadcrumb a{color:var(--accent)}
.article{max-width:780px;margin:0 auto;padding:36px 0 48px}
.article h1{font-size:clamp(1.5rem,3.4vw,2.1rem);line-height:1.3;font-weight:800}
.kategori-head{margin:36px 0 20px}
.kategori-head h1{font-size:1.7rem;font-weight:800}
.kategori-head p{color:var(--muted);margin-top:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;padding:32px 0 40px}
.mark{background:#fde68a;border-radius:3px;padding:0 2px}
"""

# ---------- _config.yml ----------
cfg = {
    'title': SITE['name'],
    'tagline': SITE['tagline'],
    'description': SITE['description'],
    'url': SITE['base_url'].replace('/aixwim', '').rstrip('/'),
    'baseurl': '/aixwim',
    'lang': 'id',
    'permalink': '/artikel/:slug/',
    'plugins': ['jekyll-sitemap'],
    'exclude': ['README.md', 'Gemfile', 'Gemfile.lock', 'data', 'tools', 'docs',
                'app', 'components', 'lib', 'scripts', 'node_modules', '.next',
                'venv', 'package.json', 'package-lock.json', 'next.config.mjs',
                'public', '.github'],
}
w('_config.yml', yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False))

# ---------- _data/categories.yml ----------
w('_data/categories.yml', yaml.safe_dump([{'slug': c['slug'], 'name': c['name']} for c in CATS], allow_unicode=True, sort_keys=False))

# ---------- _includes ----------
w('_includes/style.css', CSS + EXTRA_CSS)
w('_includes/script.js', SCRIPTS)

w('_includes/head.html', """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% if page.title and page.layout != 'home' %}{{ page.title }} — {{ site.title }}{% else %}{{ site.title }} — {{ site.tagline }}{% endif %}</title>
<meta name="description" content="{{ page.excerpt | default: site.description | strip_html | xml_escape | truncate: 160 }}">
<meta name="keywords" content="berita indonesia, ekonomi, teknologi, nasional, bisnis, pendidikan{% if page.tags %}, {{ page.tags | join: ', ' }}{% endif %}">
<meta name="theme-color" content="#2563eb">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{{ page.url | absolute_url }}">
<meta property="og:type" content="{% if page.layout == 'post' %}article{% else %}website{% endif %}">
<meta property="og:site_name" content="{{ site.title }}">
<meta property="og:title" content="{% if page.title and page.layout != 'home' %}{{ page.title }}{% else %}{{ site.title }} — {{ site.tagline }}{% endif %}">
<meta property="og:description" content="{{ page.excerpt | default: site.description | strip_html | xml_escape | truncate: 160 }}">
<meta property="og:url" content="{{ page.url | absolute_url }}">
<meta property="og:locale" content="id_ID">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{% if page.title and page.layout != 'home' %}{{ page.title }}{% else %}{{ site.title }} — {{ site.tagline }}{% endif %}">
<meta name="twitter:description" content="{{ page.excerpt | default: site.description | strip_html | xml_escape | truncate: 160 }}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='3' y='4' width='18' height='16' rx='2' fill='%232563eb'/><path d='M7 9h10M7 13h6' stroke='white' stroke-width='2' stroke-linecap='round'/></svg>">
<style>{% include style.css %}</style>
""")

w('_includes/nav.html', """<header class="nav" role="banner">
  <div class="nav-inner">
    <a class="brand" href="{{ '/' | relative_url }}"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/><path d="M7 9h10M7 13h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Aixwim</a>
    <nav class="nav-links" aria-label="Navigasi utama">
      <a href="{{ '/' | relative_url }}">Beranda</a>
      {% for c in site.data.categories %}<a href="{{ '/kategori/' | relative_url }}{{ c.slug }}/">{{ c.name }}</a>{% endfor %}
    </nav>
    <div class="nav-actions">
      <a href="{{ '/cari/' | relative_url }}" class="icon-btn search-link" aria-label="Cari artikel" title="Cari (Ctrl+/)">🔍</a>
      <button class="icon-btn" id="themeBtn" aria-label="Ganti tema" title="Tema: Light/Dark/Auto">🌓</button>
      <button class="icon-btn burger" id="burgerBtn" aria-label="Menu" aria-expanded="false">☰</button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobileMenu">
  <a href="{{ '/' | relative_url }}">Beranda</a>
  {% for c in site.data.categories %}<a href="{{ '/kategori/' | relative_url }}{{ c.slug }}/">{{ c.name }}</a>{% endfor %}
  <a href="{{ '/cari/' | relative_url }}">🔍 Cari Artikel</a>
</div>""")

w('_includes/footer.html', """<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div><h4>{{ site.title }}</h4><p style="color:var(--muted);font-size:.88rem">{{ site.description }}</p></div>
      <div><h4>Kategori</h4><ul>{% for c in site.data.categories %}<li><a href="{{ '/kategori/' | relative_url }}{{ c.slug }}/">{{ c.name }}</a></li>{% endfor %}</ul></div>
      <div><h4>Lainnya</h4><ul><li><a href="{{ '/cari/' | relative_url }}">🔍 Pencarian</a></li><li><a href="{{ '/rss.xml' | relative_url }}">📡 RSS Feed</a></li><li><a href="{{ '/sitemap.xml' | relative_url }}">🗺️ Sitemap</a></li></ul></div>
    </div>
    <div class="copy">© {{ 'now' | date: '%Y' }} {{ site.title }} · {{ site.data.meta.editor }} · {{ site.data.meta.established }}</div>
  </div>
</footer>""")

w('_includes/card.html', """<article class="card fade">
  <div class="card-body">
    <div class="meta" style="color:var(--muted);font-size:.78rem;margin-bottom:8px">{% assign cat = site.data.categories | where: 'slug', include.post.categories[0] | first %}<a href="{{ '/kategori/' | relative_url }}{{ include.post.categories[0] }}/" style="color:var(--accent);font-weight:700">{{ cat.name | default: include.post.categories[0] }}</a> · {{ include.post.date | date: '%d %b %Y' }} · {{ include.post.reading_time }}</div>
    <h3 style="font-size:1.05rem;line-height:1.45"><a href="{{ include.post.url | relative_url }}">{{ include.post.title }}</a></h3>
    <p style="color:var(--muted);font-size:.9rem;margin-top:8px">{{ include.post.excerpt | strip_html | truncate: 120 }}</p>
  </div>
</article>""")

# ---------- _layouts ----------
w('_layouts/default.html', """<!DOCTYPE html>
<html lang="id">
<head>{% include head.html %}</head>
<body>
  <a class="skip-link" href="#content">Lewati ke konten</a>
  {% include nav.html %}
  <main id="content">{{ content }}</main>
  {% include footer.html %}
  <button id="toTop" aria-label="Kembali ke atas">↑</button>
  <script>{% include script.js %}</script>
</body>
</html>""")

w('_layouts/home.html', """---
layout: default
---
<section class="hero fade">
  <h1>{{ site.title }}</h1>
  <p style="font-size:1.1rem;opacity:.95;max-width:640px;margin:0 auto">{{ site.tagline }}</p>
  <div style="margin-top:18px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
    <span class="badge">{{ site.posts | size }} Artikel</span>
    <span class="badge">{{ site.data.categories | size }} Kategori</span>
    <span class="badge">100% Statis</span>
  </div>
</section>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"{{ site.title }}","url":"{{ '/' | absolute_url }}","description":"{{ site.description | escape }}","potentialAction":{"@type":"SearchAction","target":"{{ '/cari/' | absolute_url }}?q={search_term_string}","query-input":"required name=search_term_string"}}
</script>
<div class="container">
  <div class="cards">
    {% for p in site.posts %}{% include card.html post=p %}{% endfor %}
  </div>
</div>""")

w('_layouts/post.html', """---
layout: default
---
<article class="article fade">
  <script type="application/ld+json">
  [{"@context":"https://schema.org","@type":"NewsArticle","headline":{{ page.title | jsonify }},"description":{{ page.excerpt | jsonify }},"image":[],"datePublished":{{ page.date | date_to_xmlschema | jsonify }},"dateModified":{{ page.date | date_to_xmlschema | jsonify }},"author":{"@type":"Organization","name":{{ page.author | jsonify }}},"publisher":{"@type":"Organization","name":"{{ site.title }}"},"mainEntityOfPage":{{ page.url | absolute_url | jsonify }},"keywords":{{ page.tags | join: ', ' | jsonify }},"inLanguage":"id"},
  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Beranda","item":{{ '/' | absolute_url | jsonify }}},{"@type":"ListItem","position":2,"name":{{ page.categories[0] | jsonify }},"item":{{ '/kategori/' | absolute_url | append: page.categories[0] | append: '/' | jsonify }}},{"@type":"ListItem","position":3,"name":{{ page.title | jsonify }}}]}]
  </script>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Beranda</a><span>/</span>
    <a href="{{ '/kategori/' | relative_url }}{{ page.categories[0] }}/">{{ page.categories[0] }}</a><span>/</span>
    <span>{{ page.title }}</span>
  </nav>
  <h1>{{ page.title }}</h1>
  <div class="byline">
    <span>✍️ <b>{{ page.author }}</b></span>
    <span>🗓 {{ page.date | date: '%d %B %Y' }}</span>
    <span>⏱ {{ page.reading_time }} baca</span>
    <span>🏷 <a href="{{ '/kategori/' | relative_url }}{{ page.categories[0] }}/">{{ page.categories[0] }}</a></span>
  </div>
  {{ content }}
  {% if page.tags %}<div class="tags">{% for t in page.tags %}<span class="tag">#{{ t }}</span>{% endfor %}</div>{% endif %}
  {% assign u = page.url | absolute_url %}{% assign ut = page.title | url_encode %}{% assign eu = u | url_encode %}
  <div class="share" aria-label="Bagikan artikel">
    <a class="wa" href="https://wa.me/?text={{ ut }}%20{{ eu }}" target="_blank" rel="noopener">WhatsApp</a>
    <a class="x" href="https://twitter.com/intent/tweet?text={{ ut }}&url={{ eu }}" target="_blank" rel="noopener">X</a>
    <a class="fb" href="https://www.facebook.com/sharer/sharer.php?u={{ eu }}" target="_blank" rel="noopener">Facebook</a>
    <a class="li" href="https://www.linkedin.com/sharing/share-offsite/?url={{ eu }}" target="_blank" rel="noopener">LinkedIn</a>
    <a class="tg" href="https://t.me/share/url?url={{ eu }}&text={{ ut }}" target="_blank" rel="noopener">Telegram</a>
  </div>
  {% assign same = site.posts | where_exp: 'p', 'p.categories[0] == page.categories[0]' %}{% assign rel = same | where_exp: 'p', 'p.slug != page.slug' | slice: 0, 3 %}
  {% if rel.size > 0 %}
  <aside class="related"><h3>Artikel Terkait</h3><ul>
    {% for r in rel %}<li><a href="{{ r.url | relative_url }}">{{ r.title }}</a><span class="rmeta">{{ r.date | date: '%d %B %Y' }}</span></li>{% endfor %}
  </ul></aside>
  {% endif %}
</article>""")

w('_layouts/kategori.html', """---
layout: default
---
<div class="container">
  <div class="kategori-head fade">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{{ '/' | relative_url }}">Beranda</a><span>/</span><span>{{ page.name }}</span></nav>
    <h1>{{ page.name }}</h1>
    <p>{{ site.posts | where: 'categories', page.slug | size }} artikel</p>
  </div>
  <div class="cards">
    {% for p in site.posts %}{% if p.categories[0] == page.slug %}{% include card.html post=p %}{% endif %}{% endfor %}
  </div>
</div>""")

w('_layouts/cari.html', """---
layout: default
---
<div class="container search-wrap fade" style="max-width:760px;margin:0 auto;padding:48px 20px">
  <h1>🔍 Cari Artikel</h1>
  <form class="search-form" action="{{ '/cari/' | relative_url }}" method="get" role="search">
    <input id="q" type="search" name="q" placeholder="Ketik kata kunci… (mis. ekonomi, AI, UMKM)" autofocus>
    <button type="submit">Cari</button>
  </form>
  <div id="results"><div class="empty">Ketik kata kunci untuk mencari artikel.</div></div>
  <script>
  (function(){
    var INDEX = [{% for p in site.posts %}{"slug":{{ p.slug | jsonify }},"title":{{ p.title | jsonify }},"excerpt":{{ p.excerpt | jsonify }},"category":{{ p.categories[0] | jsonify }},"date":{{ p.date | date_to_xmlschema | jsonify }},"tags":{{ p.tags | jsonify }}}{% unless forloop.last %},{% endunless %}{% endfor %}];
    var wrap = document.getElementById('results');
    var input = document.getElementById('q');
    var BASE = {{ site.baseurl | jsonify }};
    function esc(s){return s.replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
    function hl(text,q){var i=text.toLowerCase().indexOf(q.toLowerCase());if(i<0)return esc(text);return esc(text.slice(0,i))+'<mark>'+esc(text.slice(i,i+q.length))+'</mark>'+esc(text.slice(i+q.length));}
    function render(q){
      if(!q){wrap.innerHTML='<div class="empty">Ketik kata kunci untuk mencari artikel.</div>';return;}
      var terms=q.toLowerCase().split(/\\s+/).filter(Boolean);
      var scored=INDEX.map(function(a){
        var s=0, hay=(a.title+' '+(a.tags||[]).join(' ')+' '+a.category+' '+a.excerpt).toLowerCase();
        terms.forEach(function(t){if(a.title.toLowerCase().includes(t))s+=3;if((a.tags||[]).join(' ').toLowerCase().includes(t))s+=2;if(a.excerpt.toLowerCase().includes(t))s+=1;});
        return {a:a,s:s};
      }).filter(function(x){return x.s>0;}).sort(function(x,y){return y.s-x.s;});
      if(!scored.length){wrap.innerHTML='<div class="empty">Tidak ditemukan hasil untuk "'+esc(q)+'".</div>';return;}
      wrap.innerHTML=scored.slice(0,20).map(function(x){
        var a=x.a;
        return '<div class="r"><h3><a href="'+BASE+'/artikel/'+a.slug+'/">'+hl(a.title,q)+'</a></h3>'+
          '<p>'+hl(a.excerpt,q)+'</p><div class="meta" style="color:var(--muted);font-size:.78rem">🏷 '+esc(a.category)+'</div></div>';
      }).join('');
    }
    input.addEventListener('input',function(){render(input.value);});
    var q=new URLSearchParams(location.search).get('q');
    if(q){input.value=q;render(q);}
  })();
  </script>
</div>""")

w('_layouts/404.html', """---
layout: default
---
<div class="container" style="max-width:640px;margin:0 auto;text-align:center;padding:80px 20px">
  <h1 style="font-size:4rem;font-weight:800;color:var(--accent)">404</h1>
  <p style="color:var(--muted);font-size:1.1rem;margin:10px 0 26px">Halaman tidak ditemukan. Mungkin sudah dipindah atau dihapus.</p>
  <a href="{{ '/' | relative_url }}" style="background:var(--accent);color:#fff;padding:12px 24px;border-radius:10px;font-weight:700;text-decoration:none">← Kembali ke Beranda</a>
</div>""")

# ---------- halaman ----------
w('index.md', '---\nlayout: home\n---\n')

for c in CATS:
    w(f'kategori/{c["slug"]}.md', f'---\nlayout: kategori\npermalink: /kategori/{c["slug"]}/\nslug: {c["slug"]}\nname: "{c["name"]}"\n---\n')

w('cari/index.md', '---\nlayout: cari\npermalink: /cari/\n---\n')
w('404.html', '---\nlayout: 404\npermalink: /404.html\n---\n')

# ---------- _posts ----------
for a in ARTS:
    date = a['date'][:10]
    fm = {
        'layout': 'post',
        'title': a['title'],
        'date': a['date'].replace('T', ' ').replace('+07:00', ' +0700'),
        'categories': [a['category']],
        'author': a['author'],
        'excerpt': a['excerpt'],
        'reading_time': a['reading_time'],
        'tags': a.get('tags', []),
    }
    body = '\n\n'.join(a['content'])
    w(f'_posts/{date}-{a["slug"]}.md', '---\n' + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + '---\n\n' + body + '\n')

# ---------- statis ----------
w('robots.txt', f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
w('rss.xml', """---
layout: null
---
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{{ site.title }}</title>
<link>{{ site.url }}{{ site.baseurl }}/</link>
<description>{{ site.description | xml_escape }}</description>
<language>id</language>
<lastBuildDate>{{ site.time | date_to_rfc822 }}</lastBuildDate>
<atom:link href="{{ site.url }}{{ site.baseurl }}/rss.xml" rel="self" type="application/rss+xml"/>
{% for p in site.posts %}
<item>
<title>{{ p.title | xml_escape }}</title>
<link>{{ site.url }}{{ site.baseurl }}{{ p.url }}</link>
<guid isPermaLink="true">{{ site.url }}{{ site.baseurl }}{{ p.url }}</guid>
<pubDate>{{ p.date | date_to_rfc822 }}</pubDate>
<description>{{ p.excerpt | xml_escape }}</description>
<category>{{ p.categories[0] }}</category>
</item>
{% endfor %}
</channel>
</rss>
""")

# favicon dari public/
if (ROOT / 'public' / 'favicon.svg').exists():
    shutil.copy(ROOT / 'public' / 'favicon.svg', ROOT / 'favicon.svg')

# ---------- Pages CMS ----------
w('pages.yml', """media: "assets"
content:
  - name: posts
    label: Artikel
    path: "_posts"
    fields:
      - { name: title, label: Judul }
      - { name: categories, label: Kategori, widget: select, options: [ekonomi, teknologi, nasional, bisnis, pendidikan] }
      - { name: date, label: Tanggal, widget: datetime }
      - { name: author, label: Penulis }
      - { name: excerpt, label: Ringkasan, widget: text }
      - { name: reading_time, label: Waktu Baca }
      - { name: tags, label: Tag, widget: list }
      - { name: body, label: Isi Artikel, widget: markdown }
""")

# ---------- meta ----------
w('_data/meta.yml', yaml.safe_dump({'editor': SITE.get('editor', 'Tim Redaksi'), 'established': SITE.get('established', '2026')}, allow_unicode=True, sort_keys=False))

print('SELESAI — struktur Jekyll dibuat.')
