# -*- coding: utf-8 -*-
# Run: python build.py  -> regenerates all HTML pages. Edit SITE settings and MOVIES/UPCOMING/OTT below.
import os, html, json, urllib.parse
SITE_NAME = "Reely"
SITE_URL = "https://YOUR-DOMAIN.com"      # domain milne ke baad yahan badlo
EMAIL = "your-email@example.com"           # apna email likho
# Comments (giscus = GitHub Discussions). giscus.app par jakar apni repo ke liye ye 4 values nikalo, tab comments dikhenge. Khali = comments nahi dikhenge.
COMMENTS = {"repo":"","repo_id":"","category":"","category_id":""}
AD_SLOTS = {"top":"","mid":"","bottom":""}   # AdSense mein "Display ad unit" banao, uska slot number (jaise "1234567890") yahan daalo
ADSENSE = ""                               # e.g. "ca-pub-1234567890123456" (approval ke baad)
YEAR = 2026
# Apne social media links yahan daalo. Khali "" chhodoge to us ka icon chhup jayega.
SOCIAL = {"Instagram":"https://instagram.com/","YouTube":"https://youtube.com/","Facebook":"https://facebook.com/","X":"https://x.com/"}
ICONS = {
"Instagram":'<svg viewBox="0 0 24 24" width="20" height="20"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.3" fill="currentColor"/></svg>',
"YouTube":'<svg viewBox="0 0 24 24" width="20" height="20"><rect x="2" y="5" width="20" height="14" rx="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 9l5 3-5 3z" fill="currentColor"/></svg>',
"Facebook":'<svg viewBox="0 0 24 24" width="20" height="20"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v8h4v-8h3l1-4h-4V8z" fill="currentColor"/></svg>',
"WhatsApp":'<svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.5-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 8.5c0 3.3 2.7 6 6 6l1-1.8-2-1-1 .8a4 4 0 0 1-1.8-1.8l.8-1-1-2z" fill="currentColor"/></svg>',
"Copy":'<svg viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
"Bookmark":'<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4.5L6 21z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
"Sun":'<svg class="sn" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
"Moon":'<svg class="mn" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
"X":'<svg viewBox="0 0 24 24" width="20" height="20"><path d="M4 4l16 16M20 4L4 20" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'}

# id, title, year, industry, genres, director, summary(apne words), verdict
MOVIES = [
("inception","Inception",2010,"Hollywood",["Action","Sci-Fi"],"Christopher Nolan","Ek chor sapno ke andar ghus kar logon ke vichar churata hai. Is baar use vichar churane nahi, daalne ka kaam milta hai. Kahani parat-dar-parat sapno mein chalti hai.","Dimaag lagane wali, lekin dekhne mein poori tarah romanchak film."),
("the-dark-knight","The Dark Knight",2008,"Hollywood",["Action","Crime"],"Christopher Nolan","Batman, Gotham ka police wala aur ek naya district attorney milkar shehar ke apradh ko todne nikalte hain, tabhi Joker aakar sab kuch ulat deta hai.","Superhero film se zyada ek gambhir crime thriller. Joker ka kirdaar yaadgaar hai."),
("mad-max-fury-road","Mad Max: Fury Road",2015,"Hollywood",["Action"],"George Miller","Registan mein ek zalim shasak se bhaagti auraton ko max aur furiosa bachate hain. Poori film ek lambi car chase jaisi hai.","Shuru se aakhir tak tez raftaar action, kam dialogue aur zabardast stunts."),
("get-out","Get Out",2017,"Hollywood",["Horror","Thriller"],"Jordan Peele","Ek naujawan apni girlfriend ke parivar se milne jaata hai aur dheere-dheere samajhta hai ki wahan kuch gadbad hai.","Darr aur samajik tippani ka behtareen mel. Ant tak utsukta bani rehti hai."),
("the-conjuring","The Conjuring",2013,"Hollywood",["Horror"],"James Wan","Ek parivar ko apne naye ghar mein ajeeb ghatnayein hoti hain aur wo do paranormal investigators se madad maangte hain.","Seedhi-saadi bhoot-pret kahani jo mahaul ke dum par daraati hai."),
("hereditary","Hereditary",2018,"Hollywood",["Horror"],"Ari Aster","Ek parivar apni dadi ke guzarne ke baad ek ke baad ek bhayanak ghatnaon ka saamna karta hai.","Dheemi lekin bechain kar dene wali. Kamzor dil walon ke liye nahi."),
("titanic","Titanic",1997,"Hollywood",["Romance","Drama"],"James Cameron","Ek jahaaz ke pehle safar mein alag-alag tabqe ke do log pyaar kar baithte hain, jabki jahaaz ka anjaam kareeb aa raha hota hai.","Bade star-scale par bani amar prem kahani."),
("the-notebook","The Notebook",2004,"Hollywood",["Romance","Drama"],"Nick Cassavetes","Ek buzurg ek mahila ko ek purani prem kahani padh kar sunata hai jo do jawan logon ke pyaar aur doori ki hai.","Bhavuk romantic drama, rone ke liye tissue paas rakhein."),
("dilwale-dulhania-le-jayenge","Dilwale Dulhania Le Jayenge",1995,"Bollywood",["Romance"],"Aditya Chopra","Europe ki yatra par do yuva mil kar pyaar kar baithte hain, lekin ladki ka parivar use pehle se kisi aur ke saath tay kar chuka hai.","Bollywood romance ka sabse bada naam, aaj bhi taaza lagti hai."),
("jab-we-met","Jab We Met",2007,"Bollywood",["Romance","Comedy"],"Imtiaz Ali","Ek udaas business-man train mein ek bolti hui ladki se milta hai aur uski zindagi badalne lagti hai.","Halki-phulki, hansi aur dil ko chhoone wali romantic comedy."),
("3-idiots","3 Idiots",2009,"Bollywood",["Comedy","Drama"],"Rajkumar Hirani","Engineering college ke teen doston ki kahani, jo padhai ke dabav aur asli sapno ke beech sawal uthati hai.","Hansate hansate zaroori baat kehne wali film."),
("dangal","Dangal",2016,"Bollywood",["Drama","Sports"],"Nitesh Tiwari","Ek purva pehalwan apni betiyon ko kushti ke champion banane ke liye kadi mehnat karwata hai.","Prerak, bhavuk aur dekhne layak."),
("tumbbad","Tumbbad",2018,"Bollywood",["Horror","Fantasy"],"Rahi Anil Barve","Ek gaon ke purane khazane ki laalach ek aadmi ko ek khatarnak devta tak le jaati hai.","Alag mizaaj ki Hindi horror, drishyon aur vatavaran mein bahut dum."),
("war","War",2019,"Bollywood",["Action","Thriller"],"Siddharth Anand","Ek agent ko apne hi guru ko pakadne ka kaam milta hai, jo ab baaghi ban chuka hai.","Stylish stunts aur videshi locations wali masala action film."),
("andhadhun","Andhadhun",2018,"Bollywood",["Thriller","Comedy"],"Sriram Raghavan","Ek pianist jo khud ko andha dikhata hai, ek murder ka gawah ban jaata hai.","Mod-dar-mod wali dark comedy thriller."),
("gangs-of-wasseypur","Gangs of Wasseypur",2012,"Bollywood",["Action","Crime"],"Anurag Kashyap","Dhanbad ke koyla maafia ke teen peedhiyon ke dushmani ki lambi kahani.","Kachchi aur asli crime saga, bahut yaadgaar dialogue."),
]
# UPCOMING / OTT: yahan khud verified info daalo (official source se). Format: (title, date, platform_or_industry, short_note)
UPCOMING = []
OTT = []

CATS = [("top-movies","Top Movies","Sab behtareen filmein"),("horror","Horror","Darawni filmein"),("action","Action","Action filmein"),
 ("romance","Romance","Romantic filmein"),("hollywood","Hollywood","Hollywood filmein"),("bollywood","Bollywood","Bollywood filmein"),
 ("upcoming","Upcoming","Aane wali filmein"),("ott","OTT Release","OTT par aa rahi filmein")]
HUES = [200,350,28,160,265,45,320,95]

def e(s): return html.escape(str(s))
def yt(t): return "https://www.youtube.com/results?search_query="+urllib.parse.quote(t+" official trailer")
def poster(m):
    h=HUES[sum(map(ord,m[0]))%len(HUES)]
    return f'<div class="poster" style="--h:{h}"><i class="tag">{e(m[4][0])}</i><span>{e(m[1])}</span><small>{m[2]}</small></div>'
def card(m):
    return f'<a class="card" href="movie-{m[0]}.html">{poster(m)}<b>{e(m[1])}</b><em>{e(m[3])} &middot; {e(", ".join(m[4]))}</em></a>'

def layout(title, desc, body, fname, ld=""):
    ad = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>' if ADSENSE else '<!-- AdSense code yahan aayega (ADSENSE variable bharo) -->'
    if ADSENSE: ad = NPA + ad
    names = {c[0]:c[1] for c in CATS}
    main_nav = "".join(f'<a href="{k}.html">{names[k]}</a>' for k in ["top-movies","hollywood","bollywood","upcoming","ott"])
    more = "".join(f'<a href="{k}.html">{names[k]}</a>' for k in ["horror","action","romance"])
    nav = main_nav + f'<details class="more"><summary>Aur Genres</summary><div>{more}</div></details>'
    rob = '<meta name="robots" content="noindex">' if fname=="watchlist.html" else ""
    hero = HERO if fname=="index.html" else ""
    url = SITE_URL + "/" if fname=="index.html" else f"{SITE_URL}/{fname}"
    otype = "video.movie" if fname.startswith("movie-") else "website"
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICONS[n]}</a>' for n,u in SOCIAL.items() if u)
    return f'''<!DOCTYPE html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('theme')||'dark'}}catch(e){{document.documentElement.dataset.theme='dark'}}</script>{rob}
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{e(SITE_NAME)}"><meta property="og:type" content="{otype}"><meta property="og:locale" content="hi_IN">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{SITE_URL}/og.png">
<link rel="alternate" type="application/rss+xml" title="{e(SITE_NAME)}" href="feed.xml">{ld}<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="style.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;800&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">
<script src="site.js" defer></script>
{ad}</head><body>
<header><div class="wrap bar"><a class="logo" href="index.html"><img src="favicon.png" width="40" height="40" alt="">{e(SITE_NAME)}</a>
<input type="checkbox" id="mn"><label for="mn" class="burger" aria-label="Menu">Menu</label><nav>{nav}</nav><div class="tools"><a class="wl" href="watchlist.html" aria-label="Meri watchlist">{ICONS["Bookmark"]}<b id="wlc"></b></a><button id="tg" class="tg" type="button" aria-label="Light ya dark theme badlein">{ICONS["Sun"]}{ICONS["Moon"]}</button></div></div></header>
{hero}<main class="wrap">{body}</main>
<footer><div class="wrap"><img class="flogo" src="logo.png" alt="{e(SITE_NAME)} logo" width="90" height="87"><div class="soc">{soc}</div><p>&copy; {YEAR} {e(SITE_NAME)}. Ye site sirf filmon ki jaankari deti hai. Hum koi film download ya pirated link nahi dete.</p>
<p><a href="about.html">About Us</a> <a href="contact.html">Contact Us</a> <a href="privacy-policy.html">Privacy Policy</a> <a href="disclaimer.html">Disclaimer</a> <a href="terms.html">Terms</a> <a href="#" id="ck-open">Cookie settings</a> <a href="feed.xml">RSS</a></p></div></footer>{BANNER}</body></html>'''

SITEJS = r"""
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.1});
document.querySelectorAll('.card,.film,.tile').forEach((el,i)=>{el.classList.add('rv');el.style.transitionDelay=(i%6)*60+'ms';io.observe(el)});
const hd=document.querySelector('header');addEventListener('scroll',()=>hd.classList.toggle('sm',scrollY>30),{passive:true});
const q=document.getElementById('q'),box=document.getElementById('res');
if(q){q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();if(!v){box.innerHTML='';return}
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
function wrender(){if(!wg)return;const ms=wget().map(id=>IDX.find(m=>m.id===id)).filter(Boolean);
wg.innerHTML=ms.map(m=>{const h=H[[...m.id].reduce((s,c)=>s+c.charCodeAt(0),0)%8],g=m.g.split(' ')[0];
return '<div><a class="card" href="movie-'+m.id+'.html"><div class="poster" style="--h:'+h+'"><i class="tag">'+g+'</i><span>'+m.t+'</span><small>'+m.y+'</small></div><b>'+m.t+'</b><em>'+m.i+'</em></a><button class="rm" type="button" data-id="'+m.id+'">Hatayein</button></div>'}).join('');
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
"""
NPA = "<script>try{if(localStorage.getItem('cookie-ok')!=='all'){window.adsbygoogle=window.adsbygoogle||[];window.adsbygoogle.requestNonPersonalizedAds=1}}catch(e){}</script>"
BANNER = '''<div id="ck" class="ck" role="dialog" aria-label="Cookie sahmati" hidden><p>Hum site chalane aur ads dikhane ke liye cookies istemal karte hain. Aap personalised ads band bhi rakh sakte hain. <a href="privacy-policy.html">Privacy Policy</a></p><div><button id="ck-no" type="button">Sirf zaroori</button><button id="ck-yes" type="button">Sab accept karein</button></div></div>'''
SHARE = f'''<div class="share"><span>Share karein</span><a data-s="wa" href="#" target="_blank" rel="noopener">{ICONS["WhatsApp"]} WhatsApp</a><a data-s="x" href="#" target="_blank" rel="noopener">{ICONS["X"]} X</a><button type="button" id="cp">{ICONS["Copy"]} Link copy karein</button></div>'''
COMMENTS_HTML = f'<section class="comments"><h2>Aapki raay</h2><div id="gc" data-repo="{COMMENTS["repo"]}" data-repo-id="{COMMENTS["repo_id"]}" data-category="{COMMENTS["category"]}" data-category-id="{COMMENTS["category_id"]}"></div></section>' if all(COMMENTS.values()) else ""
def adslot(pos):
    sid = AD_SLOTS.get(pos, "")
    if not (ADSENSE and sid): return ""   # khali dabba kabhi nahi dikhate (AdSense policy)
    return f'<aside class="ad" aria-label="Vigyapan"><small>Vigyapan</small><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE}" data-ad-slot="{sid}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></aside>'
pages = {}
def section(title, ms, link=None):
    g = "".join(card(m) for m in ms)
    more = f'<a href="{link}">Sab dekhein</a>' if link else ""
    return f'<section><div class="sh"><h2>{e(title)}</h2>{more}</div><div class="row">{g}</div></section>'
def has(m,g): return g in m[4]

filters = {"top-movies":lambda m:True,"horror":lambda m:has(m,"Horror"),"action":lambda m:has(m,"Action"),
 "romance":lambda m:has(m,"Romance"),"hollywood":lambda m:m[3]=="Hollywood","bollywood":lambda m:m[3]=="Bollywood"}

# Home
tick = "".join(f"<span>{e(m[1])} <small>{m[2]}</small></span>" for m in MOVIES)
HERO = f'''<section class="hero"><div class="wrap hero-in"><h1>Aaj raat kaunsi film dekhein?</h1>
<p>Hollywood aur Bollywood ki filmon ke saaf review, upcoming list aur OTT release, sab ek jagah.</p>
<div class="sr"><input id="q" type="search" placeholder="Film ya genre khojein, jaise Horror" autocomplete="off" aria-label="Film khojein"><div id="res"></div></div>
<p class="chips"><a href="horror.html">Horror</a><a href="action.html">Action</a><a href="romance.html">Romance</a><a href="upcoming.html">Upcoming</a></p></div></section>
<div class="tick" aria-hidden="true"><div class="tk">{tick}{tick}</div></div>'''
home = section("Top Movies", MOVIES[:8], "top-movies.html")
home += adslot("mid")
home += section("Bollywood", [m for m in MOVIES if m[3]=="Bollywood"], "bollywood.html")
home += section("Hollywood", [m for m in MOVIES if m[3]=="Hollywood"], "hollywood.html")
home += '<section class="tiles"><a class="tile t1" href="upcoming.html"><b>Upcoming</b><span>Aane wali filmein</span></a><a class="tile t2" href="ott.html"><b>OTT Release</b><span>OTT par aa rahi filmein</span></a></section>'
pages["index.html"]=(f"{SITE_NAME} - Movie Reviews, Upcoming aur OTT Release","Hindi mein top movies, horror, action, romance, Hollywood, Bollywood, upcoming aur OTT release ki jaankari.",home)

for slug,name,sub in CATS:
    if slug in filters:
        ms=[m for m in MOVIES if filters[slug](m)]
        body=f'<h1>{e(name)} Movies</h1><p class="lead">{sub}. Har film ka chhota review aur kahani ka saar.</p>{adslot("top")}<div class="grid">'+"".join(card(m) for m in ms)+'</div>'+adslot("bottom")
    else:
        items = UPCOMING if slug=="upcoming" else OTT
        rows = "".join(f'<tr><td>{e(i[0])}</td><td>{e(i[1])}</td><td>{e(i[2])}</td><td>{e(i[3])}</td></tr>' for i in items)
        tbl = f'<div class="scroll"><table><tr><th>Film</th><th>Date</th><th>Platform / Industry</th><th>Note</th></tr>{rows}</table></div>' if items else '<p class="empty">Is list ko jald hi official sources ke hisaab se update kiya jayega.</p>'
        body=f'<h1>{e(name)}</h1><p class="lead">{sub}. Dates badal sakti hain, isliye official ghoshna zaroor dekhein.</p>{tbl}{adslot("bottom") if items else ""}'
    pages[f"{slug}.html"]=(f"{name} Movies - {SITE_NAME}",f"{name} filmon ki list aur review.",body)

for m in MOVIES:
    rel=[x for x in MOVIES if x[0]!=m[0] and (x[3]==m[3] or set(x[4])&set(m[4]))][:4]
    body=f'''<article class="film"><div>{poster(m)}</div><div><h1>{e(m[1])} ({m[2]})</h1>
<p class="meta">{e(m[3])} &middot; {e(", ".join(m[4]))} &middot; Nirdeshak: {e(m[5])}</p>
<h2>Kahani ka saar</h2><p>{e(m[6])}</p><h2>Hamari raay</h2><p>{e(m[7])}</p>
<p><a class="btn" href="{yt(m[1]+" "+str(m[2]))}" target="_blank" rel="noopener">YouTube par trailer dekhein</a><button class="btn wlb" type="button" data-id="{m[0]}">Baad mein dekhunga</button></p>{SHARE}</div></article>{adslot("mid")}
<section><h2>Ye bhi dekhein</h2><div class="grid">{"".join(card(x) for x in rel)}</div></section>{COMMENTS_HTML}{adslot("bottom")}'''
    pages[f"movie-{m[0]}.html"]=(f"{m[1]} ({m[2]}) Review, Kahani aur Jaankari - {SITE_NAME}",m[6][:150],body)

L=lambda *ps:"".join(f"<p>{p}</p>" for p in ps)
pages["about.html"]=("About Us - "+SITE_NAME,"Hamare baare mein.",f"<h1>About Us</h1>"+L(f"{SITE_NAME} ek movie information website hai jahan hum Hollywood aur Bollywood ki filmon ka review, kahani ka saar, upcoming aur OTT release ki jaankari Hindi mein dete hain.","Hamara maqsad hai ki dekhne wale ko sahi film chunne mein madad mile. Har review hamari apni raay par aadharit hota hai.","Hum piracy ka samarthan nahi karte aur kisi film ko download karne ka link nahi dete."))
pages["contact.html"]=("Contact Us - "+SITE_NAME,"Sampark karein.",f"<h1>Contact Us</h1>"+L(f'Koi sawal, sujhav ya correction ho to is email par likhein: <a href="mailto:{EMAIL}">{EMAIL}</a>',"Hum aam taur par 2-3 din mein jawab dete hain."))
pages["privacy-policy.html"]=("Privacy Policy - "+SITE_NAME,"Privacy policy.",f"<h1>Privacy Policy</h1>"+L(f"Ye website ({SITE_URL}) aapse koi personal jaankari zabardasti nahi maangti.","Cookies: Google AdSense jaise third-party vendors aapko aapki pichli visits ke aadhar par ads dikhane ke liye cookies istemal kar sakte hain. Google ka advertising cookie istemal use ko hamari site aur dusri sites par personalised ads dikhane deta hai.",'Aap <a href="https://www.google.com/settings/ads" rel="noopener">Ads Settings</a> mein jakar personalised ads band kar sakte hain.',"Watchlist aur light/dark theme ki pasand sirf aapke browser mein save hoti hai, hamare server par nahi.",*(["Comments GitHub Discussions (giscus) se chalte hain, comment karne ke liye GitHub account chahiye aur us par giscus aur GitHub ki privacy policy lagu hoti hai."] if all(COMMENTS.values()) else []),"Cookie settings: aap footer ke Cookie settings se personalised ads ki apni pasand kabhi bhi badal sakte hain.","Log files: har website ki tarah hum IP address, browser ka prakar aur visit ka samay jaise standard technical data record kar sakte hain.","Third-party links: hamari site par YouTube jaise dusri sites ke links ho sakte hain. Unki privacy policy ke liye hum zimmedar nahi hain.","Is policy mein badlav hone par ye page update hoga."))
pages["disclaimer.html"]=("Disclaimer - "+SITE_NAME,"Disclaimer.",f"<h1>Disclaimer</h1>"+L("Is website par di gayi jaankari sirf sutchna aur manoranjan ke liye hai. Review hamari niji raay hain.","Saari film ke naam, poster aur trademarks unke apne maalikon ke hain. Hum kisi film ko host ya upload nahi karte.","Release dates aur OTT platform badal sakte hain. Sahi jaankari ke liye official ghoshna dekhein."))
pages["terms.html"]=("Terms and Conditions - "+SITE_NAME,"Terms.",f"<h1>Terms and Conditions</h1>"+L("Is site ko istemal karke aap in sharton se sahmat hote hain.","Site ka content hamari ijazat ke bina copy ya dobara prakashit karna mana hai.","Hum bina soochna ke content mein badlav kar sakte hain."))
pages["watchlist.html"]=("Meri Watchlist - "+SITE_NAME,"Baad mein dekhne wali filmon ki list.",'<h1>Meri Watchlist</h1><p class="lead">Ye list sirf is browser mein save hoti hai. Film page par "Baad mein dekhunga" dabakar jodein.</p><div id="wl-grid" class="grid"></div><p id="wl-empty" class="empty" hidden>Abhi koi film nahi judi. <a href="top-movies.html">Top movies dekhein</a>.</p>')
pages["404.html"]=("Page nahi mila - "+SITE_NAME,"404","<h1>Page nahi mila</h1><p>Ye page maujood nahi hai. <a href=\"index.html\">Home par jayein</a>.</p>")

CRUMBS = {}
for slug,name,sub in CATS: CRUMBS[f"{slug}.html"] = [("Home","index.html"),(name,None)]
BYFILE = {f"movie-{m[0]}.html":m for m in MOVIES}
for f,m in BYFILE.items(): CRUMBS[f] = [("Home","index.html"),(m[3],m[3].lower()+".html"),(m[1],None)]
def jsonld(f, cr):
    out = []
    if f=="index.html": out.append({"@context":"https://schema.org","@type":"WebSite","name":SITE_NAME,"url":SITE_URL+"/","inLanguage":"hi"})
    if cr:
        out.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":n+1,"name":l,"item":SITE_URL+"/"+(h or f)} for n,(l,h) in enumerate(cr)]})
    if f in BYFILE:
        m = BYFILE[f]
        out.append({"@context":"https://schema.org","@type":"Movie","name":m[1],"description":m[6],"dateCreated":str(m[2]),"genre":m[4],"director":{"@type":"Person","name":m[5]},"url":f"{SITE_URL}/{f}"})
    return "".join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False).replace("</","<\\/")+"</script>" for o in out)
for f,(t,d,b) in pages.items():
    cr = CRUMBS.get(f)
    if cr:
        b = '<div class="crumbs" aria-label="Breadcrumb">' + ' <span>&rsaquo;</span> '.join(f'<a href="{h}">{e(l)}</a>' if h else f'<span aria-current="page">{e(l)}</span>' for l,h in cr) + '</div>' + b
    open(f,"w",encoding="utf-8").write(layout(t,d,b,f,jsonld(f,cr)))

items = "".join(f"<item><title>{e(m[1])} ({m[2]}) Review</title><link>{SITE_URL}/movie-{m[0]}.html</link><guid>{SITE_URL}/movie-{m[0]}.html</guid><description>{e(m[6])}</description></item>" for m in MOVIES)
open("feed.xml","w",encoding="utf-8").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{e(SITE_NAME)}</title><link>{SITE_URL}/</link><description>Hindi mein movie reviews, upcoming aur OTT release.</description><language>hi</language>{items}</channel></rss>')

idx=json.dumps([{"id":m[0],"t":m[1],"y":m[2],"i":m[3],"g":" ".join(m[4])} for m in MOVIES],ensure_ascii=False)
open("site.js","w",encoding="utf-8").write("const IDX="+idx+";\n"+SITEJS)
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE_URL}/{f}</loc></url>" for f in pages if f not in ("404.html","watchlist.html"))+"</urlset>")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print(len(pages),"pages ban gaye")
