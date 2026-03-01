import unittest
from src.utils.logger import Logger

class TestLogger(unittest.TestCase):
    def test_logger_setup(self):
        logger = Logger().get_logger()
        self.assertIsInstance(logger, logging.Logger)

if __name__ == '__main__':
    unittest.main()
