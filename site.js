
let IDX=null;const IMGB='';const loadIdx=()=>IDX?Promise.resolve(IDX):fetch('search.json').then(r=>r.json()).then(d=>(IDX=d));
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.1});
document.querySelectorAll('.card,.film,.tile').forEach((el,i)=>{el.classList.add('rv');el.style.transitionDelay=(i%6)*60+'ms';io.observe(el)});
const hd=document.querySelector('header');addEventListener('scroll',()=>hd.classList.toggle('sm',scrollY>30),{passive:true});
const q=document.getElementById('q'),box=document.getElementById('res');
if(q){q.addEventListener('focus',loadIdx);q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();if(!v){box.innerHTML='';return}if(!IDX){loadIdx().then(()=>q.dispatchEvent(new Event('input')));return}
const r=IDX.filter(m=>(m.t+' '+m.g+' '+m.i).toLowerCase().includes(v)).slice(0,6);
box.innerHTML=r.length?r.map(m=>'<a href="movie-'+m.id+'.html"><b>'+m.t+'</b> <small>'+m.y+' &middot; '+m.i+'</small></a>').join(''):'<a>Kuch nahi mila</a>'})}
const ck=document.getElementById('ck');
const getC=()=>{try{return localStorage.getItem('cookie-ok')}catch(e){return null}};
const setC=v=>{try{localStorage.setItem('cookie-ok',v)}catch(e){}ck.hidden=true};
if(!getC())ck.hidden=false;
document.getElementById('ck-yes').onclick=()=>setC('all');
document.getElementById('ck-no').onclick=()=>setC('min');
document.getElementById('ck-open').onclick=e=>{e.preventDefault();ck.hidden=false};
const root=document.documentElement,tg=document.getElementById('tg');
tg.onclick=()=>{const t=root.dataset.theme==='light'?'dark':'light';root.dataset.theme=t;try{localStorage.setItem('theme',t)}catch(e){}
const f=document.querySelector('iframe.giscus-frame');if(f)f.contentWindow.postMessage({giscus:{setConfig:{theme:t}}},'https://giscus.app')};
const wget=()=>{try{return JSON.parse(localStorage.getItem('watchlist')||'[]')}catch(e){return[]}};
const wset=a=>{try{localStorage.setItem('watchlist',JSON.stringify(a))}catch(e){}wui()};
function wui(){const a=wget(),c=document.getElementById('wlc');if(c)c.textContent=a.length||'';
document.querySelectorAll('.wlb').forEach(b=>{const on=a.includes(b.dataset.id);b.classList.toggle('on',on);b.textContent=on?'Watchlist mein hai':'Baad mein dekhunga';b.setAttribute('aria-pressed',on)})}
document.querySelectorAll('.wlb').forEach(b=>b.onclick=()=>{const a=wget(),i=a.indexOf(b.dataset.id);i<0?a.push(b.dataset.id):a.splice(i,1);wset(a)});
const H=[200,350,28,160,265,45,320,95],wg=document.getElementById('wl-grid');
function wrender(){if(!wg)return;if(!IDX){loadIdx().then(wrender);return}const ms=wget().map(id=>IDX.find(m=>m.id===id)).filter(Boolean);
wg.innerHTML=ms.map(m=>{const h=H[[...m.id].reduce((s,c)=>s+c.charCodeAt(0),0)%8],g=m.g.split(' ')[0];
return '<div><a class="card" href="movie-'+m.id+'.html"><div class="poster'+(m.p?' has-img':'')+'" style="--h:'+h+'">'+(m.p?'<img src="'+IMGB+'img/posters/'+m.id+'.webp" alt="" width="400" height="600" loading="lazy">':'')+'<i class="tag">'+g+'</i><span>'+m.t+'</span><small>'+m.y+'</small></div><b>'+m.t+'</b><em>'+m.i+'</em></a><button class="rm" type="button" data-id="'+m.id+'">Hatayein</button></div>'}).join('');
document.getElementById('wl-empty').hidden=ms.length>0;
wg.querySelectorAll('.rm').forEach(b=>b.onclick=()=>{wset(wget().filter(x=>x!==b.dataset.id));wrender()})}
wui();wrender();
const sh=document.querySelector('.share');
if(sh){const u=encodeURIComponent(location.href),t=encodeURIComponent(document.title);
sh.querySelector('[data-s=wa]').href='https://wa.me/?text='+t+'%20'+u;
sh.querySelector('[data-s=x]').href='https://twitter.com/intent/tweet?text='+t+'&url='+u;
const cp=document.getElementById('cp'),l=cp.lastChild.textContent;
cp.onclick=async()=>{try{await navigator.clipboard.writeText(location.href)}catch(e){prompt('Link copy karein:',location.href)}cp.lastChild.textContent=' Copy ho gaya';setTimeout(()=>cp.lastChild.textContent=l,1800)}}
const gc=document.getElementById('gc');
if(gc){new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){o.disconnect();const s=document.createElement('script');s.src='https://giscus.app/client.js';
const d=gc.dataset;[['repo',d.repo],['repo-id',d.repoId],['category',d.category],['category-id',d.categoryId],['mapping','pathname'],['reactions-enabled','1'],['input-position','top'],['theme',root.dataset.theme],['lang','hi']].forEach(([k,v])=>s.setAttribute('data-'+k,v));
s.crossOrigin='anonymous';s.async=true;gc.appendChild(s)}},{rootMargin:'300px'}).observe(gc)}
