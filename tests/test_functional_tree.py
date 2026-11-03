"""User capabilities and source-level operations are different abstractions."""
import tempfile
import unittest
from pathlib import Path
from codeatlas.app import build_report
from codeatlas.overlay import validate


class FunctionalTreeTests(unittest.TestCase):
    def test_four_arithmetic_operations_remain_one_calculator_capability(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'README.md').write_text('# Calcolatrice\n\nEsegue calcoli aritmetici.\n')
            (root/'calculator.py').write_text('import math\ndef add(a,b): return a+b\n')
            first=build_report(root)['overlay']
            (root/'calculator.py').write_text('import math\ndef add(a,b): return a+b\ndef subtract(a,b): return a-b\ndef multiply(a,b): return a*b\ndef divide(a,b): return a/b\n')
            model=validate(build_report(root)['overlay'])
            capabilities=[g for g in model['groups'] if g.get('role')=='capability']
            self.assertEqual([(g['id'],g['name']) for g in capabilities],
                             [(g['id'],g['name']) for g in first['groups'] if g.get('role')=='capability'])
            self.assertEqual(len(capabilities),1)
            self.assertEqual(capabilities[0]['name'],'Calcolatrice')
            ops=[g for g in model['groups'] if g['name'] in {'add','subtract','multiply','divide'}]
            self.assertEqual(len(ops),4)
            self.assertTrue(all(g['role']=='process' and g['parent']=='concept:file:calculator.py' for g in ops))
            self.assertTrue(all(g['role']=='foundation' for g in model['groups'] if g['id'].startswith('concept:runtime-')))
            imported=next(g for g in model['groups'] if g['id']=='concept:import:math')
            self.assertEqual(imported['role'],'foundation')
            self.assertIn('verificare',imported['description'])
            self.assertFalse(any('hardware' in g['id'] for g in model['groups']))

    def test_tests_are_support_evidence_and_legacy_overlays_remain_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'test_app.py').write_text('def test_add(): pass\n')
            groups=build_report(root)['overlay']['groups']
            self.assertTrue(all(g['role']=='foundation' for g in groups if g['id']!='concept:capability:project'))
        validate({'schema_version':1,'groups':[{'id':'old','name':'Vecchia mappa','lens':'branches'}],'relations':[]})
        with self.assertRaisesRegex(ValueError,'functional role'):
            validate({'schema_version':1,'groups':[{'id':'bad','name':'Bad','role':'invented'}],'relations':[]})

    def test_profile_supports_functional_roles_and_flow_without_changing_categories(self):
        from codeatlas.profiles import validate_profile
        p={'schema_version':1,'name':'Team','default_view':'flow','nodes':[{'id':'calc','name':'Calcolatrice','role':'capability','lens':'branches','source':'manual','status':'unknown'}]}
        self.assertEqual(validate_profile(p),p)
        p['nodes'][0]['role']='invented'
        with self.assertRaisesRegex(ValueError,'functional role'):
            validate_profile(p)
