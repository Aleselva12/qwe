"""Launch CodeAtlas locally against a repository, without modifying that repository.

Usage: python -m codeatlas.app /path/to/project --overlay /path/to/map.json
"""
import argparse
import json
import tempfile
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from functools import partial

from .engine import inventory, compare, impact
from .overlay import load
from .intelligence import enrich
from .snapshots import diff_snapshots, read_snapshot, read_junit

def build_report(root: Path, overlay_path=None, changed=None, previous=None, junit=None):
    atlas = inventory(root)
    report = {"atlas": atlas, "intelligence": enrich(root)}
    if overlay_path:
        overlay = load(overlay_path)
        report["overlay"] = overlay
        report["comparison"] = compare(atlas, overlay)
        if changed:
            report["impact"] = impact(atlas, overlay, changed)
    if previous:
        report["snapshot_diff"] = diff_snapshots(read_snapshot(Path(previous)), report)
    if junit:
        report["test_results"] = read_junit(Path(junit))
    return report

def main():
    parser=argparse.ArgumentParser(description="Local-only CodeAtlas repository explorer")
    parser.add_argument("repository",type=Path)
    parser.add_argument("--overlay",type=Path,help="Optional conceptual map JSON")
    parser.add_argument("--changed",action="append",default=[],help="Change impact node ID (repeatable)")
    parser.add_argument("--previous",type=Path,help="Older exported report JSON for structural diff")
    parser.add_argument("--junit",type=Path,help="JUnit XML evidence file, not executed by CodeAtlas")
    parser.add_argument("--save-report",type=Path,help="Export current report JSON as a version snapshot")
    parser.add_argument("--port",type=int,default=8765)
    parser.add_argument("--no-browser",action="store_true")
    args=parser.parse_args()
    if not (1<=args.port<=65535):parser.error("Port must be 1..65535")
    report=build_report(args.repository,args.overlay,args.changed,args.previous,args.junit)
    if args.save_report:
        args.save_report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    index=Path(__file__).resolve().parent.parent/"index.html"
    if not index.is_file():parser.error("index.html not found next to codeatlas package")
    with tempfile.TemporaryDirectory(prefix="codeatlas-") as temporary:
        directory=Path(temporary)
        (directory/"index.html").write_bytes(index.read_bytes())
        (directory/"report.json").write_text(json.dumps(report,ensure_ascii=False),encoding="utf-8")
        if (index.parent/"examples"/"conceptual-map.json").is_file():
            (directory/"examples").mkdir()
            (directory/"examples"/"conceptual-map.json").write_bytes((index.parent/"examples"/"conceptual-map.json").read_bytes())
        handler=partial(SimpleHTTPRequestHandler,directory=str(directory))
        server=ThreadingHTTPServer(("127.0.0.1",args.port),handler)
        address=f"http://127.0.0.1:{server.server_port}/"
        print(f"CodeAtlas ready at {address} — {len(report['atlas']['nodes'])} nodes",flush=True)
        if not args.no_browser:webbrowser.open(address)
        try:server.serve_forever()
        except KeyboardInterrupt:pass
        finally:server.server_close()

if __name__=="__main__":
    main()
