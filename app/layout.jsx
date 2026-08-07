import { CSS } from '../lib/css';
import { site, siteUrl } from '../lib/site';
import Nav from '../components/Nav';
import Footer from '../components/Footer';

export const metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: `${site.name} — ${site.tagline}`, template: `%s — ${site.name}` },
  description: site.description,
  keywords: ['berita indonesia', 'ekonomi', 'teknologi', 'nasional', 'bisnis', 'pendidikan'],
  openGraph: {
    type: 'website',
    siteName: site.name,
    title: `${site.name} — ${site.tagline}`,
    description: site.description,
  },
  icons: {
    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2" fill="%232563eb"/><path d="M7 9h10M7 13h6" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>',
  },
};

const SCRIPTS = String.raw`
(function(){
  var t=localStorage.getItem('aixwim-theme');
  if(t==='dark'){document.documentElement.classList.add('dark')}
  else if(t==='light'){document.documentElement.classList.remove('dark')}
  else{var dark=window.matchMedia('(prefers-color-scheme: dark)').matches;
    if(dark){document.documentElement.classList.add('dark')}}
})();
(function(){
  var b=document.getElementById('burgerBtn'),m=document.getElementById('mobileMenu');
  if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
  var tb=document.getElementById('themeBtn');
  if(tb){tb.addEventListener('click',function(){
    var cur=localStorage.getItem('aixwim-theme')||'auto';
    var next=cur==='auto'?'light':(cur==='light'?'dark':'auto');
    localStorage.setItem('aixwim-theme',next);
    document.documentElement.classList.toggle('dark',next==='dark');
  });}
  var tt=document.getElementById('toTop');
  if(tt){window.addEventListener('scroll',function(){tt.classList.toggle('show',window.scrollY>400);},{passive:true});
    tt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});}
  document.addEventListener('keydown',function(e){if(e.ctrlKey&&e.key==='/'){e.preventDefault();var s=document.querySelector('.search-link');if(s)location.href=s.href;}});
})();
`;

export default function RootLayout({ children }) {
  return (
    <html lang="id">
      <body>
        <style dangerouslySetInnerHTML={{ __html: CSS }} />
        <script dangerouslySetInnerHTML={{ __html: SCRIPTS }} />
        <a className="skip-link" href="#content">Lewati ke konten</a>
        <Nav />
        <main id="content">{children}</main>
        <Footer />
        <button id="toTop" aria-label="Kembali ke atas">↑</button>
      </body>
    </html>
  );
}
