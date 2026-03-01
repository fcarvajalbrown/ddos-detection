import requests
import threading
from time import sleep

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
