import { siteUrl, articles, categories, fullUrl } from '../lib/site';

export default function sitemap() {
  const now = new Date().toISOString().split('T')[0];
  const urls = [
    { url: siteUrl + '/', lastModified: now, changeFrequency: 'daily', priority: 1.0 },
    { url: fullUrl('/cari/'), lastModified: now, changeFrequency: 'monthly', priority: 0.4 },
    ...categories.map((c) => ({
      url: fullUrl(`/kategori/${c.slug}/`),
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.8,
    })),
    ...articles.map((a) => ({
      url: fullUrl(`/artikel/${a.slug}/`),
      lastModified: a.date.split('T')[0],
      changeFrequency: 'monthly',
      priority: 0.7,
    })),
  ];
  return urls;
}

export const dynamic = 'force-static';
