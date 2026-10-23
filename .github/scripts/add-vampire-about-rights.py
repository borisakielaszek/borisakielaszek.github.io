from pathlib import Path

p = Path('jeu-vampires-de-sarrebruck/index.html')
s = p.read_text(encoding='utf-8')

if 'id="aboutRightsOverlay"' in s:
    print('About & rights already present')
    raise SystemExit(0)

block = '''
<style id="aboutRightsStyles">
#aboutRightsOverlay{position:fixed;inset:0;z-index:100000;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(4,4,8,.88);backdrop-filter:blur(5px)}
#aboutRightsOverlay.open{display:flex}
#aboutRightsPanel{position:relative;width:min(760px,94vw);max-height:88vh;overflow:auto;padding:28px 24px 24px;border:1px solid rgba(188,35,49,.75);border-radius:18px;background:linear-gradient(180deg,#1a171a,#0d0b0d);box-shadow:0 18px 55px rgba(0,0,0,.7);color:#f3ece7;text-align:left}
#aboutRightsPanel h2{margin:0 42px 18px 0;color:#fff;text-align:center}
#aboutRightsPanel p{line-height:1.55;margin:0 0 14px}
#aboutRightsPanel .rights-title{font-weight:700;color:#fff}
#aboutRightsPanel .rights-copy{text-align:center;margin-top:20px;font-weight:700;color:#d7b8b8}
#aboutRightsClose{position:absolute;right:14px;top:12px;width:38px;height:38px;border:0;border-radius:50%;background:#7f1420;color:white;font-size:24px;line-height:38px;cursor:pointer}
#aboutRightsMenuBtn{margin-top:10px}
.gameCopyrightNotice{margin:10px auto 0;text-align:center;font-size:.78rem;line-height:1.35;opacity:.72;max-width:620px}
</style>
<div id="aboutRightsOverlay" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="aboutRightsTitle">
<section id="aboutRightsPanel">
<button id="aboutRightsClose" type="button" aria-label="Fermer">×</button>
<h2 id="aboutRightsTitle">À propos &amp; droits</h2>
<p><span class="rights-title">Les Vampires de Sarrebruck</span><br>Jeu créé par <strong>Boris Akielaszek</strong>, d’après l’univers du livre illustré <em>Les Vampires de Sarrebruck</em>, coécrit avec <strong>Stella</strong>.</p>
<p><strong>© 2026 Boris Akielaszek. Tous droits réservés.</strong></p>
<p>Les textes, illustrations, personnages, cartes, règles, éléments graphiques et le code original de ce jeu sont protégés par le droit d’auteur. Les musiques et sons éventuellement issus de ressources tierces restent soumis aux droits et licences de leurs auteurs respectifs.</p>
<p>Toute reproduction, copie, modification, redistribution, extraction ou réutilisation, totale ou partielle, du jeu ou de ses éléments à des fins commerciales ou de diffusion publique est interdite sans autorisation préalable.</p>
<p>L’accès au jeu est destiné à un usage personnel et privé.</p>
<p class="rights-copy">© 2026 Boris Akielaszek — Tous droits réservés</p>
</section>
</div>
<script id="aboutRightsScript">
(function(){
function norm(t){return (t||'').replace(/\\s+/g,' ').trim().toLowerCase();}
function initAboutRights(){
var overlay=document.getElementById('aboutRightsOverlay');
var close=document.getElementById('aboutRightsClose');
if(!overlay||!close)return;
var candidates=[].slice.call(document.querySelectorAll('button,a,[role="button"]'));
var origin=candidates.find(function(el){var t=norm(el.textContent);return t==='les origines du jeu'||t.indexOf('les origines du jeu')!==-1;});
if(origin&&!document.getElementById('aboutRightsMenuBtn')){
var btn=origin.cloneNode(true);
btn.id='aboutRightsMenuBtn';
btn.removeAttribute('href');
btn.removeAttribute('onclick');
btn.type='button';
btn.textContent='À propos & droits';
origin.insertAdjacentElement('afterend',btn);
var copy=document.createElement('div');
copy.className='gameCopyrightNotice';
copy.textContent='© 2026 Boris Akielaszek — Tous droits réservés';
btn.insertAdjacentElement('afterend',copy);
btn.addEventListener('click',function(e){e.preventDefault();overlay.classList.add('open');overlay.setAttribute('aria-hidden','false');close.focus();});
}
function hide(){overlay.classList.remove('open');overlay.setAttribute('aria-hidden','true');}
close.addEventListener('click',hide);
overlay.addEventListener('click',function(e){if(e.target===overlay)hide();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&overlay.classList.contains('open'))hide();});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initAboutRights);else initAboutRights();
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No closing body tag found')

s = s.replace('</body>', block + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('About & rights added')
