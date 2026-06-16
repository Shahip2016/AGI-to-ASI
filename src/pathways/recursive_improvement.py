"""
Pathway 3: Recursive Self-Improvement.

Based on Section 5.3 of the paper.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum, auto

from .base import AGItoASIPathway, PathwayResult


class RSIType(Enum):
    """Types of Recursive Self-Improvement (mapped to evolutionary analogs)."""
    GENOTYPIC = auto()    # AI writing better architectures/optimizers (Genetic Evolution)
    MEMETIC = auto()      # AI curating/generating better data (Cultural Evolution)
    SOCIOGENIC = auto()   # AI specialization/division of labor (Cooperative Evolution)
    HARDWARE = auto()     # AI designing better chips/manufacturing


@dataclass
class RSIMechanism:
    """A mechanism for recursive self-improvement."""
    rsi_type: RSIType
    name: str
    
    # Feedback strength: how much a 1% increase in AI capability 
    # translates into a % increase in the speed of AI R&D
    feedback_strength: float
    
    # Delay in years before the improvement loop closes
    cycle_delay_years: float
    
    # Diminishing returns parameter (higher means returns diminish faster)
    diminishing_returns: float = 0.0


class RecursiveImprovementPathway(AGItoASIPathway):
    """
    Simulates recursive self-improvement dynamics.
    
    If feedback strength is high enough and diminishing returns low enough,
    this can lead to super-exponential (hyperbolic) growth.
    """
    
    def __init__(self, mechanisms: list[RSIMechanism]):
        self.mechanisms = mechanisms
        
    @property
    def name(self) -> str:
        return "Recursive Self-Improvement"
        
    @property
    def description(self) -> str:
        return (
            "Progress driven by AI systems automating and accelerating AI R&D. "
            "Can lead to explosive, super-exponential (hyperbolic) growth if "
            "feedback loops are sufficiently strong."
        )
        
    def simulate(self, years: float, initial_compute: float = 1.0) -> PathwayResult:
        """
        Simulate RSI using a discretized differential equation system.
        
        dA/dt = Base_Growth + sum(mechanism_feedback * A(t-delay) / (1 + dim_returns * A))
        Where A is the capability/effective compute level.
        """
        t_points = []
        compute_points = []
        
        resolution = 100 # Higher resolution needed for ODE approximation
        total_steps = int(years * resolution)
        dt = 1.0 / resolution
        
        # Base exponential growth rate (e.g., hardware Moore's law alone ~1.5x)
        # Assuming other factors (algorithmic, investment) are now driven by RSI
        base_growth_rate = math.log(1.5) 
        
        current_compute = initial_compute
        compute_history = [initial_compute] * int(max(m.cycle_delay_years * resolution for m in self.mechanisms) + 1)
        
        bottleneck_hit = False
        bottleneck_year = None
        
        for step in range(total_steps + 1):
            year = step / resolution
            t_points.append(year)
            compute_points.append(current_compute)
            
            # Calculate derivative
            dA_dt = current_compute * base_growth_rate
            
            for mech in self.mechanisms:
                # Look up compute level from 'delay' years ago
                delay_steps = int(mech.cycle_delay_years * resolution)
                idx = max(0, len(compute_history) - 1 - delay_steps)
                past_compute = compute_history[idx]
                
                # Feedback term: past capability accelerates current growth
                # Diminished by the scale of current compute
                feedback = mech.feedback_strength * past_compute
                diminished_feedback = feedback / (1.0 + mech.diminishing_returns * current_compute)
                
                dA_dt += current_compute * diminished_feedback
            
            # Euler step
            current_compute += dA_dt * dt
            compute_history.append(current_compute)
            
            # Detect singularity / extreme growth (float limits)
            if current_compute > 1e100:
                bottleneck_hit = True
                bottleneck_name = "Computational Singularity (Overflow)"
                bottleneck_year = year
                # Cap to prevent math errors
                current_compute = 1e100
                break
                
        # Determine capabilities broadly based on final compute
        unlocked = []
        if current_compute > 100:
            unlocked.append("Automated Data Curation")
        if current_compute > 1e4:
            unlocked.append("Automated Architecture Search")
        if current_compute > 1e8:
            unlocked.append("Hyperbolic Growth (Intelligence Explosion)")
            
        return PathwayResult(
            pathway_name=self.name,
            final_compute_multiplier=compute_points[-1] / initial_compute,
            capabilities_unlocked=unlocked,
            bottleneck_hit=bottleneck_hit,
            bottleneck_name=bottleneck_year if bottleneck_hit else None,
            bottleneck_year=bottleneck_year,
            time_series={
                "year": t_points,
                "effective_compute": compute_points
            }
        )
