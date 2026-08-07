import { slugToUrl, categoryUrl, formatDate, getCategory } from '../lib/site';

export default function ArticleCard({ a }) {
  const cat = getCategory(a.category);
  return (
    <a className="card" href={slugToUrl(a.slug)}>
      <span className="cat">{cat ? cat.name : a.category}</span>
      <h3>{a.title}</h3>
      <p>{a.excerpt}</p>
      <div className="meta">
        <span>🗓 {formatDate(a.date)}</span>
        <span>⏱ {a.reading_time || '3 menit'}</span>
      </div>
    </a>
  );
}
