
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
