import tempfile
import unittest
from pathlib import Path
from codeatlas.app import build_report

class DesktopSmokeTests(unittest.TestCase):
    def test_can_scan_an_arbitrary_selected_folder(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"demo.py").write_text("def hello(): return 'ok'\n",encoding="utf-8")
            report=build_report(root)
            self.assertTrue(any(n["id"]=="file:demo.py" for n in report["atlas"]["nodes"]))
            self.assertTrue(any(n["name"]=="hello" for n in report["atlas"]["nodes"]))

    def test_view_script_served_by_desktop(self):
        import threading
        import urllib.request
        from http.server import ThreadingHTTPServer
        from codeatlas.desktop import AtlasHandler, INDEX
        with ThreadingHTTPServer(('127.0.0.1', 0), AtlasHandler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                for path, filename in (('/', 'cora-direzione.html'), ('/cora-direzione.html', 'cora-direzione.html'), ('/direzione.html', 'direzione.html'), ('/index.html', 'index.html'), ('/cora-plan.json', 'cora-plan.json')):
                    with urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}{path}') as response:
                        self.assertEqual(response.read(), (INDEX.parent / filename).read_bytes())
                for asset in ('cora-direzione.js', 'direzione.js', 'views.js', 'profiles.js', 'evidence.js', 'workbench.js'):
                    with urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/{asset}') as response:
                        self.assertIn('javascript', response.headers['Content-Type'])
                        self.assertEqual(response.read(), (INDEX.parent / asset).read_bytes())
            finally:
                server.shutdown()
                thread.join(timeout=3)
