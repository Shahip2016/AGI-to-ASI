"""
Legg-Hutter Intelligence Score.

Based on Section 3/4 of the paper: "The Legg-Hutter score formalizes intelligence
as the average performance of an agent across all computable tasks... simpler ones
(lower Kolmogorov complexity) are given more weight."
"""

from __future__ import annotations

from typing import Any

from .solomonoff_prior import ComplexityMeasure


class Environment:
    """An environment/task that an agent can be evaluated on."""
    
    def __init__(self, description: str):
        self.description = description
        
    def simulate_agent(self, agent: Any, steps: int) -> float:
        """
        Simulate the agent in this environment for a number of steps
        and return the normalized cumulative reward in [0, 1].
        """
        # In a real implementation, this would run the agent loop
        # For this conceptual framework, we'll return a mock score
        return 0.5


class LeggHutterEvaluator:
    """
    Computes a bounded approximation of the Legg-Hutter intelligence score.
    
    True Legg-Hutter score: Sum over all Turing machines (environments) of
    Prior(environment) * Expected_Reward(Agent, environment).
    
    This approximates it over a finite set of environments.
    """
    
    def __init__(self, complexity_measure: ComplexityMeasure):
        self.complexity_measure = complexity_measure
        self.environments: list[Environment] = []
        
    def add_environment(self, env: Environment) -> None:
        """Add an environment to the evaluation set."""
        self.environments.append(env)
        
    def evaluate(self, agent: Any, max_steps: int = 100) -> float:
        """
        Calculate the approximate Legg-Hutter score for an agent.
        
        Returns:
            A score in [0, 1] representing the weighted average performance.
        """
        if not self.environments:
            return 0.0
            
        total_score = 0.0
        total_weight = 0.0
        
        for env in self.environments:
            # 1. Calculate weight using Solomonoff prior: 2^-K(env)
            weight = self.complexity_measure.solomonoff_prior(env.description)
            
            # 2. Evaluate agent in environment
            reward = env.simulate_agent(agent, steps=max_steps)
            
            # 3. Accumulate weighted reward
            total_score += weight * reward
            total_weight += weight
            
        # Normalize to [0, 1]
        if total_weight > 0:
            return total_score / total_weight
        return 0.0
