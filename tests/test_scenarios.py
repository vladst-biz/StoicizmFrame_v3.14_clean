# ============================================================
#  StoicizmFrame — TestScenarioBuilder v3.15
#  Тест фабрики сценариев через ScenarioBuilder
# ============================================================

import unittest
from src.scenario.scenario_builder import ScenarioBuilder
from src.ai.azure_foundry_client import AzureFoundryClient


class TestScenarioBuilder(unittest.TestCase):
    def test_build_scenario(self):
        client = AzureFoundryClient()
        builder = ScenarioBuilder(client)

        scenario = builder.build("Test")

        self.assertIsNotNone(scenario.entry)
        self.assertIsNotNone(scenario.body)
        self.assertIsNotNone(scenario.legacy)


if __name__ == "__main__":
    unittest.main()
