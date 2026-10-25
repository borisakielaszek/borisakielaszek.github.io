(() => {
  'use strict';

  let germanIntroOpened=false;

  function removeGameLanguageSelectors(){
    document.querySelectorAll('.game-language-switch,.language-switch').forEach(el=>el.remove());
  }

  function openGermanSetup(event){
    const introTarget=document.getElementById('introScreen');
    if(!introTarget || (event?.target!==introTarget && !introTarget.contains(event?.target))) return;

    if(event?.cancelable) event.preventDefault();
    event?.stopImmediatePropagation?.();
    event?.stopPropagation?.();

    if(germanIntroOpened) return;
    germanIntroOpened=true;

    const intro=document.getElementById('introScreen');
    const menu=document.getElementById('startScreen');
    const btn=document.getElementById('enterNightBtn');
    const hiss=document.getElementById('introHissSfx');
    const music=document.getElementById('bgMusic');

    if(btn){
      btn.disabled=false;
      btn.dataset.entered='1';
      btn.classList.add('pressed');
    }

    if(hiss){
      try{hiss.pause();hiss.currentTime=0;}catch(_){}
    }

    if(intro) intro.classList.add('hidden');
    if(menu) menu.classList.remove('hidden');
    window.scrollTo(0,0);

    if(music){
      try{
        music.loop=true;
        music.volume=.22;
        const playPromise=music.play();
        if(playPromise?.catch) playPromise.catch(()=>{});
      }catch(_){}
    }

    try{
      if(typeof refreshMusicButton==='function') refreshMusicButton();
    }catch(_){}

    window.setTimeout(()=>{
      try{
        if(typeof offerFirstNightGuide==='function') offerFirstNightGuide();
      }catch(_){}
    },120);
  }

  function installGermanLaunchFix(){
    removeGameLanguageSelectors();
    const btn=document.getElementById('enterNightBtn');
    if(btn){
      btn.disabled=false;
      btn.removeAttribute('disabled');
      btn.setAttribute('aria-label','In die Nacht');
    }
    // Capture phase: this runs before the older intro handlers that wait for
    // the thunder sound. The German launch no longer depends on audio events.
    document.addEventListener('pointerup',openGermanSetup,true);
    document.addEventListener('click',openGermanSetup,true);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',installGermanLaunchFix,{once:true});
  }else{
    installGermanLaunchFix();
  }

  // Keep the complete German translation layer intact and load it with a new
  // cache key so the current corrected version is requested on mobile.
  const base=document.createElement('script');
  base.src='/jeu-vampires-de-sarrebruck/de/translations-base.js?v=20261025-de10';
  base.async=false;
  base.onload=removeGameLanguageSelectors;
  document.head.appendChild(base);
})();
