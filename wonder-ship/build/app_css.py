# -*- coding: utf-8 -*-
"""Stylesheet for the offline reader. Kept separate so app.py stays readable."""

CSS = r"""
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --deep:#0b3a4a; --mid:#0f6d80; --light:#7fd4d8; --accent:#ff7a59; --sand:#f3e2c0;
  --ink:#23303a; --paper:#fffaf0;
  --story: clamp(17px, min(3.3vh, 4.9vw), 33px);
  --safe-b: env(safe-area-inset-bottom, 0px);
  --safe-t: env(safe-area-inset-top, 0px);
}
html,body{height:100%;overflow:hidden;background:var(--deep);
  -webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{font-family:'Nunito','Trebuchet MS','DejaVu Sans',system-ui,sans-serif;
  color:var(--ink);overscroll-behavior:none}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer;touch-action:manipulation}
.hide{display:none!important}

/* ============ shell ============ */
#app{position:fixed;inset:0;display:flex;flex-direction:column}

/* ============ library ============ */
#library{position:absolute;inset:0;overflow-y:auto;background:linear-gradient(160deg,#0b3a4a,#171a4a 55%,#1f3d1e);
  padding:calc(28px + var(--safe-t)) 20px calc(28px + var(--safe-b));-webkit-overflow-scrolling:touch}
.lib-head{text-align:center;color:#fff;margin-bottom:22px}
.lib-head .sup{font-size:13px;letter-spacing:.34em;text-transform:uppercase;color:var(--light);font-weight:800}
.lib-head h1{font-size:clamp(30px,7vw,52px);margin:8px 0 6px;font-weight:800;letter-spacing:-.5px}
.lib-head p{color:#cfe6ea;font-size:clamp(14px,3.4vw,17px);max-width:52ch;margin:0 auto;line-height:1.5}
.shelf{display:grid;gap:16px;grid-template-columns:1fr;max-width:1240px;margin:18px auto 0}
@media(min-width:560px){.shelf{grid-template-columns:repeat(2,1fr)}}
@media(min-width:900px){.shelf{grid-template-columns:repeat(3,1fr)}}
@media(min-width:1220px){.shelf{grid-template-columns:repeat(4,1fr)}}
.term{max-width:1240px;margin:30px auto 6px;color:#cfe6ea;display:flex;
  align-items:baseline;gap:12px;flex-wrap:wrap;padding:0 2px}
.term h3{font-size:clamp(15px,3.4vw,20px);color:#fff;font-weight:800}
.term span{font-size:13px;color:#9fc4cc}
.term::after{content:"";flex:1 1 60px;height:2px;background:rgba(255,255,255,.14)}
.card{position:relative}
.card .wk{position:absolute;top:10px;left:10px;background:rgba(11,58,74,.9);color:#fff;
  font-size:11px;font-weight:800;letter-spacing:.1em;padding:4px 9px;border-radius:999px;z-index:2}
.card.soon{opacity:.5}
.card.soon .go{background:#8aa;color:#123}
.card .curric{font-size:11px;color:#7d8f97;margin-top:6px;line-height:1.35}
.lock{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  background:rgba(11,58,74,.55);z-index:1;border-radius:22px}
.lock b{background:#fffaf0;color:#0b3a4a;padding:8px 16px;border-radius:999px;
  font-size:13px;font-weight:800}
.yearbar{max-width:1240px;margin:14px auto 0;background:rgba(255,255,255,.10);
  border-radius:999px;height:10px;overflow:hidden}
.yearbar i{display:block;height:100%;background:var(--accent)}
.yearnote{max-width:1240px;margin:8px auto 0;color:#9fc4cc;font-size:13px;text-align:center}
.card{background:var(--paper);border-radius:22px;overflow:hidden;text-align:left;
  box-shadow:0 12px 34px rgba(0,0,0,.4);display:flex;flex-direction:column;
  transition:transform .16s ease}
.card:active{transform:scale(.975)}
@media(hover:hover){.card:hover{transform:translateY(-5px)}}
.card svg{display:block;width:100%;height:auto;aspect-ratio:1000/640}
.card .meta{padding:16px 18px 18px}
.card .num{font-size:12px;letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:var(--mid)}
.card h2{font-size:clamp(21px,4.6vw,27px);margin:5px 0 4px;font-weight:800;color:var(--deep)}
.card .world{font-size:14px;color:#5d7079;font-weight:600}
.card .go{margin-top:12px;display:inline-block;background:var(--accent);color:#fff;
  font-weight:800;padding:9px 20px;border-radius:999px;font-size:15px}
.lib-foot{max-width:1180px;margin:30px auto 0;color:#a9c6cd;font-size:13px;text-align:center;line-height:1.7}
.lib-foot b{color:var(--light)}

/* ============ reader ============ */
#reader{position:absolute;inset:0;display:flex;flex-direction:column;
  background:var(--sand);overflow:hidden;max-width:100%}
#stage{position:relative;flex:1 1 auto;min-height:0;min-width:0;display:flex;flex-direction:column}
.pg{position:absolute;inset:0;display:flex;flex-direction:column;opacity:0;
  pointer-events:none;transition:opacity .22s ease}
.pg.on{opacity:1;pointer-events:auto}

/* art */
.art{position:relative;flex:1 1 auto;min-height:0;background:var(--deep)}
.art svg{position:absolute;inset:0;width:100%;height:100%;display:block}
/* always show the whole scene; letterbox against the page's own deep colour */
.art{display:flex;align-items:center;justify-content:center}
.art svg{object-fit:contain}

/* story */
.copy{flex:0 0 auto;background:var(--paper);padding:14px 18px 12px;text-align:center;
  font-weight:800;font-size:var(--story);line-height:1.28;color:var(--deep)}
.copy .sp{display:block;height:.42em}
.copy .log{display:block;margin:10px auto 2px;max-width:34ch;padding:10px 16px;
  border:3px solid var(--accent);border-radius:14px;font-size:.62em;font-weight:700;color:var(--mid)}

/* teacher band */
.band{flex:0 0 auto;background:var(--deep);color:#dff3f6;
  padding:10px 18px calc(10px + var(--safe-b));font-size:clamp(13px,2.5vh,17px)}
.band .p{font-weight:800}.band .p b{color:var(--accent);letter-spacing:.08em}
.band .g{font-size:.8em;opacity:.78;margin-top:3px;line-height:1.4}
body.no-notes .band .g{display:none}

/* title + theme + note pages */
.full{flex:1 1 auto;min-height:0;position:relative;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;padding:22px;color:#fff;overflow:hidden}
.full .bg{position:absolute;inset:0}
.full .bg{overflow:hidden}
.full .bg svg{width:100%;height:100%;display:block;object-fit:cover}
.full .in{position:relative;z-index:1;max-width:34ch}
.full .sup{font-size:clamp(11px,2.4vw,15px);letter-spacing:.32em;text-transform:uppercase;
  font-weight:800;color:var(--light)}
.full h1{font-size:clamp(34px,8.4vw,72px);font-weight:800;margin:8px 0;line-height:1.04;
  text-shadow:0 3px 18px rgba(0,0,0,.5)}
.full .pilots{font-size:clamp(14px,3.4vw,20px);color:#eaf6f7;font-weight:700}
.full .scrim{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(8,26,34,.78) 0%,rgba(8,26,34,.30) 42%,
                          rgba(8,26,34,.34) 58%,rgba(8,26,34,.80) 100%)}
.full.cover{justify-content:flex-end;padding-bottom:9vh}
.full.cover .scrim{background:linear-gradient(180deg,rgba(8,26,34,.34) 0%,
  rgba(8,26,34,.18) 32%,rgba(8,26,34,.70) 60%,rgba(8,26,34,.93) 100%)}
.note{background:var(--paper);color:var(--deep);text-align:left;justify-content:flex-start;
  overflow-y:auto;-webkit-overflow-scrolling:touch;padding:26px 22px}
.note .kick{font-size:12px;letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:var(--mid)}
.note h2{font-size:clamp(28px,7vw,44px);margin:8px 0 14px;font-weight:800}
.note .rule{width:84px;height:5px;background:var(--accent);border-radius:3px;margin-bottom:18px}
.note p{font-size:clamp(15px,3.6vw,20px);line-height:1.6;margin-bottom:14px;max-width:56ch}

/* the 4-beat clap */
.beats{display:flex;gap:2.2vw;justify-content:center;margin:14px 0;width:100%;max-width:640px}
.beat{flex:1 1 0;background:rgba(255,255,255,.10);border:3px solid var(--mid);border-radius:16px;
  padding:12px 4px;transition:transform .1s ease,background .1s ease}
.beat.hit{background:var(--accent);transform:scale(1.13) translateY(-5px)}
.beat .n{font-size:clamp(17px,4vw,28px);font-weight:800;color:var(--accent)}
.beat.hit .n{color:#fff}
.beat .w{font-size:clamp(13px,3.2vw,21px);font-weight:800;margin:3px 0 1px;color:#fff}
.beat .d{font-size:clamp(9px,2.2vw,13px);color:var(--light);line-height:1.2}
.beat.hit .d{color:#fff}
.motto{margin-top:14px;font-style:italic;font-weight:700;color:var(--accent);
  font-size:clamp(12px,2.8vw,16px)}

/* breathing guide */
.breath{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:min(46vh,46vw);aspect-ratio:1;border-radius:50%;pointer-events:none;
  display:flex;align-items:center;justify-content:center;z-index:2;opacity:0;transition:opacity .3s}
.breath.on{opacity:1}
.breath i{position:absolute;inset:0;border-radius:50%;border:6px solid var(--accent);
  background:rgba(255,255,255,.16);animation:bre 10s ease-in-out infinite}
.breath span{position:relative;font-weight:800;color:#fff;font-size:clamp(15px,3.6vw,24px);
  text-shadow:0 2px 12px rgba(0,0,0,.7);animation:bretxt 10s steps(1) infinite}
@keyframes bre{0%{transform:scale(.42)}40%{transform:scale(1)}45%{transform:scale(1)}100%{transform:scale(.42)}}
@keyframes bretxt{0%{content:""}}

/* ============ controls ============ */
.tap{position:absolute;top:0;bottom:0;width:26%;z-index:3;background:transparent}
.tap.l{left:0}.tap.r{right:0}
#bar{position:relative;flex:0 0 auto;display:flex;align-items:center;gap:4px;
  background:var(--deep);border-top:2px solid rgba(255,255,255,.14);
  padding:7px 8px calc(7px + var(--safe-b));z-index:5;
  width:100%;min-width:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none}
#bar::-webkit-scrollbar{display:none}
#bar>*{flex:0 0 auto}
.btn{color:#dff3f6;border-radius:12px;padding:9px 9px;font-size:13px;font-weight:800;
  display:flex;align-items:center;gap:6px;min-height:44px;min-width:44px;justify-content:center}
.btn:active{background:rgba(255,255,255,.16)}
.btn.on{background:var(--accent);color:#fff}
.btn svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:2.4;
  stroke-linecap:round;stroke-linejoin:round}
.btn .lbl{display:none}
@media(min-width:640px){.btn .lbl{display:inline}}
#bar .sp{flex:1 1 auto;min-width:0}
@media(max-width:420px){
  #bar{gap:2px;padding-left:4px;padding-right:4px}
  .btn{padding:9px 7px;min-width:40px}
  #tSlow,#tFast{font-size:12px;padding:9px 6px}
  #pgno{font-size:11px;padding:0 2px}
}
#pgno{color:#9fc4cc;font-size:12px;font-weight:800;padding:0 6px;white-space:nowrap}
#prog{position:absolute;left:0;right:0;top:-2px;height:3px;background:rgba(255,255,255,.14)}
#prog i{display:block;height:100%;background:var(--accent);transition:width .22s ease}

/* landscape on a laptop: art beside the words */
@media(min-aspect-ratio:7/5) and (min-width:900px){
  .pg.story-page{flex-direction:row}
  .pg.story-page .art{flex:1 1 58%}
  .pg.story-page .txt{flex:1 1 42%;display:flex;flex-direction:column;justify-content:center;
    background:var(--paper);max-width:560px}
  .pg.story-page .copy{padding:24px 30px;flex:1 1 auto;display:flex;
    flex-direction:column;justify-content:center}
  .pg.story-page .band{margin-top:auto}
}
.txt{display:contents}
@media(min-aspect-ratio:7/5) and (min-width:900px){.txt{display:flex;flex-direction:column}}

@media(prefers-reduced-motion:reduce){
  *{animation-duration:.001ms!important;transition-duration:.001ms!important}
}
"""
