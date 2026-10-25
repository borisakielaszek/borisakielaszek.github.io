(() => {
  'use strict';
  let opened = false, context, thunderBuffer;
  const base = '/jeu-vampires-de-sarrebruck/de/';
  const removeSelectors = () => document.querySelectorAll('.game-language-switch,.language-switch').forEach(el => el.remove());
  function audioContext() {
    const Audio = window.AudioContext || window.webkitAudioContext;
    if (!context && Audio) context = new Audio();
    return context;
  }
  function thunder() {
    try {
      const ctx = audioContext(); if (!ctx) return;
      ctx.resume().catch(() => {});
      const source = ctx.createBufferSource();
      if (thunderBuffer) source.buffer = thunderBuffer;
      else {
        // Immediate local fallback while the supplied thunder is still loading.
        const buffer = ctx.createBuffer(1, ctx.sampleRate * 1.4, ctx.sampleRate);
        const data = buffer.getChannelData(0); let rumble = 0;
        for (let i = 0; i < data.length; i++) {
          const noise = Math.random() * 2 - 1;
          rumble = rumble * .94 + noise * .06;
          data[i] = (rumble * 3 + noise * .22) * Math.exp(-5 * i / data.length);
        }
        source.buffer = buffer;
      }
      const gain = ctx.createGain(); gain.gain.value = .85;
      source.connect(gain); gain.connect(ctx.destination); source.start();
    } catch (_) {}
  }
  function enter(event) {
    const intro = document.getElementById('introScreen');
    if (!intro || intro.classList.contains('hidden') || !intro.contains(event.target)) return;
    event.preventDefault(); event.stopImmediatePropagation(); event.stopPropagation();
    if (opened) return; opened = true;
    const button = document.getElementById('enterNightBtn');
    if (button) { button.dataset.entered = '1'; button.classList.add('pressed'); }
    thunder();
    // Reuse the exact six-strike animation and CSS shared with FR/EN.
    if (typeof window.choiceStormBurst === 'function') window.choiceStormBurst();
    const music = document.getElementById('bgMusic');
    if (music) { music.loop = true; music.volume = 0; music.play()?.catch(() => {}); }
    setTimeout(() => {
      intro.classList.add('hidden');
      document.getElementById('startScreen')?.classList.remove('hidden');
      window.scrollTo(0,0);
      try { musicEnabled = true; musicStarted = true; } catch (_) {}
      const music = document.getElementById('bgMusic');
      if (music) { music.loop = true; music.volume = .22; music.play()?.catch(() => {}); }
      try { refreshMusicButton(); } catch (_) {}
      setTimeout(() => { try { offerFirstNightGuide(); } catch (_) {} },120);
    },6500);
  }
  function init() {
    removeSelectors();
    const button = document.getElementById('enterNightBtn');
    if (button) { button.disabled = false; button.removeAttribute('disabled'); button.setAttribute('aria-label','Betritt die Nacht'); }
    for (const name of ['user-lightning-1.svg','user-lightning-2.svg']) { const img = new Image(); img.src = '/jeu-vampires-de-sarrebruck/assets/' + name; }
    try {
      const ctx = audioContext();
      const sound = document.getElementById('introHissSfx');
      if (ctx && sound) fetch(sound.src).then(r => r.arrayBuffer()).then(b => ctx.decodeAudioData(b)).then(b => { thunderBuffer = b; }).catch(() => {});
    } catch (_) {}
    document.addEventListener('pointerup',enter,true);
    document.addEventListener('click',enter,true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',init,{once:true}); else init();
  const script = document.createElement('script');
  script.src = base + 'translations-data.js?v=20261025-de-audit-2';
  document.head.appendChild(script);
})();
