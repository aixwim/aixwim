import fs from 'node:fs';
import path from 'node:path';

const data = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data', 'articles.json'), 'utf8'));
const { site, articles } = data;
const base = site.base_url.replace(/\/$/, '');
const items = articles
  .slice()
  .sort((a, b) => new Date(b.date) - new Date(a.date))
  .map((a) => {
    const url = `${base}/artikel/${a.slug}/`;
    const desc = a.content.join(' ').slice(0, 500) + '…';
    return `<item>
  <title><![CDATA[${a.title}]]></title>
  <link>${url}</link>
  <guid isPermaLink="true">${url}</guid>
  <pubDate>${new Date(a.date).toUTCString()}</pubDate>
  <description><![CDATA[${desc}]]></description>
  <category>${a.category}</category>
</item>`;
  }).join('\n');
const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>${site.name}</title>
  <link>${base}/</link>
  <description>${site.description}</description>
  <language>id</language>
  <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
  <atom:link href="${base}/rss.xml" rel="self" type="application/rss+xml"/>
${items}
</channel>
</rss>
`;
fs.writeFileSync(path.join(process.cwd(), 'public', 'rss.xml'), xml);
console.log(`✅ rss.xml: ${articles.length} item`);
