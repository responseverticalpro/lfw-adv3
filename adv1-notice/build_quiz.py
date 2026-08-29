# -*- coding: utf-8 -*-
"""Injeta o quiz popup (padrao nosso) no advertorial Horse Jello.

v2 - arquitetura do quiz do VigorBoost: modal com brandbar fixa, progresso
segmentado, corpo rolavel e rodape fixo. Tudo quadradao (raio maximo 4px),
final numa tela so, com a copy do doc e a foto dos 3 frascos.
"""
import os
import re

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

BLOCK = r"""
<style id="hjq-style">
.hjq-overlay{
  --hj-red:#E03A2F; --hj-cta:#7ED321; --hj-cta-dark:#6DBB16; --hj-cta-ink:#10300A; --hj-deep:#A63D40;
  --hj-ink:#141414; --hj-body:#4B5261; --hj-label:#7A828F;
  --hj-rule:#E3E6EC; --hj-tint:#FDF1F0; --hj-cream:#F8F1E4; --hj-bg:#F4F5F7;
  position:fixed;inset:0;z-index:2147483000;display:none;
  align-items:center;justify-content:center;padding:24px 16px;
  background:rgba(12,12,14,.72);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);
  font-family:Arial,Helvetica,sans-serif;color:var(--hj-body);-webkit-font-smoothing:antialiased;
}
.hjq-overlay.open{display:flex}
.hjq-overlay *{box-sizing:border-box}
.hjq-overlay button{font-family:inherit}

.hjq-modal{
  position:relative;background:#fff;width:100%;max-width:480px;max-height:92vh;max-height:92dvh;
  border-radius:4px;overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 26px 70px rgba(0,0,0,.45);
  animation:hjqIn .22s cubic-bezier(.2,.7,.3,1) both;
}
@keyframes hjqIn{from{opacity:0;transform:translateY(14px) scale(.99)}to{opacity:1;transform:none}}

/* ---- brandbar (wordmark sobre faixa preta) ---- */
.hjq-brandbar{display:flex;align-items:center;gap:10px;background:#0E0E0E;padding:11px 14px;flex:0 0 auto}
.hjq-brandbar img{height:24px;width:auto;display:block;margin-right:auto}
.hjq-trust{display:flex;flex-direction:column;align-items:flex-end;gap:3px;line-height:1}
.hjq-stars{display:inline-flex;gap:2px}
.hjq-stars i{width:13px;height:13px;background:#00B67A;display:inline-flex;align-items:center;justify-content:center}
.hjq-stars svg{width:10px;height:10px;fill:#fff;display:block}
.hjq-score{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#9AA0AB;white-space:nowrap}
.hjq-close{appearance:none;border:0;background:none;font-size:24px;line-height:1;color:#7C828E;cursor:pointer;padding:0 2px;margin-left:4px}
.hjq-close:hover{color:#fff}

/* ---- voltar + progresso segmentado ---- */
.hjq-nav{display:flex;align-items:center;gap:10px;padding:13px 16px 2px;flex:0 0 auto}
.hjq-back{appearance:none;border:0;background:none;font-size:17px;line-height:1;color:#A9AFBA;cursor:pointer;padding:2px 4px;width:24px;visibility:hidden;transition:color .15s}
.hjq-back:hover{color:var(--hj-ink)}
.hjq-back.on{visibility:visible}
.hjq-steps{display:flex;gap:5px;flex:1}
.hjq-steps i{flex:1;height:5px;background:var(--hj-rule);transition:background .3s ease}
.hjq-steps i.done{background:var(--hj-red)}

/* ---- corpo rolavel ---- */
.hjq-scroll{overflow-y:auto;-webkit-overflow-scrolling:touch;padding:14px 16px 6px;flex:1 1 auto}
.hjq-step{animation:hjqStep .26s ease both}
@keyframes hjqStep{from{opacity:0;transform:translateX(10px)}to{opacity:1;transform:none}}

.hjq-kicker{font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--hj-red);margin:0 0 8px}
.hjq-q{font-size:24px;line-height:1.2;font-weight:800;color:var(--hj-ink);margin:0 0 6px;letter-spacing:-.01em}
.hjq-sub{font-size:13.5px;line-height:1.5;color:var(--hj-label);margin:0 0 2px}

/* ---- opcoes: cartoes quadradoes ---- */
.hjq-opts{display:flex;flex-direction:column;gap:9px;margin:16px 0 4px}
.hjq-opt{
  display:flex;align-items:center;gap:12px;width:100%;text-align:left;
  background:#fff;border:2px solid var(--hj-rule);border-radius:4px;padding:15px 14px;
  cursor:pointer;font:700 15.5px/1.25 inherit;color:var(--hj-ink);
  transition:border-color .15s,background .15s,transform .1s;
}
.hjq-opt:hover{border-color:#F0BDB9}
.hjq-opt:active{transform:scale(.995)}
.hjq-opt.sel{border-color:var(--hj-red);background:var(--hj-tint)}
.hjq-opt .tick{flex:0 0 auto;width:20px;height:20px;border:2px solid #CBD1DA;background:#fff;position:relative;transition:border-color .15s,background .15s}
.hjq-opt.sel .tick{border-color:var(--hj-red);background:var(--hj-red)}
.hjq-opt.sel .tick::after{content:"";position:absolute;left:5px;top:2px;width:5px;height:10px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}
.hjq-opt .txt{flex:1}

/* ---- loader ---- */
.hjq-load{text-align:center;padding:46px 0 38px}
.hjq-spin{width:36px;height:36px;margin:0 auto 20px;border:3px solid var(--hj-rule);border-top-color:var(--hj-red);border-radius:50%;animation:hjqSpin .8s linear infinite}
@keyframes hjqSpin{to{transform:rotate(360deg)}}
.hjq-load p{margin:0 0 5px;font-size:16.5px;font-weight:800;color:var(--hj-ink)}
.hjq-load small{font-size:12.5px;color:var(--hj-label)}

/* ---- tela final: resultado ---- */
.hjq-shot{background:var(--hj-cream);padding:12px 10px;margin:14px 0 0;display:flex;justify-content:center}
.hjq-shot img{width:100%;max-width:330px;height:auto;display:block;mix-blend-mode:multiply}
.hjq-est{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--hj-label);margin:18px 0 5px}
.hjq-est svg{color:var(--hj-red);flex:0 0 auto}
.hjq-est-h{font-size:20px;font-weight:800;color:var(--hj-ink);margin:0 0 8px;line-height:1.22}
.hjq-est-p{font-size:13.5px;line-height:1.5;color:var(--hj-body);margin:0}
.hjq-est-p b{color:var(--hj-ink)}
.hjq-alloc{background:#FFF6EC;border:1px solid #F3D6B4;padding:11px 12px;margin:14px 0 0}
.hjq-alloc-top{display:flex;align-items:center;gap:7px;font-size:12.5px;line-height:1.35;color:#7C2D12}
.hjq-alloc-top b{color:#9A3412;font-weight:800}
.hjq-alloc-bar{height:7px;background:#F6E3CD;margin-top:9px;overflow:hidden}
.hjq-alloc-bar i{display:block;height:100%;background:linear-gradient(90deg,#E8A33D,#D14B12)}
.hjq-ship{display:flex;align-items:center;gap:9px;background:var(--hj-bg);padding:11px 12px;font-size:13px;line-height:1.45;color:var(--hj-body);margin:10px 0 2px}
.hjq-ship svg{flex:0 0 auto;color:var(--hj-label)}
.hjq-ship b{color:var(--hj-ink)}

/* ---- rodape fixo ---- */
.hjq-foot{padding:13px 16px;flex:0 0 auto;background:#fff;border-top:1px solid var(--hj-rule)}
.hjq-next{
  display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:54px;
  border:0;border-radius:4px;cursor:pointer;background:var(--hj-cta);color:var(--hj-cta-ink);
  font:800 17px/1.15 inherit;letter-spacing:.01em;padding:8px 14px;text-align:center;
  transition:background .15s;
}
.hjq-next:hover{background:var(--hj-cta-dark)}
.hjq-next[disabled]{background:#DCEBC6;color:#8A9B77;cursor:default}
.hjq-next .arw{transition:transform .15s}
.hjq-next:not([disabled]):hover .arw{transform:translateX(3px)}

/* No mobile continua sendo pop-up: cartao flutuante centralizado, com o fundo
   escuro aparecendo em cima e embaixo. Nunca ocupa a tela inteira. */
@media(max-width:600px){
  .hjq-overlay{padding:16px 12px}
  .hjq-modal{max-width:none;max-height:88vh;max-height:88dvh}
  .hjq-brandbar{padding:10px 12px}
  .hjq-brandbar img{height:21px}
  .hjq-nav{padding:11px 14px 2px}
  .hjq-scroll{padding:12px 14px 6px}
  .hjq-foot{padding:11px 14px}
  .hjq-q{font-size:20px}
  .hjq-opt{padding:13px 12px;font-size:14.5px}
  .hjq-est-h{font-size:18px}
  .hjq-shot img{max-width:280px}
  .hjq-next{min-height:50px;font-size:15.5px}
}
@media(max-width:600px) and (max-height:660px){
  .hjq-overlay{padding:10px}
  .hjq-modal{max-height:94vh;max-height:94dvh}
  .hjq-load{padding:32px 0 26px}
}
@media(prefers-reduced-motion:reduce){
  .hjq-modal,.hjq-step,.hjq-spin{animation:none}
  .hjq-opt,.hjq-steps i,.hjq-next .arw{transition:none}
}
</style>
<div class="hjq-overlay" id="hjqOverlay" role="dialog" aria-modal="true" aria-label="Horse Jello qualification quiz">
  <div class="hjq-modal">
    <header class="hjq-brandbar">
      <img src="images/horsejello-wordmark.png" alt="Horse Jello" decoding="async">
      <span class="hjq-trust">
        <span class="hjq-stars">
          <i><svg viewBox="0 0 24 24"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z"/></svg></i>
          <i><svg viewBox="0 0 24 24"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z"/></svg></i>
          <i><svg viewBox="0 0 24 24"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z"/></svg></i>
          <i><svg viewBox="0 0 24 24"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z"/></svg></i>
          <i><svg viewBox="0 0 24 24"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z"/></svg></i>
        </span>
        <span class="hjq-score">Excellent 4.8</span>
      </span>
      <button class="hjq-close" id="hjqClose" aria-label="Close">&times;</button>
    </header>
    <div class="hjq-nav"><button class="hjq-back" id="hjqBack" aria-label="Back">&larr;</button><div class="hjq-steps" id="hjqSteps"></div></div>
    <div class="hjq-scroll" id="hjqScroll"><div id="hjqBody"></div></div>
    <footer class="hjq-foot"><button class="hjq-next" id="hjqNext" disabled>Next <span class="arw" aria-hidden="true">&rarr;</span></button></footer>
  </div>
</div>
<script>
(function(){
  'use strict';

  /* Checkout oficial do afiliado */
  var CHECKOUT_URL = 'https://horsejello.com/cc2/pay/checkout.php?package=6b19&hid=b2lkPW9mZl8wNzY2MTI5JmFpZD1hZmZfMDc5MTk4NiZ1aWQ9YmxfOTAwMDQxMw%3D%3D&affid=aff_0791986';

  var PRODUCT_IMG   = 'images/pack-3-horsejello.webp';
  var DELIVERY_DAYS = 2;
  var ALLOCATION    = {units:300, reserved:82};

  /* ------------------------------------------------------------ conteudo */
  var INTRO='These 3 quick questions reveal whether what you’re experiencing matches the pattern the 4-step protocol was designed for — and unlock your bonus + 70% discount.';

  var SCREENS=[
    {phase:0,kicker:'Question 1 of 3',
     q:'What is your age?',
     sub:INTRO,
     o:[{t:'30–39'},{t:'40–49'},{t:'50–59'},{t:'60–69'},{t:'70+'}]},
    {phase:1,kicker:'Question 2 of 3',
     q:'How long has this been going on?',
     o:[{t:'Just the last few weeks'},{t:'A few months now'},{t:'Over a year — and it’s getting worse'}]},
    {phase:2,kicker:'Question 3 of 3',last:true,
     q:'What matters most to you right now?',
     o:[{t:'Performing without needing pills'},{t:'Feeling confident again in the bedroom'},{t:'Keeping my relationship strong'}]}
  ];

  var PHASES=4, LOADER_PHASE=3;
  var LOADERS=[
    ['Reviewing your answers…','Matching your profile against 12,000+ men'],
    ['Checking your profile against the 4-step protocol…','Dissolve · Rebuild · Protect · Reactivate'],
    ['Unlocking your bonus + 70% discount…','Reserving your allocation for the next few minutes']
  ];

  /* -------------------------------------------------------------- estado */
  var ov      = document.getElementById('hjqOverlay'),
      body    = document.getElementById('hjqBody'),
      steps   = document.getElementById('hjqSteps'),
      backBtn = document.getElementById('hjqBack'),
      nextBtn = document.getElementById('hjqNext'),
      scroll  = document.getElementById('hjqScroll'),
      answers = [], step = 0, DONE = SCREENS.length;

  /* ------------------------------------------------------------- helpers */
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}

  function setPhase(){
    var ph = step >= DONE ? LOADER_PHASE : SCREENS[step].phase;
    var kids = steps.children;
    for (var i=0;i<kids.length;i++) kids[i].className = (i<=ph) ? 'done' : '';
  }
  function setNext(label,enabled,handler){
    nextBtn.innerHTML = label + ' <span class="arw" aria-hidden="true">&rarr;</span>';
    nextBtn.disabled = !enabled;
    nextBtn.onclick = handler;
  }
  function paint(html){
    body.innerHTML = '<div class="hjq-step">'+html+'</div>';
    if (scroll) scroll.scrollTop = 0;
    backBtn.classList.toggle('on', step>0 && step<DONE);
    setPhase();
  }
  function withParams(u){
    try{
      var params = new URLSearchParams(location.search);
      ['package','hid','affid'].forEach(function(key){params.delete(key);});
      var qs = params.toString();
      if(!qs) return u;
      return u + (u.indexOf('?')>-1?'&':'?') + qs;
    }catch(e){return u;}
  }
  function fmt(d,weekday){
    var M=['January','February','March','April','May','June','July','August','September','October','November','December'];
    var W=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    return (weekday ? W[d.getDay()]+', ' : '') + M[d.getMonth()]+' '+d.getDate();
  }
  function plusDays(n,skipSunday){
    var d=new Date(); d.setDate(d.getDate()+n);
    if(skipSunday && d.getDay()===0) d.setDate(d.getDate()+1);
    return d;
  }

  /* ---------------------------------------------------------- navegacao */
  function go(n){step=n;render();}
  function back(){if(step>0&&step<DONE)go(step-1);}
  function advance(){ if(step+1<DONE) go(step+1); else renderLoader(); }

  /* ----------------------------------------------------------- perguntas */
  function renderQuestion(S){
    var html='';
    if(S.kicker) html+='<p class="hjq-kicker">'+esc(S.kicker)+'</p>';
    html+='<h2 class="hjq-q">'+esc(S.q)+'</h2>';
    if(S.sub) html+='<p class="hjq-sub">'+esc(S.sub)+'</p>';
    var chosen=answers[step];
    html+='<div class="hjq-opts">';
    S.o.forEach(function(o,i){
      html+='<button type="button" class="hjq-opt'+(chosen===i?' sel':'')+'"'
          + (S.last?' id="ViewContent"':'')+' data-i="'+i+'">'
          + '<span class="tick"></span><span class="txt">'+esc(o.t)+'</span></button>';
    });
    html+='</div>';
    paint(html);

    var btns=body.querySelectorAll('.hjq-opt');
    Array.prototype.forEach.call(btns,function(b){
      b.addEventListener('click',function(){
        answers[step]=+b.getAttribute('data-i');
        Array.prototype.forEach.call(btns,function(x){x.classList.remove('sel');});
        b.classList.add('sel');
        nextBtn.disabled=false;
        setTimeout(advance,260);
      });
    });
    setNext('Next', chosen!=null, advance);
  }

  /* -------------------------------------------------------------- loader */
  function renderLoader(i){
    i=i||0; step=DONE;
    backBtn.classList.remove('on');
    paint('<div class="hjq-load"><div class="hjq-spin"></div><p>'+LOADERS[i][0]+'</p><small>'+LOADERS[i][1]+'</small></div>');
    setNext('Next',false,null);
    var wait = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 300 : 1250;
    setTimeout(function(){ i+1<LOADERS.length ? renderLoader(i+1) : renderResult(); },wait);
  }

  /* --- tela final: resultado (copy do doc) ------------------------------- */
  function renderResult(){
    step=DONE+1;
    try{ if(window.fbq) fbq('track','Lead'); }catch(e){}
    var ship=plusDays(DELIVERY_DAYS,true);
    paint(
      '<h2 class="hjq-q">You’re a perfect match for Horse Jello!</h2>'
      + '<p class="hjq-est">'
        + '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 7-7"/><path d="M20 8V4h-4"/></svg>'
        + 'Your estimated results</p>'
      + '<h3 class="hjq-est-h">Firm Erections Back in 4 to 8 Weeks</h3>'
      + '<p class="hjq-est-p">That’s just the first two months. Men with your profile and commitment to the full Horse Jello® protocol reported firm erections that last <b>from start to finish</b> — and kept them without planning around a pill.</p>'
      + '<div class="hjq-shot"><img src="'+PRODUCT_IMG+'" alt="Horse Jello® — 3-bottle supply" decoding="async"></div>'
      + '<div class="hjq-alloc"><div class="hjq-alloc-top">'
        + '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 9v5M12 17.5v.01"/><path d="M10.3 3.9 2.4 17.4A2 2 0 0 0 4.1 20.4h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>'
        + '<span><b>'+ALLOCATION.reserved+'%</b> of this allocation of '+ALLOCATION.units+' units already reserved</span>'
        + '</div><div class="hjq-alloc-bar"><i style="width:'+ALLOCATION.reserved+'%"></i></div></div>'
      + '<p class="hjq-ship">'
        + '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>'
        + '<span>Order now and it arrives by <b>'+fmt(ship,true)+'</b> — in a discreet, unmarked box</span></p>'
    );
    backBtn.classList.remove('on');
    setNext('Unlock My 3 Free Bottles Now',true,function(){goCheckout(CHECKOUT_URL);});
  }

  /* ------------------------------------------------------------- checkout */
  function goCheckout(url){
    try{ if(window.fbq) fbq('track','InitiateCheckout'); }catch(e){}
    try{ if(window.utmify && window.utmify.track) window.utmify.track('InitiateCheckout'); }catch(e){}
    window.location.href=withParams(url);
  }

  /* -------------------------------------------------------------- router */
  function render(){
    var S=SCREENS[step];
    if(!S) return renderLoader();
    renderQuestion(S);
  }

  /* -------------------------------------------------------- abrir/fechar */
  function openQuiz(){
    answers=[]; step=0;
    steps.innerHTML=new Array(PHASES+1).join('<i></i>');
    ov.classList.add('open');
    document.body.style.overflow='hidden';
    render();
    try{ if(window.fbq) fbq('trackCustom','QuizStart'); }catch(e){}
  }
  function closeQuiz(){
    ov.classList.remove('open');
    document.body.style.overflow='';
  }

  /* abre quiz ao clicar em qualquer CTA do artigo */
  document.addEventListener('click',function(e){
    var a=e.target.closest?e.target.closest('a[href*="final-cta"], a.product-card-cta'):null;
    if(a && !a.closest('.hjq-overlay')){
      e.preventDefault();e.stopPropagation();openQuiz();
    }
  },true);
  document.getElementById('hjqClose').onclick=closeQuiz;
  backBtn.addEventListener('click',back);
  ov.addEventListener('click',function(e){if(e.target===ov)closeQuiz();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&ov.classList.contains('open'))closeQuiz();});
})();
</script>
"""

s = open(PATH, encoding='utf-8').read()
# remove injecao anterior se existir
s = re.sub(r'<style id="hjq-style">.*?</script>\n?', '', s, flags=re.S)
assert '</body>' in s
s = s.replace('</body>', BLOCK + '\n</body>', 1)
open(PATH, 'w', encoding='utf-8').write(s)
print('ok', len(s))
