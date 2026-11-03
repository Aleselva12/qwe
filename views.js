/* Pure projections: never mutate the shared conceptual model. */
(function(root){
'use strict';
function project(map, nodes){
  const all=new Map(map.groups.map(n=>[n.id,n])), visible=new Set(nodes.map(n=>n.id));
  function ancestor(id){const seen=new Set();while(id&&!visible.has(id)&&!seen.has(id)){seen.add(id);id=all.get(id)?.parent}return visible.has(id)?id:null}
  const edges=new Map();
  for(const r of map.relations){if(r.kind!=='depends_on')continue;const from=ancestor(r.from),to=ancestor(r.to);if(!from||!to||(from===to&&r.from!==r.to))continue;const key=JSON.stringify([from,to]);if(!edges.has(key))edges.set(key,{from,to,evidence:[]});edges.get(key).evidence.push(r)}
  return [...edges.values()];
}
function levels(nodes,edges){
  // Iterative Kosaraju: cycles remain explicit, including self dependencies.
  const ids=nodes.map(n=>n.id),adj=new Map(ids.map(id=>[id,[]])),rev=new Map(ids.map(id=>[id,[]]));
  for(const e of edges)if(adj.has(e.from)&&adj.has(e.to)){adj.get(e.from).push(e.to);rev.get(e.to).push(e.from)}
  const seen=new Set(),order=[];
  for(const id of ids){if(seen.has(id))continue;seen.add(id);const stack=[[id,0]];while(stack.length){const top=stack[stack.length-1],next=adj.get(top[0]);if(top[1]<next.length){const child=next[top[1]++];if(!seen.has(child)){seen.add(child);stack.push([child,0])}}else{order.push(top[0]);stack.pop()}}}
  const component=new Map(),groups=[];
  for(const id of order.reverse()){if(component.has(id))continue;const index=groups.length,group=[],stack=[id];component.set(id,index);while(stack.length){const cur=stack.pop();group.push(cur);for(const p of rev.get(cur))if(!component.has(p)){component.set(p,index);stack.push(p)}}groups.push(group)}
  const deps=groups.map(()=>new Set()),dependents=groups.map(()=>new Set());for(const e of edges){const a=component.get(e.from),b=component.get(e.to);if(a!==undefined&&b!==undefined&&a!==b){deps[a].add(b);dependents[b].add(a)}}
  const remaining=deps.map(x=>x.size),rank=groups.map(()=>0),queue=[];remaining.forEach((n,i)=>{if(!n)queue.push(i)});for(let i=0;i<queue.length;i++){const b=queue[i];for(const a of dependents[b]){rank[a]=Math.max(rank[a],rank[b]+1);if(--remaining[a]===0)queue.push(a)}}
  return groups.map((members,i)=>({members,rank:rank[i],cycle:members.length>1||edges.some(e=>e.from===members[0]&&e.to===members[0])}));
}
const api={project,levels};if(typeof module!=='undefined')module.exports=api;else root.AtlasViews=api;
})(globalThis);
