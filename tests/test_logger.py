"""Tests for the main entry point."""

import unittest
from unittest.mock import patch


class TestMain(unittest.TestCase):
    """Test suite for main()."""

    @patch('src.main.DDoSSimulator')
    def test_main(self, mock_simulator):
        """Ensure main() instantiates DDoSSimulator and calls run() exactly once."""
        from src.main import main
        main()
        mock_simulator.assert_called_once()
        mock_simulator.return_value.run.assert_called_once()


if __name__ == '__main__':
    unittest.main()