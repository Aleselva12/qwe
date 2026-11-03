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
