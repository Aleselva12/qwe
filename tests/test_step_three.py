import unittest
from codeatlas.overlay import validate

class StepThreeTests(unittest.TestCase):
    def base(self):
        return {"schema_version":1,"groups":[{"id":"root","name":"Hardware","lens":"roots","goals":[{"text":"Provide sufficient memory","status":"planned","source":"manual"}],"decisions":[{"text":"Use dedicated runtime","source":"manual"}],"issues":[{"text":"Memory not measured","source":"manual"}],"evidence":[{"text":"Configuration note","source":"document","ref":"README.md"}]}],"relations":[]}

    def test_valid_card(self):
        self.assertEqual(validate(self.base())["groups"][0]["goals"][0]["status"],"planned")

    def test_invalid_source(self):
        data=self.base()
        data["groups"][0]["evidence"][0]["source"]="verified_by_magic"
        with self.assertRaises(ValueError):
            validate(data)

    def test_invalid_goal_status(self):
        data=self.base()
        data["groups"][0]["goals"][0]["status"]="complete"
        with self.assertRaises(ValueError):
            validate(data)

    def test_blank_entries_rejected(self):
        data=self.base()
        data["groups"][0]["issues"][0]["text"]=" "
        with self.assertRaises(ValueError):
            validate(data)
