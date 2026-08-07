import { categories, basePath } from '../lib/site';

export default function Nav() {
  return (
    <>
      <header className="nav" role="banner">
        <div className="nav-inner">
          <a className="brand" href={`${basePath}/`}>
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" strokeWidth="2" />
              <path d="M7 9h10M7 13h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
            Aixwim
          </a>
          <nav className="nav-links" aria-label="Navigasi utama">
            <a href={`${basePath}/`}>Beranda</a>
            {categories.map((c) => (
              <a key={c.slug} href={`${basePath}/kategori/${c.slug}/`}>{c.name}</a>
            ))}
          </nav>
          <div className="nav-actions">
            <a href={`${basePath}/cari/`} className="icon-btn search-link" aria-label="Cari artikel" title="Cari (Ctrl+/)">🔍</a>
            <button className="icon-btn" id="themeBtn" aria-label="Ganti tema" title="Tema: Light/Dark/Auto">🌓</button>
            <button className="icon-btn burger" id="burgerBtn" aria-label="Menu" aria-expanded="false">☰</button>
          </div>
        </div>
      </header>
      <div className="mobile-menu" id="mobileMenu">
        <a href={`${basePath}/`}>Beranda</a>
        {categories.map((c) => (
          <a key={c.slug} href={`${basePath}/kategori/${c.slug}/`}>{c.name}</a>
        ))}
        <a href={`${basePath}/cari/`}>🔍 Cari Artikel</a>
      </div>
    </>
  );
}
