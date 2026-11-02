"""Human-authored conceptual classification layered over a code-derived map."""
import json
from pathlib import Path

LENSES = {"roots", "trunk", "branches", "unassigned"}
STATES = {"idea", "planned", "in_progress", "implemented", "verified", "blocked", "unknown"}
RELATIONS = {"depends_on", "supports", "blocks", "implements", "related_to"}

def validate(overlay: dict) -> dict:
    if not isinstance(overlay, dict) or overlay.get("schema_version") != 1:
        raise ValueError("Expected overlay schema_version=1")
    groups = overlay.get("groups", [])
    if not isinstance(groups, list):
        raise ValueError("groups must be a list")
    known = set()
    for item in groups:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            raise ValueError("Each group needs a nonempty string id")
        if item["id"] in known:
            raise ValueError("Duplicate group id")
        known.add(item["id"])
        if item.get("lens", "unassigned") not in LENSES:
            raise ValueError("Unknown lens")
        if item.get("status", "unknown") not in STATES:
            raise ValueError("Unknown status")
        if not isinstance(item.get("name"), str):
            raise ValueError("Each group needs a name")
        if not isinstance(item.get("code_refs", []), list) or any(not isinstance(x, str) for x in item.get("code_refs", [])):
            raise ValueError("code_refs must be string list")
        for field in ("goals", "decisions", "issues", "evidence"):
            if not isinstance(item.get(field, []), list):
                raise ValueError(f"{field} must be a list")
            for entry in item.get(field, []):
                if not isinstance(entry, dict) or not isinstance(entry.get("text"), str) or not entry["text"].strip():
                    raise ValueError(f"{field} entries require nonempty text")
                if entry.get("source", "manual") not in {"manual", "code", "test", "document", "ai_suggestion"}:
                    raise ValueError("Unknown information source")
                if field == "goals" and entry.get("status", "planned") not in STATES:
                    raise ValueError("Invalid goal status")
                if field == "evidence" and entry.get("ref") is not None and not isinstance(entry["ref"], str):
                    raise ValueError("Invalid evidence reference")
    for item in groups:
        parent = item.get("parent")
        if parent is not None and parent not in known:
            raise ValueError(f"Unknown parent: {parent}")
    parents = {g["id"]: g.get("parent") for g in groups}
    for id in known:
        visited = set()
        cur = id
        while cur is not None:
            if cur in visited:
                raise ValueError("Group hierarchy contains a cycle")
            visited.add(cur)
            cur = parents[cur]
    for edge in overlay.get("relations", []):
        if not isinstance(edge, dict) or edge.get("kind") not in RELATIONS or edge.get("from") not in known or edge.get("to") not in known:
            raise ValueError("Invalid conceptual relation")
    return overlay

def load(path: str | Path) -> dict:
    return validate(json.loads(Path(path).read_text(encoding="utf-8")))
