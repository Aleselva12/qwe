/* Test outcomes are evidence about individual cases, never a global health badge. */
(function(root){
'use strict';
function validate(run){
 if(!run||run.schema_version!==1||typeof run.id!=='string'||!run.id||typeof run.source_file!=='string'||!Array.isArray(run.test_cases)||run.test_cases.length>50000||!run.metadata||typeof run.metadata!=='object')throw Error('Report di verifica non valido.');
 for(const k of ['commit','environment','executed_at'])if(run.metadata[k]!==undefined&&typeof run.metadata[k]!=='string')throw Error('Metadati verifica non validi.');
 if(run.metadata.workspace_clean!==undefined&&typeof run.metadata.workspace_clean!=='boolean')throw Error('workspace_clean deve essere booleano.');
 const ids=new Set();for(const c of run.test_cases){if(!c||typeof c.id!=='string'||ids.has(c.id)||typeof c.name!=='string'||!['pass','fail','skip'].includes(c.result)||['classname','file','message'].some(k=>c[k]!==undefined&&typeof c[k]!=='string'))throw Error('Caso di test non valido o duplicato.');ids.add(c.id)}return run;
}
function freshness(run,version){const m=run.metadata;if(!m.commit||!version?.commit)return 'Versione non verificabile';if(m.commit!==version.commit)return 'Versione diversa dal codice attuale';if(version.dirty!==false||m.workspace_clean!==true)return 'Commit coincidente; modifiche locali non escluse';return 'Commit coincidente; provenienza dichiarata, non autenticata';}
function associated(run,node,profile,atlas){
 const paths=new Set((node.code_refs||[]).map(id=>atlas.nodes.find(n=>n.id===id)?.path).filter(Boolean));const links=(profile.test_links||[]).filter(l=>l.group_id===node.id);
 return run.test_cases.flatMap(c=>{const link=links.find(l=>['name','classname','file'].every(k=>!l[k]||l[k]===c[k]));if(link)return [{...c,association:link.source==='manual'?'Associazione dichiarata':'Associazione proposta dall’IA'}];if(c.file&&paths.has(c.file))return [{...c,association:'Corrispondenza esatta del percorso del test; non copertura della funzione'}];return []});
}
function changes(previous,current){if(!previous)return [];const old=new Map(previous.test_cases.map(c=>[c.id,c]));return current.test_cases.filter(c=>old.has(c.id)&&old.get(c.id).result!==c.result).map(c=>({name:c.name,before:old.get(c.id).result,after:c.result}));}
function summary(cases){return Object.fromEntries(['pass','fail','skip'].map(s=>[s,cases.filter(c=>c.result===s).length]));}
const api={validate,freshness,associated,changes,summary};if(typeof module!=='undefined')module.exports=api;else root.AtlasEvidence=api;
})(globalThis);
