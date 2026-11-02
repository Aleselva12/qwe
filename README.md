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

## v0.2: conceptual tree (manual, AI optional)

The UI now has a separate editable **conceptual tree**. Upload `examples/conceptual-map.json` or use "Carica esempio". Add/edit groups, choose a lens (`roots`, `trunk`, `branches`, `unassigned`), status, parent, description, and optionally attach scanner node IDs. Export the overlay to a JSON file. Data stays in the page until exported: **save your changes explicitly**.

- **Roots**: supporting conditions (hardware, OS, network, power, storage, safety, external services).
- **Trunk**: core architecture and shared runtime/orchestration.
- **Branches**: user features and agent capabilities.
- **Dependencies** are separate directed relationships; a branch can depend on multiple roots/trunk components.
- Manual classifications are assertions by the user, **not** automatically verified facts.
- Run `python -m unittest discover -s tests` to exercise the scanner and conceptual overlay validation.
- Import/export JSON is a prototype workflow, not a secure multi-user editor. No backend, no persistent database, no model inference, and no live repository synchronization.
- The conceptual classification is not based on folder locations. AI is not required; a future optional suggestion engine may propose categories with evidence and human approval.
- Example data is fictional and should not be interpreted as an audit of Serveria.

Design inspiration (concepts, not copied source): Backstage's separation of components/resources/dependencies and Graphify's deterministic extraction/provenance.

### Data separation

`atlas.json`: machine-extracted code inventory, read-only.

`codeatlas-overlay.json`: human maintained conceptual groups, status, goals, relations and code references. Never overwrite manual decisions merely because the extractor reruns.

### Known limitations

Conceptual node editor supports basic relationships but not a relation deletion UI. Parent selection is limited to nodes in the same lens. No automatic validation that `code_refs` actually exist in the uploaded code atlas. Group search and persistence are not yet implemented.
