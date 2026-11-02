"""Optional repository intelligence: history, documentation, CI evidence and infrastructure.

No repository code is executed. Git history is read through bounded subprocess commands.
"""
import json
import re
import subprocess
from pathlib import Path

DOC_NAMES={"README.md","CONTRIBUTING.md","ARCHITECTURE.md","DECISIONS.md"}
TEST_MARKERS=("test_",".test.",".spec.")
MAX_GIT_COMMITS=30

def _git(root,*args):
    try:
        p=subprocess.run(["git","-C",str(root),*args],capture_output=True,text=True,timeout=12,check=False)
        return p.stdout if p.returncode==0 else ""
    except (OSError,subprocess.TimeoutExpired):
        return ""

def history(root:Path,limit:int=15):
    limit=max(1,min(MAX_GIT_COMMITS,limit))
    output=_git(root,"log",f"-{limit}","--format=%H%x09%aI%x09%s","--name-only")
    commits=[]
    current=None
    for raw in output.splitlines():
        if "\t" in raw and len(raw.split("\t",2)[0])==40:
            sha,date,message=raw.split("\t",2)
            current={"sha":sha,"date":date,"message":message,"files":[]}
            commits.append(current)
        elif raw.strip() and current is not None:
            current["files"].append(raw.strip())
    return commits

def documentation(root:Path):
    results=[]
    for p in sorted(root.rglob("*.md")):
        parts=p.relative_to(root).parts
        if any(x in {".git","node_modules",".venv","dist","build"} for x in parts):continue
        if len(results)>=100:break
        if p.stat().st_size>500_000:continue
        data=p.read_text(encoding="utf-8",errors="replace")
        headings=[m.group(1).strip() for m in re.finditer(r"^#{1,4}\s+(.+)$",data,re.M)]
        results.append({"path":p.relative_to(root).as_posix(),"headings":headings[:60],"kind":"reference","interpreted":False})
    return results

def infrastructure(root:Path):
    results=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(x in {".git","node_modules",".venv","dist","build"} for x in p.relative_to(root).parts):continue
        if p.name in {"compose.yml","compose.yaml","docker-compose.yml","docker-compose.yaml"} and p.stat().st_size<500_000:
            text=p.read_text(encoding="utf-8",errors="replace")
            names=[]
            inside=False
            for line in text.splitlines():
                if line.strip()=="services:":inside=True;continue
                if inside and line and not line.startswith((" ","\t","#")):inside=False
                if inside:
                    m=re.match(r"^  ([A-Za-z0-9_-]+):\s*(?:#.*)?$",line)
                    if m:names.append(m.group(1))
            results.append({"path":p.relative_to(root).as_posix(),"type":"compose","services":names,"confidence":"heuristic"})
        elif p.name in {"Dockerfile","Dockerfile.dev"}:
            results.append({"path":p.relative_to(root).as_posix(),"type":"dockerfile","services":[],"confidence":"file"})
    return results

def test_evidence(root:Path):
    # Discovery is NOT execution. Never paint a node green based on name matching.
    files=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(x in {"node_modules",".git",".venv"} for x in p.relative_to(root).parts):continue
        if p.name.startswith("test_") and p.suffix==".py" or any(x in p.name for x in (".test.",".spec.")):
            files.append(p.relative_to(root).as_posix())
        if len(files)>=1000:break
    return {"test_files":files,"executed":False,"status":"unknown","note":"Discovered tests do not demonstrate passing tests."}

def enrich(root:Path):
    return {"history":history(root),"documentation":documentation(root),"infrastructure":infrastructure(root),"tests":test_evidence(root),"status_policy":{"green":"explicit passing evidence","red":"explicit failing evidence","yellow":"partial/degraded or warning","gray":"unknown/not verified"}}
