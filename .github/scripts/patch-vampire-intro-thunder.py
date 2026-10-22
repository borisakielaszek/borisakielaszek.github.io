from pathlib import Path
import re

path=Path('jeu-vampires-de-sarrebruck/index.html')
text=path.read_text(encoding='utf-8')

text=re.sub(r'<audio id="introHissSfx" preload="auto" src="[^"]+"></audio>', '<audio id="introHissSfx" preload="auto" src="assets/thunder-intro.mp3"></audio>', text, count=1)

storm_css='''<style id="v557-intro-storm">
/* V5.72 — tonnerre utilisateur + éclairs blancs lumineux */
.storm-flash.choice-storm{
  background:radial-gradient(circle at 50% 18%,rgba(255,255,255,.78) 0,rgba(247,252,255,.46) 18%,rgba(205,228,255,.22) 42%,transparent 72%)!important;
  mix-blend-mode:screen!important;overflow:hidden!important;
}
.storm-flash.choice-storm.flash{animation:choiceStormFlashV572 .26s ease-out both!important}
.storm-flash.choice-storm .storm-bolt{
  width:24px!important;height:96vh!important;background:#fff!important;opacity:0;
  filter:drop-shadow(0 0 3px #fff) drop-shadow(0 0 9px #fff) drop-shadow(0 0 22px rgba(232,244,255,.98)) drop-shadow(0 0 48px rgba(181,216,255,.90)) drop-shadow(0 0 80px rgba(118,174,255,.62))!important;
  animation:choiceBoltV572 .24s steps(1,end) both!important;
}
.storm-flash.choice-storm .storm-bolt::before{content:"";position:absolute;inset:-8px -12px;background:#fff;clip-path:inherit;opacity:.82;filter:blur(6px)}
.storm-flash.choice-storm .storm-bolt::after{content:"";position:absolute;inset:-18px -26px;background:#eaf5ff;clip-path:inherit;opacity:.48;filter:blur(18px)}
@keyframes choiceBoltV572{0%{opacity:0}7%{opacity:1}30%{opacity:1}31%{opacity:.18}49%{opacity:.96}70%{opacity:.34}100%{opacity:0}}
@keyframes choiceStormFlashV572{0%{opacity:0;background-color:rgba(255,255,255,0)}8%{opacity:1;background-color:rgba(255,255,255,.98)}26%{opacity:.34;background-color:rgba(225,240,255,.34)}48%{opacity:.92;background-color:rgba(255,255,255,.74)}70%{opacity:.20;background-color:rgba(195,222,255,.18)}100%{opacity:0;background-color:rgba(255,255,255,0)}}
</style>'''
text,n=re.subn(r'<style id="v557-intro-storm">.*?</style>',storm_css,text,count=1,flags=re.S)
if n!=1: raise SystemExit('storm style not found')

new_choice='''function choiceStormBurst(){
 const flash=el('stormFlash');if(!flash)return;
 flash.classList.add('choice-storm');
 const shapes=[
  'polygon(46% 0,71% 0,53% 15%,78% 16%,45% 36%,67% 37%,31% 59%,54% 60%,18% 100%,29% 69%,10% 68%,38% 47%,19% 46%)',
  'polygon(42% 0,68% 0,51% 18%,75% 19%,44% 39%,65% 40%,30% 63%,52% 64%,17% 100%,27% 73%,9% 72%,36% 50%,18% 49%)',
  'polygon(48% 0,73% 0,56% 17%,80% 18%,47% 40%,69% 41%,34% 63%,56% 64%,20% 100%,31% 74%,11% 72%,39% 50%,21% 49%)'
 ];
 const strikes=[
  {t:0,x:27,rot:-5,scale:1.02},
  {t:115,x:70,rot:4,scale:.88},
  {t:430,x:48,rot:-2,scale:1.12},
  {t:930,x:78,rot:5,scale:.82},
  {t:1510,x:34,rot:-4,scale:.92},
  {t:2240,x:63,rot:3,scale:.78}
 ];
 strikes.forEach((st,i)=>setTimeout(()=>{
   if(!flash.classList.contains('choice-storm'))return;
   flash.classList.remove('flash');void flash.offsetWidth;flash.classList.add('flash');
   const bolt=document.createElement('div');bolt.className='storm-bolt';
   bolt.style.left=`calc(${st.x}% - 12px)`;
   bolt.style.transform=`rotate(${st.rot}deg) scale(${st.scale})`;
   bolt.style.clipPath=shapes[i%shapes.length];
   flash.appendChild(bolt);
   setTimeout(()=>bolt.remove(),330);
   setTimeout(()=>flash.classList.remove('flash'),285);
 },st.t));
 setTimeout(()=>{flash.classList.remove('flash','choice-storm');[...flash.querySelectorAll('.storm-bolt')].forEach(n=>n.remove());},3150);
}

function enterNight'''
text,n=re.subn(r'function choiceStormBurst\(\)\{.*?\n\}\n\nfunction enterNight',new_choice,text,count=1,flags=re.S)
if n!=1: raise SystemExit('choiceStormBurst not found')

text=text.replace('hiss.volume=.82;','hiss.volume=.92;',1)
text=text.replace('// V5.60 : on reste sur la première page pendant tout le souffle.\n // Les éclairs se jouent sur cette même page pendant la durée du son 256999.','// V5.72 : tonnerre utilisateur coupé juste avant l’impact.\n // Les éclairs blancs restent sur la première page pendant l’effet.',1)
text=text.replace('// Sécurité : le fichier 256999 dure ~2,14 s ; la transition n\'arrive jamais avant sa fin normale.\n setTimeout(finishIntro,2200);','// Sécurité : le tonnerre monté dure ~3,25 s ; ended reste prioritaire.\n setTimeout(finishIntro,3400);',1)

path.write_text(text,encoding='utf-8')
print('intro thunder patched')
