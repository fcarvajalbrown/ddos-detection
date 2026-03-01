import unittest
from unittest.mock import patch, MagicMock

class TestMain(unittest.TestCase):
    @patch('src.main.DDoSSimulator')
    def test_main(self, mock_simulator):
        from src.main import main
        main()
        mock_simulator.assert_called_once()
        mock_simulator.return_value.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
