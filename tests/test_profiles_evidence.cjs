const {test}=require('node:test'),assert=require('node:assert/strict');
const P=require('../profiles.js'),E=require('../evidence.js');
const base={schema_version:1,groups:[{id:'core',name:'Core',lens:'trunk',code_refs:[]}],relations:[]};
test('Profiles extend categories, rename defaults and match paths without executing code',()=>{
 const profile={schema_version:1,name:'Customer support',categories:[{id:'trunk',label:'Servizi',color:'#123456'},{id:'customer',label:'Clienti',color:'#abcdef'}],fields:[{id:'owner',label:'Responsabile'}],nodes:[{id:'crm',name:'CRM futuro',lens:'customer',source:'ai_suggestion',status:'planned'}],rules:[{path_glob:'src/**',group_id:'crm'}]};
 const before=JSON.stringify(base),next=P.apply(base,profile,{nodes:[{id:'file:src/db/a.py',path:'src/db/a.py',kind:'file'},{id:'file:tests/a.py',path:'tests/a.py',kind:'file'}]});
 assert.equal(JSON.stringify(base),before);assert.equal(next.groups[1].status,'planned');assert.deepEqual(next.groups[1].code_refs,['file:src/db/a.py']);assert.equal(next.profile.categories.find(c=>c.id==='trunk').label,'Servizi');assert.deepEqual(P.diff(base,next).added,['CRM futuro']);
 assert.ok(P.glob('src/*.py','src/a.py'));assert.ok(!P.glob('src/*.py','src/sub/a.py'));assert.ok(P.glob('file[1].py','file[1].py'));
});
test('Invalid profiles and broken mappings rejected',()=>{
 for(const p of [{schema_version:2,name:'x'}, {...P.base,categories:[{id:'__proto__',label:'x',color:'#ffffff'}]}, {...P.base,categories:[{id:'x',label:'X',color:'red'}]}, {...P.base,test_links:[{group_id:'core',source:'manual'}]}])assert.throws(()=>P.validate(p));
 assert.throws(()=>P.apply(base,{...P.base,rules:[{path_glob:'*',group_id:'missing'}]},{nodes:[]}));
});
function run(){return {schema_version:1,id:'run',source_file:'junit.xml',metadata:{commit:'abc',workspace_clean:true},test_cases:[{id:'case',name:'save',classname:'Suite',file:'tests/test_save.py',result:'pass'}]}}
test('Passing test is never proof of freshness when commit or dirty state is unknown',()=>{
 const r=run();assert.match(E.freshness(r,{commit:'other',dirty:false}),/diversa/);assert.match(E.freshness(r,{commit:'abc',dirty:true}),/non escluse/);assert.match(E.freshness(r,{commit:'abc',dirty:false}),/non autenticata/);assert.match(E.freshness({...r,metadata:{}},{commit:'abc',dirty:false}),/non verificabile/);
});
test('Exact explicit links are separate from AI proposals and test-file matches',()=>{
 const r=run(),node={id:'core',code_refs:['file:src/save.py']},atlas={nodes:[{id:'file:src/save.py',path:'src/save.py'}]};
 assert.equal(E.associated(r,node,{test_links:[]},atlas).length,0);
 assert.match(E.associated(r,node,{test_links:[{group_id:'core',name:'save',classname:'Suite',source:'ai_suggestion'}]},atlas)[0].association,/IA/);
 assert.equal(E.associated(r,node,{test_links:[{group_id:'core',name:'save',classname:'Other',source:'manual'}]},atlas).length,0);
 assert.match(E.associated(r,{id:'test',code_refs:['file:t']},{},{nodes:[{id:'file:t',path:'tests/test_save.py'}]})[0].association,/non copertura/);
});
test('Comparisons identify changed results by stable test ID; unknown/new cases are not passes',()=>{
 const old=run(),current=run();current.test_cases[0].result='fail';current.test_cases.push({id:'new',name:'new',result:'skip'});assert.deepEqual(E.changes(old,current),[{name:'save',before:'pass',after:'fail'}]);assert.deepEqual(E.summary(current.test_cases),{pass:0,fail:1,skip:1});assert.throws(()=>E.validate({...old,test_cases:[...old.test_cases,...old.test_cases]}));
});
