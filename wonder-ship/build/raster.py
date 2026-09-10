# -*- coding: utf-8 -*-
"""Rasterise the 72 scenes to PNG.

Why: Canva's HTML importer does not render complex inline SVG faithfully —
it drops strokes and mis-maps fills inside nested transformed groups, which
wrecks the figures. Browsers render the SVG perfectly, so print, the app and
the EPUB all stay vector. Only the Canva hand-off uses these PNGs, and the
page text stays real text so it is still editable in Canva.
"""
import base64
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art                                          # noqa: E402

CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "build", ".scenes")
PW, PH = 1250, 800                                  # 1000x640 at 1.25x


def png_path(book, page):
    return os.path.join(CACHE, f"b{book}p{page:02d}.png")


def all_weeks():
    from content import catalogue
    return [b["week"] for b in catalogue()]


def render_all(force=False, weeks=None):
    os.makedirs(CACHE, exist_ok=True)
    weeks = weeks or all_weeks()
    todo = [(b, p) for b in weeks for p in range(1, 25)
            if force or not os.path.exists(png_path(b, p))]
    if not todo:
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        for b, p in todo:
            html = (f'<body style="margin:0;overflow:hidden">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 640" '
                    f'width="{PW}" height="{PH}" style="display:block">'
                    f'{art.bleed(b, p)}{art.scene(b, p)}</svg></body>')
            src = os.path.join(tmp, "s.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(html)
            subprocess.run(
                [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                 f"--screenshot={png_path(b, p)}", f"--window-size={PW},{PH}",
                 "--virtual-time-budget=2500", f"file://{src}"],
                capture_output=True, check=False)
            if not os.path.exists(png_path(b, p)):
                raise SystemExit(f"failed to rasterise book {b} page {p}")
            _quantize(png_path(b, p))
    return len(todo)


def _quantize(path):
    """The art is flat colour, so a 256-colour palette is lossless to the eye
    and roughly a third of the size — which matters when 24 of these are
    base64-inlined into one file for Canva to fetch."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.quantize(colors=192, method=Image.MEDIANCUT, dither=Image.Dither.NONE) \
      .save(path, optimize=True)


def data_uri(book, page):
    with open(png_path(book, page), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


if __name__ == "__main__":
    n = render_all(force="--force" in sys.argv)
    weeks = all_weeks()
    have = [(b, p) for b in weeks for p in range(1, 25) if os.path.exists(png_path(b, p))]
    total = sum(os.path.getsize(png_path(b, p)) for b, p in have)
    print(f"rasterised {n} new — {len(have)} scenes cached, {total/1024/1024:.1f} MB, "
          f"avg {total/max(1,len(have))/1024:.0f} KB")
