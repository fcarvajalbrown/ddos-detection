"""Tests for the DDoSSimulator class."""

import unittest
from src.utils.ddos_simulator import DDoSSimulator


class TestDDoSSimulator(unittest.TestCase):
    """Test suite for DDoSSimulator."""

    def test_load_targets(self):
        """Ensure load_targets returns the correct number of targets from config."""
        simulator = DDoSSimulator()
        targets = simulator.load_targets()
        self.assertEqual(len(targets), 9, "Expected 9 targets from config")


if __name__ == '__main__':
    unittest.main()