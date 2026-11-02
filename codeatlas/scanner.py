"""Read-only Python static scanner; never imports or executes the target project."""
import argparse
import ast
import json
from pathlib import Path

EXCLUDE = {".git", ".venv", "venv", "node_modules", "__pycache__", ".next", "dist", "build", ".mypy_cache"}
SCHEMA_VERSION = 1

def scan(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    nodes = [{"id": "project", "parent": None, "name": root.name, "kind": "project", "path": ".", "source": "extracted"}]
    edges, errors, directories = [], [], set()
    files = sorted(p for p in root.rglob("*.py") if not any(part in EXCLUDE or part.startswith(".") for part in p.relative_to(root).parts))
    for file in files:
        relative = file.relative_to(root)
        parent = "project"
        for index, part in enumerate(relative.parts[:-1]):
            folder_path = Path(*relative.parts[:index + 1]).as_posix()
            folder_id = "dir:" + folder_path
            if folder_id not in directories:
                nodes.append({"id": folder_id, "parent": parent, "name": part, "kind": "folder", "path": folder_path, "source": "extracted"})
                directories.add(folder_id)
            parent = folder_id
        path = relative.as_posix()
        fid = "file:" + path
        nodes.append({"id": fid, "parent": parent, "name": file.name, "kind": "file", "path": path, "source": "extracted"})
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"), filename=path)
        except (SyntaxError, UnicodeError, OSError) as exc:
            errors.append({"file": path, "message": str(exc)})
            continue
        for item in tree.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                kind = "class" if isinstance(item, ast.ClassDef) else "function"
                nodes.append({"id": f"{fid}:{item.name}:{item.lineno}", "parent": fid, "name": item.name, "kind": kind, "path": path, "line": item.lineno, "source": "extracted"})
            elif isinstance(item, (ast.Import, ast.ImportFrom)):
                modules = [alias.name for alias in item.names] if isinstance(item, ast.Import) else [item.module or ""]
                for module in modules:
                    if module:
                        edges.append({"from": fid, "to": "module:" + module, "kind": "imports", "source": "extracted", "line": item.lineno, "resolution": "unresolved"})
    by_module = {}
    for node in nodes:
        if node["kind"] == "file":
            name = ".".join(Path(node["path"]).with_suffix("").parts)
            if name.endswith(".__init__"):
                name = name[:-9]
            by_module[name] = node["id"]
    for edge in edges:
        module = edge["to"][7:]
        if module in by_module:
            edge["to"] = by_module[module]
            edge["resolution"] = "local-exact"
    return {"schema_version": SCHEMA_VERSION, "project": root.name, "nodes": nodes, "edges": edges, "errors": errors, "limitations": ["Python only", "Top-level declarations/imports only", "Relative imports unresolved", "No runtime execution"]}

def main():
    parser = argparse.ArgumentParser(description="Export a read-only CodeAtlas JSON map of Python files")
    parser.add_argument("path", help="Project directory")
    parser.add_argument("-o", "--output", default="atlas.json")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    output = Path(args.output).resolve()
    if output == root or root in output.parents:
        parser.error("Output must be outside scanned directory (read-only input)")
    output.write_text(json.dumps(scan(root), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output}")

if __name__ == "__main__":
    main()
