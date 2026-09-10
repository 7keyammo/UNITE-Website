# -*- coding: utf-8 -*-
"""Flatten every page to a single image, for Canva.

Canva's importer rebuilds an imported document into its own native elements
rather than rendering it. On this artwork it drops fill-only path geometry,
so both the HTML and the PDF import lose the characters' limbs and outlines.
Neither is a fault in the files — browsers, print pipelines and e-readers all
render them correctly.

So the Canva hand-off ships flattened page images: one PNG per page, imported
as 24 picture pages, pixel-identical to the real book. The trade is that page
text is not editable inside Canva; edit it in build/books.py and regenerate.
"""
import base64
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "build", ".pages")
SCALE = 1.25


PAD = 160   # headless reports a shorter viewport than --window-size asks for,
            # so capture with slack and crop back to the exact page box.


def _shoot(html_head, section, out_png, w, h):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "p.html")
        with open(src, "w", encoding="utf-8") as f:
            f.write("<body style='margin:0;overflow:hidden'>" + html_head + section)
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
             f"--force-device-scale-factor={SCALE}", f"--screenshot={out_png}",
             f"--window-size={w},{h + PAD}", "--virtual-time-budget=4000", f"file://{src}"],
            capture_output=True, check=False)
    if not os.path.exists(out_png):
        raise SystemExit("screenshot failed: " + out_png)
    from PIL import Image
    im = Image.open(out_png).convert("RGB")
    box = (0, 0, int(round(w * SCALE)), int(round(h * SCALE)))
    if im.size != (box[2], box[3]):
        im = im.crop(box)
    im.quantize(colors=192, dither=Image.Dither.NONE).save(out_png, optimize=True)


def flatten(src_html, tag, w, h, force=False):
    """Screenshot each <section> of a built page file. Returns a list of PNG paths."""
    os.makedirs(CACHE, exist_ok=True)
    doc = open(src_html, encoding="utf-8").read()
    head = doc[:doc.index("<section")]
    sections = re.findall(r"<section.*?</section>", doc, re.S)
    out = []
    for i, sec in enumerate(sections, 1):
        png = os.path.join(CACHE, f"{tag}-{i:02d}.png")
        if force or not os.path.exists(png):
            _shoot(head, sec, png, w, h)
        out.append(png)
    return out


def uri(png):
    with open(png, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def build_canva_html(pngs, title, w, h, labels):
    parts = [f"<title>{title}</title>",
             "<style>*{box-sizing:border-box;margin:0;padding:0}"
             "body{background:#444}"
             f".page{{width:{w}px;height:{h}px;margin:0 auto 20px;overflow:hidden}}"
             ".page img{width:100%;height:100%;display:block;object-fit:cover}"
             f"@page{{size:{w}px {h}px;margin:0}}"
             "@media print{body{background:#fff}.page{margin:0;page-break-after:always}"
             ".page:last-child{page-break-after:auto}}</style>"]
    for i, (png, lab) in enumerate(zip(pngs, labels), 1):
        parts.append(f'<section class="page" data-document-role="page" data-label="{lab}">'
                     f'<img src="{uri(png)}" alt=""></section>')
    return "\n".join(parts)


if __name__ == "__main__":
    import html as H
    from content import all_books
    force = "--force" in sys.argv
    books = all_books()
    made = []
    for b in books:
        labels = [f'p{p["n"]} · {H.escape(p["beat"])}' for p in b["model"]]
        # square book
        pngs = flatten(os.path.join(ROOT, "print", b["slug"] + ".html"),
                       "bk-" + b["slug"], 816, 816, force)
        doc = build_canva_html(pngs, f'The Wonder Ship — {b["title"]}', 816, 816, labels)
        p = os.path.join(ROOT, "canva", b["slug"] + ".html")
        open(p, "w", encoding="utf-8").write(doc)
        made.append((p, len(doc)))
        # 16:9 deck
        pngs = flatten(os.path.join(ROOT, "presentation",
                                    b["slug"] + "-presentation.html"),
                       "dk-" + b["slug"], 1920, 1080, force)
        doc = build_canva_html(pngs, f'The Wonder Ship — {b["title"]} (presentation)',
                               1920, 1080, labels)
        p = os.path.join(ROOT, "presentation", b["slug"] + "-presentation-canva.html")
        open(p, "w", encoding="utf-8").write(doc)
        made.append((p, len(doc)))
    for p, n in made:
        print(f"{os.path.relpath(p, ROOT)} — {n/1024/1024:.1f} MB")
