"""
Pathway 4: Multi-Agent Coordination & Collective Intelligence.

Based on Section 5.4 of the paper.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from src.compute.growth_model import ComputeGrowthModel
from .base import AGItoASIPathway, PathwayResult


@dataclass
class SwarmProperties:
    """Properties of a multi-agent swarm."""
    agent_count: int
    coordination_efficiency: float  # 1.0 = perfect parallelization, <1.0 = overhead
    communication_bandwidth_gbps: float
    specialization_factor: float    # >1.0 means heterogeneous specialized agents


class MultiAgentPathway(AGItoASIPathway):
    """
    Simulates the transition to ASI via Multi-Agent Systems (MAS).
    
    Rather than a single monolithic "God model", ASI might emerge from 
    millions of interacting AGI-level agents forming a collective intelligence
    (similar to human civilization).
    """
    
    def __init__(
        self,
        growth_model: ComputeGrowthModel,
        initial_swarm: SwarmProperties
    ):
        self.growth_model = growth_model
        self.initial_swarm = initial_swarm
        
    @property
    def name(self) -> str:
        return "Multi-Agent Coordination"
        
    @property
    def description(self) -> str:
        return (
            "Progress driven by scaling the number of interacting agents and "
            "improving their coordination. ASI emerges as a collective property "
            "of the swarm rather than a single monolithic model."
        )
        
    def _calculate_swarm_intelligence(self, swarm: SwarmProperties, compute_per_agent: float) -> float:
        """
        Estimate the effective collective intelligence of the swarm.
        Based loosely on Amdahl's Law and collective intelligence models.
        """
        # Perfect parallelization would be agent_count * compute
        # But coordination overhead limits this (Amdahl's law effect)
        # S(n) = n / (1 + alpha * (n - 1)) where alpha is the serial fraction
        
        alpha = 1.0 - swarm.coordination_efficiency
        if alpha <= 0:
            effective_n = swarm.agent_count
        else:
            effective_n = swarm.agent_count / (1.0 + alpha * (swarm.agent_count - 1))
            
        # Specialization acts as a multiplier on effective N
        return compute_per_agent * effective_n * swarm.specialization_factor
        
    def simulate(self, years: float, initial_compute: float = 1.0) -> PathwayResult:
        """Simulate the growth of the swarm over time."""
        t_points = []
        eff_compute_points = []
        agent_counts = []
        
        resolution = 10
        total_steps = int(years * resolution)
        
        current_swarm = SwarmProperties(
            agent_count=self.initial_swarm.agent_count,
            coordination_efficiency=self.initial_swarm.coordination_efficiency,
            communication_bandwidth_gbps=self.initial_swarm.communication_bandwidth_gbps,
            specialization_factor=self.initial_swarm.specialization_factor
        )
        
        for step in range(total_steps + 1):
            year = step / resolution
            t_points.append(year)
            
            # Growth allows scaling the number of agents and their individual compute
            # Let's say compute growth goes 50% to better agents, 50% to more agents
            growth = self.growth_model.compute_multiplier_at_year(year)
            compute_per_agent = initial_compute * math.sqrt(growth)
            current_swarm.agent_count = int(self.initial_swarm.agent_count * math.sqrt(growth))
            
            # Coordination efficiency might slowly improve
            current_swarm.coordination_efficiency = min(0.99, current_swarm.coordination_efficiency + 0.01 * year)
            
            agent_counts.append(current_swarm.agent_count)
            
            swarm_intelligence = self._calculate_swarm_intelligence(current_swarm, compute_per_agent)
            eff_compute_points.append(swarm_intelligence)
            
        unlocked = ["Distributed Problem Solving"]
        if eff_compute_points[-1] > 1e4:
            unlocked.append("Civilization-Scale Simulation")
            unlocked.append("Global Market Optimization")
            
        return PathwayResult(
            pathway_name=self.name,
            final_compute_multiplier=eff_compute_points[-1] / eff_compute_points[0],
            capabilities_unlocked=unlocked,
            bottleneck_hit=False,
            time_series={
                "year": t_points,
                "effective_compute": eff_compute_points,
                "agent_count": agent_counts
            }
        )
