from pathlib import Path
import re

path = Path('jeu-vampires-de-sarrebruck/index.html')
text = path.read_text(encoding='utf-8')

# Force le titre court et unique.
text = text.replace('Journal de la nuit', 'Journal nocturne')

# Le bouton d'aide doit déjà exister depuis la correction précédente.
if 'id="helpBtn"' not in text:
    raise SystemExit('helpBtn missing from game page')
if 'id="helpPanel"' not in text:
    raise SystemExit('helpPanel missing from game page')

css = r'''
<style id="v561-compact-help">
/* V5.63 — journal mobile réellement optimisé */
.action-stage{
  position:relative!important;
  display:block!important;
  width:100%!important;
  height:100%!important;
  min-height:0!important;
  padding:0!important;
  overflow:hidden!important;
  box-sizing:border-box!important;
}
.action-turn,.action-instruction,.last-action{display:none!important}
.journal-head{
  position:absolute!important;
  top:6px!important;
  left:7px!important;
  right:7px!important;
  width:auto!important;
  height:38px!important;
  min-height:38px!important;
  margin:0!important;
  padding:0 42px!important;
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  text-align:center!important;
  border:1px solid #343b48!important;
  border-bottom:0!important;
  border-radius:10px 10px 0 0!important;
  background:#131720!important;
  box-sizing:border-box!important;
  z-index:2!important;
}
.journal-head strong{
  display:block!important;
  width:100%!important;
  margin:0!important;
  padding:0!important;
  text-align:center!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
  font-family:Georgia,"Times New Roman",serif!important;
  font-size:1.06rem!important;
  line-height:1!important;
  color:#f3e4cb!important;
}
.journal-head span{display:none!important}
.action-tools.help-only{
  position:absolute!important;
  top:13px!important;
  right:14px!important;
  left:auto!important;
  bottom:auto!important;
  margin:0!important;
  padding:0!important;
  display:block!important;
  z-index:12!important;
  transform:none!important;
}
.help-orb{
  width:24px!important;
  height:24px!important;
  min-width:24px!important;
  min-height:24px!important;
  padding:0!important;
  margin:0!important;
  border-radius:50%!important;
  display:grid!important;
  place-items:center!important;
  background:linear-gradient(145deg,#a81524,#520710)!important;
  border:1px solid #d8b66d!important;
  color:#f7e1ae!important;
  font-family:Georgia,"Times New Roman",serif!important;
  font-size:.92rem!important;
  font-weight:900!important;
  line-height:1!important;
  box-shadow:0 3px 9px #000a,0 0 0 1px #4b171d88 inset!important;
}
.help-orb:hover,.help-orb:focus-visible{border-color:#f1d38d!important;outline:none!important}
#gameLog.journal-live,.game-log.journal-live{
  position:absolute!important;
  top:44px!important;
  left:7px!important;
  right:7px!important;
  bottom:7px!important;
  width:auto!important;
  height:auto!important;
  min-height:0!important;
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
  scrollbar-width:thin!important;
  font-size:.9rem!important;
  line-height:1.34!important;
}
#gameLog.journal-live .log-line,.game-log.journal-live .log-line{
  padding:5px 2px!important;
}
#gameLog.journal-live .log-line.turn,.game-log.journal-live .log-line.turn{
  margin:2px 0 5px!important;
  padding:6px 8px!important;
  font-size:1em!important;
}
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
  .journal-head{top:5px!important;left:6px!important;right:6px!important;height:36px!important;min-height:36px!important;padding:0 38px!important}
  .journal-head strong{font-size:1rem!important}
  .action-tools.help-only{top:11px!important;right:12px!important}
  .help-orb{width:23px!important;height:23px!important;min-width:23px!important;min-height:23px!important;font-size:.88rem!important}
  #gameLog.journal-live,.game-log.journal-live{top:41px!important;left:6px!important;right:6px!important;bottom:6px!important;padding:7px 9px 10px!important;font-size:.88rem!important}
}
</style>
'''

pattern = re.compile(r'<style id="v561-compact-help">.*?</style>', re.S)
if pattern.search(text):
    text = pattern.sub(css.strip(), text, count=1)
else:
    if '</head>' not in text:
        raise SystemExit('Missing </head>')
    text = text.replace('</head>', css + '\n</head>', 1)

path.write_text(text, encoding='utf-8')
