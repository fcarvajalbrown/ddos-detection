from src.utils.ddos_simulator import DDoSSimulator


def main():
    """Entry point for the DDoS testing tool."""
    simulator = DDoSSimulator()
    simulator.run()


if __name__ == "__main__":
    main()