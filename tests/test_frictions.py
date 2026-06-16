import pytest
import math

from src.frictions.models import Bottleneck, FrictionCategory, CompositeFrictionModel


def test_bottleneck_friction():
    b = Bottleneck(
        category=FrictionCategory.COMPUTE_LIMITS,
        name="Power Wall",
        activation_year=3.0,
        severity=0.8 # Will reduce growth to 20% at full severity
    )
    
    # Before activation, multiplier is 1.0
    assert b.calculate_friction_multiplier(2.0) == 1.0
    
    # Deep into activation, multiplier approaches (1 - severity)
    late_multiplier = b.calculate_friction_multiplier(10.0)
    assert math.isclose(late_multiplier, 0.2, abs_tol=0.01)


def test_composite_friction():
    b1 = Bottleneck(FrictionCategory.DATA_EXHAUSTION, "Data", 2.0, 0.5)
    b2 = Bottleneck(FrictionCategory.COMPUTE_LIMITS, "Power", 4.0, 0.5)
    
    model = CompositeFrictionModel([b1, b2])
    
    # Year 1: No bottlenecks active
    assert model.get_effective_growth_multiplier(1.0) == 1.0
    assert len(model.get_active_bottlenecks(1.0)) == 0
    
    # Year 10: Both fully active. 0.5 * 0.5 = 0.25
    assert math.isclose(model.get_effective_growth_multiplier(10.0), 0.25, abs_tol=0.01)
    
    active = model.get_active_bottlenecks(10.0)
    assert "Data" in active
    assert "Power" in active
