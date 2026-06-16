"""
Integrated Simulator for the AGI to ASI transition.
"""

from __future__ import annotations

import argparse
import sys
from typing import Mapping

from src.forecasting.scenarios import ScenarioGenerator
from src.visualization.plots import Dashboard
from src.research_agenda.open_questions import ResearchAgenda
from src.pathways.base import PathwayResult


class Simulator:
    """Main interface for running the AGI to ASI simulations."""
    
    def __init__(self):
        self.generator = ScenarioGenerator()
        self.dashboard = Dashboard()
        
    def run_all_scenarios(self, years: float = 10.0, plot: bool = True) -> Mapping[str, PathwayResult]:
        """Run all predefined scenarios and optionally plot them."""
        print(f"Simulating AGI to ASI transition over {years} years...")
        scenarios = self.generator.generate_all()
        
        for name, res in scenarios.items():
            print(f"\nScenario: {name}")
            print(f"  Pathway: {res.pathway_name}")
            print(f"  Final Compute Multiplier: {res.final_compute_multiplier:.2f}x")
            print(f"  Bottleneck Hit: {res.bottleneck_hit}")
            if res.bottleneck_hit:
                print(f"  Bottleneck Name: {res.bottleneck_name}")
            print(f"  Capabilities Unlocked: {len(res.capabilities_unlocked)}")
            for cap in res.capabilities_unlocked:
                print(f"    - {cap}")
                
        if plot:
            self.dashboard.plot_scenario_comparison(scenarios)
            
        return scenarios
        
    def show_research_agenda(self) -> None:
        """Display the research agenda from the paper."""
        ResearchAgenda.print_agenda()
