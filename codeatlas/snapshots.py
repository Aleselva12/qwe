"""Snapshot comparison and evidence import; all operations remain local and read-only."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def diff_snapshots(before:dict,after:dict)->dict:
    def normalized(report):
        atlas=report.get("atlas",report)
        nodes={n["id"]:n for n in atlas.get("nodes",[])}
        edges={(e.get("from"),e.get("to"),e.get("kind")) for e in atlas.get("edges",[])}
        return nodes,edges
    prior,old_edges=normalized(before)
    current,new_edges=normalized(after)
    added=sorted(current.keys()-prior.keys())
    removed=sorted(prior.keys()-current.keys())
    changed=sorted(k for k in current.keys()&prior.keys() if prior[k]!=current[k])
    return {"added_nodes":added,"removed_nodes":removed,"changed_nodes":changed,
            "added_edges":[list(e) for e in sorted(new_edges-old_edges)],
            "removed_edges":[list(e) for e in sorted(old_edges-new_edges)],
            "note":"Structural metadata changes, not a source-code or runtime correctness diff."}

def read_junit(path:Path):
    """Read JUnit XML results; only explicit, available test output counts as evidence."""
    root=ET.parse(path).getroot()
    cases=[]
    for suite in root.iter("testcase"):
        name=suite.get("name","unnamed")
        cls=suite.get("classname","")
        result="pass"
        if suite.find("failure") is not None or suite.find("error") is not None:
            result="fail"
        elif suite.find("skipped") is not None:
            result="skip"
        cases.append({"name":name,"classname":cls,"result":result,"source":"test","reference":str(path.name)})
    return {"test_cases":cases,"summary":{status:sum(x["result"]==status for x in cases) for status in ("pass","fail","skip")},
            "source_file":path.name,"warning":"Imported XML is not independently authenticated; CI provenance is not verified."}

def read_snapshot(path:Path):
    obj=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj,dict) or not isinstance(obj.get("atlas",obj).get("nodes"),list):
        raise ValueError("Invalid snapshot schema")
    return obj
