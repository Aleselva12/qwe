import tempfile
import unittest
from pathlib import Path
from codeatlas.engine import inventory, compare

class EngineTests(unittest.TestCase):
    def test_python_typescript_and_infra(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"app.py").write_text("import json\nclass Service: pass\ndef serve(): pass\n",encoding="utf-8")
            (root/"client.ts").write_text("import {x} from './utils'\n",encoding="utf-8")
            (root/"utils.ts").write_text("export const x = 1;\n",encoding="utf-8")
            (root/"compose.yml").write_text("services: {}\n",encoding="utf-8")
            (root/"node_modules").mkdir()
            (root/"node_modules"/"ignore.ts").write_text("x",encoding="utf-8")
            data=inventory(root)
            ids={n["id"] for n in data["nodes"]}
            self.assertIn("file:app.py",ids)
            self.assertIn("file:client.ts",ids)
            self.assertIn("file:compose.yml",ids)
            self.assertNotIn("file:node_modules/ignore.ts",ids)
            self.assertTrue(any(n["name"]=="Service" for n in data["nodes"]))
            self.assertTrue(any(e["from"]=="file:client.ts" and e["to"]=="file:utils.ts" for e in data["edges"]))
            overlay={"schema_version":1,"groups":[{"id":"g","name":"Core","lens":"trunk","code_refs":["file:app.py","file:missing.py"]}],"relations":[]}
            result=compare(data,overlay)
            self.assertEqual(result["results"][0]["classification"],"partially_mapped")
            self.assertEqual(result["summary"]["partial"],1)

    def test_unmapped_not_a_false_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            atlas=inventory(Path(temp))
            result=compare(atlas,{"schema_version":1,"groups":[{"id":"x","name":"Feature","lens":"branches"}],"relations":[]})
            self.assertEqual(result["results"][0]["classification"],"unmapped")

if __name__=="__main__":
    unittest.main()
