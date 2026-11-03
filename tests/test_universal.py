import tempfile
import unittest
from pathlib import Path
from codeatlas.app import build_report
from codeatlas.snapshots import read_junit
from codeatlas.overlay import validate

class UniversalTests(unittest.TestCase):
    def test_additional_languages_inventory_and_test_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for filename in ('app.go', 'main.rs', 'Site.vue', 'UserTest.java', 'logic_test.go', 'test_views.cjs', 'package.json'):
                (root / filename).write_text('')
            (root / '.github/workflows').mkdir(parents=True)
            (root / '.github/workflows/check.yml').write_text('name: Check')
            report = build_report(root)
            files = {n['path'] for n in report['atlas']['nodes'] if n['kind'] == 'file'}
            self.assertIn('main.rs', files)
            self.assertIn('app.go', files)
            self.assertIn('logic_test.go', report['intelligence']['tests']['test_files'])
            self.assertIn('.github/workflows/check.yml', report['intelligence']['tests']['configurations'])
            self.assertEqual(report['version'], {'commit':'', 'dirty':None})

    def test_junit_metadata_duplicates_failure_and_entities(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'report.xml'
            p.write_text('<testsuite timestamp="2026-11-03T10:00:00Z"><properties><property name="commit" value="abc"/><property name="workspace_clean" value="true"/></properties><testcase name="x" classname="Suite" file="test_x.py"/><testcase name="x" classname="Suite" file="test_x.py"><failure message="broken"/></testcase></testsuite>')
            r = read_junit(p)
            self.assertEqual(r['metadata']['commit'], 'abc')
            self.assertTrue(r['metadata']['workspace_clean'])
            self.assertNotEqual(r['test_cases'][0]['id'], r['test_cases'][1]['id'])
            self.assertEqual(r['test_cases'][1]['message'], 'broken')
            p.write_text('<!DOCTYPE test [<!ENTITY x "value">]><testsuite/>')
            with self.assertRaises(ValueError): read_junit(p)
            p.write_text('<arbitrary/>')
            with self.assertRaises(ValueError): read_junit(p)

    def test_custom_category_overlay_remains_cli_compatible(self):
        m = {'schema_version':1, 'profile':{'schema_version':1, 'name':'Team', 'categories':[{'id':'customers', 'label':'Clienti', 'color':'#abcdef'}]}, 'groups':[{'id':'crm','name':'CRM','lens':'customers','code_refs':[]}], 'relations':[]}
        self.assertEqual(validate(m), m)
        m['profile']['schema_version'] = 9
        with self.assertRaises(ValueError): validate(m)
