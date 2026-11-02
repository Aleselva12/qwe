import unittest
from codeatlas.overlay import validate

class OverlayTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(len(validate({"schema_version":1,"groups":[{"id":"h","name":"Hardware","lens":"roots"}],"relations":[]})["groups"]),1)
    def test_cycle(self):
        with self.assertRaises(ValueError):
            validate({"schema_version":1,"groups":[{"id":"a","name":"A","parent":"b"},{"id":"b","name":"B","parent":"a"}]})
    def test_unknown_relation(self):
        with self.assertRaises(ValueError):
            validate({"schema_version":1,"groups":[{"id":"a","name":"A"}],"relations":[{"from":"a","to":"b","kind":"depends_on"}]})
