(() => {
  'use strict';

  let opened=false;

  function removeLanguageControls(){
    document.querySelectorAll('.game-language-switch,.language-switch').forEach(el=>el.remove());
  }

  function enter(event){
    const target=event?.target?.closest?.('#enterNightBtn,.de-intro-brand');
    if(!target || opened) return;
    if(event?.cancelable) event.preventDefault();
    event?.stopImmediatePropagation?.();
    event?.stopPropagation?.();
    opened=true;

    const intro=document.getElementById('introScreen');
    const menu=document.getElementById('startScreen');
    const btn=document.getElementById('enterNightBtn');
    const hiss=document.getElementById('introHissSfx');
    const music=document.getElementById('bgMusic');

    if(btn){btn.disabled=false;btn.removeAttribute('disabled');btn.dataset.entered='1';}
    try{if(typeof window.choiceStormBurst==='function')window.choiceStormBurst(true);}catch(_){}
    if(hiss){try{hiss.currentTime=0;hiss.volume=.9;const soundPromise=hiss.play();if(soundPromise?.catch)soundPromise.catch(()=>{});}catch(_){}}
    intro?.classList.add('hidden');
    menu?.classList.remove('hidden');
    window.scrollTo(0,0);

    if(music){try{music.loop=true;music.volume=.22;const p=music.play();if(p?.catch)p.catch(()=>{});}catch(_){}}
    try{if(typeof refreshMusicButton==='function')refreshMusicButton();}catch(_){}
    setTimeout(()=>{try{if(typeof offerFirstNightGuide==='function')offerFirstNightGuide();}catch(_){}},120);
  }

  function init(){
    removeLanguageControls();
    const btn=document.getElementById('enterNightBtn');
    if(btn){btn.disabled=false;btn.removeAttribute('disabled');btn.setAttribute('aria-label','In die Nacht');}
    document.addEventListener('pointerup',enter,true);
    document.addEventListener('click',enter,true);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
