"""Schema invariants for the human-authored Cora V2 direction plan.

Do not conflate an implemented file, an imported test, and real Debian evidence.
This test reads only the map; it never scans or executes Serveria.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "cora-plan.json").read_text(encoding="utf-8"))


class CoraV2StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = PLAN["nodes"]
        cls.ids = {node["id"]: node for node in cls.nodes}

    def test_ids_unique_and_parents_acyclic(self):
        self.assertEqual(len(self.ids), len(self.nodes))
        for node in self.nodes:
            with self.subTest(node=node["id"]):
                seen = set()
                current = node
                path = []
                while current:
                    ident = current["id"]
                    self.assertNotIn(ident, seen, "circular parent reference")
                    seen.add(ident)
                    path.append(ident)
                    parent = current.get("parent")
                    self.assertTrue(parent is None or parent in self.ids)
                    current = self.ids.get(parent)
                self.assertLessEqual(len(path), 5 if path[-1] == "radici" else 4)

    def test_root_trunk_and_branch_structure(self):
        self.assertEqual(PLAN["version"], 1)
        self.assertEqual([x["id"] for x in self.nodes if x.get("role") == "radici"], ["radici"])
        self.assertEqual([x["id"] for x in self.nodes if x.get("role") == "tronco"], ["tronco"])
        self.assertEqual({x["id"] for x in self.nodes if x.get("role") == "ramo"},
                         {"A", "B", "C", "programmi", "E", "macchine", "G"})
        self.assertEqual({x["id"] for x in self.nodes if x.get("parent") == "radici"},
                         {f"R{i}" for i in range(1, 7)})

        stars = [n for n in self.nodes if n.get("classification") == "star"]
        self.assertEqual(len(stars), 45)
        self.assertEqual(len([s for s in stars if s["id"].startswith("T")]), 13)
        self.assertEqual(len([s for s in stars if s["id"].startswith("R")]), 14)
        self.assertEqual(len([s for s in stars if not s["id"].startswith(("T", "R"))]), 18)
        self.assertEqual(len([n for n in self.nodes if n.get("classification") == "planet"]), 151)
        self.assertEqual(len([n for n in self.nodes if n.get("classification") == "moon"]), 304)
        self.assertEqual(len({n["code"] for n in stars}), len(stars))
        self.assertEqual([s["id"] for s in stars if s.get("parent") == "G"], ["G1"])
        self.assertEqual(PLAN["visibility"]["onSelect"], "planets-and-moons")

    def test_legacy_ids_preserved_and_calendars_future_ideas_not_lost(self):
        for ident in ["programmi", "macchine", "immich", "nextcloud", "magazzino",
                      "worker", "installare", "assegnare", "C1a", "C1b", "C1c", "C1d", "C1e"]:
            self.assertIn(ident, self.ids)
        self.assertEqual(self.ids["worker"]["code"], "F1")
        self.assertEqual(self.ids["immich"]["code"], "D1")
        for ident in ["installare", "assegnare"]:
            self.assertEqual(self.ids[ident]["parent"], "worker")
            self.assertEqual(self.ids[ident]["classification"], "planet")
        for ident in ["C1d", "C1e"]:
            self.assertEqual(self.ids[ident]["status"], "idea")
        self.assertTrue("una sola volta" in self.ids["C1"]["note"])

    def test_status_not_confused_with_health_priority(self):
        severities = {"unknown", "ok", "plan", "minor", "problem"}
        states = {"present", "partial", "planned", "idea", "unverified"}
        for node in self.nodes:
            with self.subTest(node=node["id"]):
                self.assertIn(node.get("priority", "unknown"), severities)
                if "status" in node:
                    self.assertIn(node["status"], states)
                    self.assertEqual(node.get("priority"), "unknown",
                                     "Do not infer green or warning from plan/implementation")

    def test_no_dangling_relations_or_duplicated_stored_links(self):
        accepted = {"uses", "depends_on", "communicates_with", "produces_for"}
        edge_ids = set()
        for edge in PLAN["relations"]:
            key = (edge["from"], edge["to"], edge["kind"])
            self.assertNotIn(key, edge_ids)
            edge_ids.add(key)
            self.assertIn(edge["from"], self.ids)
            self.assertIn(edge["to"], self.ids)
            self.assertIn(edge["kind"], accepted)
            self.assertEqual(edge["status"], "proposed")
        for node in self.nodes:
            for target in node.get("trunkLinks", []):
                self.assertIn(target, self.ids)
                self.assertEqual(self.ids[target]["parent"], "tronco")

    def test_work_priorities_remain_agreed(self):
        self.assertEqual(len(PLAN["nextWork"]), 3)
        self.assertIn("W1 Orchestratore", PLAN["nextWork"][0])
        self.assertIn("W2 Aggiornamenti", PLAN["nextWork"][1])
        self.assertIn("W3 Agente programmatore", PLAN["nextWork"][2])
        self.assertIn("R6.2", self.ids)
        self.assertIn("T11", self.ids)
        self.assertIn("F2", self.ids)


if __name__ == "__main__":
    unittest.main()
