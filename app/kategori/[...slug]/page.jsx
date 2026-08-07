import { notFound } from 'next/navigation';
import { categories, getCategory, byCategory, siteUrl, fullUrl, categoryUrl, PER_PAGE } from '../../../lib/site';
import ArticleCard from '../../../components/ArticleCard';

export function generateStaticParams() {
  const out = [];
  for (const c of categories) {
    out.push({ slug: [c.slug] }); // halaman 1
    const pages = Math.ceil(byCategory(c.slug).length / PER_PAGE);
    for (let p = 2; p <= pages; p++) out.push({ slug: [c.slug, String(p)] });
  }
  return out;
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const c = getCategory(slug[0]);
  if (!c) return {};
  const page = slug.length > 1 ? parseInt(slug[1], 10) : 1;
  return {
    title: page > 1 ? `${c.name} — Halaman ${page}` : c.name,
    description: c.description,
    alternates: { canonical: page > 1 ? `/kategori/${c.slug}/page/${page}/` : `/kategori/${c.slug}/` },
  };
}

export default async function CategoryPage({ params }) {
  const { slug } = await params;
  if (slug.length > 2) notFound();
  const kategori = slug[0];
  const c = getCategory(kategori);
  if (!c) notFound();
  const n = slug.length > 1 ? parseInt(slug[1], 10) : 1;
  const list = byCategory(kategori);
  const totalPages = Math.max(1, Math.ceil(list.length / PER_PAGE));
  if (isNaN(n) || n < 1 || n > totalPages) notFound();
  const pageItems = list.slice((n - 1) * PER_PAGE, n * PER_PAGE);
  const ld = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Beranda', item: siteUrl },
      { '@type': 'ListItem', position: 2, name: c.name, item: fullUrl(`/kategori/${kategori}/`) },
      ...(n > 1 ? [{ '@type': 'ListItem', position: 3, name: `Halaman ${n}` }] : []),
    ],
  });
  return (
    <section className="section fade">
      <div className="container">
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: ld }} />
        <nav className="breadcrumb" aria-label="Breadcrumb">
          <a href={`/aixwim/`}>Beranda</a><span>/</span>
          {n > 1 && <><a href={categoryUrl(kategori)}>{c.name}</a><span>/</span></>}
          <span>{n > 1 ? `Halaman ${n}` : c.name}</span>
        </nav>
        <h2 style={{ marginBottom: 8 }}>{n > 1 ? `${c.name} — Halaman ${n}` : c.name}</h2>
        <p style={{ color: 'var(--muted)', marginBottom: 24 }}>{c.description}</p>
        <div className="grid">
          {pageItems.map((a) => <ArticleCard key={a.slug} a={a} />)}
        </div>
        {totalPages > 1 && (
          <nav className="pagination" aria-label="Navigasi halaman">
            {n > 1 && <a href={n > 2 ? `${categoryUrl(kategori)}page/${n - 1}/` : categoryUrl(kategori)}>← Sebelumnya</a>}
            <span>Halaman {n} / {totalPages}</span>
            {n < totalPages && <a href={`${categoryUrl(kategori)}page/${n + 1}/`}>Berikutnya →</a>}
          </nav>
        )}
      </div>
    </section>
  );
}
