# -*- coding: utf-8 -*-
# Run: python build.py  -> regenerates all HTML pages. Edit SITE settings and MOVIES/UPCOMING/OTT below.
import os, html, urllib.parse
SITE_NAME = "Reely"
SITE_URL = "https://YOUR-DOMAIN.com"      # domain milne ke baad yahan badlo
EMAIL = "your-email@example.com"           # apna email likho
ADSENSE = ""                               # e.g. "ca-pub-1234567890123456" (approval ke baad)
YEAR = 2026

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
    return f'<div class="poster" style="--h:{h}"><span>{e(m[1])}</span><small>{m[2]}</small></div>'
def card(m):
    return f'<a class="card" href="movie-{m[0]}.html">{poster(m)}<b>{e(m[1])}</b><em>{e(m[3])} &middot; {e(", ".join(m[4]))}</em></a>'

def layout(title, desc, body, fname):
    ad = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>' if ADSENSE else '<!-- AdSense code yahan aayega (ADSENSE variable bharo) -->'
    names = {c[0]:c[1] for c in CATS}
    main_nav = "".join(f'<a href="{k}.html">{names[k]}</a>' for k in ["top-movies","hollywood","bollywood","upcoming","ott"])
    more = "".join(f'<a href="{k}.html">{names[k]}</a>' for k in ["horror","action","romance"])
    nav = main_nav + f'<details class="more"><summary>Aur Genres</summary><div>{more}</div></details>'
    return f'''<!DOCTYPE html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE_URL}/{fname}"><link rel="stylesheet" href="style.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;800&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">
{ad}</head><body>
<header><div class="wrap bar"><a class="logo" href="index.html">{e(SITE_NAME)}</a>
<input type="checkbox" id="mn"><label for="mn" class="burger" aria-label="Menu">Menu</label><nav>{nav}</nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><p>&copy; {YEAR} {e(SITE_NAME)}. Ye site sirf filmon ki jaankari deti hai. Hum koi film download ya pirated link nahi dete.</p>
<p><a href="about.html">About Us</a> <a href="contact.html">Contact Us</a> <a href="privacy-policy.html">Privacy Policy</a> <a href="disclaimer.html">Disclaimer</a> <a href="terms.html">Terms</a></p></div></footer></body></html>'''

pages = {}
def section(title, ms, more=None):
    g = "".join(card(m) for m in ms) or '<p class="empty">Is section mein jald hi filmein judengi.</p>'
    return f'<section><h2>{e(title)}</h2><div class="grid">{g}</div></section>'
def has(m,g): return g in m[4]

filters = {"top-movies":lambda m:True,"horror":lambda m:has(m,"Horror"),"action":lambda m:has(m,"Action"),
 "romance":lambda m:has(m,"Romance"),"hollywood":lambda m:m[3]=="Hollywood","bollywood":lambda m:m[3]=="Bollywood"}

# Home
home = f'''<section class="hero"><h1>Filmon ki saaf, seedhi jaankari</h1>
<p>Top movies, horror, action, romance, Hollywood aur Bollywood. Upcoming aur OTT release ki khabar, har film par hamari apni raay.</p></section>'''
home += section("Top Movies", MOVIES[:8])
home += section("Bollywood", [m for m in MOVIES if m[3]=="Bollywood"][:4])
home += section("Hollywood", [m for m in MOVIES if m[3]=="Hollywood"][:4])
home += '<section><h2>Upcoming aur OTT</h2><p><a class="btn" href="upcoming.html">Upcoming movies</a> <a class="btn" href="ott.html">OTT release</a></p></section>'
pages["index.html"]=(f"{SITE_NAME} - Movie Reviews, Upcoming aur OTT Release","Hindi mein top movies, horror, action, romance, Hollywood, Bollywood, upcoming aur OTT release ki jaankari.",home)

for slug,name,sub in CATS:
    if slug in filters:
        ms=[m for m in MOVIES if filters[slug](m)]
        body=f'<h1>{e(name)} Movies</h1><p class="lead">{sub}. Har film ka chhota review aur kahani ka saar.</p><div class="grid">'+"".join(card(m) for m in ms)+'</div>'
    else:
        items = UPCOMING if slug=="upcoming" else OTT
        rows = "".join(f'<tr><td>{e(i[0])}</td><td>{e(i[1])}</td><td>{e(i[2])}</td><td>{e(i[3])}</td></tr>' for i in items)
        tbl = f'<div class="scroll"><table><tr><th>Film</th><th>Date</th><th>Platform / Industry</th><th>Note</th></tr>{rows}</table></div>' if items else '<p class="empty">Is list ko jald hi official sources ke hisaab se update kiya jayega.</p>'
        body=f'<h1>{e(name)}</h1><p class="lead">{sub}. Dates badal sakti hain, isliye official ghoshna zaroor dekhein.</p>{tbl}'
    pages[f"{slug}.html"]=(f"{name} Movies - {SITE_NAME}",f"{name} filmon ki list aur review.",body)

for m in MOVIES:
    rel=[x for x in MOVIES if x[0]!=m[0] and (x[3]==m[3] or set(x[4])&set(m[4]))][:4]
    body=f'''<article class="film"><div>{poster(m)}</div><div><h1>{e(m[1])} ({m[2]})</h1>
<p class="meta">{e(m[3])} &middot; {e(", ".join(m[4]))} &middot; Nirdeshak: {e(m[5])}</p>
<h2>Kahani ka saar</h2><p>{e(m[6])}</p><h2>Hamari raay</h2><p>{e(m[7])}</p>
<p><a class="btn" href="{yt(m[1]+" "+str(m[2]))}" target="_blank" rel="noopener">YouTube par trailer dekhein</a></p></div></article>
<section><h2>Ye bhi dekhein</h2><div class="grid">{"".join(card(x) for x in rel)}</div></section>'''
    pages[f"movie-{m[0]}.html"]=(f"{m[1]} ({m[2]}) Review, Kahani aur Jaankari - {SITE_NAME}",m[6][:150],body)

L=lambda *ps:"".join(f"<p>{p}</p>" for p in ps)
pages["about.html"]=("About Us - "+SITE_NAME,"Hamare baare mein.",f"<h1>About Us</h1>"+L(f"{SITE_NAME} ek movie information website hai jahan hum Hollywood aur Bollywood ki filmon ka review, kahani ka saar, upcoming aur OTT release ki jaankari Hindi mein dete hain.","Hamara maqsad hai ki dekhne wale ko sahi film chunne mein madad mile. Har review hamari apni raay par aadharit hota hai.","Hum piracy ka samarthan nahi karte aur kisi film ko download karne ka link nahi dete."))
pages["contact.html"]=("Contact Us - "+SITE_NAME,"Sampark karein.",f"<h1>Contact Us</h1>"+L(f'Koi sawal, sujhav ya correction ho to is email par likhein: <a href="mailto:{EMAIL}">{EMAIL}</a>',"Hum aam taur par 2-3 din mein jawab dete hain."))
pages["privacy-policy.html"]=("Privacy Policy - "+SITE_NAME,"Privacy policy.",f"<h1>Privacy Policy</h1>"+L(f"Ye website ({SITE_URL}) aapse koi personal jaankari zabardasti nahi maangti.","Cookies: Google AdSense jaise third-party vendors aapko aapki pichli visits ke aadhar par ads dikhane ke liye cookies istemal kar sakte hain. Google ka advertising cookie istemal use ko hamari site aur dusri sites par personalised ads dikhane deta hai.",'Aap <a href="https://www.google.com/settings/ads" rel="noopener">Ads Settings</a> mein jakar personalised ads band kar sakte hain.',"Log files: har website ki tarah hum IP address, browser ka prakar aur visit ka samay jaise standard technical data record kar sakte hain.","Third-party links: hamari site par YouTube jaise dusri sites ke links ho sakte hain. Unki privacy policy ke liye hum zimmedar nahi hain.","Is policy mein badlav hone par ye page update hoga."))
pages["disclaimer.html"]=("Disclaimer - "+SITE_NAME,"Disclaimer.",f"<h1>Disclaimer</h1>"+L("Is website par di gayi jaankari sirf sutchna aur manoranjan ke liye hai. Review hamari niji raay hain.","Saari film ke naam, poster aur trademarks unke apne maalikon ke hain. Hum kisi film ko host ya upload nahi karte.","Release dates aur OTT platform badal sakte hain. Sahi jaankari ke liye official ghoshna dekhein."))
pages["terms.html"]=("Terms and Conditions - "+SITE_NAME,"Terms.",f"<h1>Terms and Conditions</h1>"+L("Is site ko istemal karke aap in sharton se sahmat hote hain.","Site ka content hamari ijazat ke bina copy ya dobara prakashit karna mana hai.","Hum bina soochna ke content mein badlav kar sakte hain."))
pages["404.html"]=("Page nahi mila - "+SITE_NAME,"404","<h1>Page nahi mila</h1><p>Ye page maujood nahi hai. <a href=\"index.html\">Home par jayein</a>.</p>")

for f,(t,d,b) in pages.items():
    open(f,"w",encoding="utf-8").write(layout(t,d,b,f))

open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE_URL}/{f}</loc></url>" for f in pages if f!="404.html")+"</urlset>")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print(len(pages),"pages ban gaye")
