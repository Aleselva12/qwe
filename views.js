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
function role(node){
  return node.role || (node.lens==='roots'?'foundation':node.lens==='branches'&&!node.parent?'capability':'process');
}
function functionalLayout(map,nodes){
  const positions=new Map(),byId=new Map(nodes.map(n=>[n.id,n]));
  const capabilities=nodes.filter(n=>role(n)==='capability'),processes=nodes.filter(n=>role(n)==='process'),bases=nodes.filter(n=>role(n)==='foundation');
  const processIDs=new Set(processes.map(n=>n.id)),edges=project(map,nodes).filter(e=>processIDs.has(e.from)&&processIDs.has(e.to));
  const components=levels(processes,edges),ranks=new Map(components.flatMap(c=>c.members.map(id=>[id,c.rank])));
  const maxRank=Math.max(0,...ranks.values()),depth=new Map();
  function nesting(n){if(depth.has(n.id))return depth.get(n.id);let d=0,p=byId.get(n.parent),seen=new Set([n.id]);while(p&&!seen.has(p.id)){seen.add(p.id);if(role(p)==='process')d++;p=byId.get(p.parent)}depth.set(n.id,d);return d;}
  const rows=new Map();
  for(const n of [...processes].sort((a,b)=>nesting(a)-nesting(b))){
    let row=maxRank-(ranks.get(n.id)||0)+nesting(n);
    const parent=positions.get(n.parent);
    if(parent)row=Math.max(row,parent.row+1);
    positions.set(n.id,{row});if(!rows.has(row))rows.set(row,[]);rows.get(row).push(n);
  }
  const width=Math.max(1200,capabilities.length*290,Math.min(bases.length,6)*250);
  capabilities.forEach((n,i)=>positions.set(n.id,{x:(i+1)*width/(capabilities.length+1),y:85+(i%2)*30}));
  let processY=290;
  for(const [row,list]of [...rows].sort((a,b)=>a[0]-b[0])){
    list.sort((a,b)=>String(a.parent||'').localeCompare(String(b.parent||''))||a.id.localeCompare(b.id));
    for(let start=0;start<list.length;start+=4){
      const chunk=list.slice(start,start+4);
      chunk.forEach((n,i)=>positions.set(n.id,{x:(i+1)*width/(chunk.length+1),y:processY+Math.floor(start/4)*170+(i%2)*22}));
    }
    processY+=Math.ceil(list.length/4)*170+40;
  }
  const ground=Math.max(490,...processes.map(n=>(positions.get(n.id)?.y||0)+190));
  const baseRows=new Map();
  for(const n of bases){let d=0,p=byId.get(n.parent),seen=new Set([n.id]);while(p&&role(p)==='foundation'&&!seen.has(p.id)){seen.add(p.id);d++;p=byId.get(p.parent)}if(!baseRows.has(d))baseRows.set(d,[]);baseRows.get(d).push(n);}
  let bottom=ground;
  let baseY=ground;
  for(const[d,list]of [...baseRows].sort((a,b)=>a[0]-b[0])){for(let i=0;i<list.length;i+=6){const row=list.slice(i,i+6);const y=baseY+Math.floor(i/6)*145;row.forEach((n,j)=>positions.set(n.id,{x:(j+1)*width/(row.length+1),y:y+(j%2)*22}));bottom=Math.max(bottom,y+110);}baseY+=Math.ceil(list.length/6)*145+70;}
  const children=new Map();for(const n of nodes){if(!children.has(n.parent))children.set(n.parent,[]);children.get(n.parent).push(n);}
  return {positions,children,width,height:bottom+80,ground:ground-70,bands:[{label:'UTILITÀ · VERSO L’UTENTE',y:15},{label:'PROCESSI · REALIZZAZIONE',y:220},{label:'BASI · REQUISITI',y:ground-70}],cycles:components.filter(c=>c.cycle).flatMap(c=>c.members)};
}
function flow(map,nodes){
  // Support direction: requirements -> realization -> utility. Original import
  // evidence stays unchanged; hierarchy means membership, never runtime order.
  const result=project(map,nodes).map(e=>({...e,from:e.to,to:e.from,hierarchy:false}));
  const ids=new Set(nodes.map(n=>n.id));
  for(const n of nodes)if(n.parent&&ids.has(n.parent))result.push({from:n.id,to:n.parent,hierarchy:true,evidence:[{from:n.id,to:n.parent,kind:'part_of',source:'hierarchy'}]});
  return result;
}
function flowLayout(map,nodes){
  const positions=new Map(),columns=['foundation','process','capability'],counts=columns.map(c=>nodes.filter(n=>role(n)===c).length),height=Math.max(720,...counts.map(n=>n*100+130));
  columns.forEach((column,i)=>{const list=nodes.filter(n=>role(n)===column);list.forEach((n,j)=>positions.set(n.id,{x:160+i*480,y:100+(j+.5)*(height-180)/Math.max(1,list.length)}));});
  return {positions,width:1280,height,bands:[],children:new Map()};
}

const api={project,levels,role,functionalLayout,flow,flowLayout};if(typeof module!=='undefined')module.exports=api;else root.AtlasViews=api;
})(globalThis);
