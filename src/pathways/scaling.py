"""
Pathway 1: Scaling compute, models, and data.

Based on Section 5.1 of the paper.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.compute.growth_model import ComputeGrowthModel
from src.compute.scaling_laws import CapabilityExtrapolator
from .base import AGItoASIPathway, PathwayResult


@dataclass
class DataWallConstraints:
    """Models the exhaustion of high-quality human data (Section 5.1)."""
    exhaustion_year: float = 4.0  # e.g., 4 years from now
    synthetic_data_efficiency: float = 0.5  # How well synthetic data substitutes
    
    def effective_data_multiplier(self, year: float) -> float:
        """Calculate effective data scaling taking the data wall into account."""
        if year <= self.exhaustion_year:
            return 1.0  # No penalty
            
        # Post-exhaustion, growth relies on synthetic data which is less efficient
        years_past = year - self.exhaustion_year
        # Exponential decay of effective data growth
        return self.synthetic_data_efficiency ** years_past


class ScalingPathway(AGItoASIPathway):
    """
    Simulates the pathway of pure quantitative scaling of compute and data
    to transition from AGI to ASI.
    """
    
    def __init__(
        self, 
        growth_model: ComputeGrowthModel,
        capability_model: CapabilityExtrapolator,
        data_wall: DataWallConstraints | None = None
    ):
        self.growth_model = growth_model
        self.capability_model = capability_model
        self.data_wall = data_wall or DataWallConstraints()
        
    @property
    def name(self) -> str:
        return "Quantitative Scaling"
        
    @property
    def description(self) -> str:
        return (
            "Extrapolating current scaling laws. Assumes AGI is reached and "
            "subsequent progress is driven by massive scaling of effective "
            "compute and data (including synthetic), without fundamental "
            "paradigm shifts."
        )
        
    def simulate(self, years: float, initial_compute: float = 1.0) -> PathwayResult:
        """Simulate scaling over time, accounting for the data wall."""
        t_points = []
        compute_points = []
        eff_compute_points = []
        
        bottleneck_hit = False
        bottleneck_year = None
        
        resolution = 10 # 10 steps per year
        total_steps = int(years * resolution)
        
        for step in range(total_steps + 1):
            year = step / resolution
            t_points.append(year)
            
            # Raw effective compute growth (hardware + algos)
            raw_compute = self.growth_model.effective_compute_at_year(year) * initial_compute
            compute_points.append(raw_compute)
            
            # Apply data wall friction
            data_penalty = self.data_wall.effective_data_multiplier(year)
            if data_penalty < 1.0 and not bottleneck_hit:
                bottleneck_hit = True
                bottleneck_year = year
                
            # If we lack data, we can't fully utilize compute optimally (Chinchilla)
            # So effective capabilities grow slower than raw compute
            eff_compute = raw_compute * data_penalty
            eff_compute_points.append(eff_compute)
            
        final_compute = eff_compute_points[-1]
        capabilities = self.capability_model.capabilities_at_compute(final_compute)
        
        return PathwayResult(
            pathway_name=self.name,
            final_compute_multiplier=final_compute / initial_compute,
            capabilities_unlocked=capabilities,
            bottleneck_hit=bottleneck_hit,
            bottleneck_name="Data Wall" if bottleneck_hit else None,
            bottleneck_year=bottleneck_year,
            time_series={
                "year": t_points,
                "raw_compute": compute_points,
                "effective_compute": eff_compute_points
            }
        )
