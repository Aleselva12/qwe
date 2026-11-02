"""Double-click local CodeAtlas launcher with a folder-path picker in the web UI."""
import json
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .app import build_report

INDEX = Path(__file__).resolve().parent.parent / "index.html"
EXAMPLE = INDEX.parent / "examples" / "conceptual-map.json"

class AtlasHandler(BaseHTTPRequestHandler):
    report = None
    token = ""
    def _respond(self, status, data, content_type="application/json; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:")
        self.end_headers()
        self.wfile.write(data)
    def _json(self, status, obj):
        self._respond(status, json.dumps(obj, ensure_ascii=False).encode("utf-8"))
    def do_GET(self):
        path = urlsplit(self.path).path
        if path in ("/", "/index.html"):
            self._respond(200, INDEX.read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/session":
            self._json(200, {"token": self.token, "loaded": getattr(self.server, 'report', None) is not None})
        elif path == "/report.json":
            if getattr(self.server, 'report', None) is None:
                self._json(404, {"error":"No repository selected"})
            else:
                self._json(200, self.server.report)
        elif path == "/examples/conceptual-map.json" and EXAMPLE.is_file():
            self._respond(200, EXAMPLE.read_bytes())
        else:
            self._json(404, {"error":"Not found"})
    def do_POST(self):
        if urlsplit(self.path).path != "/api/open":
            return self._json(404, {"error":"Not found"})
        origin = self.headers.get("Origin", "")
        expected = "http://" + self.headers.get("Host", "")
        if origin != expected or self.headers.get("X-Atlas-Token") != self.token:
            return self._json(403, {"error":"Invalid local request"})
        try:
            length = int(self.headers.get("Content-Length", "-1"))
            if not 0 < length <= 4096:
                return self._json(400, {"error":"Invalid request length"})
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            entered = payload.get("path")
            if not isinstance(entered, str) or not entered.strip():
                return self._json(400, {"error":"Enter a folder path"})
            folder = Path(entered.strip().strip('"')).expanduser().resolve()
            if not folder.is_dir():
                return self._json(400, {"error":"The selected path is not a directory"})
            # Read only. The analysis is local; target project code is never executed.
            generated = build_report(folder)
            self.server.report = generated
            return self._json(200, generated)
        except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
            return self._json(400, {"error": str(exc)})
    def log_message(self, format, *args):
        pass

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("Invalid port")
    handler = type("LocalHandler", (AtlasHandler,), {"token": secrets.token_urlsafe(24)})
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        url = f"http://127.0.0.1:{server.server_port}/"
        print("CodeAtlas:",url,flush=True)
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
