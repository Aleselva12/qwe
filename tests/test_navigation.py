"""Regressions for source hierarchy and cross-directory JS dependencies."""
import tempfile
import unittest
from pathlib import Path
from codeatlas.app import build_report
from codeatlas.engine import inventory
from codeatlas.overlay import validate


class NavigationTests(unittest.TestCase):
    def test_declarations_are_scoped_to_their_source_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'engine.py').write_text('import scanner\ndef start(): pass\n')
            (root / 'scanner.py').write_text('def start(): pass\n')
            report = build_report(root)
            groups = validate(report['overlay'])['groups']
            files = {n['id']: n for n in groups if n['id'].startswith('concept:file:')}
            starts = [n for n in groups if n['name'] == 'start']
            self.assertEqual(len(starts), 2)
            self.assertEqual({n['parent'] for n in starts}, set(files))
            self.assertTrue(all(n['parent'] == 'concept:analysis' for n in files.values()))
            node_ids = {n['id'] for n in report['atlas']['nodes']}
            for declaration in starts:
                self.assertTrue(set(declaration['code_refs']) <= node_ids)
                self.assertTrue(all(':start:' in ref for ref in declaration['code_refs']))
            self.assertTrue(any(e['from'] == 'concept:file:engine.py' and e['to'] == 'concept:file:scanner.py'
                                for e in report['overlay']['relations']))
            identities = {n['id'] for n in starts}
            (root / 'engine.py').write_text('\n\ndef start(): pass\n')
            self.assertEqual(identities, {n['id'] for n in build_report(root)['overlay']['groups'] if n['name'] == 'start'})

    def test_js_parent_directory_imports_resolve_to_real_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'src' / 'views').mkdir(parents=True)
            (root / 'src' / 'utils.ts').write_text('export const value = 1;\n')
            (root / 'src' / 'views' / 'page.ts').write_text("import {value} from '../utils';\n")
            edge = inventory(root)['edges'][0]
            self.assertEqual(edge['to'], 'file:src/utils.ts')
            self.assertEqual(edge['resolution'], 'local-exact')
