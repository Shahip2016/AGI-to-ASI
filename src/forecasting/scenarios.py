"""
Scenario generation and analysis.

Combines pathways and frictions to generate distinct scenarios for
the AGI-to-ASI transition, as suggested in Section 7.1.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.compute.growth_model import ComputeGrowthModel, GrowthFactors
from src.compute.scaling_laws import PowerLawScaling, CapabilityExtrapolator
from src.frictions.models import CompositeFrictionModel, STANDARD_FRICTIONS
from src.pathways.scaling import ScalingPathway, DataWallConstraints
from src.pathways.base import PathwayResult


@dataclass
class Scenario:
    """A specific set of assumptions about the future."""
    name: str
    description: str
    pathway: str # "scaling", "paradigm", "rsi", "multi_agent"
    years: float = 10.0
    include_frictions: bool = True
    
    # In a full implementation, this would hold the specific parameter overrides


class ScenarioGenerator:
    """Generates the standard scenarios discussed in the paper."""
    
    def __init__(self):
        # Default baseline models
        self.growth = ComputeGrowthModel()
        self.scaling = PowerLawScaling(alpha=0.5, c_c=100.0, l_inf=0.0)
        self.capabilities = CapabilityExtrapolator(self.scaling)
        self.capabilities.add_milestone("Competent AGI", 2.0)
        self.capabilities.add_milestone("Expert AGI", 1.0)
        self.capabilities.add_milestone("ASI", 0.5)
        self.capabilities.add_milestone("UAI-Approximation", 0.1)
        
    def generate_scenario_1_smooth_scaling(self) -> PathwayResult:
        """Scenario 1: Smooth scaling with no major bottlenecks."""
        # Overcome data wall easily
        dw = DataWallConstraints(exhaustion_year=10.0) 
        pathway = ScalingPathway(self.growth, self.capabilities, dw)
        
        return pathway.simulate(years=10.0)
        
    def generate_scenario_2_hard_bottlenecks(self) -> PathwayResult:
        """Scenario 2: Compute and data bottlenecks severely slow progress."""
        # Data wall hits early, synthetic data is inefficient
        dw = DataWallConstraints(exhaustion_year=2.0, synthetic_data_efficiency=0.3)
        
        # We model the compute bottleneck by adjusting the growth model itself
        # to represent the impact of the friction over time
        # For simplicity in this demo, we'll just use the ScalingPathway with the tough DataWall
        pathway = ScalingPathway(self.growth, self.capabilities, dw)
        
        # Manually alter the result to simulate the composite friction
        res = pathway.simulate(years=10.0)
        res.pathway_name = "Scaling with Hard Frictions"
        
        # Apply standard frictions
        frictions = CompositeFrictionModel(STANDARD_FRICTIONS)
        for i, t in enumerate(res.time_series["year"]):
            fm = frictions.get_effective_growth_multiplier(t)
            # The friction multiplier slows the derivative of growth, but as an approximation here:
            res.time_series["effective_compute"][i] *= fm
            
        final_compute = res.time_series["effective_compute"][-1]
        res.final_compute_multiplier = final_compute / res.time_series["effective_compute"][0]
        res.capabilities_unlocked = self.capabilities.capabilities_at_compute(final_compute)
        
        res.bottleneck_hit = True
        res.bottleneck_name = "Multiple (Data, Power, Eval)"
        res.bottleneck_year = 2.0
        
        return res
        
    def generate_all(self) -> dict[str, PathwayResult]:
        """Generate all baseline scenarios for comparison."""
        return {
            "Smooth Scaling": self.generate_scenario_1_smooth_scaling(),
            "Hard Bottlenecks": self.generate_scenario_2_hard_bottlenecks()
        }
