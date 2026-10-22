from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

# Titre du journal : formulation courte et centrée.
text = text.replace(
    '<div class="journal-head"><strong>Journal de la nuit</strong><span>Fais défiler au doigt pour relire.</span></div>',
    '<div class="journal-head"><strong>Journal nocturne</strong><span>Fais défiler au doigt pour relire.</span></div>',
    1,
)

# Garde le bouton d'aide unique si le vieux trio existe encore sur une ancienne version.
old_buttons = '''        <div class="action-tools">
          <button id="latestBtn" class="ghost-btn">↓ Dernier</button>
          <button id="rulesBtn" class="ghost-btn">Règles</button>
          <button id="restartBtn" class="ghost-btn">Recommencer</button>
        </div>'''
new_buttons = '''        <div class="action-tools help-only">
          <button id="helpBtn" class="help-orb" type="button" aria-label="Aide et options" title="Aide et options">?</button>
        </div>'''
if old_buttons in text:
    text = text.replace(old_buttons, new_buttons, 1)

help_css = r'''
<style id="v561-compact-help">
/* V5.62 — Journal nocturne centré et panneau central pleine hauteur */
.action-stage{
  position:relative!important;
  display:flex!important;
  flex-direction:column!important;
  align-items:stretch!important;
  justify-content:flex-start!important;
  gap:0!important;
  width:100%!important;
  height:100%!important;
  min-height:0!important;
  padding:6px 8px 7px!important;
  overflow:hidden!important;
  box-sizing:border-box!important;
}
.journal-head{
  position:relative!important;
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  flex:0 0 auto!important;
  width:100%!important;
  min-height:44px!important;
  margin:0!important;
  padding:6px 48px!important;
  text-align:center!important;
  border:1px solid #343b48!important;
  border-bottom:0!important;
  border-radius:10px 10px 0 0!important;
  background:#131720!important;
  box-sizing:border-box!important;
}
.journal-head strong{
  display:block!important;
  width:100%!important;
  margin:0!important;
  text-align:center!important;
  font-family:Georgia,"Times New Roman",serif!important;
  font-size:clamp(1.18rem,5vw,1.5rem)!important;
  line-height:1.08!important;
  color:#f3e4cb!important;
}
.journal-head span{display:none!important}
.action-tools.help-only{
  position:absolute!important;
  right:13px!important;
  top:12px!important;
  bottom:auto!important;
  left:auto!important;
  display:block!important;
  z-index:12!important;
  transform:none!important;
}
.help-orb{
  width:32px!important;
  height:32px!important;
  min-width:32px!important;
  padding:0!important;
  border-radius:50%!important;
  display:grid!important;
  place-items:center!important;
  background:linear-gradient(145deg,#a81524,#520710)!important;
  border:1px solid #d8b66d!important;
  color:#f7e1ae!important;
  font-family:Georgia,"Times New Roman",serif!important;
  font-size:1.16rem!important;
  font-weight:900!important;
  line-height:1!important;
  box-shadow:0 4px 12px #000a,0 0 0 2px #4b171d88 inset!important;
}
.help-orb:hover,.help-orb:focus-visible{border-color:#f1d38d!important;outline:none!important}
.journal-live{
  display:block!important;
  flex:1 1 auto!important;
  align-self:stretch!important;
  width:100%!important;
  min-height:0!important;
  height:auto!important;
  max-height:none!important;
  margin:0!important;
  padding:8px 10px 12px!important;
  overflow-y:auto!important;
  overflow-x:hidden!important;
  border:1px solid #343b48!important;
  border-radius:0 0 10px 10px!important;
  background:linear-gradient(180deg,#0b0e14,#07090d)!important;
  box-sizing:border-box!important;
  touch-action:pan-y!important;
  overscroll-behavior:contain!important;
  -webkit-overflow-scrolling:touch!important;
}
.last-action{display:none!important}
.help-panel{position:fixed;inset:0;z-index:180;display:flex;align-items:center;justify-content:center;padding:18px;background:#03050ad9;backdrop-filter:blur(12px)}
.help-card{position:relative;width:min(520px,94vw);max-height:88vh;overflow:auto;padding:22px 18px 18px;border:1px solid #49505f;border-radius:22px;background:linear-gradient(180deg,#171b25,#090c12);box-shadow:0 24px 80px #000d}
.help-card h2{margin:0 44px 5px 0;color:#f2dfba;font-size:1.6rem}
.help-subtitle{margin:0 0 17px;color:#aeb5c0;font-family:system-ui,sans-serif;font-size:.9rem;line-height:1.4}
.help-close{position:absolute;right:11px;top:10px;width:38px;height:38px;padding:0;border-radius:50%;background:#202633;border-color:#444d5d;color:#e4e7eb;font-size:1.45rem;line-height:1}
.help-actions{display:grid;gap:10px}
.help-action{width:100%;min-height:68px;padding:12px 14px;text-align:left;border-radius:14px;background:linear-gradient(180deg,#191f2a,#10151e);border:1px solid #394253;color:#f4eee2}
.help-action strong{display:block;font-size:1.03rem;color:#f0d49a;margin-bottom:3px}
.help-action span{display:block;font-family:system-ui,sans-serif;font-size:.82rem;line-height:1.35;color:#b6bdc8}
.help-action.danger{border-color:#63232d;background:linear-gradient(180deg,#29151a,#160d11)}
.help-action.danger strong{color:#efb3b9}
@media(max-width:430px){
  .action-stage{padding:5px 7px 6px!important}
  .journal-head{min-height:42px!important;padding:5px 45px!important}
  .journal-head strong{font-size:1.28rem!important}
  .action-tools.help-only{right:11px!important;top:10px!important}
  .help-orb{width:30px!important;height:30px!important;min-width:30px!important;font-size:1.1rem!important}
  .journal-live{height:auto!important;min-height:0!important;padding:7px 9px 10px!important}
  .help-card{padding:19px 14px 14px}
}
</style>
'''

style_pattern = re.compile(r'<style id="v561-compact-help">.*?</style>', re.S)
if style_pattern.search(text):
    text = style_pattern.sub(help_css.strip(), text, count=1)
else:
    if '</head>' not in text:
        raise SystemExit('Missing </head>')
    text = text.replace('</head>', help_css + '\n</head>', 1)

# Harmonise les textes du panneau d'aide.
text = text.replace('laisser plus de place au Journal de la nuit.', 'laisser plus de place au Journal nocturne.')
text = text.replace('du Journal de la nuit.', 'du Journal nocturne.')

# Le panneau et le JavaScript d'aide restent inchangés s'ils sont déjà présents.
if 'id="helpPanel"' not in text:
    help_panel = r'''
<div id="helpPanel" class="help-panel hidden" role="dialog" aria-modal="true" aria-labelledby="helpPanelTitle">
  <div class="help-card">
    <button id="helpCloseBtn" class="help-close" type="button" aria-label="Fermer">×</button>
    <h2 id="helpPanelTitle">Aide & options</h2>
    <p class="help-subtitle">Les commandes secondaires sont regroupées ici pour laisser plus de place au Journal nocturne.</p>
    <div class="help-actions">
      <button id="latestBtn" class="help-action" type="button">
        <strong>↓ Dernier événement</strong>
        <span>Revenir à l’action la plus récente du Journal nocturne.</span>
      </button>
      <button id="rulesBtn" class="help-action" type="button">
        <strong>Règles</strong>
        <span>Consulter les règles sans quitter la partie en cours.</span>
      </button>
      <button id="restartBtn" class="help-action danger" type="button">
        <strong>Recommencer</strong>
        <span>Relancer une nouvelle partie.</span>
      </button>
    </div>
  </div>
</div>
'''
    marker = '<div id="toast" class="toast hidden"></div>'
    if marker not in text:
        raise SystemExit('Toast marker not found')
    text = text.replace(marker, help_panel + '\n' + marker, 1)

if "const helpBtn=el('helpBtn')" not in text:
    old_js = " const latestBtn=el('latestBtn');\n if(latestBtn)latestBtn.addEventListener('click',()=>{const j=el('gameLog');if(j){journalAutoFollow=true;j.scrollTo({top:j.scrollHeight,behavior:'smooth'});}});\n const startBtn=el('startBtn');"
    new_js = " const latestBtn=el('latestBtn');\n if(latestBtn)latestBtn.addEventListener('click',()=>{const j=el('gameLog');if(j){journalAutoFollow=true;j.scrollTo({top:j.scrollHeight,behavior:'smooth'});}});\n const helpBtn=el('helpBtn'),helpPanel=el('helpPanel'),helpCloseBtn=el('helpCloseBtn');\n const closeHelp=()=>{if(helpPanel)helpPanel.classList.add('hidden');};\n if(helpBtn)helpBtn.addEventListener('click',()=>{if(helpPanel)helpPanel.classList.remove('hidden');});\n if(helpCloseBtn)helpCloseBtn.addEventListener('click',closeHelp);\n if(helpPanel)helpPanel.addEventListener('click',e=>{if(e.target===helpPanel)closeHelp();});\n if(latestBtn)latestBtn.addEventListener('click',closeHelp);\n const helpRulesBtn=el('rulesBtn');if(helpRulesBtn)helpRulesBtn.addEventListener('click',closeHelp);\n document.addEventListener('keydown',e=>{if(e.key==='Escape')closeHelp();});\n const startBtn=el('startBtn');"
    if old_js not in text:
        raise SystemExit('Latest button setup block not found')
    text = text.replace(old_js, new_js, 1)

path.write_text(text, encoding='utf-8')
