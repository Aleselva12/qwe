import tempfile
import unittest
from pathlib import Path
from codeatlas.scanner import scan

class ScannerTests(unittest.TestCase):
    def test_nested_paths_and_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "one" / "one"
            path.mkdir(parents=True)
            (path / "alpha.py").write_text("import json\n\ndef hello():\n    return 1\n")
            result = scan(root)
            ids = {node["id"] for node in result["nodes"]}
            self.assertIn("dir:one/one", ids)
            self.assertIn("file:one/one/alpha.py", ids)
            self.assertTrue(any(node["name"] == "hello" for node in result["nodes"]))
            self.assertEqual(len(result["errors"]), 0)

if __name__ == "__main__":
    unittest.main()
