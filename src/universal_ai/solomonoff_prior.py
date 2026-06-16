"""
Solomonoff's Universal Prior.

Based on Section 4 of the paper: "lower (Kolmogorov) complexity environments 
and reward functions are (exponentially) more likely a priori."

Since true Kolmogorov complexity is incomputable, this module provides
conceptual interfaces and computable approximations (e.g., using standard
compression algorithms like zlib/lzma) to illustrate the concept.
"""

from __future__ import annotations

import zlib
from abc import ABC, abstractmethod


class ComplexityMeasure(ABC):
    """Abstract base class for environment complexity measures."""
    
    @abstractmethod
    def complexity(self, description: str | bytes) -> int:
        """
        Calculate the complexity (length in bits) of a description.
        In theory, this should be the Kolmogorov complexity K(x).
        """
        pass
        
    def solomonoff_prior(self, description: str | bytes) -> float:
        """
        Calculate the unnormalized Solomonoff prior probability: 2^{-K(x)}.
        """
        k = self.complexity(description)
        try:
            return 2.0 ** (-k)
        except OverflowError:
            return 0.0


class LempelZivComplexity(ComplexityMeasure):
    """
    Approximates Kolmogorov complexity using zlib (LZ77) compression.
    
    While not theoretically optimal, it captures the intuition that
    more compressible (simpler) environments should have lower complexity
    and thus higher prior probability.
    """
    
    def complexity(self, description: str | bytes) -> int:
        if isinstance(description, str):
            data = description.encode('utf-8')
        else:
            data = description
            
        if not data:
            return 0
            
        # Compress and get length in bits
        compressed = zlib.compress(data)
        # Adding 1 to avoid giving zero complexity to very small strings
        return len(compressed) * 8
        

class DescriptionLengthComplexity(ComplexityMeasure):
    """
    A naive complexity measure based purely on description length in bits.
    Useful for testing theoretical scenarios.
    """
    
    def complexity(self, description: str | bytes) -> int:
        if isinstance(description, str):
            return len(description.encode('utf-8')) * 8
        return len(description) * 8
