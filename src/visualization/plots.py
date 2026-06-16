"""
Plotting utilities for generating the visualization dashboard.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from typing import Mapping

from src.pathways.base import PathwayResult


class Dashboard:
    """Generates plots to visualize AGI->ASI trajectories."""
    
    def __init__(self, style: str = 'dark_background'):
        plt.style.use(style)
        
    def plot_scenario_comparison(self, scenarios: Mapping[str, PathwayResult], save_path: str | None = None) -> None:
        """Plot the effective compute growth for multiple scenarios."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for name, res in scenarios.items():
            if not res.time_series or "effective_compute" not in res.time_series:
                continue
                
            years = res.time_series["year"]
            compute = res.time_series["effective_compute"]
            
            # Plot line
            line = ax.plot(years, compute, label=name, linewidth=2)[0]
            
            # Mark bottleneck if hit
            if res.bottleneck_hit and res.bottleneck_year:
                ax.plot(
                    res.bottleneck_year, 
                    compute[int(res.bottleneck_year * 10)], # Assumes resolution=10
                    'x', 
                    color=line.get_color(), 
                    markersize=10,
                    mew=2
                )
                ax.annotate(
                    f"Bottleneck:\n{res.bottleneck_name}",
                    (res.bottleneck_year, compute[int(res.bottleneck_year * 10)]),
                    xytext=(10, -20),
                    textcoords='offset points',
                    color=line.get_color(),
                    fontsize=9
                )
                
        ax.set_yscale('log')
        ax.set_title("AGI to ASI: Trajectory Scenarios", fontsize=14)
        ax.set_xlabel("Years after AGI", fontsize=12)
        ax.set_ylabel("Effective Compute (Log Scale)", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"Saved plot to {save_path}")
        else:
            plt.show()
            
    def plot_capabilities(self, scenario: PathwayResult, save_path: str | None = None) -> None:
        """Display the unlocked capabilities as a timeline/list."""
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis('off')
        
        title = f"Unlocked Capabilities: {scenario.pathway_name}"
        if scenario.bottleneck_hit:
            title += " (Bottlenecked)"
            
        ax.text(0.5, 0.9, title, fontsize=14, ha='center', weight='bold')
        
        y_pos = 0.7
        for i, cap in enumerate(scenario.capabilities_unlocked):
            ax.text(0.1, y_pos - (i * 0.1), f"✓ {cap}", fontsize=12)
            
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"Saved capabilities to {save_path}")
        else:
            plt.show()
