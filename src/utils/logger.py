"""Logger module providing a configured logger instance for the tool."""

import logging


class Logger:
    """Wraps Python's logging module with a pre-configured stream handler."""

    def __init__(self):
        """Set up the DDoSLogger with formatting."""
        self.logger = logging.getLogger('DDoSLogger')
        self.setup_logger()

    def setup_logger(self):
        """Attach a stream handler with timestamp/level formatting."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """Return the configured logger instance."""
        return self.logger