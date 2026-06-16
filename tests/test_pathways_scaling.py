import pytest

from src.compute.growth_model import ComputeGrowthModel, GrowthFactors
from src.compute.scaling_laws import PowerLawScaling, CapabilityExtrapolator
from src.pathways.scaling import ScalingPathway, DataWallConstraints


def test_data_wall_constraints():
    # Exhausts at year 2, synthetic efficiency 0.5
    dw = DataWallConstraints(exhaustion_year=2.0, synthetic_data_efficiency=0.5)
    
    assert dw.effective_data_multiplier(1.0) == 1.0
    assert dw.effective_data_multiplier(2.0) == 1.0
    
    # 1 year past -> multiplier is 0.5^1 = 0.5
    assert dw.effective_data_multiplier(3.0) == 0.5
    
    # 2 years past -> multiplier is 0.5^2 = 0.25
    assert dw.effective_data_multiplier(4.0) == 0.25


def test_scaling_pathway():
    growth = ComputeGrowthModel(GrowthFactors(2.0, 1.0, 1.0)) # 2x per year
    scaling = PowerLawScaling(alpha=0.5, c_c=100.0, l_inf=0.0)
    capabilities = CapabilityExtrapolator(scaling)
    capabilities.add_milestone("Expert AGI", 2.0) # Needs 25 compute
    capabilities.add_milestone("ASI", 0.5)        # Needs 400 compute
    
    # Data wall hits at year 3
    dw = DataWallConstraints(exhaustion_year=3.0, synthetic_data_efficiency=0.5)
    
    pathway = ScalingPathway(growth, capabilities, dw)
    
    # Simulate 5 years, starting at compute=10
    # Year 0: C=10
    # Year 1: C=20
    # Year 2: C=40 (Expert AGI reached)
    # Year 3: C=80
    # Year 4: C=160 (Raw), but Data Wall hit (1 yr past) -> Eff_C = 160 * 0.5 = 80
    # Year 5: C=320 (Raw), Data wall (2 yr past) -> Eff_C = 320 * 0.25 = 80
    
    res = pathway.simulate(years=5.0, initial_compute=10.0)
    
    assert res.pathway_name == "Quantitative Scaling"
    assert res.bottleneck_hit is True
    assert res.bottleneck_name == "Data Wall"
    assert res.bottleneck_year == 3.1 # First step past 3.0
    
    # Final effective compute should be around 80, which is < 400, so ASI not reached
    assert "Expert AGI" in res.capabilities_unlocked
    assert "ASI" not in res.capabilities_unlocked
