import pytest
import math

from src.compute.growth_model import ComputeGrowthModel, GrowthFactors
from src.compute.scaling_laws import PowerLawScaling, CapabilityExtrapolator
from src.pathways.paradigm_shifts import ParadigmShiftPathway, ParadigmShiftEvent
from src.pathways.architecture_evolution import ARCHITECTURAL_EVOLUTIONS


def test_paradigm_shift_pathway():
    growth = ComputeGrowthModel(GrowthFactors(1.0, 1.0, 1.0)) # 1x per year (flat raw compute)
    scaling = PowerLawScaling(alpha=0.5, c_c=100.0, l_inf=0.0)
    capabilities = CapabilityExtrapolator(scaling)
    
    # Create two shifts
    shifts = [
        ParadigmShiftEvent("Shift 1", 2.0, 10.0, ["Cap 1"]),
        ParadigmShiftEvent("Shift 2", 4.0, 5.0, ["Cap 2"])
    ]
    
    pathway = ParadigmShiftPathway(growth, capabilities, shifts)
    
    # Simulate 5 years, starting at compute=10
    # Year 0-1.9: eff_C = 10
    # Year 2.0-3.9: eff_C = 10 * 10.0 = 100
    # Year 4.0-5.0: eff_C = 100 * 5.0 = 500
    
    res = pathway.simulate(years=5.0, initial_compute=10.0)
    
    assert res.pathway_name == "Algorithmic Paradigm Shifts"
    assert math.isclose(res.final_compute_multiplier, 50.0)
    assert "Cap 1" in res.capabilities_unlocked
    assert "Cap 2" in res.capabilities_unlocked
    
    # Verify time series
    t_idx_yr2 = 20 # resolution is 10, so step 20 is year 2.0
    assert res.time_series["effective_compute"][t_idx_yr2] == 100.0
    
    t_idx_yr4 = 40
    assert res.time_series["effective_compute"][t_idx_yr4] == 500.0

def test_architecture_evolution():
    # Just verify the list is imported correctly
    assert len(ARCHITECTURAL_EVOLUTIONS) >= 5
    assert any(shift.name.startswith("Linear-Time Sequence") for shift in ARCHITECTURAL_EVOLUTIONS)
