const fs=require('fs'),vm=require('vm');
const nodes=new Map();const node=id=>{if(!nodes.has(id))nodes.set(id,{value:id==='playerCount'?'3':id==='vampireChoice'?'random':id==='playerName0'?'Van Helsing':'normal',classList:{add(){},remove(){},contains(){return false}},querySelector(){return null},querySelectorAll(){return []}});return nodes.get(id)};
const ctx={console,Math,setTimeout,clearTimeout,requestAnimationFrame:f=>f(),document:{getElementById:node,body:{classList:{add(){},remove(){},contains(){return false}}}},window:{scrollTo(){},addEventListener(){}},navigator:{}};vm.createContext(ctx);
const path=require('path');const input=process.argv[2]||path.join(__dirname,'../jeu-vampires-de-sarrebruck/index.html');let raw=fs.readFileSync(input,'utf8');if(input.endsWith('.html'))raw=[...raw.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]).sort((a,b)=>b.length-a.length)[0];let source=raw.replace(/init\(\);\s*wireUI\(\);\s*$/,'').replace('const sleep=ms=>new Promise(r=>setTimeout(r,ms));','let sleep=async()=>{};');
const test=`(async()=>{
const assert=(v,m)=>{if(!v)throw Error(m)};log=()=>{};render=()=>{};switchToGameMusic=()=>{};refreshMusicButton=()=>{};gameLoop=()=>{};openTapDismissInfo=async()=>{};showCombatScene=async()=>{};showHumanEliminationScene=async()=>{};openModal=async()=>true;
for(const n of [1,2,3,4])for(const d of ['easy','normal','hard']){
 el('playerCount').value=String(n+1);el('difficultyChoice').value=d;await startGame();const p=S.players[0],cfg=helsingBalance(n,d);S.awaitingHuman=true;
 assert(aiDifficulty()===d,'Difficulty honored');assert(p.hp===10&&p.hand.length===0,'Human HP and no vampire cards');
 for(const [key,value]of Object.entries(cfg.initial))assert(p[key]===value,'Initial stock '+key);
 assert(!secretPowersHTML(p).includes('data-gear="van_helsing_broom"')&&!secretPowersHTML(p).includes('data-gear="van_helsing_armed_broom"'),'Brooms hidden before event');
 for(let i=0;i<100;i++)recoverHelsingAmmo(p,i/100);for(const [key,cap]of Object.entries(cfg.caps))assert(p[key]<=cap,'Supply caps');
 assert(recoverHelsingAmmo(p,0)===null,'Full pack no overflow');p.silverBolts=0;assert(recoverHelsingAmmo(p,.999)==='silverBolts'&&p.silverBolts===1,'Full stocks excluded, empty crossbow reloads');
 p.dawnUses=p.dawnLimit;assert(!secretPowerAvailable(p,'van_helsing_dawn')&&helsingGearUnavailableReason(p,'van_helsing_dawn').includes('épuisé'),'Lantern exhausted');
 const enemy=S.players[1];await grantHelsingBroom(enemy,'hexennacht',null);assert(!p.broomCharges,'Replay does not award gear');await grantHelsingBroom(enemy,'hexennacht','normal');assert(p.broomCharges===1&&!p.armedBroomCharges,'Hex only simple broom');await grantHelsingBroom(enemy,'sorcieres','normal');assert(p.armedBroomCharges===1,'Oeting only armed broom');
 assert(!canUseHelsingBroom(p,enemy,'meute','van_helsing_armed_broom')&&!canUseHelsingBroom(p,enemy,'abomination','van_helsing_broom'),'Wolf and barred immunity');
 chooseDefense=async()=> 'van_helsing_armed_broom';const hp=p.hp,ehp=enemy.hp;await resolveAttackInstance(enemy,p,'morsure');assert(p.hp===hp&&enemy.hp===Math.max(0,ehp-3)&&p.armedBroomCharges===0,'Armed broom defense/counter');
 assert(secretPowersHTML(p).includes('data-gear="van_helsing_armed_broom"'),'Spent unlocked broom remains inspectable');
 assert(!canUseMirror(p,enemy,'meute')&&!canUseRosary(p,enemy,'meute'),'No sacred wolf defense');
 const game=S;S.discard=[];S.deck=[];S.players.forEach(x=>x.witches=false);settleImmediateDraw(game,'sorcieres');settleImmediateDraw(game,'sorcieres');assert(S.discard.filter(x=>x==='sorcieres').length===1,'Unique witches settlement');
}
el('playerName0').value='Boris';await startGame();assert(!S.secretMode&&S.players[0].hand.length===6,'Normal mode deal preserved');console.log('PASS: 12 stock profiles, difficulty, supply caps/reload, lantern limit, both broom events/defense, immediate accounting and normal mode');
})()`;vm.runInContext(source+test,ctx).catch(e=>{console.error(e);process.exitCode=1});
