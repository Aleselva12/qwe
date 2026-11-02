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

def build_report(root: Path, overlay_path=None, changed=None):
    atlas = inventory(root)
    report = {"atlas": atlas}
    if overlay_path:
        overlay = load(overlay_path)
        report["overlay"] = overlay
        report["comparison"] = compare(atlas, overlay)
        if changed:
            report["impact"] = impact(atlas, overlay, changed)
    return report

def main():
    parser=argparse.ArgumentParser(description="Local-only CodeAtlas repository explorer")
    parser.add_argument("repository",type=Path)
    parser.add_argument("--overlay",type=Path,help="Optional conceptual map JSON")
    parser.add_argument("--changed",action="append",default=[],help="Change impact node ID (repeatable)")
    parser.add_argument("--port",type=int,default=8765)
    parser.add_argument("--no-browser",action="store_true")
    args=parser.parse_args()
    if not (1<=args.port<=65535):parser.error("Port must be 1..65535")
    report=build_report(args.repository,args.overlay,args.changed)
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
