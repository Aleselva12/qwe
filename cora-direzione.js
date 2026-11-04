'use strict';
const labels={unknown:'Da valutare',ok:'Tutto ok',plan:'Aggiornamento previsto',minor:'Problema minore',problem:'Problema'};
const ranks=Object.keys(labels);
const storage='codeatlas:cora:direction:v1';
let plan;
const $=id=>document.getElementById(id);
function element(tag,text){const item=document.createElement(tag);if(text!==undefined)item.textContent=text;return item}
function trail(node,byId){
  const path=[],seen=new Set();
  while(node){
    if(seen.has(node.id))throw Error('Gerarchia ciclica');
    path.unshift(node);seen.add(node.id);
    if(!node.parent)break;
    node=byId.get(node.parent);if(!node)throw Error('Genitore assente');
  }
  return path;
}
function validate(data){
  if(data?.version!==1||!Array.isArray(data.nodes))throw Error('Formato pianta non valido');
  const byId=new Map();
  for(const n of data.nodes){
    if(!n||typeof n.id!=='string'||!n.id||byId.has(n.id)||typeof n.title!=='string'||!n.title.trim()||!ranks.includes(n.priority??'unknown'))throw Error('Nodo o priorità non validi');
    byId.set(n.id,n);
  }
  for(const n of data.nodes){
    const path=trail(n,byId);
    if(!['radici','tronco','ramo'].includes(path[0].role)||path.length>(path[0].role==='radici'?5:4))throw Error('Struttura non valida o livelli eccedenti: '+n.id);
    if(n.trunkLinks!==undefined&&(!Array.isArray(n.trunkLinks)||n.trunkLinks.some(id=>!byId.has(id)||trail(byId.get(id),byId)[0].role!=='tronco')))throw Error('Collegamento al tronco non valido');
  }
  if(data.relations!==undefined){
    if(!Array.isArray(data.relations))throw Error('Collegamenti non validi');
    for(const link of data.relations)if(!byId.has(link.from)||!byId.has(link.to)||!['uses','depends_on','communicates_with','produces_for'].includes(link.kind))throw Error('Collegamento non valido tra stelle');
  }
  for(const role of ['radici','tronco'])if(data.nodes.filter(n=>!n.parent&&n.role===role).length!==1)throw Error('Servono radici e un solo tronco');
  return data;
}
function commit(next){
  validate(next);localStorage.setItem(storage,JSON.stringify(next));plan=next;render();$('message').textContent='Pianta salvata in questo browser.';
}
function action(text,fn){const b=element('button',text);b.onclick=()=>{try{fn()}catch(e){$('message').textContent=e.message}};return b}
function badge(value){const b=element('span',labels[value]);b.className='badge '+value;return b}
function role(path){if(path.length===1)return path[0].role;return (path[0].role==='radici'?['','', 'area','stella','pianeta','luna']:['','','stella','pianeta','luna'])[path.length]||'componente'}
function edit(id,parent,top=false){
  const n=plan.nodes.find(n=>n.id===id);const form=element('dialog');document.body.append(form);
  const criteria=element('textarea');const title=element('input'),note=element('textarea'),priority=element('select'),position=element('select'),links=element('select');links.multiple=true;
  function field(label,control){const l=element('label',label+' ');l.append(control);form.append(l)}
  function option(control,value,text){const o=element('option',text);o.value=value;control.append(o)}
  title.value=n?.title||'';note.value=n?.note||'';field('Nome',title);field('Scopo e piani',note);criteria.value=(n?.completionCriteria||[]).join('\n');field('Criteri di chiusura (uno per riga)',criteria);
  for(const k of ranks)option(priority,k,labels[k]);priority.value=n?.priority||'unknown';field('Priorità propria',priority);
  const map=new Map(plan.nodes.map(x=>[x.id,x]));
  const fixed=n&&!n.parent&&['radici','tronco'].includes(n.role);
  if(!fixed){option(position,'','Ramo autonomo');for(const p of plan.nodes){const path=trail(p,map);if(path.length<(path[0].role==='radici'?5:4)&&!path.some(x=>x.id===id))option(position,p.id,path.map(x=>x.title).join(' / '))}position.value=n?.parent||parent||'';field('Collocazione',position)}
  for(const p of plan.nodes)if(p.parent&&trail(p,map)[0].role==='tronco'){option(links,p.id,p.title);links.lastChild.selected=(n?.trunkLinks||[]).includes(p.id)}
  if(links.options.length)field('Componenti del tronco utilizzati',links);
  form.append(action('Salva',()=>{const next=structuredClone(plan);let dst=next.nodes.find(x=>x.id===id);if(!dst){dst={id:crypto.randomUUID()};next.nodes.push(dst)}Object.assign(dst,{title:title.value.trim(),note:note.value,completionCriteria:criteria.value.split('\n').map(x=>x.trim()).filter(Boolean),priority:priority.value,trunkLinks:Array.from(links.selectedOptions,o=>o.value)});if(!fixed){if(position.value){dst.parent=position.value;delete dst.role}else{delete dst.parent;dst.role='ramo'}}const byId=new Map(next.nodes.map(x=>[x.id,x]));for(const x of next.nodes){const r=role(trail(x,byId));if(['area','stella','pianeta','luna'].includes(r))x.classification=({area:'area',stella:'star',pianeta:'planet',luna:'moon'})[r];else delete x.classification}commit(next);form.close()}),action('Annulla',()=>form.close()));
  form.onclose=()=>form.remove();form.showModal();
}
function renderTree(){
 const host=$('tree');host.replaceChildren();const byId=new Map(plan.nodes.map(n=>[n.id,n]));
 function draw(n){const path=trail(n,byId),box=element('details'),s=element('summary');box.open=path.length<=(path[0].role==='radici'?2:1);s.append(document.createTextNode(role(path)+' · '+n.title+' '),badge(n.priority||'unknown'));box.append(s);
 if(n.note)box.append(element('p',n.note));for(const id of n.trunkLinks||[])box.append(element('p','Usa dal tronco: '+byId.get(id).title));
 box.append(action('Modifica o sposta',()=>edit(n.id)));if(path.length<(path[0].role==='radici'?5:4))box.append(action('Aggiungi sottopunto',()=>edit(null,n.id)));
 for(const child of plan.nodes.filter(x=>x.parent===n.id))box.append(draw(child));return box}
 for(const n of plan.nodes.filter(x=>!x.parent)){const card=element('article');card.append(draw(n));host.append(card)}
}
let selected=null,focusStar=null,expandedPlanet=null,textMode=false,zoom=1,pan={x:0,y:0};
const colors={unknown:'#8290a4',ok:'#63d6a0',plan:'#f5d46c',minor:'#ffa35c',problem:'#ff6d7c'};
let indexedPlan,indexedNodes;
function index(){if(indexedPlan!==plan){indexedPlan=plan;indexedNodes=new Map(plan.nodes.map(n=>[n.id,n]))}return indexedNodes}
function children(id){return plan.nodes.filter(n=>n.parent===id)}
function kind(n){return role(trail(n,index()))}
function effective(n){
 const causes=[];let priority=n.priority||'unknown';
 if(kind(n)==='stella')for(const other of plan.nodes){if(other.id!==n.id&&['minor','problem'].includes(other.priority)&&trail(other,index()).some(p=>p.id===n.id)){causes.push(other);if(ranks.indexOf(other.priority)>ranks.indexOf(priority))priority=other.priority}}
 return {priority,causes};
}
function select(id){selected=id;const path=trail(index().get(id),index()),star=path.find(n=>kind(n)==='stella');focusStar=star?.id||null;expandedPlanet=path.find(n=>kind(n)==='pianeta')?.id||null;zoom=1;pan={x:0,y:0};render()}
function overview(){selected=null;focusStar=null;expandedPlanet=null;zoom=1;pan={x:0,y:0};textMode=false;render()}
function svg(tag,attrs={},text){const n=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;return n}
function lines(text,max=24){const words=text.split(/\s+/),out=[''];for(const word of words){if((out.at(-1)+' '+word).trim().length>max&&out.at(-1))out.push(word);else out[out.length-1]+=(out.at(-1)?' ':'')+word}return out}
function drawMap(){
 const host=$('map');host.replaceChildren();const width=1400,height=focusStar?1120:1450;host.setAttribute('viewBox',`0 0 ${width} ${height}`);
 const scene=svg('g',{transform:`translate(${pan.x} ${pan.y}) translate(700 640) scale(${zoom}) translate(-700 -640)`});host.append(scene);const edges=svg('g'),nodes=svg('g');scene.append(edges,nodes);const positions=new Map();
 function line(a,b,cross=false){edges.append(svg('path',{d:`M${a.x},${a.y} Q${a.x},${(a.y+b.y)/2} ${b.x},${b.y}`,class:cross?'edge cross':'edge'}))}
 function point(n,x,y,size=8){positions.set(n.id,{x,y});const color=colors[effective(n).priority];const g=svg('g',{class:'node',tabindex:0,role:'button','aria-label':`${kind(n)} ${n.title}: ${labels[effective(n).priority]}`,'data-id':n.id,transform:`translate(${x} ${y})`});g.append(svg('circle',{r:size+12,fill:color,class:'halo'}),svg('circle',{r:size+4,fill:'none',stroke:color,'stroke-opacity':.4}),svg('circle',{r:size,fill:color}));const text=svg('text',{'text-anchor':'middle',y:size+26,'font-size':size>8?19:17});lines(n.title,focusStar?27:22).forEach((t,i)=>text.append(svg('tspan',{x:0,dy:i?21:0},t)));g.append(text);if(n.id===selected)g.append(svg('circle',{r:size+8,fill:'none',stroke:'#bcefff','stroke-width':2}));g.onclick=()=>select(n.id);g.onkeydown=e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();select(n.id)}};nodes.append(g)}
 function heading(text,x,y){nodes.append(svg('text',{x,y,'font-size':13,'letter-spacing':2,fill:'#718aa6'},text.toUpperCase()))}
 if(!focusStar){
 const branches=plan.nodes.filter(n=>!n.parent&&n.role==='ramo');heading('RAMI · LE FUNZIONI DI CORA',40,35);
 branches.forEach((b,i)=>{const x=105+i*(1190/Math.max(1,branches.length-1));const title=svg('text',{x,y:76,'text-anchor':'middle','font-size':14});lines(b.title,20).forEach((t,j)=>title.append(svg('tspan',{x,dy:j?18:0},t)));nodes.append(title);let prev={x,y:110};children(b.id).forEach((n,j)=>{const p={x,y:155+j*96};line(prev,p);point(n,p.x,p.y);prev=p})});
 heading('TRONCO · CAPACITÀ COMUNI',40,650);const trunk=plan.nodes.find(n=>n.role==='tronco');children(trunk.id).forEach((n,i)=>{const x=105+(i%7)*198,y=705+Math.floor(i/7)*100;if(i%7)line({x:x-198,y},{x,y});point(n,x,y)});
 heading('RADICI · LE BASI DEL PROGETTO',40,900);const root=plan.nodes.find(n=>n.role==='radici');children(root.id).forEach((area,i)=>{const x=115+i*232;const label=svg('text',{x,y:940,'text-anchor':'middle','font-size':14});lines(area.title,24).forEach((t,j)=>label.append(svg('tspan',{x,dy:j?18:0},t)));nodes.append(label);children(area.id).forEach((n,j)=>point(n,x,1025+j*95,6))});
 }else{
 const star=index().get(focusStar);heading('DENTRO LA STELLA · SELEZIONA UN PIANETA',40,40);point(star,700,440,15);
 const planets=children(star.id);planets.forEach((n,i)=>{const angle=-Math.PI/2+i*2*Math.PI/Math.max(1,planets.length),p={x:700+430*Math.cos(angle),y:440+280*Math.sin(angle)};line({x:700,y:440},p);point(n,p.x,p.y,9)});
 if(expandedPlanet){heading('LUNE · '+index().get(expandedPlanet).title,80,845);const moons=children(expandedPlanet);moons.forEach((n,i)=>{const p={x:150+(i%5)*270,y:910+Math.floor(i/5)*100};line(positions.get(expandedPlanet),p);point(n,p.x,p.y,6)})}
 }
 if(selected){for(const rel of plan.relations||[]){if(rel.from===selected||rel.to===selected){const a=positions.get(rel.from),b=positions.get(rel.to);if(a&&b)line(a,b,true)}}}
}
function inspector(){
 const host=$('inspector');host.replaceChildren();const n=index().get(selected);
 if(!n){host.append(element('div','LA PIANTA DEL PROGETTO'),element('h2','Uno sguardo su Cora'),element('p','Ciò che esiste, ciò che manca e ciò che vogliamo costruire. Ogni stella è un punto importante del progetto, non un file di codice.'));host.firstChild.className='eyebrow';const stars=plan.nodes.filter(n=>kind(n)==='stella');host.append(element('p',`${stars.length} stelle · ${plan.nodes.filter(n=>kind(n)==='pianeta').length} pianeti · ${plan.nodes.filter(n=>kind(n)==='luna').length} lune`),element('h3','Esplora senza sovrappopolare'),element('p','Seleziona una stella per aprire i pianeti. Entra in un pianeta per vedere le lune. La panoramica mantiene stabile il tronco e separa rami e radici.'),element('h3','Priorità e realtà'),element('p','Grigio significa da valutare. I colori sono dichiarati: un problema arancione o rosso su un discendente segnala anche la sua stella. La presenza nella pianta non prova il funzionamento su Debian.'),element('p','Trascina lo spazio per spostare la mappa; usa + e − per lo zoom.'));return}
 const path=trail(n,index());host.append(element('div',path.map(p=>p.code||p.title).join(' / ')),element('h2',n.title),badge(effective(n).priority));host.firstChild.className='eyebrow';
 function section(title,items,empty){host.append(element('h3',title));if(!items?.length){host.append(element('p',empty||'Non ancora documentato.'));return}const list=element('ul');for(const item of items)list.append(element('li',typeof item==='string'?item:JSON.stringify(item)));host.append(list)}
 host.append(element('p',n.note||'Scopo da definire.'),element('p','Stato dichiarato: '+(n.status||'da valutare')+' · '+kind(n)));
 const eff=effective(n);if(eff.causes.length){host.append(element('h3','Problemi nei discendenti'));for(const cause of eff.causes)host.append(action(labels[cause.priority]+' · '+cause.title,()=>select(cause.id)))}
 section('Problemi e dubbi',n.knownIssues,'Nessun problema documentato qui; non equivale a un collaudo.');
 section('Passato',n.timeline?.past,'Storia ancora da documentare.');section('Presente',[n.timeline?.present?.statement||n.note||'Da definire']);host.append(element('p',n.timeline?.present?.runtimeVerified?'Verifica runtime dichiarata nella pianta.':'Funzionamento runtime non verificato da questa mappa.'));
 section('Futuro',n.timeline?.future,'Obiettivi futuri da definire.');section('Cosa serve per chiudere questo punto',n.completionCriteria,'Criteri di chiusura da concordare; nessuna chiusura automatica.');
 if(n.observations?.length)section('Osservazioni e provenienza',n.observations.map(o=>`${o.text} — ${o.type||'fonte non indicata'}; versione: ${o.commit||'non indicata'}; data: ${o.observedAt||'non indicata'}`));
 if(n.roadmapRefs?.length)section('Roadmap',n.roadmapRefs);
 const links=(plan.relations||[]).filter(r=>r.from===n.id||r.to===n.id);if(links.length){host.append(element('h3','Collegamenti concettuali'));for(const l of links){const target=l.from===n.id?l.to:l.from;host.append(action(index().get(target).title,()=>select(target)),element('p',l.note||l.kind))}}
 if(children(n.id).length){host.append(element('h3','Esplora'));for(const c of children(n.id))host.append(action(c.title,()=>select(c.id)))}
 host.append(element('h3','Cura della pianta'),action('Modifica o sposta',()=>edit(n.id)));if(path.length<(path[0].role==='radici'?5:4))host.append(action('Aggiungi sottopunto',()=>edit(null,n.id)));
}
function render(){if(selected&&!index().has(selected))selected=null;$('canvas').hidden=textMode;$('tree').hidden=!textMode;if(textMode)renderTree();else drawMap();inspector()}
function download(data,name='cora-plan.json'){const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=element('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
async function start(){
 const response=await fetch('/cora-plan.json');if(!response.ok)throw Error('Impossibile caricare la pianta Cora');const template=validate(await response.json());let saved=null;
 try{saved=localStorage.getItem(storage);plan=saved?validate(JSON.parse(saved)):template}catch(e){plan=template;$('message').textContent='Pianta locale non leggibile: mostro la versione distribuita senza cancellare i dati locali.'}
 if(saved&&plan.revision!==template.revision){const box=$('recovery');box.append(element('span','Hai una pianta locale di una revisione diversa. '),action('Esporta copia locale',()=>download(JSON.parse(saved),'cora-copia-locale.json')),action('Apri la pianta Cora aggiornata',()=>{localStorage.setItem(storage+':backup:'+Date.now(),saved);commit(structuredClone(template));box.replaceChildren();overview()}));}
 render();for(const k of ranks)$('legend').append(badge(k));
 $('overview').onclick=overview;$('back').onclick=overview;$('fit').onclick=()=>{zoom=1;pan={x:0,y:0};drawMap()};$('text-view').onclick=()=>{textMode=!textMode;render()};
 $('zoom-in').onclick=()=>{zoom=Math.min(3,zoom*1.25);drawMap()};$('zoom-out').onclick=()=>{zoom=Math.max(.5,zoom/1.25);drawMap()};
 let drag=null;const map=$('map');map.onpointerdown=e=>{if(e.target.closest('.node'))return;drag={x:e.clientX,y:e.clientY,px:pan.x,py:pan.y};map.setPointerCapture(e.pointerId)};map.onpointermove=e=>{if(!drag)return;const scale=Math.min(map.clientWidth/1400,map.clientHeight/(focusStar?1120:1450));pan={x:drag.px+(e.clientX-drag.x)/scale,y:drag.py+(e.clientY-drag.y)/scale};drawMap()};map.onpointerup=map.onpointercancel=()=>drag=null;
 $('search').oninput=e=>{const host=$('results');host.replaceChildren();const query=e.target.value.trim().toLocaleLowerCase();if(!query)return;const matches=plan.nodes.filter(n=>(n.title+' '+(n.note||'')).toLocaleLowerCase().includes(query));for(const n of matches.slice(0,30))host.append(action(n.title,()=>{textMode=false;select(n.id);host.replaceChildren();$('search').value=''}));if(!matches.length)host.append(element('p','Nessun punto trovato.'))};
 $('backups').onclick=()=>{const dialog=element('dialog');dialog.append(element('h2','Copie locali'));const keys=Object.keys(localStorage).filter(k=>k.startsWith(storage+':backup:')).sort().reverse();for(const key of keys)dialog.append(action('Esporta copia '+new Date(Number(key.split(':').at(-1))).toLocaleString(),()=>download(JSON.parse(localStorage.getItem(key)),'cora-recupero.json')));if(!keys.length)dialog.append(element('p','Nessuna copia di sicurezza presente.'));dialog.append(action('Chiudi',()=>dialog.close()));dialog.onclose=()=>dialog.remove();document.body.append(dialog);dialog.showModal()};$('add').onclick=()=>edit(null);$('export').onclick=()=>download(plan);$('import-button').onclick=()=>$('import').click();
 $('import').onchange=async e=>{try{const file=e.target.files[0];if(file){const next=validate(JSON.parse(await file.text()));if(confirm('Sostituire la pianta locale? Una copia di sicurezza rimarrà in questo browser.')){if(localStorage.getItem(storage))localStorage.setItem(storage+':backup:'+Date.now(),localStorage.getItem(storage));commit(next);overview()}}}catch(err){$('message').textContent=err.message}finally{e.target.value=''}};
}
start().catch(e=>$('message').textContent=e.message);
