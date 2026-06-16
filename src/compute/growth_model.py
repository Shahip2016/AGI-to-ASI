"""
Models for forecasting the growth of effective compute.

Based on Section 2 of the paper: The ~10x per year effective compute growth
is composed of three compounding factors:
1. Hardware improvements (Moore's law): ~1.5x / year
2. Hardware investments: ~2.5x / year
3. Algorithmic efficiency: ~3x / year (up to 6x/year per Ho et al., 2025)

Combined: 1.5 * 2.5 * 3 = 11.25x (conservatively estimated as 10x per year).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class GrowthFactors:
    """
    The multiplicative factors driving effective compute growth per year.
    
    Values default to the conservative estimates from the paper (Section 2).
    """
    hardware_improvements: float = 1.5
    investment_growth: float = 2.5
    algorithmic_efficiency: float = 3.0
    
    @property
    def total_effective_growth(self) -> float:
        """Combined multiplicative growth per year (e.g., 1.5 * 2.5 * 3 = 11.25)."""
        return self.hardware_improvements * self.investment_growth * self.algorithmic_efficiency


class ComputeGrowthModel:
    """
    Forecasts effective compute over time using exponential growth dynamics.
    """
    
    def __init__(self, factors: Optional[GrowthFactors] = None, initial_compute: float = 1.0):
        """
        Args:
            factors: Growth factors per year. Defaults to conservative paper estimates.
            initial_compute: Baseline compute (e.g., in FLOPs) at year 0.
        """
        self.factors = factors or GrowthFactors()
        self.initial_compute = initial_compute
        
    def effective_compute_at_year(self, year: float) -> float:
        """
        Calculate the expected effective compute at a given year.
        
        Assumes constant multiplicative growth (exponential dynamics).
        """
        return self.initial_compute * (self.factors.total_effective_growth ** year)
        
    def compute_multiplier_at_year(self, year: float) -> float:
        """
        Calculate how many times larger compute is at a given year compared to year 0.
        """
        return self.factors.total_effective_growth ** year
        
    def year_to_reach_multiplier(self, target_multiplier: float) -> float:
        """
        Calculate the number of years required to reach a target compute multiplier.
        """
        if target_multiplier <= 0:
            raise ValueError("Target multiplier must be positive.")
            
        # target = growth_rate ^ years
        # log(target) = years * log(growth_rate)
        return math.log(target_multiplier) / math.log(self.factors.total_effective_growth)
        
    def year_to_reach_compute(self, target_compute: float) -> float:
        """
        Calculate the number of years required to reach a target absolute compute.
        """
        if target_compute < self.initial_compute:
            return 0.0
            
        multiplier = target_compute / self.initial_compute
        return self.year_to_reach_multiplier(multiplier)
        
    def trajectory(self, years: int, resolution_per_year: int = 1) -> tuple[list[float], list[float]]:
        """
        Generate a trajectory of compute over time.
        
        Args:
            years: Total years to simulate.
            resolution_per_year: Number of data points per year.
            
        Returns:
            A tuple of (time_points, compute_values).
        """
        t_points = [i / resolution_per_year for i in range(years * resolution_per_year + 1)]
        c_points = [self.effective_compute_at_year(t) for t in t_points]
        return t_points, c_points
