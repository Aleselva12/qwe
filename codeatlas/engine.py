"""Portable, deterministic code inventory for CodeAtlas.

No project code is imported or executed. JS/TS results are deliberately file-level:
the Python AST is the only detailed symbol extractor in this release.
"""
import ast
import json
import posixpath
import re
from pathlib import Path

IGNORE = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build", ".next", ".mypy_cache", ".pytest_cache", "coverage"}
EXTENSIONS = {".py": "python", ".js": "javascript", ".jsx": "javascript", ".ts": "typescript", ".tsx": "typescript"}
# Additional languages are inventoried without pretending to parse their semantics.
EXTENSIONS.update({".mjs":"javascript", ".cjs":"javascript", ".go":"go", ".rs":"rust", ".java":"java",
                   ".cs":"csharp", ".c":"c", ".cpp":"cpp", ".h":"c", ".rb":"ruby", ".php":"php",
                   ".swift":"swift", ".kt":"kotlin", ".sql":"sql", ".html":"html", ".css":"css",
                   ".vue":"vue", ".svelte":"svelte"})
INFRA = {"Dockerfile", "compose.yml", "compose.yaml", "docker-compose.yml", "docker-compose.yaml", "pyproject.toml", "package.json", "requirements.txt", "Makefile", ".env.example"}
MAX_SIZE = 2_000_000

def inventory(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("Path must be an existing directory")
    nodes = [{"id":"project","name":root.name,"parent":None,"path":".","kind":"project","source":"extracted"}]
    edges, errors, known_dirs = [], [], set()
    # Prune dependency/vendor directories before traversal: critical on large monorepos.
    import os
    files = []
    for current, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE and not d.startswith("."))
        for name in names:
            path = Path(current) / name
            if (path.suffix in EXTENSIONS or name in INFRA) and not path.is_symlink():
                files.append(path)
    files.sort()
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.stat().st_size > MAX_SIZE:
            errors.append({"file":rel,"message":"Size limit exceeded"});continue
        parent = "project"
        for idx, part in enumerate(path.relative_to(root).parts[:-1]):
            dp = "/".join(path.relative_to(root).parts[:idx+1])
            ident = "dir:"+dp
            if ident not in known_dirs:
                nodes.append({"id":ident,"parent":parent,"name":part,"path":dp,"kind":"folder","source":"extracted"})
                known_dirs.add(ident)
            parent = ident
        fid = "file:"+rel
        lang = EXTENSIONS.get(path.suffix, "infrastructure")
        nodes.append({"id":fid,"parent":parent,"name":path.name,"path":rel,"kind":"file","language":lang,"source":"extracted"})
        if lang == "infrastructure":continue
        try:
            source = path.read_text(encoding="utf-8")
        except (UnicodeError,OSError) as exc:
            errors.append({"file":rel,"message":str(exc)});continue
        if lang == "python":
            try: tree = ast.parse(source,filename=rel)
            except SyntaxError as exc:
                errors.append({"file":rel,"message":str(exc)});continue
            file_node = next(n for n in nodes if n['id'] == fid)
            file_node['documentation'] = ast.get_docstring(tree) or ''
            for item in tree.body:
                if isinstance(item,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                    nodes.append({"id":f"{fid}:{item.name}:{item.lineno}","parent":fid,"name":item.name,"path":rel,"line":item.lineno,"kind":"class" if isinstance(item,ast.ClassDef) else "function","source":"extracted"})
                if isinstance(item,(ast.Import,ast.ImportFrom)):
                    modules=[x.name for x in item.names] if isinstance(item,ast.Import) else [item.module or ""]
                    if isinstance(item, ast.ImportFrom) and item.level:
                        package = list(Path(rel).parent.parts)
                        keep = len(package) - item.level + 1
                        if keep >= 0:
                            prefix = package[:keep]
                            modules = ['.'.join(prefix + ([item.module] if item.module else [alias.name]))
                                       for alias in (item.names[:1] if item.module else item.names)]
                    for name in modules:
                        if name:edges.append({"from":fid,"to":"module:"+name,"kind":"imports","line":item.lineno,"resolution":"unresolved","source":"extracted"})
        elif lang in {"javascript", "typescript"}:
            # Heuristic declarations for JS/TS. Source ranges are hints, not compiler semantics.
            for line_no,line in enumerate(source.splitlines(),1):
                m=re.match(r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function|class|interface|type|enum)\s+([A-Za-z_$][\w$]*)",line)
                if not m:
                    m=re.match(r"^\s*(?:export\s+)?(?:const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>",line)
                if m:
                    label="class" if re.search(r"\bclass\s+",line) else "symbol"
                    nodes.append({"id":f"{fid}:{m.group(1)}:{line_no}","parent":fid,"name":m.group(1),"path":rel,"line":line_no,"kind":label,"source":"heuristic"})
            # Deliberately conservative: only ESM import/export-from paths at file level.
            for line_no,line in enumerate(source.splitlines(),1):
                m=re.match(r'^\s*(?:import\s+(?:.*?\s+from\s+)?|export\s+.*?\s+from\s+)[\'"]([^\'"]+)[\'"]',line)
                if m: edges.append({"from":fid,"to":"module:"+m.group(1),"kind":"imports","line":line_no,"resolution":"unresolved","source":"extracted"})
    module_map={}
    for n in nodes:
        if n["kind"]=="file" and n.get("language")=="python":
            key=".".join(Path(n["path"]).with_suffix("").parts)
            if key.endswith(".__init__"):key=key[:-9]
            module_map[key]=n["id"]
    for e in edges:
        target=e["to"].removeprefix("module:")
        if target in module_map:
            e["to"]=module_map[target];e["resolution"]="local-exact"
        elif target.startswith("."):
            base=Path(e["from"][5:]).parent
            for candidate in (base / target,base / (target+".ts"),base / (target+".tsx"),base / (target+".js"),base / (target+".jsx"),base / target / "index.ts",base / target / "index.js"):
                normalized=posixpath.normpath(candidate.as_posix())
                if normalized.startswith("./"):normalized=normalized[2:]
                if any(n["id"]=="file:"+normalized for n in nodes):
                    e["to"]="file:"+normalized;e["resolution"]="local-exact";break
    return {"schema_version":1,"project":root.name,"nodes":nodes,"edges":edges,"errors":errors,"limitations":["Python top-level AST only","JS/TS file-level imports only","No runtime execution","Some imports unresolved"]}

def compare(atlas:dict,overlay:dict)->dict:
    from codeatlas.overlay import validate
    validate(overlay)
    ids={n["id"] for n in atlas["nodes"]}
    results=[]
    for g in overlay["groups"]:
        refs=g.get("code_refs",[])
        found=[x for x in refs if x in ids]
        missing=[x for x in refs if x not in ids]
        results.append({"id":g["id"],"name":g["name"],"lens":g.get("lens","unassigned"),"status":g.get("status","unknown"),"found":found,"missing":missing,"classification":"unmapped" if not refs else "partially_mapped" if missing else "mapped"})
    return {"schema_version":1,"project":atlas["project"],"results":results,"summary":{"mapped":sum(x["classification"]=="mapped" for x in results),"partial":sum(x["classification"]=="partially_mapped" for x in results),"unmapped":sum(x["classification"]=="unmapped" for x in results)},"warning":"Missing references are not proof a feature is absent; unmapped means not yet associated with evidence."}


def impact(atlas: dict, overlay: dict, changed: list[str]) -> dict:
    """Find potential reverse dependencies, never assert actual breakage."""
    from codeatlas.overlay import validate
    validate(overlay)
    nodes={node["id"] for node in atlas.get("nodes", [])}
    groups={g["id"]:g for g in overlay["groups"]}
    reverse={}
    for edge in atlas.get("edges",[]):
        if edge.get("to") in nodes and edge.get("from") in nodes:
            reverse.setdefault(edge["to"],set()).add(edge["from"])
    for edge in overlay.get("relations",[]):
        if edge.get("kind")=="depends_on":
            reverse.setdefault(edge["to"],set()).add(edge["from"])
    # Bridge implementation references to conceptual components.
    for group in groups.values():
        for ref in group.get("code_refs",[]):
            if ref in nodes: reverse.setdefault(ref,set()).add(group["id"])
    unknown=[ident for ident in changed if ident not in nodes and ident not in groups]
    seen=set(changed)-set(unknown)
    queue=list(seen)
    while queue:
        for dependent in reverse.get(queue.pop(0),()):
            if dependent not in seen:
                seen.add(dependent)
                queue.append(dependent)
    return {"changed":changed,"unknown":unknown,"potentially_affected":sorted(seen-set(changed)), "warning":"Static potential impact only. Missing or dynamic dependencies may not appear."}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("root")
    p.add_argument("--overlay")
    p.add_argument("--output",default="codeatlas-report.json")
    p.add_argument("--changed",action="append",default=[],help="Changed node ID; repeat to simulate impact")
    args=p.parse_args()
    root=Path(args.root).resolve()
    target=Path(args.output).resolve()
    if target==root or root in target.parents:p.error("Output must be outside the scanned project")
    atlas=inventory(root)
    report={"atlas":atlas}
    if args.overlay:
        from codeatlas.overlay import load
        report["overlay"]=load(args.overlay)
        report["comparison"]=compare(atlas,report["overlay"])
        if args.changed:report["impact"]=impact(atlas,report["overlay"],args.changed)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Saved {target}: {len(atlas['nodes'])} nodes, {len(atlas['edges'])} edges")

if __name__=="__main__":main()
