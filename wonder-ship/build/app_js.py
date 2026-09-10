# -*- coding: utf-8 -*-
"""Reader behaviour for the offline app. No libraries, no network."""

JS = r"""
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)};
var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};

var state={book:null,page:0,notes:true,speaking:false};
var LS='wondership.v1';
function save(){try{localStorage.setItem(LS,JSON.stringify({b:state.book,p:state.page,n:state.notes}))}catch(e){}}
function load(){try{return JSON.parse(localStorage.getItem(LS))||{}}catch(e){return{}}}

/* ---------------- audio: a click generated on the fly, no files ------- */
var actx=null;
function tone(freq,dur,vol){
  try{
    if(!actx){var AC=window.AudioContext||window.webkitAudioContext; if(!AC)return; actx=new AC();}
    if(actx.state==='suspended')actx.resume();
    var o=actx.createOscillator(),g=actx.createGain();
    o.type='sine'; o.frequency.value=freq;
    g.gain.setValueAtTime(0.0001,actx.currentTime);
    g.gain.exponentialRampToValueAtTime(vol||0.3,actx.currentTime+0.012);
    g.gain.exponentialRampToValueAtTime(0.0001,actx.currentTime+(dur||0.16));
    o.connect(g); g.connect(actx.destination);
    o.start(); o.stop(actx.currentTime+(dur||0.16)+0.02);
  }catch(e){}
}
function clapSound(i){ tone(i===3?280:(i===2?420:660), i===3?0.34:0.13, 0.28); }

/* ---------------- read aloud ------------------------------------------ */
var synth=window.speechSynthesis||null;
function speak(txt){
  if(!synth){flash('Read-aloud is not available on this device');return}
  synth.cancel();
  if(!txt){return}
  var u=new SpeechSynthesisUtterance(txt);
  u.rate=0.82; u.pitch=1.12;
  u.onend=function(){state.speaking=false;syncSpeakBtn()};
  u.onerror=function(){state.speaking=false;syncSpeakBtn()};
  state.speaking=true; syncSpeakBtn();
  synth.speak(u);
}
function stopSpeak(){ if(synth)synth.cancel(); state.speaking=false; syncSpeakBtn(); }
function syncSpeakBtn(){ var b=$('#bRead'); if(b)b.classList.toggle('on',state.speaking); }

function flash(msg){
  var t=$('#toast'); t.textContent=msg; t.style.opacity='1';
  clearTimeout(flash.t); flash.t=setTimeout(function(){t.style.opacity='0'},2400);
}

/* ---------------- navigation ------------------------------------------ */
function writeHash(){
  var h = state.book===null ? '' : ('#b'+state.book+'p'+(state.page+1));
  if(location.hash!==h){ try{history.replaceState(null,'',h||location.pathname)}catch(e){} }
}
function readHash(){
  var m=/^#b(\d+)p(\d+)$/.exec(location.hash||'');
  if(!m)return null;
  var b=+m[1], p=+m[2]-1;
  if(b<1||b>50||p<0||p>23)return null;
  return {b:b,p:p};
}
var LOADED={};
window.__ws_book=function(week,html){
  LOADED[week]=true;
  var host=document.getElementById('stage');
  var d=document.createElement('div');
  d.className='bookwrap hide'; d.setAttribute('data-week',week);
  d.innerHTML=html; host.appendChild(d);
  if(pendingOpen&&pendingOpen.w===week){var p=pendingOpen;pendingOpen=null;openBook(p.w,p.p)}
};
var pendingOpen=null;
function wrapFor(week){ return document.querySelector('.bookwrap[data-week="'+week+'"]') }

function openBook(week,page){
  var w=wrapFor(week);
  if(!w){
    if(LOADED[week]===undefined){
      LOADED[week]=null; pendingOpen={w:week,p:page||0};
      $('#library').classList.add('hide'); $('#reader').classList.remove('hide');
      $('#pgno').textContent='loading…';
      var sc=document.createElement('script');
      sc.src='books/'+String(week).padStart(2,'0')+'.js';
      sc.onerror=function(){
        pendingOpen=null; LOADED[week]=undefined;
        closeBook(); flash('That book is not on this device yet');
      };
      document.head.appendChild(sc);
    }else{ pendingOpen={w:week,p:page||0} }
    return;
  }
  state.book=week; state.page=page||0;
  $('#library').classList.add('hide');
  $('#reader').classList.remove('hide');
  $$('.bookwrap').forEach(function(el){el.classList.toggle('hide',el!==w)});
  render(); save(); writeHash();
}
function closeBook(){
  stopSpeak(); stopClap();
  $('#reader').classList.add('hide');
  $('#library').classList.remove('hide');
  state.book=null; save(); writeHash();
}
function go(d){
  var pages=$$('.pg',wrapFor(state.book));
  var n=state.page+d;
  if(n<0){return}
  if(n>=pages.length){flash('That is the end. Fly again any time.');return}
  state.page=n; stopSpeak(); stopClap(); render(); save(); writeHash();
}
function render(){
  var wrap=wrapFor(state.book);
  if(!wrap){return}
  var pages=$$('.pg',wrap);
  pages.forEach(function(p,k){p.classList.toggle('on',k===state.page)});
  var cur=pages[state.page];
  $('#pgno').textContent=(state.page+1)+' / '+pages.length;
  $('#prog i').style.width=(((state.page+1)/pages.length)*100)+'%';
  var br=$('.breath',cur); $$('.breath').forEach(function(b){b.classList.remove('on')});
  if(br)br.classList.add('on');
  $('#bClap').classList.toggle('hide', !cur.hasAttribute('data-clap'));
  var t=cur.getAttribute('data-speech')||'';
  $('#bRead').classList.toggle('hide', !t);
}

/* ---------------- the Wonder Ship Clap -------------------------------- */
var clapTimer=null, clapBeat=0, clapMs=900;
function startClap(){
  var cur=$$('.pg',wrapFor(state.book))[state.page];
  var beats=$$('.beat',cur);
  if(!beats.length){ beats=$$('.beat',$('#clapbar')); $('#clapbar').classList.remove('hide'); }
  stopClap(true);
  clapBeat=0; $('#bClap').classList.add('on');
  var tick=function(){
    beats.forEach(function(b,k){b.classList.toggle('hit',k===clapBeat)});
    clapSound(clapBeat);
    clapBeat=(clapBeat+1)%4;
  };
  tick(); clapTimer=setInterval(tick,clapMs);
}
function stopClap(quiet){
  if(clapTimer){clearInterval(clapTimer);clapTimer=null}
  $$('.beat').forEach(function(b){b.classList.remove('hit')});
  var c=$('#bClap'); if(c)c.classList.remove('on');
  if(!quiet)$('#clapbar').classList.add('hide');
}
function toggleClap(){ clapTimer?stopClap():startClap(); }
function setTempo(ms){ clapMs=ms; $('#tSlow').classList.toggle('on',ms>=900);
  $('#tFast').classList.toggle('on',ms<900); if(clapTimer)startClap(); }

/* ---------------- input ----------------------------------------------- */
function bind(){
  $$('.card').forEach(function(c){
    c.addEventListener('click',function(){
      if(this.classList.contains('soon')){
        flash('Book '+this.getAttribute('data-week')+' arrives in week '+this.getAttribute('data-week'));
        return;
      }
      openBook(+this.getAttribute('data-week'),0);
    });
  });
  $('#bHome').addEventListener('click',closeBook);
  $('#bNext').addEventListener('click',function(){go(1)});
  $('#bPrev').addEventListener('click',function(){go(-1)});
  $('#bNotes').addEventListener('click',function(){
    state.notes=!state.notes;
    document.body.classList.toggle('no-notes',!state.notes);
    this.classList.toggle('on',state.notes);
    flash(state.notes?'Teacher notes on':'Teacher notes hidden');
    save();
  });
  $('#bRead').addEventListener('click',function(){
    if(state.speaking){stopSpeak();return}
    var cur=$$('.pg',wrapFor(state.book))[state.page];
    speak(cur.getAttribute('data-speech')||'');
  });
  $('#bClap').addEventListener('click',toggleClap);
  $('#tSlow').addEventListener('click',function(){setTempo(1150)});
  $('#tFast').addEventListener('click',function(){setTempo(520)});
  $('#bFull').addEventListener('click',function(){
    var d=document.documentElement;
    if(document.fullscreenElement||document.webkitFullscreenElement){
      (document.exitFullscreen||document.webkitExitFullscreen).call(document);
    }else{
      var f=d.requestFullscreen||d.webkitRequestFullscreen;
      if(f)f.call(d); else flash('Fullscreen is not available here');
    }
  });
  $$('.tap.l').forEach(function(e){e.addEventListener('click',function(){go(-1)})});
  $$('.tap.r').forEach(function(e){e.addEventListener('click',function(){go(1)})});

  document.addEventListener('keydown',function(e){
    if(state.book===null){return}
    if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();go(1)}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(-1)}
    else if(e.key==='Escape'){closeBook()}
    else if(e.key.toLowerCase()==='c'){toggleClap()}
    else if(e.key.toLowerCase()==='r'){$('#bRead').click()}
  });

  /* swipe */
  var x0=null,y0=null,t0=0;
  var st=$('#reader');
  st.addEventListener('touchstart',function(e){
    var t=e.changedTouches[0]; x0=t.clientX; y0=t.clientY; t0=Date.now();
  },{passive:true});
  st.addEventListener('touchend',function(e){
    if(x0===null)return;
    var t=e.changedTouches[0], dx=t.clientX-x0, dy=t.clientY-y0;
    if(Date.now()-t0<700 && Math.abs(dx)>52 && Math.abs(dx)>Math.abs(dy)*1.6){ go(dx<0?1:-1) }
    x0=null;
  },{passive:true});

  /* first gesture unlocks audio on iOS */
  document.addEventListener('pointerdown',function once(){
    try{if(!actx){var AC=window.AudioContext||window.webkitAudioContext;if(AC)actx=new AC()}
        if(actx&&actx.state==='suspended')actx.resume()}catch(e){}
    document.removeEventListener('pointerdown',once);
  });
}

/* ---------------- boot ------------------------------------------------- */
function boot(){
  bind();
  var s=load();
  if(s.n===false){state.notes=false;document.body.classList.add('no-notes')}
  $('#bNotes').classList.toggle('on',state.notes);
  var h=readHash();
  if(h){ openBook(h.b,h.p); }
  else if(typeof s.b==='number'&&s.b>=0&&s.b<3){
    openBook(s.b,s.p||0);
    if(s.p)flash('Picked up where you left off');
  }
  window.addEventListener('hashchange',function(){
    var g=readHash();
    if(g&&(g.b!==state.book||g.p!==state.page))openBook(g.b,g.p);
  });
  if('serviceWorker' in navigator && location.protocol.indexOf('http')===0){
    navigator.serviceWorker.register('sw.js').catch(function(){});
  }
}
if(document.readyState!=='loading')boot(); else document.addEventListener('DOMContentLoaded',boot);
})();
"""
