"""
Command-line interface for the AGI-to-ASI framework.
"""

import argparse
import sys

from src.simulator import Simulator


def main():
    parser = argparse.ArgumentParser(
        description="AGI to ASI Simulation Framework (arXiv:2606.12683)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Sim command
    sim_parser = subparsers.add_parser("simulate", help="Run scenario simulations")
    sim_parser.add_parser("simulate", help="Run scenario simulations")
    sim_parser.add_argument("--years", type=float, default=10.0, help="Years to simulate post-AGI")
    sim_parser.add_argument("--no-plot", action="store_true", help="Disable plotting")
    
    # Agenda command
    subparsers.add_parser("agenda", help="View the research agenda and benchmarks")
    
    args = parser.parse_args()
    
    simulator = Simulator()
    
    if args.command == "simulate":
        simulator.run_all_scenarios(years=args.years, plot=not args.no_plot)
    elif args.command == "agenda":
        simulator.show_research_agenda()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
