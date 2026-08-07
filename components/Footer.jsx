import { site, categories, basePath } from '../lib/site';

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid">
          <div>
            <h4>{site.name}</h4>
            <p style={{ color: 'var(--muted)', fontSize: '.88rem' }}>{site.description}</p>
          </div>
          <div>
            <h4>Kategori</h4>
            <ul>
              {categories.map((c) => (
                <li key={c.slug}><a href={`${basePath}/kategori/${c.slug}/`}>{c.name}</a></li>
              ))}
            </ul>
          </div>
          <div>
            <h4>Lainnya</h4>
            <ul>
              <li><a href={`${basePath}/cari/`}>🔍 Pencarian</a></li>
              <li><a href={`${basePath}/rss.xml`}>📡 RSS Feed</a></li>
              <li><a href={`${basePath}/sitemap.xml`}>🗺️ Sitemap</a></li>
            </ul>
          </div>
        </div>
        <div className="copy">© {year} {site.name} · {site.editor} · {site.established}</div>
      </div>
    </footer>
  );
}
