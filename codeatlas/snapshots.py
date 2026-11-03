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
    """Import bounded JUnit output; metadata is producer-declared, never inferred."""
    import hashlib
    from datetime import datetime, timezone
    raw = path.read_bytes()
    declarations = raw.replace(b"\x00", b"").upper()
    if len(raw) > 10_000_000 or b"<!DOCTYPE" in declarations or b"<!ENTITY" in declarations:
        raise ValueError("JUnit too large or contains unsupported entity declarations")
    root = ET.fromstring(raw)
    if root.tag not in {"testsuite", "testsuites"}:
        raise ValueError("Expected testsuite or testsuites")
    cases, occurrences = [], {}
    for case in root.iter("testcase"):
        if len(cases) >= 50000:
            raise ValueError("Too many test cases")
        name, cls, file = case.get("name", "unnamed"), case.get("classname", ""), case.get("file", "")
        key = json.dumps([file, cls, name], ensure_ascii=False, separators=(",", ":"))
        occurrence = occurrences.get(key, 0)
        occurrences[key] = occurrence + 1
        failure = case.find("failure")
        if failure is None:
            failure = case.find("error")
        result = "fail" if failure is not None else "skip" if case.find("skipped") is not None else "pass"
        cases.append({"id":key+":"+str(occurrence), "name":name, "classname":cls, "file":file,
                      "result":result, "source":"test", "reference":path.name,
                      "message": ((failure.get("message", "") or failure.text or "")[:4000] if failure is not None else "")})
    # Only report-level properties: suite-specific commits must not be promoted to a whole run.
    props = {p.get("name"):p.get("value", "") for p in root.findall("./properties/property")}
    metadata = {"commit":props.get("commit", ""), "environment":props.get("environment", ""),
                "executed_at":root.get("timestamp", "")}
    if props.get("workspace_clean") in {"true", "false"}:
        metadata["workspace_clean"] = props["workspace_clean"] == "true"
    return {"schema_version":1, "id":hashlib.sha256(raw).hexdigest(), "metadata":metadata,
            "imported_at":datetime.now(timezone.utc).isoformat(), "test_cases":cases,
            "summary":{status:sum(x["result"]==status for x in cases) for status in ("pass", "fail", "skip")},
            "source_file":path.name, "warning":"Imported XML is not independently authenticated; CI provenance is not verified."}

def read_snapshot(path:Path):
    obj=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj,dict) or not isinstance(obj.get("atlas",obj).get("nodes"),list):
        raise ValueError("Invalid snapshot schema")
    return obj
