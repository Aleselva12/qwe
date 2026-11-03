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
    if(!['radici','tronco','ramo'].includes(path[0].role)||path.length>4)throw Error('Struttura non valida o più di quattro livelli');
    if(n.trunkLinks!==undefined&&(!Array.isArray(n.trunkLinks)||n.trunkLinks.some(id=>!byId.has(id)||trail(byId.get(id),byId)[0].role!=='tronco')))throw Error('Collegamento al tronco non valido');
  }
  for(const role of ['radici','tronco'])if(data.nodes.filter(n=>!n.parent&&n.role===role).length!==1)throw Error('Servono radici e un solo tronco');
  return data;
}
function commit(next){
  validate(next);localStorage.setItem(storage,JSON.stringify(next));plan=next;render();$('message').textContent='Pianta salvata in questo browser.';
}
function action(text,fn){const b=element('button',text);b.onclick=()=>{try{fn()}catch(e){$('message').textContent=e.message}};return b}
function badge(value){const b=element('span',labels[value]);b.className='badge '+value;return b}
function role(path){if(path.length===1)return path[0].role;if(path[0].role!=='ramo')return 'componente';return ['','', 'stella','pianeta','luna'][path.length]}
function edit(id,parent,top=false){
  const n=plan.nodes.find(n=>n.id===id);const form=element('dialog');document.body.append(form);
  const title=element('input'),note=element('textarea'),priority=element('select'),position=element('select'),links=element('select');links.multiple=true;
  function field(label,control){const l=element('label',label+' ');l.append(control);form.append(l)}
  function option(control,value,text){const o=element('option',text);o.value=value;control.append(o)}
  title.value=n?.title||'';note.value=n?.note||'';field('Nome',title);field('Scopo e piani',note);
  for(const k of ranks)option(priority,k,labels[k]);priority.value=n?.priority||'unknown';field('Priorità propria',priority);
  const map=new Map(plan.nodes.map(x=>[x.id,x]));
  const fixed=n&&!n.parent&&['radici','tronco'].includes(n.role);
  if(!fixed){option(position,'','Ramo autonomo');for(const p of plan.nodes){const path=trail(p,map);if(path.length<4&&!path.some(x=>x.id===id))option(position,p.id,path.map(x=>x.title).join(' / '))}position.value=n?.parent||parent||'';field('Collocazione',position)}
  for(const p of plan.nodes)if(p.parent&&trail(p,map)[0].role==='tronco'){option(links,p.id,p.title);links.lastChild.selected=(n?.trunkLinks||[]).includes(p.id)}
  if(links.options.length)field('Componenti del tronco utilizzati',links);
  form.append(action('Salva',()=>{const next=structuredClone(plan);let dst=next.nodes.find(x=>x.id===id);if(!dst){dst={id:crypto.randomUUID()};next.nodes.push(dst)}Object.assign(dst,{title:title.value.trim(),note:note.value,priority:priority.value,trunkLinks:Array.from(links.selectedOptions,o=>o.value)});if(!fixed){if(position.value){dst.parent=position.value;delete dst.role}else{delete dst.parent;dst.role='ramo'}}commit(next);form.close()}),action('Annulla',()=>form.close()));
  form.onclose=()=>form.remove();form.showModal();
}
function render(){
 const host=$('tree');host.replaceChildren();const byId=new Map(plan.nodes.map(n=>[n.id,n]));
 function draw(n){const path=trail(n,byId),box=element('details'),s=element('summary');box.open=path.length===1;s.append(document.createTextNode(role(path)+' · '+n.title+' '),badge(n.priority||'unknown'));box.append(s);
 if(n.note)box.append(element('p',n.note));for(const id of n.trunkLinks||[])box.append(element('p','Usa dal tronco: '+byId.get(id).title));
 box.append(action('Modifica o sposta',()=>edit(n.id)));if(path.length<4)box.append(action('Aggiungi sottopunto',()=>edit(null,n.id)));
 for(const child of plan.nodes.filter(x=>x.parent===n.id))box.append(draw(child));return box}
 for(const n of plan.nodes.filter(x=>!x.parent)){const card=element('article');card.append(draw(n));host.append(card)}
}
async function start(){const saved=localStorage.getItem(storage);plan=validate(saved?JSON.parse(saved):await (await fetch('/cora-plan.json')).json());render();
 for(const k of ranks)$('legend').append(badge(k),document.createTextNode(' '));
 $('add').onclick=()=>edit(null);$('export').onclick=()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(plan,null,2)],{type:'application/json'}));const a=element('a');a.href=url;a.download='cora-plan.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
 $('import').onchange=async e=>{try{const file=e.target.files[0];if(file&&confirm('Sostituire la pianta locale con quella importata?'))commit(JSON.parse(await file.text()))}catch(err){$('message').textContent=err.message}finally{e.target.value=''}}}
start().catch(e=>$('message').textContent=e.message);
