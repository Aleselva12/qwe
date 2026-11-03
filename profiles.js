/* Declarative work profiles. No executable hooks, network requests or shell commands. */
(function(root){
'use strict';
const base={schema_version:1,name:'Albero CodeAtlas',default_view:'graph',categories:[
{id:'roots',label:'Radici',color:'#b495ff'},{id:'trunk',label:'Tronco',color:'#63b4ff'},
{id:'branches',label:'Rami',color:'#63e1bf'},{id:'unassigned',label:'Da classificare',color:'#e6bd72'}],fields:[],nodes:[],rules:[],test_links:[]};
const views=['graph','text','network','layers','matrix','files'];
const safe=id=>typeof id==='string'&&/^[a-z][a-z0-9_-]{0,63}$/.test(id)&&!['constructor','prototype','__proto__'].includes(id);
function validate(p){
 if(!p||p.schema_version!==1||typeof p.name!=='string'||!p.name.trim()||!views.includes(p.default_view||'graph'))throw Error('Profilo: versione, nome o vista non validi.');
 for(const key of ['categories','fields','nodes','rules','test_links'])if(p[key]!==undefined&&!Array.isArray(p[key]))throw Error('Profilo: '+key+' deve essere una lista.');
 for(const key of ['categories','fields']){const seen=new Set();for(const x of p[key]||[]){if(!x||!safe(x.id)||seen.has(x.id)||typeof x.label!=='string'||!x.label.trim())throw Error('Campo/categoria non valido o duplicato.');if(key==='categories'&&!/^#[0-9a-f]{6}$/i.test(x.color))throw Error('Colore non valido: usa #RRGGBB.');seen.add(x.id)}}
 const ids=new Set();for(const n of p.nodes||[]){if(!n||typeof n.id!=='string'||!n.id||ids.has(n.id)||typeof n.name!=='string'||!n.name||!['manual','ai_suggestion'].includes(n.source)||!['idea','planned','in_progress','implemented','verified','blocked','unknown'].includes(n.status))throw Error('Nodo profilo: ID, nome, provenienza e stato obbligatori.');ids.add(n.id)}
 for(const r of p.rules||[])if(!r||typeof r.path_glob!=='string'||!r.path_glob||r.path_glob.length>300||typeof r.group_id!=='string')throw Error('Regola di raggruppamento non valida.');
 for(const l of p.test_links||[])if(!l||typeof l.group_id!=='string'||!['manual','ai_suggestion'].includes(l.source)||!['name','classname','file'].some(k=>typeof l[k]==='string'&&l[k])||['name','classname','file'].some(k=>l[k]!==undefined&&typeof l[k]!=='string'))throw Error('Associazione test non valida: serve almeno un selettore esatto e la provenienza.');
 return p;
}
function normalize(p){validate(p);const categories=base.categories.map(c=>({...c}));for(const c of p.categories||[]){const i=categories.findIndex(x=>x.id===c.id);if(i<0)categories.push({...c});else categories[i]={...c}}return {...structuredClone(base),...structuredClone(p),categories};}
function glob(pattern,path){const escaped=pattern.split('**').map(part=>part.split('*').map(s=>s.replace(/[.+?^${}()|[\]\\]/g,'\\$&')).join('[^/]*')).join('.*');return new RegExp('^'+escaped+'$').test(path)}
function apply(map,p,atlas){
 const profile=normalize(p),next=structuredClone(map);next.profile=profile;
 for(const node of profile.nodes){const i=next.groups.findIndex(n=>n.id===node.id);if(i<0)next.groups.push({parent:null,lens:'unassigned',code_refs:[],issues:[],...structuredClone(node)});else next.groups[i]={...next.groups[i],...structuredClone(node)};}
 for(const rule of profile.rules){const node=next.groups.find(n=>n.id===rule.group_id);if(!node)throw Error('Regola riferita a un nodo inesistente: '+rule.group_id);const refs=atlas.nodes.filter(n=>n.kind==='file'&&glob(rule.path_glob,n.path)).map(n=>n.id);node.code_refs=[...new Set([...(node.code_refs||[]),...refs])];node.source=node.source==='ai_suggestion'?'ai_suggestion':'manual';}
 for(const l of profile.test_links)if(!next.groups.some(n=>n.id===l.group_id))throw Error('Test associato a nodo inesistente: '+l.group_id);
 return next;
}
function diff(before,after){const old=new Map(before.groups.map(n=>[n.id,n])),current=new Set(after.groups.map(n=>n.id));return {added:after.groups.filter(n=>!old.has(n.id)).map(n=>n.name),changed:after.groups.filter(n=>old.has(n.id)&&JSON.stringify(old.get(n.id))!==JSON.stringify(n)).map(n=>n.name),removed:before.groups.filter(n=>!current.has(n.id)).map(n=>n.name)}}
const api={base,normalize,validate,apply,diff,glob};if(typeof module!=='undefined')module.exports=api;else root.AtlasProfiles=api;
})(globalThis);
