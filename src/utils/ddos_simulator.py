"""DDoS simulator module for sending concurrent requests to target URLs."""

import configparser
from cProfile import label
import json
import os
import threading

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DDoSSimulator:
    """Simulates DDoS traffic by spawning threads that repeatedly hit target URLs."""

    def __init__(self, threads_per_target=None):
        """Initialize the simulator, load config and targets."""
        self.config = self._load_config()
        self.targets = self.load_targets()
        self.results = {}
        self.threads_per_target = threads_per_target or int(self.config['General']['max_threads'])
        self.timeout = int(self.config['General']['timeout_seconds'])
        self.requests_per_thread = int(self.config['General']['requests_per_thread'])

    def _load_config(self):
        """Load settings from config/settings.ini."""
        config_path = os.path.join(BASE_DIR, '..', '..', 'config', 'settings.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def load_targets(self):
        """Load and return the list of targets from config/targets.json."""
        config_path = os.path.join(BASE_DIR, '..', '..', 'config', 'targets.json')
        with open(config_path, 'r') as f:
            return json.load(f)['targets']

    def attack_target(self, target):
        """Send GET requests to a single target using a session, logging status, attack type and response time."""
        STATUS_LABELS = {
            200: 'OK',
            403: 'Forbidden',
            404: 'Not Found',
            429: 'Rate Limited',
            503: 'Unavailable',
        }
        TYPE_LABELS = {
            'HTTP_FLOOD': 'HTF',
            'SYN_FLOOD': 'SYN',
            'SLOWLORIS': 'SLW',
        }
        blocked_codes = [int(c) for c in self.config['Reporting']['blocked_codes'].split(',')]
        attack_type = TYPE_LABELS.get(self.config['Simulator']['attack_type'], 'UNK')
        success, blocked, failed = 0, 0, 0
        with requests.Session() as session:
            for i in range(self.requests_per_thread):
                try:
                    response = session.get(target['url'], timeout=self.timeout)
                    label = STATUS_LABELS.get(response.status_code, 'Unknown')
                    elapsed = response.elapsed.total_seconds()
                    print(f"[{target['id']}] [{attack_type}] {i+1}/{self.requests_per_thread}: {response.status_code} {label} ({elapsed:.2f}s)")
                    if response.status_code == 200:
                        success += 1
                    elif response.status_code in blocked_codes:
                        blocked += 1
                    else:
                        failed += 1
                except requests.exceptions.RequestException as e:
                    print(f"[{target['id']}] [{attack_type}] {i+1}/{self.requests_per_thread}: FAILED ({e})")
                    failed += 1
        self.results[target['id']] = {'success': success, 'blocked': blocked, 'failed': failed}

    def run(self):
        threads = []
        for target in self.targets:
            for _ in range(self.threads_per_target):
                thread = threading.Thread(target=self.attack_target, args=(target,))
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.join()

        print("\n===== RESULTS =====")
        for target_id, stats in self.results.items():
            total = sum(stats.values())
            print(f"[{target_id}] Success: {stats['success']} | Blocked: {stats['blocked']} | Failed: {stats['failed']} / {total}")