import json
import tempfile
import unittest
from pathlib import Path
from codeatlas.app import build_report

class LocalAppTests(unittest.TestCase):
    def test_build_report_and_impact(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"service.py").write_text("def ping(): return True\n",encoding="utf-8")
            overlay=root.parent/("atlas-test-"+root.name+".json")
            overlay.write_text(json.dumps({"schema_version":1,"groups":[{"id":"service","name":"Service","lens":"trunk","code_refs":["file:service.py"]}],"relations":[]}),encoding="utf-8")
            try:
                report=build_report(root,overlay,["file:service.py"])
                self.assertEqual(report["comparison"]["summary"]["mapped"],1)
                self.assertEqual(report["impact"]["changed"],["file:service.py"])
                self.assertTrue(any(n["name"]=="ping" for n in report["atlas"]["nodes"]))
            finally:overlay.unlink(missing_ok=True)
