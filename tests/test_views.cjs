const {test}=require('node:test');
const assert=require('node:assert/strict');
const {project,levels}=require('../views.js');
test('Collapsed children aggregate cross-branch dependencies with evidence, without inventing parent self loops',()=>{
 const groups=[{id:'a'},{id:'b'},{id:'a1',parent:'a'},{id:'a2',parent:'a'}];
 const relations=[{from:'a1',to:'b',kind:'depends_on'},{from:'a2',to:'b',kind:'depends_on'},{from:'a1',to:'a2',kind:'depends_on'},{from:'b',to:'a',kind:'supports'}];
 const map={groups,relations},before=JSON.stringify(map);const result=project(map,groups.slice(0,2));assert.equal(result.length,1);assert.equal(result[0].evidence.length,2);assert.equal(result[0].from,'a');assert.equal(JSON.stringify(map),before);
 assert.equal(project(map,groups).length,3);assert.equal(project(map,[groups[1]]).length,0);
});
test('SCC levels retain cycles, self loops, isolated nodes and dependency order',()=>{
 const nodes=['a','b','c','d','e'].map(id=>({id})),edges=[{from:'a',to:'b'},{from:'b',to:'a'},{from:'b',to:'c'},{from:'d',to:'d'}];
 const result=levels(nodes,edges);const a=result.find(g=>g.members.includes('a')),c=result.find(g=>g.members.includes('c'));assert.equal(a.cycle,true);assert.equal(a.members.length,2);assert.ok(a.rank>c.rank);assert.equal(result.find(g=>g.members.includes('d')).cycle,true);assert.equal(result.find(g=>g.members.includes('e')).cycle,false);assert.deepEqual(levels([],[]),[]);
});
test('Deep dependency chains do not use the JavaScript call stack',()=>{
 const nodes=Array.from({length:5000},(_,i)=>({id:String(i)})),edges=nodes.slice(1).map((n,i)=>({from:String(i),to:n.id}));const result=levels(nodes,edges);assert.equal(result.find(g=>g.members.includes('0')).rank,4999);
});
test('Inline application script parses',()=>{
 const fs=require('node:fs'),path=require('node:path');
 const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
 new Function(html.split('<script>')[1].split('</script>')[0]);
});
test('Functional tree places utility above its realization and requirements, with all nodes retained',()=>{
 const {functionalLayout}=require('../views.js');
 const groups=[{id:'calculator',role:'capability'},{id:'ops',role:'process',parent:'calculator'},{id:'add',role:'process',parent:'ops'},{id:'python',role:'foundation'}];
 const map={groups,relations:[{from:'ops',to:'python',kind:'depends_on'}]},before=JSON.stringify(map),layout=functionalLayout(map,groups);
 assert.equal(layout.positions.size,groups.length);
 const pos=id=>layout.positions.get(id);
 assert.ok(pos('calculator').y<pos('ops').y);
 assert.ok(pos('ops').y<pos('add').y);
 assert.ok(pos('add').y<pos('python').y);
 assert.equal(JSON.stringify(map),before);
});
test('Support flow reverses dependency direction while preserving original evidence and hierarchy meaning',()=>{
 const {flow,flowLayout}=require('../views.js');
 const groups=[{id:'cap',role:'capability'},{id:'proc',role:'process',parent:'cap'},{id:'lib',role:'foundation'}];
 const original={from:'proc',to:'lib',kind:'depends_on',source:'static_import'},map={groups,relations:[original]},before=JSON.stringify(map);
 const edges=flow(map,groups),dep=edges.find(e=>!e.hierarchy),association=edges.find(e=>e.hierarchy);
 assert.equal(dep.from,'lib');assert.equal(dep.to,'proc');assert.equal(dep.evidence[0],original);
 assert.equal(association.from,'proc');assert.equal(association.to,'cap');assert.equal(association.evidence[0].source,'hierarchy');
 const layout=flowLayout(map,groups);assert.ok(layout.positions.get('lib').x<layout.positions.get('proc').x);assert.ok(layout.positions.get('proc').x<layout.positions.get('cap').x);
 assert.equal(JSON.stringify(map),before);
});
test('Deep foundation expansion and cyclic processes keep finite distinct positions',()=>{
 const {functionalLayout}=require('../views.js');
 const groups=[{id:'cap',role:'capability'},{id:'a',role:'process',parent:'cap'},{id:'b',role:'process',parent:'cap'},...Array.from({length:15},(_,i)=>({id:'base'+i,role:'foundation',parent:i>8?'base0':undefined}))];
 const layout=functionalLayout({groups,relations:[{from:'a',to:'b',kind:'depends_on'},{from:'b',to:'a',kind:'depends_on'}]},groups);
 assert.equal(layout.positions.size,groups.length);assert.equal(new Set([...layout.positions.values()].map(p=>JSON.stringify([p.x,p.y]))).size,groups.length);
 assert.ok([...layout.positions.values()].every(p=>Number.isFinite(p.x)&&Number.isFinite(p.y)));assert.equal(layout.cycles.length,2);
});
