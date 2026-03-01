"""DDoS simulator module for sending concurrent requests to target URLs."""

import json
import os
import threading

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DDoSSimulator:
    """Simulates DDoS traffic by spawning threads that repeatedly hit target URLs."""

    def __init__(self):
        """Initialize the simulator and load targets from config."""
        self.targets = self.load_targets()

    def load_targets(self):
        """Load and return the list of targets from config/targets.json."""
        config_path = os.path.join(BASE_DIR, '..', '..', 'config', 'targets.json')
        with open(config_path, 'r') as f:
            return json.load(f)['targets']

    def attack_target(self, target):
        """Send 10 GET requests to a single target, logging any request errors.
        
        Args:
            target (dict): Target dict with 'id' and 'url' keys.
        """
        for _ in range(10):
            try:
                requests.get(target['url'])
            except requests.exceptions.RequestException as e:
                print(f"Error attacking {target['id']}: {e}")

    def run(self):
        """Spawn one thread per target and wait for all to complete."""
        threads = []
        for target in self.targets:
            thread = threading.Thread(target=self.attack_target, args=(target,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()