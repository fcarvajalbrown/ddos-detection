import unittest
from src.utils.ddos_simulator import DDoSSimulator

class TestDDoSSimulator(unittest.TestCase):
    def test_load_targets(self):
        simulator = DDoSSimulator()
        targets = simulator.load_targets()
        self.assertEqual(len(targets), 2)

if __name__ == '__main__':
    unittest.main()
