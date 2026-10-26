(() => {
  'use strict';

  const REV = '20261026-en-fix-1';
  let started = false;

  function loadBaseTranslations() {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = './translations-base.js?v=' + REV;
      script.async = false;
      script.onload = resolve;
      script.onerror = reject;
      (document.head || document.documentElement).appendChild(script);
    });
  }

  function replaceFrenchText(root) {
    if (!root) return;
    const replacements = new Map([
      ['Rester ici', 'Stay here']
    ]);

    const replaceNode = (node) => {
      const raw = node.nodeValue;
      if (!raw) return;
      const trimmed = raw.trim();
      const replacement = replacements.get(trimmed);
      if (!replacement) return;
      node.nodeValue = raw.replace(trimmed, replacement);
    };

    if (root.nodeType === Node.TEXT_NODE) {
      replaceNode(root);
      return;
    }

    if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_FRAGMENT_NODE && root !== document.body) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) replaceNode(node);
  }

  function ensureCombatStyle() {
    if (document.getElementById('english-combat-art-fix')) return;
    const style = document.createElement('style');
    style.id = 'english-combat-art-fix';
    style.textContent = `
      .combat-visual-localized{position:relative;width:100%;margin:0 auto 18px;overflow:hidden;border-radius:18px;background:#090b0d}
      .combat-visual-localized .combat-visual-scene{width:100%;aspect-ratio:1.72;overflow:hidden;background:#090b0d}
      .combat-visual-localized img,
      .combat-result-card .combat-visual-localized img.combat-art{width:100%!important;height:100%!important;display:block;object-fit:cover!important;object-position:50% 51%!important;max-height:none!important;margin:0!important;border-radius:0!important}
      .combat-visual-localized .combat-visual-heading{position:absolute;inset:10px 14px auto;text-align:center;z-index:2;font-family:Georgia,'Times New Roman',serif;font-size:clamp(28px,8vw,54px);font-weight:900;line-height:1;color:#fff;text-shadow:0 3px 8px #000,0 0 16px #000;pointer-events:none}
    `;
    document.head.appendChild(style);
  }

  function localizeCombatArt(root) {
    if (!root || (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_FRAGMENT_NODE && root !== document.body)) return;
    const images = root.matches && root.matches('.combat-result-card > img.combat-art')
      ? [root]
      : Array.from(root.querySelectorAll ? root.querySelectorAll('.combat-result-card > img.combat-art') : []);

    images.forEach((img) => {
      if (img.closest('.combat-visual-localized')) return;
      const isFailed = img.classList.contains('failure');
      const frame = document.createElement('div');
      frame.className = 'combat-visual-localized ' + (isFailed ? 'failure' : 'success');
      const scene = document.createElement('div');
      scene.className = 'combat-visual-scene';
      const heading = document.createElement('div');
      heading.className = 'combat-visual-heading';
      heading.textContent = isFailed ? 'Attack failed!' : 'Attack successful!';
      img.parentNode.insertBefore(frame, img);
      scene.appendChild(img);
      frame.appendChild(scene);
      frame.appendChild(heading);
    });
  }

  function forceCorrectDaybreak(root) {
    if (!root || (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_FRAGMENT_NODE && root !== document.body)) return;
    const imgs = root.matches && root.matches('img') ? [root] : Array.from(root.querySelectorAll ? root.querySelectorAll('img') : []);
    imgs.forEach((img) => {
      const src = img.getAttribute('src') || '';
      if (!src.includes('daybreak-franco-german-garden-en.png') && !src.includes('50dce702b58f8bd97256.webp')) return;
      const wanted = 'assets/daybreak-franco-german-garden-en.png?v=' + REV;
      if (src !== wanted) img.setAttribute('src', wanted);
    });
  }

  function patch(root) {
    replaceFrenchText(root);
    localizeCombatArt(root);
    forceCorrectDaybreak(root);
  }

  function start() {
    if (started) return;
    started = true;
    ensureCombatStyle();
    patch(document.body);

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'characterData') {
          replaceFrenchText(mutation.target);
          continue;
        }
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.TEXT_NODE) replaceFrenchText(node);
          else if (node.nodeType === Node.ELEMENT_NODE) patch(node);
        });
      }
    });
    observer.observe(document.body, {subtree:true, childList:true, characterData:true});
  }

  loadBaseTranslations()
    .catch((err) => console.error('English base translations failed to load', err))
    .finally(() => {
      if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true});
      else start();
    });
})();
