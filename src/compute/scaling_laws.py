"""
Scaling laws modeling the relationship between compute and capabilities.

Based on Section 2 of the paper: "how will that compute translate into
capabilities?" Uses scaling law models (Kaplan et al., Hoffmann et al.)
to extrapolate performance from compute.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class PowerLawScaling:
    """
    Models a standard power-law relationship: L(C) = L_inf + (C_c / C)^alpha
    where:
    - L(C) is the loss given compute C
    - L_inf is the irreducible loss (entropy of the data distribution)
    - C_c is the scale constant
    - alpha is the scaling exponent
    
    Reference: Kaplan et al. (2020), "Scaling Laws for Neural Language Models"
    """
    alpha: float
    c_c: float
    l_inf: float = 0.0
    
    def loss(self, compute: float) -> float:
        """Calculate the expected loss given compute."""
        if compute <= 0:
            return float('inf')
        return self.l_inf + (self.c_c / compute) ** self.alpha
        
    def compute_needed(self, target_loss: float) -> float:
        """Calculate compute needed to reach a target loss."""
        if target_loss <= self.l_inf:
            return float('inf')
        return self.c_c / ((target_loss - self.l_inf) ** (1 / self.alpha))


class CapabilityExtrapolator:
    """
    Extrapolates qualitative capabilities from compute scaling.
    
    While loss scales smoothly, capabilities on specific benchmarks often
    exhibit step-changes or "emergence" (though the paper notes this might
    be a metric artifact).
    """
    
    def __init__(self, scaling_law: PowerLawScaling):
        self.scaling_law = scaling_law
        # Map of generic capability milestones to loss thresholds
        self.milestones: dict[str, float] = {}
        
    def add_milestone(self, name: str, loss_threshold: float) -> None:
        """Add a capability milestone reached at a specific loss threshold."""
        self.milestones[name] = loss_threshold
        
    def capabilities_at_compute(self, compute: float) -> list[str]:
        """Get the list of capabilities unlocked at a given compute scale."""
        current_loss = self.scaling_law.loss(compute)
        return [
            name for name, threshold in self.milestones.items()
            if current_loss <= threshold
        ]
        
    def compute_for_milestone(self, name: str) -> float:
        """Get the compute required to reach a specific milestone."""
        if name not in self.milestones:
            raise KeyError(f"Unknown milestone: {name}")
        return self.scaling_law.compute_needed(self.milestones[name])
