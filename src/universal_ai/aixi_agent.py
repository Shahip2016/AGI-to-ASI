"""
Conceptual AIXI Agent formulation.

Based on Section 4 of the paper: AIXI is a theoretical agent that:
1. Maintains a Bayesian mixture over all computable environments.
2. Solves interactive decision-making via general reinforcement learning.
3. Implicitly solves the exploration-exploitation trade-off.

Since AIXI is incomputable, this module provides abstract interfaces
and simplified computable approximations to demonstrate the concepts.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .solomonoff_prior import ComplexityMeasure

Action = TypeVar('Action')
Observation = TypeVar('Observation')
Reward = float


@dataclass
class Experience(Generic[Action, Observation]):
    """A single interaction step."""
    action: Action
    observation: Observation
    reward: Reward


class EnvironmentHypothesis(ABC, Generic[Action, Observation]):
    """
    Represents a hypothesis about how the environment works.
    
    In full AIXI, this would be a Turing machine. In practical approximations,
    it could be a Markov Decision Process (MDP) or a neural sequence model.
    """
    
    @abstractmethod
    def get_description(self) -> str | bytes:
        """Get the description of this hypothesis (for complexity calculation)."""
        pass
        
    @abstractmethod
    def predict_next(
        self, 
        history: list[Experience[Action, Observation]], 
        action: Action
    ) -> tuple[Observation, Reward]:
        """Predict the next observation and reward given history and action."""
        pass


class ConceptualAIXI(Generic[Action, Observation]):
    """
    A conceptual implementation of the AIXI agent.
    
    Demonstrates the core mechanics: Bayesian mixture over hypotheses
    weighted by the Solomonoff prior, and lookahead planning.
    
    Note: A true AIXI would search over the space of ALL computable
    environments. This implementation only searches over a finite,
    provided set of hypotheses.
    """
    
    def __init__(
        self, 
        hypotheses: list[EnvironmentHypothesis[Action, Observation]],
        complexity_measure: ComplexityMeasure,
        discount_factor: float = 0.9,
        planning_horizon: int = 3
    ):
        self.hypotheses = hypotheses
        self.complexity_measure = complexity_measure
        self.gamma = discount_factor
        self.horizon = planning_horizon
        
        self.history: list[Experience[Action, Observation]] = []
        
        # Initialize prior probabilities based on complexity
        self.beliefs = {}
        total_prior = 0.0
        
        for hyp in hypotheses:
            prior = self.complexity_measure.solomonoff_prior(hyp.get_description())
            self.beliefs[hyp] = prior
            total_prior += prior
            
        # Normalize priors
        if total_prior > 0:
            for hyp in hypotheses:
                self.beliefs[hyp] /= total_prior
                
    def update_beliefs(self, action: Action, observation: Observation, reward: Reward) -> None:
        """
        Update the Bayesian posterior based on a new experience.
        
        In this simplified version, we just eliminate hypotheses that 
        made incorrect predictions. A more robust version would use 
        probabilistic likelihoods.
        """
        new_experience = Experience(action, observation, reward)
        
        total_prob = 0.0
        for hyp in self.hypotheses:
            if self.beliefs[hyp] <= 0:
                continue
                
            try:
                # Ask hypothesis what it would have predicted
                pred_obs, pred_reward = hyp.predict_next(self.history, action)
                
                # If prediction is perfect, keep belief; else set to 0 (deterministic envs)
                # For stochastic envs, this would multiply by likelihood P(obs, reward | history, action, hyp)
                if pred_obs != observation or not math.isclose(pred_reward, reward, abs_tol=1e-5):
                    self.beliefs[hyp] = 0.0
            except Exception:
                # Hypothesis failed to predict
                self.beliefs[hyp] = 0.0
                
            total_prob += self.beliefs[hyp]
            
        # Normalize posterior
        if total_prob > 0:
            for hyp in self.hypotheses:
                self.beliefs[hyp] /= total_prob
                
        # Record experience
        self.history.append(new_experience)
        
    def expected_reward(self, action: Action) -> float:
        """Calculate the expected immediate reward for an action across all valid hypotheses."""
        expected_r = 0.0
        for hyp, prob in self.beliefs.items():
            if prob > 0:
                try:
                    _, r = hyp.predict_next(self.history, action)
                    expected_r += prob * r
                except Exception:
                    pass
        return expected_r
        
    def act(self, available_actions: list[Action]) -> Action:
        """
        Choose the best action using 1-step lookahead.
        
        A full AIXI would use expectimax tree search up to the planning horizon.
        For simplicity, this conceptual version only does 1-step greedy planning.
        """
        if not available_actions:
            raise ValueError("No actions available")
            
        best_action = available_actions[0]
        max_expected_reward = float('-inf')
        
        for action in available_actions:
            expected_r = self.expected_reward(action)
            if expected_r > max_expected_reward:
                max_expected_reward = expected_r
                best_action = action
                
        return best_action
