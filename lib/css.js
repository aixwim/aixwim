export const CSS = String.raw`
:root{--bg:#f8fafc;--surface:#ffffff;--text:#0f172a;--muted:#64748b;--accent:#2563eb;--accent2:#7c3aed;--border:#e2e8f0;--radius:12px;--shadow:0 1px 3px rgba(15,23,42,.08);--shadow-lg:0 12px 30px rgba(15,23,42,.12);--font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--maxw:1100px}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;height:auto}
.container{max-width:var(--maxw);margin:0 auto;padding:0 20px}
.skip-link{position:absolute;left:-9999px;top:0;background:var(--accent);color:#fff;padding:10px 16px;border-radius:0 0 8px 0;z-index:200}
.skip-link:focus{left:0}
/* NAV */
.nav{position:sticky;top:0;z-index:100;background:var(--surface);border-bottom:1px solid var(--border);backdrop-filter:blur(8px)}
.nav-inner{max-width:var(--maxw);margin:0 auto;padding:0 20px;height:60px;display:flex;align-items:center;gap:20px}
.brand{display:flex;align-items:center;gap:8px;font-weight:800;font-size:1.15rem;color:var(--text)}
.brand svg{width:26px;height:26px}
.nav-links{display:flex;align-items:center;gap:4px;margin-left:auto}
.nav-links a{color:var(--muted);font-weight:600;font-size:.92rem;padding:8px 12px;border-radius:8px;transition:.15s}
.nav-links a:hover{color:var(--accent);background:var(--bg);text-decoration:none}
.nav-actions{display:flex;align-items:center;gap:4px}
.icon-btn{background:none;border:1px solid var(--border);border-radius:8px;width:36px;height:36px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--text);font-size:1rem;transition:.15s}
.icon-btn:hover{border-color:var(--accent);color:var(--accent)}
.burger{display:none}
.mobile-menu{display:none;flex-direction:column;background:var(--surface);border-bottom:1px solid var(--border);padding:12px 20px;gap:2px}
.mobile-menu.open{display:flex}
.mobile-menu a{padding:10px 8px;border-radius:8px;color:var(--muted);font-weight:600}
.mobile-menu a:hover{background:var(--bg);color:var(--accent);text-decoration:none}
/* HERO */
.hero{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;padding:64px 0 56px;text-align:center}
.hero h1{font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;max-width:760px;margin:0 auto 14px;line-height:1.2}
.hero p{max-width:640px;margin:0 auto;font-size:1.05rem;opacity:.92}
.hero .badge{display:inline-flex;gap:8px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);padding:8px 18px;border-radius:999px;font-weight:700;font-size:.85rem;margin-bottom:18px}
/* CARDS */
.section{padding:48px 0}
.section h2{font-size:1.5rem;font-weight:800;margin-bottom:24px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px;display:flex;flex-direction:column;gap:10px;transition:transform .18s,box-shadow .18s;box-shadow:var(--shadow)}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);text-decoration:none}
.card .cat{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--accent);background:rgba(37,99,235,.1);padding:4px 10px;border-radius:999px;width:fit-content}
.card h3{font-size:1.05rem;line-height:1.4;color:var(--text)}
.card p{font-size:.9rem;color:var(--muted);flex:1}
.card .meta{font-size:.78rem;color:var(--muted);display:flex;gap:10px;flex-wrap:wrap}
/* CATEGORY PILLS */
.cat-pills{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.cat-pill{background:var(--surface);border:1px solid var(--border);border-radius:999px;padding:10px 20px;font-weight:700;font-size:.9rem;color:var(--text);transition:.15s}
.cat-pill:hover{border-color:var(--accent);color:var(--accent);text-decoration:none;transform:translateY(-2px)}
/* ARTICLE */
.article{max-width:760px;margin:0 auto;padding:40px 0}
.breadcrumb{font-size:.8rem;color:var(--muted);margin-bottom:18px;display:flex;gap:6px;flex-wrap:wrap}
.breadcrumb a{color:var(--muted)}
.breadcrumb a:hover{color:var(--accent)}
.article h1{font-size:clamp(1.6rem,3.5vw,2.2rem);font-weight:800;line-height:1.25;margin-bottom:14px}
.article .byline{display:flex;flex-wrap:wrap;gap:14px;color:var(--muted);font-size:.85rem;border-bottom:1px solid var(--border);padding-bottom:18px;margin-bottom:22px}
.article .byline b{color:var(--text)}
.article p{margin-bottom:18px;font-size:1.02rem}
.article .lead{font-size:1.08rem;color:var(--text)}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0}
.tag{font-size:.75rem;background:var(--bg);border:1px solid var(--border);padding:4px 12px;border-radius:999px;color:var(--muted)}
/* SHARE */
.share{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 28px}
.share a{font-size:.8rem;font-weight:700;padding:8px 14px;border-radius:8px;color:#fff;background:var(--accent);transition:.15s}
.share a:hover{opacity:.85;text-decoration:none}
.share a.x{background:#111}
.share a.fb{background:#1877f2}
.share a.li{background:#0a66c2}
.share a.wa{background:#25d366;color:#075e54}
.share a.tg{background:#229ed9}
/* RELATED */
.related{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-top:32px}
.related h3{font-size:1.1rem;margin-bottom:14px}
.related ul{list-style:none;display:grid;gap:10px}
.related a{display:block;font-weight:600;font-size:.95rem}
.related .rmeta{font-size:.78rem;color:var(--muted)}
/* FOOTER */
.footer{background:var(--surface);border-top:1px solid var(--border);margin-top:48px;padding:40px 0 24px}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:28px;margin-bottom:24px}
.footer h4{font-size:.95rem;margin-bottom:12px}
.footer ul{list-style:none;display:grid;gap:8px}
.footer a{color:var(--muted);font-size:.88rem}
.footer a:hover{color:var(--accent)}
.footer .copy{text-align:center;color:var(--muted);font-size:.8rem;border-top:1px solid var(--border);padding-top:20px}
/* PAGINATION */
.pagination{display:flex;gap:10px;justify-content:center;margin-top:30px}
.pagination a,.pagination span{background:var(--surface);border:1px solid var(--border);padding:8px 16px;border-radius:8px;font-weight:700;font-size:.9rem}
.pagination a:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
/* BACK TO TOP */
#toTop{position:fixed;bottom:24px;right:24px;width:44px;height:44px;border-radius:50%;background:var(--accent);color:#fff;border:none;font-size:1.2rem;cursor:pointer;opacity:0;visibility:hidden;transition:.25s;z-index:90;box-shadow:var(--shadow-lg)}
#toTop.show{opacity:1;visibility:visible}
/* SEARCH */
.search-wrap{max-width:760px;margin:0 auto;padding:40px 0}
.search-wrap h1{font-size:1.8rem;font-weight:800;margin-bottom:18px}
.search-form{display:flex;gap:10px;margin-bottom:26px}
.search-form input{flex:1;padding:12px 16px;border:1px solid var(--border);border-radius:10px;font-size:1rem;background:var(--surface);color:var(--text)}
.search-form button{padding:12px 22px;background:var(--accent);color:#fff;border:none;border-radius:10px;font-weight:700;cursor:pointer}
#results{display:grid;gap:14px}
#results .r{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px}
#results .r h3{font-size:1rem;margin-bottom:6px}
#results .r p{font-size:.88rem;color:var(--muted)}
#results mark{background:#fef08a;border-radius:3px;padding:0 2px}
.empty{color:var(--muted);text-align:center;padding:30px 0}
/* 404 */
.nf{text-align:center;padding:90px 20px}
.nf h1{font-size:5rem;font-weight:900;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.nf p{margin:12px 0 24px;color:var(--muted)}
/* MISC */
.fade{animation:fade .4s ease}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media(max-width:720px){
  .nav-links a:not(.search-link){display:none}
  .burger{display:flex}
  .hero{padding:44px 0 40px}
  .section{padding:36px 0}
}
@media(prefers-color-scheme:dark){
  :root{--bg:#0b1120;--surface:#111a2e;--text:#e2e8f0;--muted:#94a3b8;--border:#1e293b}
  .card,.cat-pill,.search-form input{background:var(--surface)}
  .share a.x{background:#000}
}
`;
