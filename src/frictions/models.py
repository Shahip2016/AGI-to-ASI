"""
Models of development frictions and deployment bottlenecks.

Based on Section 5.5 of the paper.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol


class FrictionCategory(Enum):
    """Categories of friction from Section 5.5."""
    DATA_EXHAUSTION = auto()     # Running out of high-quality human data
    COMPUTE_LIMITS = auto()      # Energy, manufacturing, and cooling limits
    COORDINATION_OVERHEAD = auto() # Communication limits in large swarms
    ALIGNMENT_TAX = auto()       # Cost of ensuring safety and alignment
    REAL_WORLD_EVAL = auto()     # Slow feedback loops for real-world interactions


@dataclass
class Bottleneck:
    """A limit that creates friction against exponential growth."""
    category: FrictionCategory
    name: str
    activation_year: float
    severity: float # 0.0 (no friction) to 1.0 (complete halt)
    
    def calculate_friction_multiplier(self, year: float) -> float:
        """
        Calculate the multiplier to apply to growth at a given year.
        1.0 means no friction, 0.0 means no growth.
        """
        if year < self.activation_year:
            return 1.0
            
        # Logistic onset of friction
        years_past = year - self.activation_year
        onset = 1.0 / (1.0 + math.exp(-2.0 * years_past + 2.0))
        
        return 1.0 - (onset * self.severity)


class CompositeFrictionModel:
    """Combines multiple bottlenecks to determine total growth friction."""
    
    def __init__(self, bottlenecks: list[Bottleneck]):
        self.bottlenecks = bottlenecks
        
    def get_effective_growth_multiplier(self, year: float) -> float:
        """
        Calculates the combined multiplier. Frictions multiply
        (i.e., they compound each other).
        """
        multiplier = 1.0
        for b in self.bottlenecks:
            multiplier *= b.calculate_friction_multiplier(year)
        return multiplier
        
    def get_active_bottlenecks(self, year: float, threshold: float = 0.95) -> list[str]:
        """Get names of bottlenecks that are actively slowing growth."""
        active = []
        for b in self.bottlenecks:
            if b.calculate_friction_multiplier(year) < threshold:
                active.append(b.name)
        return active

# Common bottleneck scenarios from the paper

STANDARD_FRICTIONS = [
    Bottleneck(
        category=FrictionCategory.DATA_EXHAUSTION,
        name="High-Quality Text Exhaustion",
        activation_year=2.0,
        severity=0.5
    ),
    Bottleneck(
        category=FrictionCategory.COMPUTE_LIMITS,
        name="Gigawatt Datacenter Power Limit",
        activation_year=5.0,
        severity=0.8
    ),
    Bottleneck(
        category=FrictionCategory.REAL_WORLD_EVAL,
        name="Embodiment / Robotics Data Wall",
        activation_year=1.0,
        severity=0.9
    )
]
