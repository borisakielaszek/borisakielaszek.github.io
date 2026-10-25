(() => {
  'use strict';

  // Keep the complete German translation dictionary in its own immutable file.
  const translations=document.createElement('script');
  translations.src='/jeu-vampires-de-sarrebruck/de/translations-data.js?v=20261025-de10';
  translations.async=false;
  document.head.appendChild(translations);

  // Independent launch repair: the German intro must never depend on audio.
  const launch=document.createElement('script');
  launch.src='/jeu-vampires-de-sarrebruck/de/launch-fix.js?v=20261025-de8';
  launch.async=false;
  document.head.appendChild(launch);
})();
