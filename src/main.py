from src.utils.ddos_simulator import DDoSSimulator

def main():
    simulator = DDoSSimulator()
    simulator.run()

def load_targets(self):
    with open(config_path, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    main()
