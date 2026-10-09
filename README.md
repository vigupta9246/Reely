# Cine Duniya - movie website (static)
1. build.py kholo, upar SITE_NAME, SITE_URL, EMAIL badlo. `python build.py` chalao (HTML dobara ban jayega).
2. Is poore folder ko GitHub repo mein upload karo -> Settings > Pages > Deploy from branch (main, / root).
3. Domain milne par repo mein `CNAME` file banao (sirf apna domain likho, jaise www.example.com) aur DNS mein GitHub Pages ke records lagao.
4. UPCOMING aur OTT list official sources se bharo, nayi filmein MOVIES mein jodo. AdSense apply karne se pehle kam se kam 20-30 original review daalo.
5. AdSense approval ke baad ADSENSE variable bharo, aur `ads.txt` mein Google ki di hui line daalo.

## Naya: data.json, posters aur auto-build
- **Film jodna:** sirf `data.json` mein ek naya block jodo (id wahi naam hoga jo film page ka address banta hai, jaise "kgf-chapter-2"). Upcoming/OTT bhi usi file mein.
- **Auto-build (python ki zaroorat nahi):** repo Settings > Pages > Source = "GitHub Actions". Uske baad GitHub par `data.json` edit karke Commit karte hi site apne aap ban kar live ho jati hai. Workflow file: `.github/workflows/pages.yml`.
- **Posters:** `img/posters/<film-id>.webp` naam se rakho (400x600). Badi photo ko chhota karne ke liye squoosh.app (free) ya `python optimize_images.py` (originals `posters_src/` mein). Poster na ho to rangeen placeholder dikhta hai.
- **CDN (traffic badhne par):** `IMG_BASE` mein jsDelivr ka link daalo, jaise https://cdn.jsdelivr.net/gh/USERNAME/REPO@main/
