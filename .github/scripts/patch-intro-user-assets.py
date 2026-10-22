from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

# Use the rebuilt thunder asset.
text = re.sub(
    r'<audio id="introHissSfx" preload="auto" src="[^"]+"></audio>',
    '<audio id="introHissSfx" preload="auto" src="assets/thunder-intro-user.mp3?v=573"></audio>',
    text,
    count=1,
)

# Intro-only lightning styling. These are the user supplied lightning drawings vectorised to white.
style = r'''<style id="v557-intro-storm">
/* V5.73 — éclairs provenant des deux images fournies par Boris */
.storm-flash.choice-storm{
  background:radial-gradient(circle at 50% 17%,rgba(255,255,255,.82) 0,rgba(238,248,255,.46) 22%,rgba(170,208,255,.18) 48%,transparent 76%)!important;
  mix-blend-mode:screen!important;
  overflow:hidden!important;
}
.storm-flash.choice-storm.flash{animation:introUserSkyFlash .30s ease-out both!important}
.intro-user-lightning{
  position:absolute;
  left:50%;
  top:-1vh;
  width:min(108vw,1800px);
  max-width:none;
  height:auto;
  transform:translateX(-50%);
  transform-origin:50% 0;
  opacity:0;
  pointer-events:none;
  filter:drop-shadow(0 0 4px #fff) drop-shadow(0 0 12px #fff) drop-shadow(0 0 30px rgba(220,240,255,.98)) drop-shadow(0 0 68px rgba(125,187,255,.86));
  animation:introUserBolt .34s steps(1,end) both;
}
.intro-user-lightning.sheet2{top:-3vh;width:min(104vw,1740px)}
@keyframes introUserBolt{
  0%{opacity:0}
  7%{opacity:1}
  28%{opacity:1}
  29%{opacity:.18}
  47%{opacity:.98}
  68%{opacity:.34}
  100%{opacity:0}
}
@keyframes introUserSkyFlash{
  0%{opacity:0;background-color:rgba(255,255,255,0)}
  8%{opacity:1;background-color:rgba(255,255,255,.98)}
  27%{opacity:.28;background-color:rgba(220,239,255,.30)}
  48%{opacity:.92;background-color:rgba(255,255,255,.74)}
  72%{opacity:.18;background-color:rgba(170,210,255,.18)}
  100%{opacity:0;background-color:rgba(255,255,255,0)}
}
</style>'''
text = re.sub(r'<style id="v557-intro-storm">.*?</style>', style, text, count=1, flags=re.S)

# Replace only the intro storm animation. In-game stormBurst keeps its own visual effect.
new_choice = r'''function choiceStormBurst(){
 const flash=el('stormFlash');if(!flash)return;
 flash.classList.add('choice-storm');
 [...flash.querySelectorAll('.intro-user-lightning')].forEach(n=>n.remove());
 const strikes=[
   {t:0,src:'assets/user-lightning-1.svg',cls:'sheet1',scale:1},
   {t:105,src:'assets/user-lightning-2.svg',cls:'sheet2',scale:1.01},
   {t:620,src:'assets/user-lightning-1.svg',cls:'sheet1',scale:.98},
   {t:1320,src:'assets/user-lightning-2.svg',cls:'sheet2',scale:1.02},
   {t:2380,src:'assets/user-lightning-1.svg',cls:'sheet1',scale:1.01},
   {t:3500,src:'assets/user-lightning-2.svg',cls:'sheet2',scale:.99}
 ];
 strikes.forEach(st=>setTimeout(()=>{
   if(!flash.classList.contains('choice-storm'))return;
   flash.classList.remove('flash');void flash.offsetWidth;flash.classList.add('flash');
   const bolt=document.createElement('img');
   bolt.className=`intro-user-lightning ${st.cls}`;
   bolt.src=st.src;
   bolt.alt='';bolt.setAttribute('aria-hidden','true');
   bolt.style.transform=`translateX(-50%) scale(${st.scale})`;
   flash.appendChild(bolt);
   setTimeout(()=>bolt.remove(),430);
   setTimeout(()=>flash.classList.remove('flash'),340);
 },st.t));
 setTimeout(()=>{
   flash.classList.remove('flash','choice-storm');
   [...flash.querySelectorAll('.intro-user-lightning')].forEach(n=>n.remove());
 },4900);
}

function enterNight'''
text, n = re.subn(r'function choiceStormBurst\(\)\{.*?\n\}\n\nfunction enterNight', new_choice, text, count=1, flags=re.S)
if n != 1:
    raise SystemExit('choiceStormBurst function not found')

# Cleanup both old and new intro bolt nodes when the page changes.
text = text.replace(
    "[...flash.querySelectorAll('.storm-bolt')].forEach(n=>n.remove());",
    "[...flash.querySelectorAll('.storm-bolt,.intro-user-lightning')].forEach(n=>n.remove());",
)

# Start the thunder at once; the rebuilt file already has its initial silence removed.
text = re.sub(
    r"if\(hiss\)\{try\{hiss\.pause\(\);hiss\.currentTime=0;hiss\.volume=\.\d+;const hp=hiss\.play\(\);if\(hp&&hp\.catch\)hp\.catch\(\(\)=>\{\}\);\}catch\(_\)\{\}\s*\}",
    "if(hiss){try{hiss.pause();hiss.currentTime=0;hiss.volume=1;const hp=hiss.play();if(hp&&hp.catch)hp.catch(()=>{});}catch(_){}}",
    text,
    count=1,
)
text = re.sub(r'// Sécurité :[^\n]*\n\s*setTimeout\(finishIntro,\d+\);', "// Sécurité : le fichier monté dure environ 4,8 s ; l’événement ended reste prioritaire.\n setTimeout(finishIntro,5100);", text, count=1)

path.write_text(text, encoding='utf-8')
print('Intro thunder/lightning patch applied')
