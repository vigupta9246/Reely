# Poster chhote karne ka tool (free). Use:
#   1. Original poster ko posters_src/ folder mein rakho, naam = film ka id (jaise inception.jpg, the-dark-knight.png)
#   2. python optimize_images.py   ->  img/posters/inception.webp (400x600, ~20-35 KB) ban jayega
# Zaroorat: pip install pillow
import os, sys
from PIL import Image, ImageOps
SRC, DST = "posters_src", os.path.join("img", "posters")
if not os.path.isdir(SRC):
    print(SRC, "folder nahi mila, kuch nahi karna."); sys.exit(0)
os.makedirs(DST, exist_ok=True)
for f in sorted(os.listdir(SRC)):
    stem, ext = os.path.splitext(f)
    if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"): continue
    out = os.path.join(DST, stem + ".webp")
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(os.path.join(SRC, f)): continue
    im = ImageOps.fit(Image.open(os.path.join(SRC, f)).convert("RGB"), (400, 600), Image.LANCZOS)
    im.save(out, "WEBP", quality=78, method=6)
    print(stem, os.path.getsize(out) // 1024, "KB")
