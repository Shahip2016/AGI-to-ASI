"""
Base abstract representations for AGI->ASI pathways.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class PathwayResult:
    """The outcome of simulating a pathway for a given time period."""
    pathway_name: str
    final_compute_multiplier: float
    capabilities_unlocked: list[str]
    bottleneck_hit: bool
    bottleneck_name: str | None = None
    bottleneck_year: float | None = None
    time_series: dict[str, list[float]] | None = None


class AGItoASIPathway(ABC):
    """
    Abstract base class for simulating a technological pathway
    from AGI to ASI.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the pathway."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the pathway based on the paper."""
        pass

    @abstractmethod
    def simulate(self, years: float, initial_compute: float = 1.0) -> PathwayResult:
        """
        Simulate the progress along this pathway for a given number of years.
        
        Args:
            years: Number of years to simulate.
            initial_compute: Baseline compute (1.0 = current AGI level).
            
        Returns:
            PathwayResult containing the outcomes.
        """
        pass
