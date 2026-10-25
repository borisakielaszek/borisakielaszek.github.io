(() => {
  'use strict';

  function installFastGermanStart(){
    const bind=()=>{
      const btn=document.getElementById('enterNightBtn');
      const hiss=document.getElementById('introHissSfx');
      if(!btn || btn.dataset.deFastStartBound==='1') return;
      btn.dataset.deFastStartBound='1';
      let timer=null;

      const forceIntoNight=()=>{
        if(timer!==null) return;
        timer=window.setTimeout(()=>{
          const intro=document.getElementById('introScreen');
          const menu=document.getElementById('startScreen');
          if(!intro || intro.classList.contains('hidden')) return;

          // The normal German intro listens for the thunder sound's "ended"
          // event. Some Android browsers do not reliably emit it, so trigger
          // the same normal completion path after 2.5 seconds.
          if(hiss){
            try{hiss.dispatchEvent(new Event('ended'));}catch(_){}
          }

          // Last-resort visual fallback if the original listener was not bound.
          window.setTimeout(()=>{
            if(!intro.classList.contains('hidden')){
              intro.classList.add('hidden');
              if(menu) menu.classList.remove('hidden');
              window.scrollTo(0,0);
            }
          },60);
        },2500);
      };

      btn.addEventListener('pointerup',forceIntoNight,{passive:true});
      btn.addEventListener('click',forceIntoNight);
    };

    if(document.readyState==='loading'){
      document.addEventListener('DOMContentLoaded',bind,{once:true});
    }else{
      bind();
    }
  }

  // Preserve the complete German translation layer unchanged; it is copied
  // locally from the previous published version so no labels are lost.
  const base=document.createElement('script');
  base.src='/jeu-vampires-de-sarrebruck/de/translations-base.js?v=20261025-de5-base';
  base.async=false;
  base.onload=installFastGermanStart;
  base.onerror=installFastGermanStart;
  document.head.appendChild(base);
})();
