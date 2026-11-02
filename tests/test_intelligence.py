import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from codeatlas.intelligence import documentation,infrastructure,test_evidence,history

class ResearchTests(unittest.TestCase):
    def test_documents_compose_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/"README.md").write_text("# Hello\n## Setup\n",encoding="utf-8")
            (p/"compose.yml").write_text("services:\n  api:\n    image: python\n  db:\n    image: postgres\n",encoding="utf-8")
            (p/"test_main.py").write_text("def test_ok(): assert True\n",encoding="utf-8")
            self.assertEqual(documentation(p)[0]["headings"],["Hello","Setup"])
            self.assertEqual(infrastructure(p)[0]["services"],["api","db"])
            evidence=test_evidence(p)
            self.assertFalse(evidence["executed"])
            self.assertEqual(evidence["status"],"unknown")
            self.assertIn("test_main.py",evidence["test_files"])
    def test_bounded_history(self):
        with patch("codeatlas.intelligence._git",return_value="a"*40+"\t2026-11-02T12:00:00Z\tFix\n\nmain.py\n"):
            result=history(Path("."),15)
            self.assertEqual(result[0]["files"],["main.py"])

if __name__=="__main__":
    unittest.main()
