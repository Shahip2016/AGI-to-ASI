import pytest

from src.forecasting.scenarios import ScenarioGenerator


def test_scenario_generator():
    gen = ScenarioGenerator()
    
    # Run smooth scaling
    res_smooth = gen.generate_scenario_1_smooth_scaling()
    assert res_smooth.pathway_name == "Quantitative Scaling"
    assert not res_smooth.bottleneck_hit
    
    # With 10x growth per year for 10 years, compute reaches 10^10.
    # At C=10^10, loss is (100 / 10^10)^0.5 = (10^-8)^0.5 = 10^-4 = 0.0001
    # This is < 0.1, so UAI-Approximation should be unlocked
    assert "UAI-Approximation" in res_smooth.capabilities_unlocked
    
    # Run hard bottlenecks
    res_hard = gen.generate_scenario_2_hard_bottlenecks()
    assert res_hard.bottleneck_hit
    assert "Multiple" in res_hard.bottleneck_name
    
    # Hard scenario should have lower final compute than smooth
    assert res_hard.final_compute_multiplier < res_smooth.final_compute_multiplier
    
    # Generate all
    all_scenarios = gen.generate_all()
    assert len(all_scenarios) == 2
    assert "Smooth Scaling" in all_scenarios
    assert "Hard Bottlenecks" in all_scenarios
