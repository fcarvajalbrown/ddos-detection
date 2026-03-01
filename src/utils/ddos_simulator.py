import requests
import threading
from time import sleep
import os

# In ddos_simulator.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, '..', '..', 'config', 'targets.json')

with open(config_path, 'r') as f:
    return json.load(f)

class DDoSSimulator:
    def __init__(self):
        self.targets = self.load_targets()

    def load_targets(self):
        with open('../config/targets.json', 'r') as f:
            targets_data = json.load(f)
        return targets_data['targets']

    def attack_target(self, target):
        for _ in range(10):
            try:
                requests.get(target['url'])
            except requests.exceptions.RequestException as e:
                print(f"Error attacking {target['id']}: {e}")

    def run(self):
        threads = []
        for target in self.targets:
            thread = threading.Thread(target=self.attack_target, args=(target,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
