const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {JSDOM}=require('jsdom');

test('Project plans survive rescans, ignore unconfirmed suggestions and stay separate',async()=>{
  const html=fs.readFileSync('direzione.html','utf8');
  const dom=new JSDOM(html,{runScripts:'outside-only',url:'http://localhost'});
  const w=dom.window;
  let project='/projects/A';
  w.fetch=async()=>({ok:true,json:async()=>({project_key:project,overlay:{groups:[{id:'scan',name:'Suggested'}]}})});
  try{
    w.eval(fs.readFileSync('direzione.js','utf8')+';window.restart=start;window.savePlan=commit');
    await new Promise(resolve=>setImmediate(resolve));
    assert.equal(w.document.querySelectorAll('#tree summary').length,2);
    const plan={version:1,nodes:[{id:'r',role:'radici',title:'Risorse'},{id:'t',role:'tronco',title:'Base'},{id:'b',role:'ramo',title:'Progetto futuro'},{id:'star',parent:'b',title:'Ancora da costruire',priority:'plan'}]};
    w.savePlan(plan);
    await w.restart();
    assert.match(w.document.querySelector('#tree').textContent,/Ancora da costruire/);
    project='/projects/B';
    await w.restart();
    assert.equal(w.document.querySelectorAll('#tree summary').length,2);
    assert.doesNotMatch(w.document.querySelector('#tree').textContent,/Ancora da costruire|Suggested/);
  }finally{w.close()}
});
