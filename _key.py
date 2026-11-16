import numpy as np, os
from PIL import Image, ImageFilter
im = Image.open(r"C:\Users\Jyozhou\.cursor\projects\d-Research-Test-SLG\assets\ch_parrot2.jpg").convert("RGB")
a = np.asarray(im).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
m = np.minimum(r, b) - g
alpha = np.clip((170 - m) / 80, 0, 1)
tr = Image.fromarray(((alpha < 0.5) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
edge = (np.asarray(tr) > 0) | (alpha < 1)
ex = np.clip(m, 0, None) * edge
a[..., 0] = r - ex
a[..., 2] = b - ex
al = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
res = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
res.putalpha(al)
bb = al.point(lambda v: 255 if v > 40 else 0).getbbox()
res = res.crop((bb[0], bb[1], bb[2], im.height))
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "parrot.webp")
res.save(p, "WEBP", quality=92, method=4)
print(res.size, os.path.getsize(p) // 1024, "KB")
