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


---

## CodeAtlas 1.0 — local-first release (validation pending)

CodeAtlas is a standalone **read-only codebase explorer** with a human-maintained conceptual map of roots (operating conditions), trunk (core architecture), and branches (features). The repo being inspected is never imported/executed or modified.

### One-command launch (Python 3.10+)

```bash
git clone https://github.com/Aleselva12/qwe.git
cd qwe
python -m codeatlas.app /absolute/path/to/other/repository
```

The browser opens `http://127.0.0.1:8765/`; use Ctrl+C to stop. The web server binds **127.0.0.1 only**, not the LAN. No service account, API key, LLM, or package installation needed for the default scanner.

To compare a manually authored architecture with source code:

```bash
python -m codeatlas.app /absolute/path/to/repository --overlay examples/conceptual-map.json --changed file:sample.py
```

Or use the JSON report generator with `python -m codeatlas.engine`; the browser can load a generated report or code inventory manually.

### How to use it for research

1. Clone a repository you are authorized to inspect. CodeAtlas reads its local working directory; it does not download arbitrary repos by itself.
2. Launch the program, then inspect the extracted file tree and direct import relations.
3. Load an overlay or build one manually: *roots* for hardware/network/runtime constraints, *trunk* for shared components and orchestration, *branches* for product features.
4. Link a conceptual node to exact code IDs such as `file:package/module.py`. Export the JSON overlay to keep a durable, portable copy; local browser persistence is only a convenience.
5. Run `--overlay ... --changed file:package/module.py` for a conservative reverse-dependency impact report.
6. Keep all manually inferred intent separate from actually extracted source: linked/mapped does **not** mean working or tested.

### Verification

```bash
python -m unittest discover -s tests -v
python -m compileall -q codeatlas tests
```

GitHub Actions `.github/workflows/checks.yml` runs those checks on push and PR. Passing tests would validate these isolated operations, not full browser functionality or scan accuracy across real-world repos.

### Real limitations and roadmap after 1.0

- JS/TS parsing is only a conservative import-line heuristic, not AST, typing or symbol-level analysis.
- Docker, YAML, infrastructure and hardware are not introspected automatically: infrastructure manifests are merely indexed; hardware is modeled as manual roots.
- No package-manager dependency graph, runtime tracing, call graph or cross-repository graph.
- Automatic code-to-architecture mapping is intentionally not attempted without user input.
- Browser editor cannot edit every evidence/provenance field; relationships are only partially editable.
- Browser localStorage is not a reliable collaborative/project-isolated database; keep exported overlays in version control.
- Potential impact shows traversable known edges, not proven runtime failures; coverage and test execution still need external verification.
- The Graphify/Backstage/LikeC4 concepts informed the design, but their source implementations were not copied, linked as mandatory dependencies, or embedded.
- UI browser integration, large-repo performance and CI outcomes require independent verification before claiming production-grade reliability.

### Versioning and security

The intended v1.0 scope is a local, non-destructive Python/JS/TS code inventory with an editable conceptual overlay. This is a self-contained candidate implementation; public repository visibility does not grant permission to access private code or servers. Scanning untrusted repositories can consume resources; use an isolated machine when necessary.


## Experimental v1.1 extensions: requested research views

The standalone app now adds:
- **Interactive point graph** showing up to 130 manually classified conceptual nodes with root/trunk/branch columns and links. Click a point for its textual detail and editing panel; switch to text-only mode. Long names are abbreviated in the graphic.
- **Git timeline (read-only):** recent commits, date, message and modified files (up to 30). This is a chronological research view, not historical snapshots of the entire conceptual map. Full version-by-version graph diff remains future work.
- **Document index separate from architecture:** scans Markdown file names and headings only. The program does **not** interpret their meaning or rewrite conceptual nodes from docs.
- **Infrastructure heuristic:** detects Compose services by basic indentation and Dockerfiles. This is not a full YAML parser, service dependency resolver or live hardware scanner.
- **Test inventory:** lists test-like files without running them. Discovery does not imply success.
- **Evidence-aware graph palette:** green requires a test evidence entry with `source: "test", result: "pass"` and no open issues; red requires `result: "fail"`; yellow is used for issues or incomplete implementation, grey for unknown. This evidence is currently user supplied and **not cryptographically checked or linked to CI**. Never confuse a green badge with a verified CI result.

Test locally with `python -m unittest discover -s tests -v`.

**Deferred to optional Serveria integration:** AI-assisted architecture classification, doc interpretation, suggestions and human review. No AI is included or required in this release.

### Outstanding limitations

Detailed JS/TS semantic analysis and reliable test result ingestion from CI are not complete; the current engine remains import-oriented. The point graph is a compact SVG proof of concept, not a large-scale force-directed/zoomable visualization. Comparative version snapshots are not automatically preserved. Large repositories, private projects and browser workflows still need hands-on validation.

### Latest graph and historical drill-down

Selecting a conceptual point opens a textual card and lists recent Git commits touching its linked `code_refs` paths, when present. This is an initial historical third dimension, **not** a structural graph diff across arbitrary revisions. JS/TS now indexes some top-level declarations via regular-expression heuristics, each explicitly marked `source: heuristic`; full semantic graphing requires a real parser in a future release.

**Color rules:** green only with explicitly entered passing test evidence, red with explicitly entered failed test evidence, yellow for open issues/in-progress/implemented without passing evidence, gray for unknown. The current app cannot independently prove that a manually entered test outcome is genuine. Test discovery alone yields unknown.

**Deferred for Serveria integration:** AI-assisted categorization and automated interpretation of source/documentation; keep evidence, confidence, proposed change and user approval separate.

**Validation status:** Changes were committed and source files retrieved for inspection. A local clone/test run could not complete because the execution container could not resolve github.com. Do not label the current update as end-to-end verified until CI and browser checks are successful.
