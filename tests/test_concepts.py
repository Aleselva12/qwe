import json
import tempfile
import threading
import unittest
from pathlib import Path
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from codeatlas.app import build_report
from codeatlas.desktop import AtlasHandler
from codeatlas.overlay import validate
from codeatlas.engine import inventory


class FunctionalMapTests(unittest.TestCase):
    def test_relative_python_imports_and_typescript_responsibilities(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'pkg').mkdir()
            (root/'pkg'/'app.py').write_text('from .calendar import sync\n')
            (root/'pkg'/'calendar.py').write_text('def sync(): pass\n')
            (root/'calendar.ts').write_text('export function syncCalendar() {}\nexport const schedule = () => 1;\n')
            atlas = inventory(root)
            self.assertTrue(any(e['from']=='file:pkg/app.py' and e['to']=='file:pkg/calendar.py' for e in atlas['edges']))
            self.assertTrue({'syncCalendar','schedule'} <= {n['name'] for n in atlas['nodes']})

    def test_suggestions_are_valid_deterministic_and_do_not_invent_intent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'calendar.py').write_text('def sync(): pass\n')
            (root/'app.py').write_text('import calendar\n')
            a, b = build_report(root), build_report(root)
            validate(a['overlay'])
            self.assertEqual(a['overlay'], b['overlay'])
            groups = a['overlay']['groups']
            calendar = next(n for n in groups if n['id']=='concept:calendar')
            self.assertEqual(calendar['lens'], 'branches')
            self.assertTrue(any(n.get('parent') == calendar['id'] for n in groups))
            self.assertTrue(any(n['lens']=='roots' for n in groups))
            self.assertTrue(all(n['source']=='heuristic' and not n['purpose'] for n in groups))
            self.assertTrue(any(e['to']==calendar['id'] for e in a['overlay']['relations']))
            self.assertEqual(sorted(p.name for p in root.iterdir()), ['app.py','calendar.py'])

    def test_unknown_and_empty_projects_are_honest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(build_report(root)['overlay']['groups'], [])
            (root/'odd.py').write_text('x=1\n')
            self.assertTrue(any(n['lens']=='unassigned' for n in build_report(root)['overlay']['groups']))

    def test_desktop_open_reload_and_rejected_requests(self):
        handler = type('TestHandler',(AtlasHandler,),{'token':'test-token'})
        server = ThreadingHTTPServer(('127.0.0.1',0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as d:
                (Path(d)/'app.py').write_text('def start(): pass\n')
                host = '127.0.0.1:'+str(server.server_port)
                def request(method, path, body=None, headers=None):
                    c=HTTPConnection('127.0.0.1',server.server_port)
                    c.request(method,path,body,headers or {})
                    r=c.getresponse(); result=(r.status,json.loads(r.read())); c.close(); return result
                body=json.dumps({'path':d})
                self.assertEqual(request('POST','/api/open',body)[0],403)
                headers={'Origin':'http://'+host,'X-Atlas-Token':'test-token','Content-Type':'application/json'}
                self.assertEqual(request('POST','/api/open',body,headers)[0],200)
                code, report=request('GET','/report.json')
                self.assertEqual(code,200)
                self.assertTrue(report['overlay']['groups'])
                self.assertTrue(request('GET','/api/session')[1]['loaded'])
                self.assertEqual(request('POST','/api/open',json.dumps({'path':d+'/missing'}),headers)[0],400)
                self.assertEqual(request('GET','/report.json')[1]['project_key'], str(Path(d).resolve()))
        finally:
            server.shutdown(); server.server_close(); thread.join()
