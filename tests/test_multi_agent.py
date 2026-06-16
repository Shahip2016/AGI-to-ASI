import pytest
import math

from src.compute.growth_model import ComputeGrowthModel, GrowthFactors
from src.pathways.multi_agent import MultiAgentPathway, SwarmProperties


def test_swarm_intelligence_scaling():
    growth = ComputeGrowthModel(GrowthFactors(1.0, 1.0, 1.0))
    swarm = SwarmProperties(
        agent_count=1000,
        coordination_efficiency=1.0, # Perfect
        communication_bandwidth_gbps=100.0,
        specialization_factor=1.0
    )
    
    pathway = MultiAgentPathway(growth, swarm)
    intel = pathway._calculate_swarm_intelligence(swarm, compute_per_agent=1.0)
    
    # Perfect efficiency -> N * C
    assert math.isclose(intel, 1000.0)
    
    # Add overhead (efficiency 0.9 -> serial fraction 0.1)
    swarm.coordination_efficiency = 0.9
    intel_overhead = pathway._calculate_swarm_intelligence(swarm, compute_per_agent=1.0)
    
    # N / (1 + 0.1 * 999) = 1000 / 100.9 ~= 9.9
    assert intel_overhead < 10.0 
    
    # Add specialization
    swarm.specialization_factor = 2.0
    intel_specialized = pathway._calculate_swarm_intelligence(swarm, compute_per_agent=1.0)
    assert math.isclose(intel_specialized, intel_overhead * 2.0)


def test_multi_agent_pathway_simulation():
    growth = ComputeGrowthModel(GrowthFactors(2.0, 1.0, 1.0)) # 2x per year
    swarm = SwarmProperties(
        agent_count=100,
        coordination_efficiency=0.8,
        communication_bandwidth_gbps=10.0,
        specialization_factor=1.2
    )
    
    pathway = MultiAgentPathway(growth, swarm)
    res = pathway.simulate(years=4.0, initial_compute=1.0)
    
    assert res.pathway_name == "Multi-Agent Coordination"
    assert "agent_count" in res.time_series
    
    # Agent count should have grown: initial * sqrt(2^4) = 100 * 4 = 400
    final_agents = res.time_series["agent_count"][-1]
    assert final_agents == 400
    
    assert res.final_compute_multiplier > 1.0
    assert "Distributed Problem Solving" in res.capabilities_unlocked
