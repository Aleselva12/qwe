import unittest
from codeatlas.engine import impact

class ImpactTests(unittest.TestCase):
    def test_propagates_to_conceptual_branch(self):
        atlas={"nodes":[{"id":"file:core.py"},{"id":"file:ui.py"}],"edges":[{"from":"file:ui.py","to":"file:core.py","kind":"imports"}]}
        overlay={"schema_version":1,"groups":[{"id":"trunk","name":"Trunk","lens":"trunk","code_refs":["file:core.py"]},{"id":"chat","name":"Chat","lens":"branches","code_refs":["file:ui.py"]}],"relations":[{"from":"chat","to":"trunk","kind":"depends_on"}]}
        result=impact(atlas,overlay,["file:core.py"])
        self.assertIn("file:ui.py",result["potentially_affected"])
        self.assertIn("trunk",result["potentially_affected"])
        self.assertIn("chat",result["potentially_affected"])
    def test_unknown_changes(self):
        result=impact({"nodes":[],"edges":[]},{"schema_version":1,"groups":[],"relations":[]},["missing"])
        self.assertEqual(result["unknown"],["missing"])
