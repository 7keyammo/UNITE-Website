# -*- coding: utf-8 -*-
"""Build fixed-layout EPUB 3 ebooks — one per book.

Fixed layout is the right call for a picture book: the illustration and its
words must stay together on the page. Every page is 816 x 816 (the print
trim), so the ebook and the paperback are the same book.
"""
import html
import os
import re
import sys
import uuid
import zipfile
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art                                          # noqa: E402
from content import all_books                       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "ebook")
W = H = 816

XMLNS = 'xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"'


def xhtmlify(s):
    """HTML fragments in the content model use <br>; XHTML needs <br/>."""
    return s.replace("<br>", "<br/>").replace("&nbsp;", "&#160;")


STYLE = """
@page { margin: 0; }
html, body { margin:0; padding:0; }
body { width:%(w)spx; height:%(h)spx; font-family:'Nunito','Trebuchet MS',sans-serif; }
.page { position:absolute; inset:0; width:%(w)spx; height:%(h)spx; overflow:hidden;
        display:flex; flex-direction:column; background:var(--sand); }
.art { position:relative; flex:1 1 auto; min-height:0; overflow:hidden; }
.art svg { position:absolute; top:0; left:0; width:100%%; height:100%%; }
.story { flex:0 0 auto; padding:18px 46px 12px; text-align:center; background:#fffaf0;
         font-weight:800; font-size:26px; line-height:1.3; color:var(--deep); }
.story .sp { display:block; height:.44em; }
.story .log { display:block; margin:10px auto 0; max-width:30ch; padding:10px 16px;
              border:3px solid var(--accent); border-radius:14px;
              font-size:18px; font-weight:700; color:var(--mid); }
.band { flex:0 0 auto; background:var(--deep); color:#dff3f6; padding:12px 46px 14px; }
.band .p { font-weight:800; font-size:16px; line-height:1.35; }
.band .p b { color:var(--accent); letter-spacing:.09em; }
.band .g { font-size:12px; line-height:1.45; opacity:.8; margin-top:5px; }
.full { position:relative; flex:1 1 auto; display:flex; flex-direction:column;
        align-items:center; justify-content:center; text-align:center;
        padding:46px; color:#fff; }
.full .bg { position:absolute; top:0; left:0; right:0; bottom:0; overflow:hidden; }
.full .bg svg { width:100%%; height:100%%; }
.scrim { position:absolute; top:0; left:0; right:0; bottom:0; }
.cover { justify-content:flex-end; padding-bottom:76px; }
.in { position:relative; z-index:1; max-width:30ch; }
.sup { font-weight:800; font-size:20px; letter-spacing:.3em; text-transform:uppercase; color:var(--light); }
h1 { font-size:60px; line-height:1.05; margin:12px 0 8px; font-weight:800; }
.pilots { font-weight:600; font-size:19px; line-height:1.5; color:#eaf6f7; }
.note { background:var(--sand); color:var(--deep); text-align:left;
        align-items:flex-start; justify-content:center; }
.kick { font-weight:800; font-size:13px; letter-spacing:.2em; text-transform:uppercase; color:var(--mid); }
h2 { font-size:40px; line-height:1.15; margin:10px 0 16px; font-weight:800; }
.rule { width:88px; height:5px; background:var(--accent); border-radius:3px; margin-bottom:22px; }
.note p { font-size:20px; line-height:1.6; margin:0 0 16px; max-width:52ch; }
.note p b { color:var(--mid); }
.beats { display:flex; margin:22px 0; width:100%%; }
.beat { flex:1 1 0; background:rgba(255,255,255,.10); border:3px solid var(--mid);
        border-radius:16px; padding:16px 6px; margin:0 7px; }
.beat .n { font-size:28px; font-weight:800; color:var(--accent); }
.beat .w { font-size:21px; font-weight:800; margin:6px 0 3px; }
.beat .d { font-size:13px; line-height:1.3; color:var(--light); }
.dial { font-size:23px; line-height:1.55; font-weight:700; color:var(--light); }
.motto { margin-top:20px; font-size:15px; font-weight:600; font-style:italic; color:var(--accent); }
""" % dict(w=W, h=H)


def svg(book, page):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 640" '
            f'preserveAspectRatio="xMidYMid slice" role="img">'
            f'{art.bleed(book, page)}{art.scene(book, page)}</svg>')


def story(lines):
    return "".join('<span class="sp"></span>' if not l else xhtmlify(l) + "<br/>" for l in lines)


def page_doc(book, p):
    bn, n = book["number"], p["n"]
    pal = book["palette"]
    vars_ = (f"--deep:{pal['deep']};--mid:{pal['mid']};--light:{pal['light']};"
             f"--accent:{pal['accent']};--sand:{pal['sand']}")

    if p["kind"] == "title":
        inner = (f'<div class="full cover" style="{vars_}"><div class="bg">{svg(bn, n)}</div>'
                 f'<div class="scrim" style="background:linear-gradient(180deg,'
                 f'rgba(8,26,34,.34) 0%,rgba(8,26,34,.20) 34%,rgba(8,26,34,.72) 62%,'
                 f'rgba(8,26,34,.92) 100%)"></div>'
                 f'<div class="in"><div class="sup">{html.escape(p["series"])}</div>'
                 f'<h1>{html.escape(p["title"])}</h1>'
                 f'<div class="pilots">{html.escape(p["pilots"])}</div></div></div>')
    elif p["kind"] == "note":
        ps = "".join(f"<p>{xhtmlify(t)}</p>" for t in p["text"])
        inner = (f'<div class="full note" style="{vars_}"><div class="in" style="max-width:56ch">'
                 f'<div class="kick">{html.escape(p["kicker"])}</div>'
                 f'<h2>{html.escape(p["heading"])}</h2><div class="rule"></div>{ps}</div></div>')
    elif p["kind"] == "theme":
        beats = "".join(f'<div class="beat"><div class="n">{a}</div><div class="w">{b}</div>'
                        f'<div class="d">{c}</div></div>' for a, b, c in p["clap"])
        inner = (f'<div class="full" style="{vars_}"><div class="bg">{svg(bn, n)}</div>'
                 f'<div class="scrim" style="background:rgba(8,26,34,.66)"></div>'
                 f'<div class="in" style="max-width:40ch">'
                 f'<h1 style="font-size:44px">{html.escape(p["heading"])}</h1>'
                 f'<div class="pilots">{html.escape(p["sub"])}</div>'
                 f'<div class="beats">{beats}</div>'
                 f'<div class="dial">{"<br/>".join(p["dial"])}</div>'
                 f'<div class="motto">{html.escape(p["motto"])}</div></div></div>')
    else:
        inner = (f'<div class="art">{svg(bn, n)}</div>'
                 f'<div class="story">{story(p["text"])}</div>'
                 f'<div class="band"><div class="p"><b>PAUSE:</b> {xhtmlify(p["pause"])}</div>'
                 f'<div class="g"><b>GROWN-UPS:</b> {xhtmlify(p["grown"])}</div></div>')

    return (f'<?xml version="1.0" encoding="utf-8"?>\n'
            f'<html {XMLNS}><head><meta charset="utf-8"/>'
            f'<title>{html.escape(book["title"])} — page {n}</title>'
            f'<meta name="viewport" content="width={W}, height={H}"/>'
            f'<link rel="stylesheet" type="text/css" href="style.css"/></head>'
            f'<body><div class="page" style="{vars_}">{inner}</div></body></html>')


def opf(book, uid):
    items, spine = [], []
    for p in book["model"]:
        i = f"p{p['n']:02d}"
        items.append(f'<item id="{i}" href="{i}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{i}"/>')
    return f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:uuid:{uid}</dc:identifier>
    <dc:title>The Wonder Ship {book["number"]}: {html.escape(book["title"])}</dc:title>
    <dc:language>en</dc:language>
    <dc:creator>Mr. Domkam and Mr. Johnson</dc:creator>
    <dc:description>A read-aloud picture book for ages 3, with a movement break on every page.</dc:description>
    <dc:subject>Juvenile Nonfiction / Science</dc:subject>
    <meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>
    <meta property="rendition:layout">pre-paginated</meta>
    <meta property="rendition:orientation">auto</meta>
    <meta property="rendition:spread">auto</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="style.css" media-type="text/css"/>
    {chr(10).join("    " + i for i in items)}
  </manifest>
  <spine>
    {chr(10).join("    " + s for s in spine)}
  </spine>
</package>'''


def nav(book):
    lis = "".join(f'<li><a href="p{p["n"]:02d}.xhtml">'
                  f'{html.escape(p["beat"])} (page {p["n"]})</a></li>'
                  for p in book["model"])
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<html {XMLNS}><head><meta charset="utf-8"/>'
            f'<title>Contents</title></head><body><nav epub:type="toc" id="toc">'
            f'<h1>Contents</h1><ol>{lis}</ol></nav></body></html>')


def build_one(book):
    uid = uuid.uuid5(uuid.NAMESPACE_URL, "wondership/" + book["slug"])
    path = os.path.join(OUT, book["slug"] + ".epub")
    docs = {f'p{p["n"]:02d}.xhtml': page_doc(book, p) for p in book["model"]}

    # every XHTML file must actually parse as XML, or readers reject the book
    for name, doc in docs.items():
        try:
            ET.fromstring(doc.encode("utf-8"))
        except ET.ParseError as e:
            raise SystemExit(f"{book['slug']} {name} is not well-formed XML: {e}")
    ET.fromstring(nav(book).encode("utf-8"))
    ET.fromstring(opf(book, uid).encode("utf-8"))

    with zipfile.ZipFile(path, "w") as z:
        # mimetype must be first and stored uncompressed
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        z.writestr(zi, "application/epub+zip")
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="utf-8"?>\n'
                   '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/></rootfiles></container>',
                   zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf(book, uid), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav(book), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", STYLE, zipfile.ZIP_DEFLATED)
        for name, doc in docs.items():
            z.writestr("OEBPS/" + name, doc, zipfile.ZIP_DEFLATED)
    return path


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for b in all_books():
        p = build_one(b)
        print(f"{os.path.basename(p)} — {os.path.getsize(p)/1024:.0f} KB, 24 fixed-layout pages")
