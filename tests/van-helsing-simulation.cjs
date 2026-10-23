const fs=require('fs'),vm=require('vm');
const path=require('path');const input=process.argv[2]||path.join(__dirname,'../jeu-vampires-de-sarrebruck/index.html');let raw=fs.readFileSync(input,'utf8');if(input.endsWith('.html'))raw=[...raw.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]).sort((a,b)=>b.length-a.length)[0];const source=raw.replace(/init\(\);\s*wireUI\(\);\s*$/,'').replace('const sleep=ms=>new Promise(r=>setTimeout(r,ms));','let sleep=async()=>{};');
const compiledGame=new vm.Script(source,{filename:'game-engine.js'});
const repeats=Number(process.argv[3]||10),results=[];
function seeded(seed){let x=seed>>>0;return ()=>{x+=0x6D2B79F5;let t=x;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296}}
async function run(ais,diff,seed,override=null){
 const nodes=new Map(),node=id=>{if(!nodes.has(id))nodes.set(id,{value:id==='playerCount'?String(ais+1):id==='vampireChoice'?'random':id==='playerName0'?'Van Helsing':diff,classList:{add(){},remove(){},contains(){return false}},querySelector(){return null},querySelectorAll(){return []},textContent:'',disabled:false});return nodes.get(id)};
 const math=Object.create(Math);math.random=seeded(seed);
 const c={balanceOverride:override,simLog:[],console,Math:math,setTimeout,clearTimeout,queueMicrotask,requestAnimationFrame:f=>f(),document:{getElementById:node,body:{classList:{add(){},remove(){},contains(){return false}}}},window:{addEventListener(){},scrollTo(){}},navigator:{}};vm.createContext(c);
 const script=`
 if(balanceOverride){const originalBalance=helsingBalance;helsingBalance=(n,d)=>({...originalBalance(n,d),...balanceOverride});}
 (async()=>{
 let turns=0,humanTurns=0,scheduled=false,loopPromise,error=null,totalBlood=0;const history=[];const used={};
 log=(msg)=>{simLog.push(msg);history.push(msg);if(history.length>12)history.shift()};
 sleep=async()=>{};switchToGameMusic=()=>{};refreshMusicButton=()=>{};playEndgameMusic=()=>{};stopEndgameMusic=()=>{};closeHand=()=>{};
 showCombatScene=async()=>{};showAttackReveal=async()=>{};showDrawScene=async()=>{};showGlobalImmediateNotice=async()=>{};showImmediateScene=async()=>{};showImmediateRepickNotice=async()=>{};showHumanEliminationScene=async()=>{};openTapDismissInfo=async()=>true;
 openModal=async o=>{const buttons=o.buttons||[];if(o.title==='Nouvelle partie ?')return 'stay';const b=buttons.find(x=>x.value===true)||buttons.find(x=>!['cancel',null,false].includes(x.value));return b?.value??true};
 choosePlayer=async(prompt,players)=>players.slice().sort((a,b)=>a.hp-b.hp)[0]||null;
 chooseCardFromHand=async()=>0;chooseDiscardCandidate=async()=>0;chooseHexennachtBack=async()=>0;
 chooseSecretPowerTarget=async(game,p,id)=>{const a=secretPowerTargets(game,p).sort((a,b)=>a.hp-b.hp);if(id==='van_helsing_whip'||id==='van_helsing_dawn')return a.length?true:null;if(id==='van_helsing_water')return a.slice(0,Math.min(2,a.length));return id==='van_helsing_stake'?a.slice().sort((x,y)=>y.hp-x.hp)[0]:a[0]};
 chooseDefense=async(t,a,id,defs)=>{if(!t.human)return aiChooseDefense(t,a,id,defs);if(defs.includes('van_helsing_armed_broom'))return 'van_helsing_armed_broom';if(defs.includes('van_helsing_broom'))return 'van_helsing_broom';if(defs.includes('van_helsing_silver_defense'))return 'van_helsing_silver_defense';if(defs.includes('van_helsing_mirror'))return 'van_helsing_mirror';if(defs.includes('van_helsing_rosary'))return 'van_helsing_rosary';return null};
 const assert=(v,msg)=>{if(!v)throw Error(msg)};
 function invariant(){if(!S)return;const p=S.players[0];assert(p.hand.length===0,'Hunter received vampire cards');assert(Number.isFinite(S.pool)&&S.pool>=0,'Invalid pool');for(const t of S.players){assert(Number.isFinite(t.hp)&&t.hp>=0&&t.hp<=playerMaxHp(t),'Invalid HP');assert(t.alive===(t.hp>0),'Alive/HP mismatch');if(!t.human)assert(t.hand.length<=maxHand(t),'Hand overflow');}for(const key of ['silverBolts','blessedBullets','gepettoStakes','medkitUses','elixirDoses','rosaryCharges','mirrorCharges'])assert(Number.isInteger(p[key])&&p[key]>=0,'Invalid stock '+key);assert(S.pool+S.players.reduce((n,t)=>n+t.hp,0)===totalBlood,'Blood conservation');const cards=[...S.deck,...S.discard,...S.players.flatMap(t=>t.hand),...S.players.filter(t=>t.witches).map(()=> 'sorcieres')];assert(cards.length===buildActionDeck().length,'Card conservation '+cards.length+'/'+buildActionDeck().length);for(const id of cards)assert(CARDS[id],'Unknown card');if(typeof currentHelsingBalance==='function')for(const [key,cap]of Object.entries(currentHelsingBalance().caps))assert(p[key]<=cap,'Supply cap exceeded');}
 async function hunterTurn(){
 const p=S.players[0],a=secretPowerTargets(S,p),count=a.length,minHp=Math.min(...a.map(t=>t.hp)),maxHp=Math.max(...a.map(t=>t.hp));let choice;
 if(p.hp<=6&&secretPowerAvailable(p,'van_helsing_elixir'))choice='elixir';
 else if(p.hp<=7&&secretPowerAvailable(p,'van_helsing_medkit'))choice='medkit';
 else{
 const opts=[];const add=(id,score)=>{if(secretPowerAvailable(p,id))opts.push({id,score})};
 add('van_helsing_stake',Math.ceil(maxHp/2)*2.5+(maxHp===1?5:0));add('van_helsing_bullet',Math.min(2,minHp)*2.5+(minHp<=2?5:0));add('van_helsing_bolt',2.5+(minHp===1?5:0)+.6);add('van_helsing_cross',Math.min(2,minHp)*2.5+(minHp<=2?5:0));add('van_helsing_whip',count*2.5+(minHp===1?5:0));add('van_helsing_water',Math.min(2,count)*3.1+(minHp===1?5:0));add('van_helsing_dawn',a.reduce((n,t)=>n+Math.min(2,t.hand.length),0)*.45);
 opts.sort((x,y)=>y.score-x.score);choice=opts[0]?.id;
 }
 humanTurns++;used[choice||'resupply']=(used[choice||'resupply']||0)+1;
 if(choice==='elixir')await useHelsingElixir();else if(choice==='medkit')await useHelsingMedkit();else if(choice)await useSecretPower(choice);else await helsingResupply();
 if(S.awaitingHuman&&!S.gameOver&&!actionBusy&&humanTurnResolve)endHumanTurn();
 }
 render=()=>{if(S?.awaitingHuman&&!scheduled&&!actionBusy){scheduled=true;queueMicrotask(async()=>{try{if(S?.awaitingHuman&&!actionBusy&&humanTurnResolve)await hunterTurn()}catch(e){error=e;S.gameOver=true;endHumanTurn()}finally{scheduled=false}})}};
 showTurnNotice=async()=>{turns++;if(turns>800)throw Error('Turn limit 800');invariant()};
 const originalLoop=gameLoop;gameLoop=()=>{totalBlood=S.pool+S.players.reduce((n,t)=>n+t.hp,0);loopPromise=originalLoop()};
 await startGame();totalBlood=S.pool+S.players.reduce((n,t)=>n+t.hp,0);await loopPromise;if(error)throw error;invariant();
 return {ais:${ais},difficulty:'${diff}',seed:${seed},winner:S.winner?.human?'hunter':S.winner?'vampire':'draw',turns,humanTurns,used,actualDifficulty:aiDifficulty(),history};
 })()`;
 let timer;try{compiledGame.runInContext(c);return await Promise.race([vm.runInContext(script,c),new Promise((_,rej)=>{timer=setTimeout(()=>rej(Error('Timeout')),5000)})])}catch(e){return{ais,difficulty:diff,seed,error:e.stack,history:c.simLog.slice(-15),cardDiff:vm.runInContext("Object.entries(CARDS).map(([id,c])=>({id,expected:c.qty,actual:[...S.deck,...S.discard,...S.players.flatMap(p=>p.hand),...S.players.filter(p=>p.witches).map(()=> 'sorcieres')].filter(x=>x===id).length})).filter(x=>x.actual!==x.expected)",c)}}finally{clearTimeout(timer)}
}
module.exports={run};
if(require.main===module)(async()=>{for(const ais of [1,2,3,4])for(const diff of ['easy','normal','hard'])for(let k=0;k<repeats;k++)results.push(await run(ais,diff,Number(process.argv[5]||0)+9973+k*131+ais*100003));
const summary=[];for(const ais of [1,2,3,4])for(const difficulty of ['easy','normal','hard']){const a=results.filter(r=>r.ais===ais&&r.difficulty===difficulty);summary.push({ais,difficulty,games:a.length,wins:a.filter(r=>r.winner==='hunter').length,errors:a.filter(r=>r.error).length,avgTurns:Math.round(a.reduce((n,r)=>n+(r.turns||0),0)/a.length),actual:a.find(r=>!r.error)?.actualDifficulty})}fs.writeFileSync(process.argv[4]||'van-helsing-simulation-results.json',JSON.stringify({summary,results},null,2));console.log(JSON.stringify(summary,null,2));const errors=results.filter(r=>r.error);if(errors.length){console.log('ERRORS',JSON.stringify(errors.slice(0,8)));process.exitCode=1;}})();
