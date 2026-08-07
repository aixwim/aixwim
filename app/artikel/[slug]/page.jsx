import { notFound } from 'next/navigation';
import { articles, getArticle, getCategory, siteUrl, fullUrl, slugToUrl, categoryUrl, formatDate, related, readingTime } from '../../../lib/site';

export function generateStaticParams() {
  return articles.map((a) => ({ slug: a.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const a = getArticle(slug);
  if (!a) return {};
  return {
    title: a.title,
    description: a.excerpt,
    alternates: { canonical: `/artikel/${slug}/` },
    openGraph: { title: a.title, description: a.excerpt, type: 'article', publishedTime: a.date },
    keywords: (a.tags || []).join(', '),
  };
}

export default async function ArticlePage({ params }) {
  const { slug } = await params;
  const a = getArticle(slug);
  if (!a) notFound();
  const cat = getCategory(a.category);
  const url = fullUrl(`/artikel/${a.slug}/`);
  const title = a.title.replace(/"/g, '&quot;');
  const enc = encodeURIComponent(url);
  const encTitle = encodeURIComponent(a.title);
  const rel = related(a);
  const ld = JSON.stringify([
    {
      '@context': 'https://schema.org',
      '@type': 'NewsArticle',
      headline: a.title,
      description: a.excerpt,
      image: [],
      datePublished: a.date,
      dateModified: a.date,
      author: { '@type': 'Organization', name: a.author },
      publisher: { '@type': 'Organization', name: 'Aixwim News' },
      mainEntityOfPage: url,
      keywords: (a.tags || []).join(', '),
      inLanguage: 'id',
    },
    {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Beranda', item: siteUrl },
        { '@type': 'ListItem', position: 2, name: cat ? cat.name : a.category, item: fullUrl(`/kategori/${a.category}/`) },
        { '@type': 'ListItem', position: 3, name: a.title },
      ],
    },
  ]);
  return (
    <article className="article fade">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: ld }} />
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <a href={`/aixwim/`}>Beranda</a><span>/</span>
        <a href={categoryUrl(a.category)}>{cat ? cat.name : a.category}</a><span>/</span>
        <span>{a.title}</span>
      </nav>
      <h1>{a.title}</h1>
      <div className="byline">
        <span>✍️ <b>{a.author}</b></span>
        <span>🗓 {formatDate(a.date)}</span>
        <span>⏱ {readingTime(a)} baca</span>
        <span>🏷 <a href={categoryUrl(a.category)}>{cat ? cat.name : a.category}</a></span>
      </div>
      {a.content.map((p, i) => (
        <p key={i} className={i === 0 ? 'lead' : ''}>{p}</p>
      ))}
      {a.tags && (
        <div className="tags">
          {a.tags.map((t) => <span className="tag" key={t}>#{t}</span>)}
        </div>
      )}
      <div className="share" aria-label="Bagikan artikel">
        <a className="wa" href={`https://wa.me/?text=${encTitle}%20${enc}`} target="_blank" rel="noopener">WhatsApp</a>
        <a className="x" href={`https://twitter.com/intent/tweet?text=${encTitle}&url=${enc}`} target="_blank" rel="noopener">X</a>
        <a className="fb" href={`https://www.facebook.com/sharer/sharer.php?u=${enc}`} target="_blank" rel="noopener">Facebook</a>
        <a className="li" href={`https://www.linkedin.com/sharing/share-offsite/?url=${enc}`} target="_blank" rel="noopener">LinkedIn</a>
        <a className="tg" href={`https://t.me/share/url?url=${enc}&text=${encTitle}`} target="_blank" rel="noopener">Telegram</a>
      </div>
      {rel.length > 0 && (
        <aside className="related">
          <h3>Artikel Terkait</h3>
          <ul>
            {rel.map((r) => (
              <li key={r.slug}>
                <a href={slugToUrl(r.slug)}>{r.title}</a>
                <span className="rmeta">{formatDate(r.date)}</span>
              </li>
            ))}
          </ul>
        </aside>
      )}
    </article>
  );
}
