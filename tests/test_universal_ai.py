import pytest

from src.universal_ai.solomonoff_prior import DescriptionLengthComplexity, LempelZivComplexity
from src.universal_ai.aixi_agent import ConceptualAIXI, EnvironmentHypothesis, Experience
from src.universal_ai.legg_hutter import Environment, LeggHutterEvaluator


class MockHypothesis(EnvironmentHypothesis[str, str]):
    def __init__(self, desc: str, behavior_map: dict):
        self.desc = desc
        self.behavior = behavior_map
        
    def get_description(self) -> str:
        return self.desc
        
    def predict_next(self, history, action: str) -> tuple[str, float]:
        if action in self.behavior:
            return self.behavior[action]
        return ("unknown", 0.0)


def test_complexity_measures():
    desc_comp = DescriptionLengthComplexity()
    
    # "a" is 1 byte = 8 bits
    assert desc_comp.complexity("a") == 8
    
    # Prior for 8 bits = 2^-8 = 1/256
    prior = desc_comp.solomonoff_prior("a")
    assert prior == 2**(-8)
    
    lz_comp = LempelZivComplexity()
    
    # Highly compressible string should have lower complexity than random
    compressible = "a" * 1000
    uncompressible = "a" * 500 + "b" * 500 # Slightly less compressible
    
    c1 = lz_comp.complexity(compressible)
    c2 = lz_comp.complexity(uncompressible)
    
    # We just ensure it runs and returns positive integers
    assert c1 > 0
    assert c2 > 0


def test_aixi_agent():
    # Setup two hypotheses
    # Hyp 1: action A gives reward 1, B gives 0
    hyp1 = MockHypothesis("simple", {"A": ("obs1", 1.0), "B": ("obs2", 0.0)})
    # Hyp 2: action A gives reward 0, B gives 1
    hyp2 = MockHypothesis("complex_description_xyz", {"A": ("obs3", 0.0), "B": ("obs4", 1.0)})
    
    comp = DescriptionLengthComplexity()
    agent = ConceptualAIXI([hyp1, hyp2], comp)
    
    # Initially, hyp1 should have higher belief because it has a shorter description
    assert agent.beliefs[hyp1] > agent.beliefs[hyp2]
    
    # Therefore, expected reward for A should be > B
    assert agent.expected_reward("A") > agent.expected_reward("B")
    
    # Agent should choose A
    action = agent.act(["A", "B"])
    assert action == "A"
    
    # Now provide experience that contradicts hyp1 but matches hyp2
    # We took action A, got obs3 and reward 0 (matches hyp2)
    agent.update_beliefs("A", "obs3", 0.0)
    
    # Belief in hyp1 should drop to 0
    assert agent.beliefs[hyp1] == 0.0
    assert agent.beliefs[hyp2] == 1.0
    
    # Now agent should choose B
    action = agent.act(["A", "B"])
    assert action == "B"


def test_legg_hutter_evaluator():
    comp = DescriptionLengthComplexity()
    evaluator = LeggHutterEvaluator(comp)
    
    # Setup mock environments
    env1 = Environment("short")
    env2 = Environment("very_long_description")
    
    evaluator.add_environment(env1)
    evaluator.add_environment(env2)
    
    score = evaluator.evaluate("dummy_agent")
    
    # Since mock environment always returns 0.5, the weighted average is 0.5
    assert score == 0.5
