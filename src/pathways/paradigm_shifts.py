"""
Pathway 2: Algorithmic Paradigm Shifts.

Based on Section 5.2 of the paper.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from src.compute.growth_model import ComputeGrowthModel
from src.compute.scaling_laws import CapabilityExtrapolator
from .base import AGItoASIPathway, PathwayResult


@dataclass
class ParadigmShiftEvent:
    """A qualitative leap in architecture or algorithm."""
    name: str
    year_expected: float
    compute_efficiency_multiplier: float
    capabilities_unlocked: list[str]


class ParadigmShiftPathway(AGItoASIPathway):
    """
    Simulates the pathway driven by algorithmic paradigm shifts and architectural 
    evolutions (e.g., Mamba/SSMs, continuous learning, explicit world models).
    """
    
    def __init__(
        self,
        growth_model: ComputeGrowthModel,
        capability_model: CapabilityExtrapolator,
        potential_shifts: list[ParadigmShiftEvent]
    ):
        self.growth_model = growth_model
        self.capability_model = capability_model
        self.potential_shifts = sorted(potential_shifts, key=lambda s: s.year_expected)
        
    @property
    def name(self) -> str:
        return "Algorithmic Paradigm Shifts"
        
    @property
    def description(self) -> str:
        return (
            "Progress driven by qualitative architectural and algorithmic leaps "
            "that break through the ceilings of previous paradigms, dramatically "
            "increasing compute efficiency or unlocking capabilities orthogonally "
            "to scale."
        )
        
    def simulate(self, years: float, initial_compute: float = 1.0) -> PathwayResult:
        """Simulate progress, applying step-function multipliers at paradigm shifts."""
        t_points = []
        compute_points = []
        eff_compute_points = []
        
        current_multiplier = 1.0
        active_shifts = []
        unlocked_caps = set()
        
        resolution = 10
        total_steps = int(years * resolution)
        
        for step in range(total_steps + 1):
            year = step / resolution
            t_points.append(year)
            
            # Check if any shifts trigger this year
            for shift in self.potential_shifts:
                if shift not in active_shifts and year >= shift.year_expected:
                    active_shifts.append(shift)
                    # Paradigm shifts increase the *efficiency* of compute
                    current_multiplier *= shift.compute_efficiency_multiplier
                    for cap in shift.capabilities_unlocked:
                        unlocked_caps.add(cap)
            
            raw_compute = self.growth_model.effective_compute_at_year(year) * initial_compute
            compute_points.append(raw_compute)
            
            # Effective compute is boosted by paradigm shifts
            eff_compute = raw_compute * current_multiplier
            eff_compute_points.append(eff_compute)
            
        final_compute = eff_compute_points[-1]
        
        # Base capabilities from scale
        base_caps = self.capability_model.capabilities_at_compute(final_compute)
        for cap in base_caps:
            unlocked_caps.add(cap)
            
        return PathwayResult(
            pathway_name=self.name,
            final_compute_multiplier=final_compute / initial_compute,
            capabilities_unlocked=list(unlocked_caps),
            bottleneck_hit=False,
            time_series={
                "year": t_points,
                "raw_compute": compute_points,
                "effective_compute": eff_compute_points
            }
        )
