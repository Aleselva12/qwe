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
