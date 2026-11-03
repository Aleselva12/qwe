'use strict';
/* Check the real browser validator/role functions without starting an HTTP server. */
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const assert=require('node:assert/strict');
const {test}=require('node:test');
const root=path.resolve(__dirname,'..');
const plan=JSON.parse(fs.readFileSync(path.join(root,'cora-plan.json'),'utf8'));
const src=fs.readFileSync(path.join(root,'direzione.js'),'utf8');
const entry="start().catch(e=>$('message').textContent=e.message);";
assert.ok(src.includes(entry),'Direzione entry point not found');
const ctx=vm.createContext({});
vm.runInContext(src.replace(entry,'globalThis.directionTest={validate,role};'),ctx,{filename:'direzione.js'});
const {validate,role}=ctx.directionTest;
const byId=new Map(plan.nodes.map(n=>[n.id,n]));
function trail(id) {
 let cur=byId.get(id),result=[],seen=new Set();
 while(cur){
   assert.ok(!seen.has(cur.id),'cyclic hierarchy');
   result.unshift(cur);seen.add(cur.id);
   cur=cur.parent?byId.get(cur.parent):null;
 }
 return result;
}

test('real Direzione validator accepts complete Cora V2 without losing identifiers',()=>{
  assert.equal(validate(plan),plan);
  assert.equal(byId.size,plan.nodes.length);
});
test('root areas, trunk stars, branch stars, planets and moons display correct labels',()=>{
  assert.equal(role(trail('R1')),'area');
  assert.equal(role(trail('R1.1')),'stella');
  assert.equal(role(trail('R1.1.p1')),'pianeta');
  assert.equal(role(trail('R1.1.p1.m1')),'luna');
  assert.equal(role(trail('T1')),'stella');
  assert.equal(role(trail('T1.p1')),'pianeta');
  assert.equal(role(trail('T1.p1.m1')),'luna');
  assert.equal(role(trail('C1')),'stella');
  assert.equal(role(trail('C1a')),'pianeta');
  assert.equal(role(trail('C1a.m1')),'luna');
});
test('reject broken crosslinks or an excessive hierarchy',()=>{
 const broken=structuredClone(plan);
 broken.relations[0].to='not-an-existing-star';
 assert.throws(()=>validate(broken),/Collegamento/);
 const tooDeep=structuredClone(plan);
 tooDeep.nodes.push({id:'bad-sixth-level',parent:'R1.1.p1.m1',title:'Too deep',priority:'unknown'});
 assert.throws(()=>validate(tooDeep),/livelli/);
});
