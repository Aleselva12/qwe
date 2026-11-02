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

## v0.3 — Step 3: project cards

Each conceptual node can now hold four kinds of structured entries:
- `goals`: planned outcomes, with a separate status field (API/model level).
- `decisions`: human design decisions.
- `issues`: known problems and blockers.
- `evidence`: notes linking a claim to a source/ref.

Entries carry a `source` value: `manual`, `code`, `test`, `document`, or `ai_suggestion`. A manually entered `source` is an *assertion*, not a validated provenance check. v0.3 browser editing supports adding, editing the description text, and deleting entries; source/reference/status metadata are preserved on import/export, but not yet directly editable in the UI. No AI is required.

### Roadmap and honest completion criteria

- **Step 1 (v0.1):** simple Python scanner and JSON export — prototype.
- **Step 2 (v0.2):** manually editable roots/trunk/branches and relationships — prototype.
- **Step 3 (v0.3):** structured cards for goals, decisions, issues, status and evidence — baseline implemented; code cross-reference validation, metadata editing, and durable saving remain.
- **Step 4 (v0.4 planned):** compare intended architecture against extracted repository reality; distinguish verified gaps and unverified assumptions.
- **Step 5 (v0.5 planned):** dependency-based change impact and test coverage evidence.
- **v1.0 (future):** installable standalone application, reproducible tests, persistence, multiple languages and adapter API for optional Serveria integration.

Run unit tests locally with `python -m unittest discover -s tests -v`.

## v0.5 release candidate — integration trial (2026-11)

The program now includes an independent multi-language static engine. **Not yet a certified v1.0**: browser behavior and GitHub Actions must pass before tagging.

### Scope

- Python: top-level functions, classes and imports using the Python AST.
- JavaScript / TypeScript (including JSX/TSX): source file inventory and simple ESM import relations only. No full semantic/type-aware parser, no call graph.
- Infrastructure: Dockerfile, Docker Compose manifests, pyproject, package.json, requirements and Makefile as inventory items. This **does not** analyze real hardware or containers; roots are editable conceptual nodes.
- Excludes typical generated/vendor folders and files over 2 MB.
- No LLM and no project code execution.
- The program does not modify or automatically commit any target repository.

### Generate and view a report

From a cloned working copy:

```bash
python -m codeatlas.engine demo --overlay examples/conceptual-map.json --changed file:sample.py --output /tmp/codeatlas-report.json
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/`, upload the resulting report in **Confronto architettura / codice**. The scanner's `demo` directory is only an illustrative test target. The included conceptual groups intentionally lack code references until users assign them.

For a real project:

```bash
python -m codeatlas.engine /path/to/repo --overlay /path/to/overlay.json --changed file:app/main.py --output /tmp/atlas-report.json
```

The overlay references exact scanner node IDs such as `file:app/main.py`. A missing ID is not proof that the intended feature is missing. Use `python -m unittest discover -s tests -v` for tests.

### Step 4 and 5 mechanics

- **Step 4:** compares manually linked conceptual groups with code node identifiers, reporting `mapped`, `partially_mapped`, or `unmapped`; unlinked groups are not automatically called incomplete.
- **Step 5:** reverse graph traversal over resolved static imports, conceptual `depends_on` links and code-to-concept links. Reports `potentially_affected` and unknown IDs. Dynamic imports, runtime plugins, container network dependencies, and actual test coverage are not resolved yet.

### Before v1.0

Confirm CI status, run the end-to-end report import in a browser, fix any findings, add automatic persistence instead of relying on manual export, and verify a multi-project project size/latency benchmark. Python/JS/TS support is **deliberately uneven**. Never treat `mapped` as verified correctness or `verified` manual status as a passing test.
