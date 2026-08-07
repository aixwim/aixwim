import { articles, basePath, siteUrl } from '../../lib/site';

export const metadata = {
  title: 'Pencarian',
  description: 'Cari artikel di Aixwim News',
  alternates: { canonical: '/cari/' },
};

const INDEX = articles.map((a) => ({
  slug: a.slug,
  title: a.title,
  excerpt: a.excerpt,
  category: a.category,
  date: a.date,
  tags: a.tags || [],
}));

const SEARCH_JS = String.raw`
(function(){
  var INDEX = __INDEX__;
  var wrap = document.getElementById('results');
  var input = document.getElementById('q');
  function esc(s){return s.replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function hl(text,q){var i=text.toLowerCase().indexOf(q.toLowerCase());if(i<0)return esc(text);return esc(text.slice(0,i))+'<mark>'+esc(text.slice(i,i+q.length))+'</mark>'+esc(text.slice(i+q.length));}
  function render(q){
    if(!q){wrap.innerHTML='<div class="empty">Ketik kata kunci untuk mencari artikel.</div>';return;}
    var terms=q.toLowerCase().split(/\s+/).filter(Boolean);
    var scored=INDEX.map(function(a){
      var s=0, hay=(a.title+' '+(a.tags||[]).join(' ')+' '+a.category+' '+a.excerpt).toLowerCase();
      terms.forEach(function(t){if(a.title.toLowerCase().includes(t))s+=3;if((a.tags||[]).join(' ').toLowerCase().includes(t))s+=2;if(a.excerpt.toLowerCase().includes(t))s+=1;});
      return {a:a,s:s};
    }).filter(function(x){return x.s>0;}).sort(function(x,y){return y.s-x.s;});
    if(!scored.length){wrap.innerHTML='<div class="empty">Tidak ditemukan hasil untuk "'+esc(q)+'".</div>';return;}
    wrap.innerHTML=scored.slice(0,20).map(function(x){
      var a=x.a;
      return '<div class="r"><h3><a href="'+'__BASE__/artikel/'+a.slug+'/">'+hl(a.title,q)+'</a></h3>'+
        '<p>'+hl(a.excerpt,q)+'</p><div class="meta" style="color:var(--muted);font-size:.78rem">🏷 '+esc(a.category)+'</div></div>';
    }).join('');
  }
  input.addEventListener('input',function(){render(input.value);});
  var q=new URLSearchParams(location.search).get('q');
  if(q){input.value=q;render(q);}
})();
`.replace('__INDEX__', JSON.stringify(INDEX)).replace('__BASE__', basePath);

export default function SearchPage() {
  return (
    <div className="search-wrap fade">
      <h1>🔍 Cari Artikel</h1>
      <form className="search-form" action={`${basePath}/cari/`} method="get" role="search">
        <input id="q" type="search" name="q" placeholder="Ketik kata kunci… (mis. ekonomi, AI, UMKM)" autoFocus />
        <button type="submit">Cari</button>
      </form>
      <div id="results"><div className="empty">Ketik kata kunci untuk mencari artikel.</div></div>
      <script dangerouslySetInnerHTML={{ __html: SEARCH_JS }} />
    </div>
  );
}
