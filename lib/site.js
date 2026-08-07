import fs from 'node:fs';
import path from 'node:path';

const BASE = '/aixwim';
const raw = fs.readFileSync(path.join(process.cwd(), 'data', 'articles.json'), 'utf8');
const data = JSON.parse(raw);

export const site = data.site;
export const categories = data.categories;
export const articles = data.articles;
export const basePath = BASE;
export const siteUrl = site.base_url.replace(/\/$/, '');
export const fullUrl = (p) => siteUrl + (p.startsWith('/') ? p : '/' + p);
export const slugToUrl = (slug) => `${BASE}/artikel/${slug}/`;
export const categoryUrl = (slug) => `${BASE}/kategori/${slug}/`;
export const searchUrl = () => `${BASE}/cari/`;
export const getArticle = (slug) => articles.find((a) => a.slug === slug);
export const getCategory = (slug) => categories.find((c) => c.slug === slug);
export const byCategory = (slug) => articles.filter((a) => a.category === slug);
export const related = (art, n = 3) => byCategory(art.category).filter((a) => a.slug !== art.slug).slice(0, n);
export const formatDate = (iso) =>
  new Date(iso).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
export const readingTime = (art) =>
  art.reading_time ||
  `${Math.max(1, Math.round(art.content.join(' ').split(/\s+/).length / 130))} menit`;

export const PER_PAGE = 6;
