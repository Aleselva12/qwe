# CodeAtlas

A standalone, local-first codebase map prototype. This repository is independent of Serveria/Cora.

## v0.1

- Read-only Python AST scanner, no execution of target project code.
- JSON export with folders, files, definitions, and imports.
- Searchable static HTML viewer with component inspector.
- No external services or third-party source code copied.

## Try it

```bash
python -m codeatlas.scanner /path/to/python/project -o atlas.json
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000`, load the generated `atlas.json` using the file picker.

## Limitations

Only Python `.py` files; only top-level classes/functions/imports; imports may be unresolved; no call graph, planning overlays, or Graphify integration yet. The tool does not assess runtime correctness. Do not open untrusted HTML or execute code from analyzed repositories.

## Next steps

1. Graphify adapter with versioned input validation.
2. Separate architecture/roadmap annotations from code-derived evidence.
3. Dependency graph and change-impact views.
4. Tests, Git integration, and optional Serveria plugin/embedding.

## License

No license granted yet. Choose a license before inviting public reuse or copying external code.
