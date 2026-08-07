(function(){
  'use strict';
  var root=document.documentElement;
  /* Tema: light/dark/auto (persist localStorage) */
  var t=localStorage.getItem('aixwim-theme');
  if(t==='dark'){root.classList.add('dark')}
  else if(t==='light'){root.classList.remove('dark')}
  else if(window.matchMedia('(prefers-color-scheme: dark)').matches){root.classList.add('dark')}
  var tb=document.getElementById('themeBtn');
  if(tb){tb.addEventListener('click',function(){
    var cur=localStorage.getItem('aixwim-theme')||'auto';
    var next=cur==='auto'?'light':(cur==='light'?'dark':'auto');
    localStorage.setItem('aixwim-theme',next);
    root.classList.toggle('dark',next==='dark');
  });}
  /* Burger menu mobile */
  var b=document.getElementById('burgerBtn'),m=document.getElementById('mobileMenu');
  if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
  /* Back to top */
  var tt=document.getElementById('toTop');
  if(tt){window.addEventListener('scroll',function(){tt.classList.toggle('show',window.scrollY>400);},{passive:true});
    tt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});}
  /* Ctrl+/ → fokus pencarian */
  document.addEventListener('keydown',function(e){if(e.ctrlKey&&e.key==='/'){e.preventDefault();var s=document.querySelector('.search-link');if(s)location.href=s.href;}});
})();
