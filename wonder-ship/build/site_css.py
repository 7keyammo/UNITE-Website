# -*- coding: utf-8 -*-
"""Stylesheet for the public site. One file, no framework, no CDN."""

CSS = r"""
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --deep:#0b3a4a; --mid:#0f6d80; --light:#7fd4d8; --accent:#ff7a59;
  --gold:#ffd166; --sand:#f3e2c0; --paper:#fffaf0; --ink:#23303a;
  --muted:#5d7079; --line:rgba(11,58,74,.14);
  --wrap:1180px;
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Nunito','Trebuchet MS','DejaVu Sans',system-ui,sans-serif;
  color:var(--ink);background:var(--paper);line-height:1.6;overflow-x:hidden}
img,svg{max-width:100%;display:block}
a{color:var(--mid);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 20px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}

/* ---- nav ---- */
header.nav{position:sticky;top:0;z-index:50;background:rgba(11,58,74,.97);
  backdrop-filter:blur(6px);border-bottom:2px solid rgba(255,255,255,.10)}
.nav .wrap{display:flex;align-items:center;gap:8px;height:62px}
.brand{display:flex;align-items:center;gap:10px;color:#fff;font-weight:800;
  font-size:17px;letter-spacing:-.2px;margin-right:auto}
.brand:hover{text-decoration:none}
.brand svg{width:30px;height:30px;flex:0 0 auto}
.nav a.lnk{color:#cfe6ea;font-weight:700;font-size:14px;padding:8px 11px;border-radius:10px}
.nav a.lnk:hover{background:rgba(255,255,255,.12);color:#fff;text-decoration:none}
.nav a.cta{background:var(--accent);color:#fff}
.nav a.cta:hover{background:#ff6742;color:#fff}
@media(max-width:720px){.nav a.lnk{padding:8px 8px;font-size:13px}.brand span{display:none}}

/* ---- hero ---- */
.hero{background:linear-gradient(165deg,#0b3a4a 0%,#171a4a 52%,#1f3d1e 100%);
  color:#fff;padding:clamp(44px,8vw,88px) 0 clamp(40px,7vw,76px);position:relative;overflow:hidden}
.hero .wrap{position:relative;z-index:1}
.hero .sup{font-size:13px;letter-spacing:.32em;text-transform:uppercase;
  font-weight:800;color:var(--light)}
.hero h1{font-size:clamp(34px,7.2vw,64px);line-height:1.04;font-weight:800;
  margin:14px 0 16px;max-width:16ch;letter-spacing:-1px}
.hero p.lede{font-size:clamp(17px,2.4vw,21px);color:#d7ecf0;max-width:56ch}
.hero .row{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-block;font-weight:800;font-size:16px;padding:14px 26px;
  border-radius:999px;border:0;cursor:pointer;transition:transform .12s ease}
.btn:hover{text-decoration:none;transform:translateY(-2px)}
.btn.p{background:var(--accent);color:#fff}
.btn.s{background:rgba(255,255,255,.14);color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.34)}
.btn.g{background:var(--gold);color:#3a2a08}
.hero .ship{position:absolute;right:-40px;bottom:-30px;width:min(44vw,460px);
  aspect-ratio:1000/640;z-index:0;opacity:.34;border-radius:26px;overflow:hidden;
  -webkit-mask-image:radial-gradient(120% 100% at 78% 78%,#000 30%,transparent 74%);
  mask-image:radial-gradient(120% 100% at 78% 78%,#000 30%,transparent 74%)}
.hero .ship svg{width:100%;height:100%;object-fit:cover}
@media(max-width:900px){.hero .ship{display:none}}
.stats{display:flex;gap:26px;flex-wrap:wrap;margin-top:30px;padding-top:22px;
  border-top:1px solid rgba(255,255,255,.18)}
.stat b{display:block;font-size:clamp(24px,4vw,34px);font-weight:800;line-height:1}
.stat span{font-size:13px;color:#a9cdd4}

/* ---- sections ---- */
section{padding:clamp(40px,6vw,72px) 0}
section.alt{background:var(--sand)}
h2.sec{font-size:clamp(25px,4.4vw,38px);font-weight:800;letter-spacing:-.5px;
  color:var(--deep);margin-bottom:10px}
p.sub{color:var(--muted);max-width:62ch;font-size:clamp(15px,2vw,18px);margin-bottom:26px}

/* ---- cards ---- */
.grid{display:grid;gap:18px;grid-template-columns:1fr}
@media(min-width:600px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:940px){.grid{grid-template-columns:repeat(3,1fr)}}
@media(min-width:1180px){.grid.four{grid-template-columns:repeat(4,1fr)}}
.bk{background:#fff;border-radius:20px;overflow:hidden;border:2px solid var(--line);
  display:flex;flex-direction:column;transition:transform .14s ease,box-shadow .14s ease;position:relative}
.bk:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(11,58,74,.16);text-decoration:none}
.bk .cov{position:relative;aspect-ratio:1000/640;background:var(--deep);overflow:hidden}
.bk .cov svg{width:100%;height:100%;object-fit:cover}
.bk .wk{position:absolute;top:10px;left:10px;background:rgba(11,58,74,.92);color:#fff;
  font-size:11px;font-weight:800;letter-spacing:.1em;padding:4px 10px;border-radius:999px}
.bk .m{padding:15px 17px 18px;display:flex;flex-direction:column;flex:1}
.bk h3{font-size:19px;font-weight:800;color:var(--deep);line-height:1.2}
.bk .w{font-size:13px;color:var(--muted);font-weight:700;margin-top:4px}
.bk .c{font-size:11px;color:#8aa0a8;margin-top:7px;line-height:1.4}
.bk .go{margin-top:12px;align-self:flex-start;background:var(--accent);color:#fff;
  font-weight:800;font-size:13px;padding:7px 16px;border-radius:999px}
.bk.soon{opacity:.62}
.bk.soon .cov{background:linear-gradient(150deg,#1a3b47,#28506a);display:flex;
  align-items:center;justify-content:center}
.bk.soon .lockmsg{color:#cfe6ea;font-weight:800;font-size:14px}
.bk.soon .go{background:#8fa8b0}
.termhead{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin:34px 0 14px}
.termhead h3{font-size:clamp(18px,3vw,23px);font-weight:800;color:var(--deep)}
.termhead span{font-size:14px;color:var(--muted)}
.termhead::after{content:"";flex:1 1 60px;height:2px;background:var(--line)}

/* ---- feature rows ---- */
.feat{display:grid;gap:22px;grid-template-columns:1fr}
@media(min-width:820px){.feat{grid-template-columns:repeat(3,1fr)}}
.f{background:#fff;border:2px solid var(--line);border-radius:18px;padding:22px}
.f .ic{width:46px;height:46px;border-radius:13px;background:var(--sand);
  display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.f .ic svg{width:26px;height:26px}
.f h4{font-size:18px;font-weight:800;color:var(--deep);margin-bottom:6px}
.f p{font-size:15px;color:var(--muted)}

/* ---- book detail ---- */
.bkhead{background:var(--deep);color:#fff;padding:0}
.bkhead .cover{aspect-ratio:1000/640;max-height:52vh;overflow:hidden;background:#000}
.bkhead .cover svg{width:100%;height:100%;object-fit:cover}
.bkbody{padding:clamp(28px,5vw,52px) 0}
.crumb{font-size:13px;color:var(--muted);margin-bottom:12px}
.bkbody h1{font-size:clamp(30px,6vw,50px);font-weight:800;color:var(--deep);
  line-height:1.05;letter-spacing:-.8px}
.bkbody .big{font-size:clamp(17px,2.6vw,22px);color:var(--mid);font-weight:700;margin-top:10px}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 26px}
.pill{background:var(--sand);color:var(--deep);font-weight:800;font-size:12px;
  padding:6px 13px;border-radius:999px;border:2px solid var(--line)}
.cols{display:grid;gap:30px;grid-template-columns:1fr}
@media(min-width:900px){.cols{grid-template-columns:1.35fr .85fr}}
.beats{list-style:none;counter-reset:b}
.beats li{counter-increment:b;padding:12px 0 12px 46px;position:relative;
  border-bottom:1px solid var(--line)}
.beats li::before{content:counter(b);position:absolute;left:0;top:12px;width:30px;height:30px;
  border-radius:50%;background:var(--mid);color:#fff;font-weight:800;font-size:13px;
  display:flex;align-items:center;justify-content:center}
.beats b{color:var(--deep);display:block;font-size:15px}
.beats span{font-size:13px;color:var(--muted)}
.side{background:var(--sand);border-radius:20px;padding:22px;border:2px solid var(--line);
  align-self:start;position:sticky;top:80px}
.side h4{font-size:15px;font-weight:800;color:var(--deep);letter-spacing:.06em;
  text-transform:uppercase;margin-bottom:12px}
.side .dl{display:flex;flex-direction:column;gap:9px}
.side .dl a{background:#fff;border:2px solid var(--line);border-radius:12px;padding:11px 14px;
  font-weight:800;font-size:14px;color:var(--deep);display:flex;justify-content:space-between;
  align-items:center;gap:8px}
.side .dl a:hover{border-color:var(--accent);text-decoration:none}
.side .dl a em{font-style:normal;font-size:11px;color:var(--muted);font-weight:700}
.side .dl a.main{background:var(--accent);color:#fff;border-color:var(--accent)}
.side .dl a.main em{color:rgba(255,255,255,.85)}

/* ---- tables ---- */
.tw{overflow-x:auto;border:2px solid var(--line);border-radius:16px;background:#fff}
table{border-collapse:collapse;width:100%;min-width:520px;font-size:14px}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line)}
th{background:var(--sand);font-weight:800;color:var(--deep);font-size:12px;
  text-transform:uppercase;letter-spacing:.06em}
tr:last-child td{border-bottom:0}

/* ---- print pack ---- */
.pack{display:grid;gap:26px;grid-template-columns:1fr}
@media(min-width:900px){.pack{grid-template-columns:1.3fr .9fr}}
.picklist{border:2px solid var(--line);border-radius:18px;background:#fff;overflow:hidden}
.pick{display:flex;align-items:center;gap:13px;padding:12px 16px;border-bottom:1px solid var(--line);cursor:pointer}
.pick:last-child{border-bottom:0}
.pick:hover{background:var(--sand)}
.pick input{width:21px;height:21px;accent-color:var(--accent);flex:0 0 auto;cursor:pointer}
.pick .th{width:62px;aspect-ratio:1000/640;border-radius:7px;overflow:hidden;flex:0 0 auto;background:var(--deep)}
.pick .th svg{width:100%;height:100%;object-fit:cover}
.pick .t{flex:1;min-width:0}
.pick .t b{display:block;font-size:15px;color:var(--deep)}
.pick .t span{font-size:12px;color:var(--muted)}
.pick .qty{width:62px;padding:6px 8px;border:2px solid var(--line);border-radius:9px;
  font-weight:800;text-align:center;font-size:14px;font-family:inherit}
.tools{display:flex;gap:8px;padding:12px 16px;background:var(--sand);border-bottom:1px solid var(--line);flex-wrap:wrap}
.tools button{background:#fff;border:2px solid var(--line);border-radius:999px;padding:6px 14px;
  font-weight:800;font-size:13px;color:var(--deep);cursor:pointer;font-family:inherit}
.tools button:hover{border-color:var(--accent)}
.summary{background:var(--deep);color:#fff;border-radius:18px;padding:24px;align-self:start;position:sticky;top:80px}
.summary h4{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--light);margin-bottom:14px}
.summary .n{font-size:40px;font-weight:800;line-height:1}
.summary .n span{font-size:15px;color:#a9cdd4;font-weight:700}
.summary ul{list-style:none;margin:16px 0;font-size:14px;color:#cfe6ea}
.summary ul li{padding:5px 0;border-bottom:1px solid rgba(255,255,255,.13);display:flex;justify-content:space-between;gap:10px}
.summary .btn{width:100%;text-align:center;margin-top:8px}
.spec{font-size:13px;color:#a9cdd4;margin-top:14px;line-height:1.7}
.spec b{color:#fff}

/* ---- steps ---- */
.steps{counter-reset:s;list-style:none;display:grid;gap:16px}
.steps li{counter-increment:s;background:#fff;border:2px solid var(--line);border-radius:16px;
  padding:20px 22px 20px 66px;position:relative}
.steps li::before{content:counter(s);position:absolute;left:20px;top:19px;width:32px;height:32px;
  border-radius:50%;background:var(--accent);color:#fff;font-weight:800;
  display:flex;align-items:center;justify-content:center;font-size:15px}
.steps b{display:block;color:var(--deep);font-size:17px;margin-bottom:3px}
.steps p{color:var(--muted);font-size:15px}
.steps code{background:var(--sand);padding:2px 7px;border-radius:6px;font-size:13px;
  font-family:ui-monospace,Menlo,monospace}

/* ---- footer ---- */
footer{background:var(--deep);color:#a9cdd4;padding:44px 0 34px;font-size:14px;margin-top:20px}
footer .wrap{display:grid;gap:24px;grid-template-columns:1fr}
@media(min-width:760px){footer .wrap{grid-template-columns:2fr 1fr 1fr}}
footer h5{color:#fff;font-size:13px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:10px}
footer a{color:#a9cdd4;display:block;padding:3px 0}
footer a:hover{color:#fff}
footer .motto{color:var(--gold);font-style:italic;font-weight:700;margin-top:12px}

@media print{
  header.nav,footer,.hero .ship,.btn,.tools{display:none!important}
  body{background:#fff}
  .summary{background:#fff;color:#000;border:2px solid #000}
  .summary h4,.summary ul,.summary .spec{color:#000}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto}}
"""
