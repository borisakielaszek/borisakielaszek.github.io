(() => {
  'use strict';
  let opened = false;
  function enter(event) {
    const intro = document.getElementById('introScreen');
    if (!intro || intro.classList.contains('hidden') || !intro.contains(event.target)) return;
    event.preventDefault(); event.stopImmediatePropagation(); event.stopPropagation();
    if (opened) return;
    opened = true;
    enterOriginalNight(event);
  }
function enterOriginalNight(e){
 if(e&&e.preventDefault)e.preventDefault();
 const intro=el('introScreen'), menu=el('startScreen'), a=el('bgMusic'), hiss=el('introHissSfx'), btn=el('enterNightBtn');
 if(btn?.dataset.entered==='1')return;
 if(btn){btn.dataset.entered='1';btn.disabled=true;btn.classList.add('pressed');}
 haptic(30);
 musicEnabled=true;musicStarted=true;
 // V5.72 : tonnerre utilisateur coupé juste avant l’impact.
 // Les éclairs blancs restent sur la première page pendant l’effet.
 let stormStarted=false;
 const startIntroStorm=()=>{if(stormStarted)return;stormStarted=true;choiceStormBurst();};
 if(hiss)hiss.addEventListener('playing',startIntroStorm,{once:true});
 setTimeout(startIntroStorm,700);
 if(hiss){try{hiss.pause();hiss.currentTime=0;hiss.volume=1;const hp=hiss.play();if(hp&&hp.catch)hp.catch(startIntroStorm);}catch(_){}}
 // On amorce la musique du menu à volume nul dans le geste utilisateur pour préserver l'autoplay Android.
 if(a){try{a.loop=true;a.currentTime=0;a.volume=0;const mp=a.play();if(mp&&mp.catch)mp.catch(()=>{});}catch(_){} }
 let transitioned=false;
 const finishIntro=()=>{
   if(transitioned)return;transitioned=true;
   const flash=el('stormFlash');if(flash){flash.classList.remove('flash','choice-storm');[...flash.querySelectorAll('.storm-bolt,.intro-user-lightning')].forEach(n=>n.remove());}
   if(intro)intro.classList.add('hidden');
   if(menu)menu.classList.remove('hidden');
   window.scrollTo(0,0);
   if(a&&musicEnabled){try{a.currentTime=0;a.volume=.22;const pr=a.play();if(pr&&pr.catch)pr.catch(()=>{});}catch(_){} }
   refreshMusicButton();
   offerFirstNightGuide();
 };
 if(hiss){try{hiss.addEventListener('ended',finishIntro,{once:true});}catch(_){} }
 // Sécurité : le fichier monté dure environ 6,4 s ; l’événement ended reste prioritaire.
 setTimeout(finishIntro,7200);
}

  function init() {
    document.querySelectorAll('.game-language-switch,.language-switch').forEach(el => el.remove());
    const button = document.getElementById('enterNightBtn');
    if (button) { button.disabled = false; button.removeAttribute('disabled'); button.setAttribute('aria-label','Betritt die Nacht'); }
    for (const name of ['user-lightning-1.svg','user-lightning-2.svg']) { const img = new Image(); img.src = '/jeu-vampires-de-sarrebruck/assets/' + name; }
    document.addEventListener('pointerup',enter,true);
    document.addEventListener('click',enter,true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',init,{once:true}); else init();
  const script = document.createElement('script');
  script.src = '/jeu-vampires-de-sarrebruck/de/translations-data.js?v=20261025-de-result3';
  document.head.appendChild(script);
})();
