const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const {JSDOM}=require('jsdom');
const root=path.join(__dirname,'..');
function setup(){
 const html=fs.readFileSync(path.join(root,'index.html'),'utf8'),dom=new JSDOM(html,{runScripts:'outside-only',url:'http://localhost:8765'}),w=dom.window,context=dom.getInternalVMContext();
 w.ResizeObserver=class{observe(){}};w.HTMLCanvasElement.prototype.getContext=()=>({font:'',measureText:t=>({width:t.length*7})});
 w.structuredClone=structuredClone;w.fetch=async()=>({ok:false});w.TextEncoder=TextEncoder;Object.defineProperty(w.crypto,'subtle',{value:require('node:crypto').webcrypto.subtle});w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false};
 for(const file of ['views.js','profiles.js','evidence.js','workbench.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),context);
 vm.runInContext(html.split('<script>')[1].split('</script>')[0],context);
 const report={project_key:'test',version:{commit:'abc',dirty:false},overlay:{schema_version:1,groups:[{id:'core',name:'Core',lens:'trunk',code_refs:['file:app.py']}],relations:[]},atlas:{project:'Test',nodes:[{id:'project',name:'Test',path:'.',kind:'project'},{id:'file:app.py',parent:'project',name:'app.py',path:'app.py',kind:'file'}],edges:[],errors:[]},intelligence:{tests:{test_files:['tests/test_app.py'],configurations:['pytest.ini']}}};
 w.load(report);return {dom,w,context,report};
}
const button=(w,text)=>[...w.document.querySelectorAll('button')].find(b=>b.textContent===text);
test('Profile preview is non-mutating, applies custom category/fields and persists across rescans; undo restores',()=>{
 const {dom,w,context,report}=setup();try{
 const p={schema_version:1,name:'CRM',categories:[{id:'customers',label:'Clienti',color:'#abcdef'}],fields:[{id:'owner',label:'Responsabile'}],nodes:[{id:'crm',name:'CRM futuro',lens:'customers',source:'ai_suggestion',status:'planned'}]};
 const candidate=w.AtlasProfiles.apply(vm.runInContext('map',context),p,report.atlas);w.previewMap(candidate,'Preview');assert.equal(vm.runInContext('map.groups.length',context),1);button(w,'Applica modifiche').onclick();assert.equal(vm.runInContext('map.groups.length',context),2);assert.match(w.document.querySelector('#legend').textContent,/Clienti/);assert.equal(w.document.querySelectorAll('#graph .node').length,2);
 w.load(report);assert.equal(vm.runInContext('map.groups.length',context),2);w.choose(vm.runInContext('map.groups.find(n=>n.id==="crm")',context));assert.match(w.document.querySelector('#inspector').textContent,/Responsabile/);assert.match(w.document.querySelector('#inspector').textContent,/proposta IA/);
 w.showProfiles();button(w,'Ripristina precedente').onclick();button(w,'Applica modifiche').onclick();assert.equal(vm.runInContext('map.groups.length',context),1);
 }finally{dom.window.close()}
});
test('JUnit imports, explicit mapping, stale version, duplicate rejection and persistent evidence',async()=>{
 const {dom,w,context,report}=setup();try{
 const xml='<testsuite><testcase name="save" classname="Suite"><failure message="broken"/></testcase><testcase name="skip"><skipped/></testcase></testsuite>';
 const run=await w.parseJUnit({name:'report.xml',size:xml.length,text:async()=>xml});assert.equal(run.test_cases[0].result,'fail');assert.equal(run.metadata.commit,'');w.stageRun(run);button(w,'Importa risultato').onclick();assert.match(w.document.querySelector('#panelBody').textContent,/1 falliti/);assert.match(w.document.querySelector('#panelBody').textContent,/Versione non verificabile/);
 w.document.querySelector('.testCase select').value='core';button(w,'Associa').onclick();w.load(report);w.choose(vm.runInContext('map.groups[0]',context));assert.match(w.document.querySelector('#inspector').textContent,/1 falliti/);assert.match(w.document.querySelector('#inspector').textContent,/Associazione dichiarata/);
 w.stageRun(run);button(w,'Importa risultato').onclick();assert.match(w.document.querySelector('#panelBody').textContent,/già importato/);assert.equal(vm.runInContext('map.verification_runs.length',context),1);
 await assert.rejects(()=>w.parseJUnit({name:'bad.xml',size:9,text:async()=>'<garbage/>'}));
 for(const mode of ['graph','network','layers','matrix','files','flow','text']){w.setMode(mode);assert.ok(w.document.querySelector(['text','matrix'].includes(mode)?'#textView':'#graph').children.length)}
 }finally{dom.window.close()}
});
test('Corrupt persisted map falls back to clean scan and imported custom maps validate independently of current profile',()=>{
 const {dom,w,context,report}=setup();try{
 w.localStorage.setItem('codeatlas-v2:test',JSON.stringify({schema_version:1,groups:[{id:'broken',name:'broken',lens:'other'}],relations:[]}));w.load(report);assert.equal(vm.runInContext('map.groups[0].id',context),'core');
 assert.throws(()=>w.previewMap({...report.overlay,verification_runs:[{id:'bad'}]},'Bad'));
 }finally{dom.window.close()}
});
test('Storage quota failure does not replace the in-memory map',()=>{
 const {dom,w,context,report}=setup();try{
 const next=structuredClone(report.overlay);next.groups[0].name='Changed';
 const original=w.Storage.prototype.setItem;
 w.Storage.prototype.setItem=function(key,value){if(key==='codeatlas-v2:test')throw Error('Quota exceeded');return original.call(this,key,value)};
 assert.throws(()=>w.commitMap(next),/Quota exceeded/);assert.equal(vm.runInContext('map.groups[0].name',context),'Core');
 }finally{dom.window.close()}
});
