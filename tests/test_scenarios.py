# -*- coding: utf-8 -*-
import unittest
from src.scenario_builder import build_scenario

class TestScenarioBuilder(unittest.TestCase):
    def test_build_scenario(self):
        scenario = build_scenario("Test", ["scene1", "scene2"])
        self.assertEqual(scenario["title"], "Test")
        self.assertEqual(scenario["length"], 2)

if __name__ == "__main__":
    unittest.main()
