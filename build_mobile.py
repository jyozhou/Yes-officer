# 把 index.html 和 assets 里的图片打包成一个可单独发送的 HTML 文件
import base64, json, os
d = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(d, "index.html"), encoding="utf-8").read()
mime = {".webp": "image/webp", ".jpg": "image/jpeg"}
assets = {}
for f in sorted(os.listdir(os.path.join(d, "assets"))):
    ext = os.path.splitext(f)[1]
    if ext in mime:
        b = open(os.path.join(d, "assets", f), "rb").read()
        assets[f] = "data:%s;base64,%s" % (mime[ext], base64.b64encode(b).decode())
tag = "<script>window.ASSETS=" + json.dumps(assets) + "</script>\n<script>"
assert html.count("<script>") == 1
out = os.path.join(d, "是鹤总-手机版.html")
open(out, "w", encoding="utf-8").write(html.replace("<script>", tag))
print(len(assets), "images,", os.path.getsize(out) // 1024, "KB")
