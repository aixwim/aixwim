import { site, articles, categories, basePath, siteUrl, fullUrl, slugToUrl, categoryUrl, formatDate, getCategory } from '../lib/site';
import ArticleCard from '../components/ArticleCard';

export const metadata = {
  alternates: { canonical: '/' },
};

export default function Home() {
  const ld = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: site.name,
    url: siteUrl,
    description: site.description,
    potentialAction: {
      '@type': 'SearchAction',
      target: { '@type': 'EntryPoint', urlTemplate: fullUrl('/cari/?q={search_term_string}') },
      'query-input': 'required name=search_term_string',
    },
  });
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: ld }} />
      <section className="hero">
        <div className="container">
          <span className="badge">📰 {articles.length} Artikel · {categories.length} Kategori · {site.established}</span>
          <h1>{site.tagline}</h1>
          <p>{site.description}</p>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Kategori</h2>
          <div className="cat-pills">
            {categories.map((c) => (
              <a className="cat-pill" key={c.slug} href={categoryUrl(c.slug)}>{c.name}</a>
            ))}
          </div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Artikel Terbaru</h2>
          <div className="grid">
            {articles.map((a) => <ArticleCard key={a.slug} a={a} />)}
          </div>
        </div>
      </section>
    </>
  );
}
