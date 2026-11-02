import tempfile
import unittest
from pathlib import Path
from codeatlas.snapshots import diff_snapshots, read_junit, read_snapshot

class SnapshotTests(unittest.TestCase):
    def test_diff(self):
        a={"atlas":{"nodes":[{"id":"a","name":"A"}],"edges":[]}}
        b={"atlas":{"nodes":[{"id":"a","name":"Changed"},{"id":"b","name":"B"}],"edges":[{"from":"b","to":"a","kind":"imports"}]}}
        diff=diff_snapshots(a,b)
        self.assertEqual(diff["added_nodes"],["b"])
        self.assertEqual(diff["changed_nodes"],["a"])
        self.assertEqual(len(diff["added_edges"]),1)

    def test_junit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"junit.xml"
            p.write_text('<testsuite><testcase name="ok" classname="x"/><testcase name="bad" classname="x"><failure message="oops"/></testcase><testcase name="skip"><skipped/></testcase></testsuite>',encoding="utf-8")
            result=read_junit(p)
            self.assertEqual(result["summary"],{"pass":1,"fail":1,"skip":1})

if __name__=="__main__":
    unittest.main()
