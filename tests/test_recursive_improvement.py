import pytest
import math

from src.pathways.recursive_improvement import (
    RecursiveImprovementPathway, 
    RSIMechanism, 
    RSIType
)


def test_recursive_improvement_exponential():
    # Weak feedback, long delay -> Should be normal exponential growth
    mech = RSIMechanism(
        rsi_type=RSIType.MEMETIC,
        name="Data curation",
        feedback_strength=0.01,
        cycle_delay_years=1.0
    )
    pathway = RecursiveImprovementPathway([mech])
    
    res = pathway.simulate(years=5.0, initial_compute=1.0)
    
    assert res.pathway_name == "Recursive Self-Improvement"
    assert res.final_compute_multiplier > 1.0
    assert not res.bottleneck_hit


def test_recursive_improvement_hyperbolic():
    # Strong feedback, short delay -> Should trigger intelligence explosion (hyperbolic)
    mech = RSIMechanism(
        rsi_type=RSIType.GENOTYPIC,
        name="Automated AI Researcher",
        feedback_strength=2.0, # Very strong feedback
        cycle_delay_years=0.1  # Fast iteration
    )
    pathway = RecursiveImprovementPathway([mech])
    
    res = pathway.simulate(years=10.0, initial_compute=1.0)
    
    # Should hit the singularity cap
    assert res.bottleneck_hit
    assert "Singularity" in res.bottleneck_name
    assert "Hyperbolic Growth (Intelligence Explosion)" in res.capabilities_unlocked


def test_recursive_improvement_diminishing_returns():
    # Strong feedback but with diminishing returns
    mech = RSIMechanism(
        rsi_type=RSIType.HARDWARE,
        name="Hardware Design",
        feedback_strength=2.0,
        cycle_delay_years=0.1,
        diminishing_returns=0.1 # Dampens hyperbolic growth
    )
    pathway = RecursiveImprovementPathway([mech])
    
    res = pathway.simulate(years=10.0, initial_compute=1.0)
    
    # Should not hit singularity because diminishing returns caps the growth derivative
    assert not res.bottleneck_hit
    assert res.final_compute_multiplier > 10.0 # But still significant growth
