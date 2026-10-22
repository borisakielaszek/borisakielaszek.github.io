from pathlib import Path

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

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
elif 'id="helpBtn"' not in text:
    raise SystemExit('Action buttons block not found')

help_css = r'''
<style id="v561-compact-help">
/* Commandes secondaires regroupées dans l'aide */
.action-stage{padding:6px 8px!important}
.action-tools.help-only{position:absolute!important;right:10px!important;top:8px!important;bottom:auto!important;display:block!important;z-index:12!important}
.journal-head{padding-right:46px!important}
.help-orb{width:31px!important;height:31px!important;min-width:31px!important;padding:0!important;border-radius:50%!important;display:grid!important;place-items:center!important;background:linear-gradient(145deg,#a81524,#520710)!important;border:1px solid #d8b66d!important;color:#f7e1ae!important;font-family:Georgia,"Times New Roman",serif!important;font-size:1.15rem!important;font-weight:900!important;line-height:1!important;box-shadow:0 4px 12px #000a,0 0 0 2px #4b171d88 inset!important}
.help-orb:hover,.help-orb:focus-visible{border-color:#f1d38d!important;outline:none!important}
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
  .action-stage{padding:5px 7px!important}
  .action-tools.help-only{right:8px!important;top:7px!important}
  .journal-head{padding-right:43px!important}
  .help-orb{width:29px!important;height:29px!important;min-width:29px!important;font-size:1.08rem!important}
  .help-card{padding:19px 14px 14px}
}
</style>
'''
if 'id="v561-compact-help"' not in text:
    text = text.replace('</head>', help_css + '\n</head>', 1)

help_panel = r'''
<div id="helpPanel" class="help-panel hidden" role="dialog" aria-modal="true" aria-labelledby="helpPanelTitle">
  <div class="help-card">
    <button id="helpCloseBtn" class="help-close" type="button" aria-label="Fermer">×</button>
    <h2 id="helpPanelTitle">Aide & options</h2>
    <p class="help-subtitle">Les commandes secondaires sont regroupées ici pour laisser plus de place au Journal de la nuit.</p>
    <div class="help-actions">
      <button id="latestBtn" class="help-action" type="button">
        <strong>↓ Dernier événement</strong>
        <span>Revenir à l’action la plus récente du Journal de la nuit.</span>
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
if 'id="helpPanel"' not in text:
    marker = '<div id="toast" class="toast hidden"></div>'
    if marker not in text:
        raise SystemExit('Toast marker not found')
    text = text.replace(marker, help_panel + '\n' + marker, 1)

old_js = " const latestBtn=el('latestBtn');\n if(latestBtn)latestBtn.addEventListener('click',()=>{const j=el('gameLog');if(j){journalAutoFollow=true;j.scrollTo({top:j.scrollHeight,behavior:'smooth'});}});\n const startBtn=el('startBtn');"
new_js = " const latestBtn=el('latestBtn');\n if(latestBtn)latestBtn.addEventListener('click',()=>{const j=el('gameLog');if(j){journalAutoFollow=true;j.scrollTo({top:j.scrollHeight,behavior:'smooth'});}});\n const helpBtn=el('helpBtn'),helpPanel=el('helpPanel'),helpCloseBtn=el('helpCloseBtn');\n const closeHelp=()=>{if(helpPanel)helpPanel.classList.add('hidden');};\n if(helpBtn)helpBtn.addEventListener('click',()=>{if(helpPanel)helpPanel.classList.remove('hidden');});\n if(helpCloseBtn)helpCloseBtn.addEventListener('click',closeHelp);\n if(helpPanel)helpPanel.addEventListener('click',e=>{if(e.target===helpPanel)closeHelp();});\n if(latestBtn)latestBtn.addEventListener('click',closeHelp);\n const helpRulesBtn=el('rulesBtn');if(helpRulesBtn)helpRulesBtn.addEventListener('click',closeHelp);\n document.addEventListener('keydown',e=>{if(e.key==='Escape')closeHelp();});\n const startBtn=el('startBtn');"
if old_js in text:
    text = text.replace(old_js, new_js, 1)
elif "const helpBtn=el('helpBtn')" not in text:
    raise SystemExit('Latest button setup block not found')

path.write_text(text, encoding='utf-8')
