# -*- coding: utf-8 -*-
"""Build the print pack: every released book merged into one PDF, plus a
printer-facing cover sheet.

One file is the difference between "download the pack" working and a browser
silently blocking thirteen sequential downloads.
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import all_books                          # noqa: E402
from website import SPEC                               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "print")
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")


def cover_sheet(books, path):
    """A single 8.5in square page the printer reads before anything else."""
    rows = "".join(
        f'<tr><td>{b["week"]}</td><td><b>{b["title"]}</b></td>'
        f'<td>{i * 24 + 25}&ndash;{i * 24 + 48}</td></tr>'
        for i, b in enumerate(books))
    specs = "".join(f"<tr><th>{k.title()}</th><td>{v}</td></tr>" for k, v in SPEC.items())
    doc = f"""<!doctype html><meta charset="utf-8"><style>
@page{{size:8.5in 8.5in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:816px;height:816px;font-family:'Nunito','DejaVu Sans',sans-serif;
  padding:46px 50px;color:#23303a;background:#fffaf0}}
h1{{font-size:33px;font-weight:800;color:#0b3a4a;line-height:1.1}}
.sup{{font-size:11px;letter-spacing:.26em;text-transform:uppercase;font-weight:800;color:#0f6d80}}
.rule{{height:5px;width:86px;background:#ff7a59;border-radius:3px;margin:12px 0 16px}}
p{{font-size:13px;line-height:1.5;color:#5d7079;margin-bottom:10px}}
table{{border-collapse:collapse;width:100%;font-size:11.5px;margin-top:8px}}
th,td{{text-align:left;padding:4px 7px;border-bottom:1px solid rgba(11,58,74,.14)}}
th{{color:#0b3a4a;font-weight:800;width:112px}}
h2{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#0b3a4a;
  font-weight:800;margin:16px 0 2px}}
.note{{margin-top:14px;background:#f3e2c0;border-radius:12px;padding:12px 14px;font-size:12px;
  color:#23303a;line-height:1.5}}
.foot{{position:absolute;bottom:34px;left:50px;right:50px;font-size:10.5px;color:#8aa0a8}}
</style>
<div class="sup">The Wonder Ship</div>
<h1>Print order &amp; specification</h1>
<div class="rule"></div>
<p>This file contains <b>{len(books)} complete picture books</b>, one after another,
{len(books)} &times; 24 = <b>{len(books) * 24} pages</b> in total. Each book is a separate
finished product &mdash; please print and bind them <b>individually</b>, not as one volume.</p>

<h2>Specification</h2>
<table>{specs}</table>

<h2>Books in this file</h2>
<table><tr><th>Week</th><th>Title</th><th>Pages in this PDF</th></tr>{rows}</table>

<div class="note"><b>Important:</b> print at 100% &mdash; do not scale or "fit to page".
Pages are already the finished trim size. Page 1 of each book is its cover.</div>
<div class="foot">Mentality Over Excuses &mdash; no materials, no excuses, all music. &nbsp;·&nbsp;
The Wonder Ship &mdash; ages 3 &mdash; 24 pages each</div>
"""
    with tempfile.TemporaryDirectory() as t:
        src = os.path.join(t, "c.html")
        open(src, "w", encoding="utf-8").write(doc)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", "--virtual-time-budget=4000",
                        f"--print-to-pdf={path}", "file://" + src], capture_output=True)
    return os.path.exists(path)


def build():
    from pypdf import PdfWriter, PdfReader
    books = [b for b in all_books()
             if os.path.exists(os.path.join(OUT, b["slug"] + ".pdf"))]
    if not books:
        print("no book PDFs found — run bot.py build --pdf first")
        return None
    sheet = os.path.join(OUT, "_cover-sheet.pdf")
    cover_sheet(books, sheet)

    w = PdfWriter()
    if os.path.exists(sheet):
        for p in PdfReader(sheet).pages:
            w.add_page(p)
    for b in books:
        r = PdfReader(os.path.join(OUT, b["slug"] + ".pdf"))
        w.add_outline_item(f'Week {b["week"]} — {b["title"]}', len(w.pages))
        for p in r.pages:
            w.add_page(p)
    out = os.path.join(OUT, "wonder-ship-print-pack.pdf")
    with open(out, "wb") as f:
        w.write(f)
    if os.path.exists(sheet):
        os.remove(sheet)
    mb = os.path.getsize(out) / 1024 / 1024
    print(f"print pack — {len(books)} books, {len(w.pages)} pages, {mb:.1f} MB")
    return out


if __name__ == "__main__":
    build()
