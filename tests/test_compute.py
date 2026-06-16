import pytest
import math

from src.compute.growth_model import GrowthFactors, ComputeGrowthModel
from src.compute.scaling_laws import PowerLawScaling, CapabilityExtrapolator


def test_growth_factors_total():
    """Test the combined growth rate calculation."""
    # Paper defaults: 1.5 * 2.5 * 3 = 11.25
    factors = GrowthFactors()
    assert math.isclose(factors.total_effective_growth, 11.25)
    
    # Custom
    factors = GrowthFactors(1.0, 2.0, 2.0)
    assert math.isclose(factors.total_effective_growth, 4.0)


def test_compute_growth_model():
    """Test exponential compute forecasting."""
    model = ComputeGrowthModel(GrowthFactors(1.0, 2.0, 5.0), initial_compute=100)
    
    # Year 0
    assert model.effective_compute_at_year(0) == 100
    
    # Total growth is 10x per year
    assert model.effective_compute_at_year(1) == 1000
    assert model.effective_compute_at_year(2) == 10000
    
    # Inverse
    assert math.isclose(model.year_to_reach_compute(10000), 2.0)
    assert math.isclose(model.year_to_reach_multiplier(100), 2.0)


def test_power_law_scaling():
    """Test loss scaling with compute."""
    # L(C) = 1.0 + (100 / C)^0.5
    scaling = PowerLawScaling(alpha=0.5, c_c=100.0, l_inf=1.0)
    
    # At C=100 -> 1.0 + 1^0.5 = 2.0
    assert math.isclose(scaling.loss(100.0), 2.0)
    
    # At C=400 -> 1.0 + 0.25^0.5 = 1.5
    assert math.isclose(scaling.loss(400.0), 1.5)
    
    # Inverse
    assert math.isclose(scaling.compute_needed(1.5), 400.0)


def test_capability_extrapolator():
    """Test capability milestone thresholding."""
    scaling = PowerLawScaling(alpha=0.5, c_c=100.0, l_inf=0.0) # L(C) = (100/C)^0.5
    
    extrapolator = CapabilityExtrapolator(scaling)
    extrapolator.add_milestone("Basic Logic", 2.0) # Needs C=25
    extrapolator.add_milestone("Advanced Math", 0.5) # Needs C=400
    
    assert "Basic Logic" not in extrapolator.capabilities_at_compute(10.0) # Loss is ~3.16
    assert "Basic Logic" in extrapolator.capabilities_at_compute(50.0)     # Loss is ~1.41
    assert "Advanced Math" not in extrapolator.capabilities_at_compute(50.0)
    assert "Advanced Math" in extrapolator.capabilities_at_compute(500.0)  # Loss is ~0.44
    
    assert math.isclose(extrapolator.compute_for_milestone("Advanced Math"), 400.0)
