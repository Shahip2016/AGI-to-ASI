"""
Architectural evolution definitions.

Based on Section 5.2 of the paper: "missing pieces and features of today's
architectures" such as explicit world models, continual learning, and
linear-time sequence architectures (Mamba/S4).
"""

from src.pathways.paradigm_shifts import ParadigmShiftEvent

# Potential architectural evolutions discussed in the paper
# These act as step-function boosts to compute efficiency or unlock new capabilities

ARCHITECTURAL_EVOLUTIONS = [
    ParadigmShiftEvent(
        name="Linear-Time Sequence Architectures (Mamba/SSMs)",
        year_expected=1.5,
        compute_efficiency_multiplier=5.0, # Breaks O(N^2) attention bottleneck
        capabilities_unlocked=["Infinite Context", "Streaming Real-World processing"]
    ),
    ParadigmShiftEvent(
        name="Robust Internal World Models",
        year_expected=3.0,
        compute_efficiency_multiplier=2.0, # Better sample efficiency
        capabilities_unlocked=["Zero-shot Counterfactual Reasoning", "Long-horizon Planning"]
    ),
    ParadigmShiftEvent(
        name="Continual Learning without Catastrophic Forgetting",
        year_expected=4.5,
        compute_efficiency_multiplier=1.5,
        capabilities_unlocked=["Perpetual Adaptation", "On-the-fly Specialization"]
    ),
    ParadigmShiftEvent(
        name="Test-time Scaling / Search-Augmented Distillation",
        year_expected=2.0,
        compute_efficiency_multiplier=10.0, # Huge boost to effective intelligence
        capabilities_unlocked=["Self-Correction", "System 2 Thinking"]
    ),
    ParadigmShiftEvent(
        name="Neuromorphic / Analog Computing Transition",
        year_expected=8.0,
        compute_efficiency_multiplier=100.0, # Massive energy efficiency gain
        capabilities_unlocked=["Billion-Agent Swarms"]
    )
]
