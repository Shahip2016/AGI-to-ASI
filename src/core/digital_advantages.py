"""
Advantages of digital intelligence over biological intelligence.

Implements Table 1 from the paper (Section 3): properties of digital
intelligence that scale with more compute, in ways that biological
intelligence cannot be scaled.

Key insight: ALL advantages intensify with more (effective) compute,
meaning the gap between humans and AI systems widens as compute grows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .definitions import AdvantageCategory


@dataclass(frozen=True)
class DigitalAdvantage:
    """
    A specific advantage of digital intelligence over biological.

    Each advantage scales with compute in ways biological intelligence cannot.

    Attributes:
        category: The type of advantage.
        name: Short name for the advantage.
        description: Detailed description from the paper.
        scaling_description: How this advantage scales with more compute.
        human_limitation: The corresponding human limitation.
        compute_multiplier: Rough factor by which this advantage grows
            per order of magnitude of additional compute.
    """

    category: AdvantageCategory
    name: str
    description: str
    scaling_description: str
    human_limitation: str
    compute_multiplier: float = 1.0


# Table 1 from the paper: Advantages of digital intelligence
# These are properties that grow with more compute in ways biology cannot match.

DIGITAL_ADVANTAGES: list[DigitalAdvantage] = [
    DigitalAdvantage(
        category=AdvantageCategory.SPEED,
        name="Processing Speed",
        description=(
            "Digital systems can process information orders of magnitude faster "
            "than biological neurons. Clock speeds of digital computers far "
            "exceed neural firing rates (~1000 Hz)."
        ),
        scaling_description=(
            "Faster hardware directly translates to faster processing. "
            "An AI can 'think' for the equivalent of years in hours of wall "
            "clock time with sufficient compute."
        ),
        human_limitation=(
            "Human neural processing speed is fixed by biology (~100 Hz "
            "effective processing rate). Cannot be sped up."
        ),
        compute_multiplier=10.0,  # ~10× faster per OOM of compute
    ),
    DigitalAdvantage(
        category=AdvantageCategory.PARALLELISM,
        name="Massive Parallelism",
        description=(
            "Multiple identical instances can be run simultaneously, each "
            "working on different aspects of a problem or different problems "
            "entirely. Unlike human teams, these instances can be truly "
            "identical in knowledge and capability."
        ),
        scaling_description=(
            "More compute directly enables more parallel instances. "
            "If 1000 instances exist today, 10× compute means 10,000 "
            "instances, or 1,000 instances 10× faster."
        ),
        human_limitation=(
            "Each human is a unique entity. Coordination overhead limits "
            "effective parallelism in human teams. Training a new human "
            "expert takes decades."
        ),
        compute_multiplier=10.0,
    ),
    DigitalAdvantage(
        category=AdvantageCategory.MEMORY,
        name="Perfect Memory & Recall",
        description=(
            "Digital systems have perfect recall of stored information. "
            "Memory states can be saved, restored, and shared. No forgetting, "
            "no memory degradation."
        ),
        scaling_description=(
            "More compute/storage enables larger working memory, more "
            "context, and the ability to maintain more facts and relationships "
            "simultaneously."
        ),
        human_limitation=(
            "Human memory is lossy, subject to bias, and degrades over time. "
            "Working memory is severely limited (~7±2 items)."
        ),
        compute_multiplier=3.0,
    ),
    DigitalAdvantage(
        category=AdvantageCategory.COMMUNICATION,
        name="High-Bandwidth Communication",
        description=(
            "AI instances can share information at the bandwidth of digital "
            "interconnects — entire model states, learned representations, "
            "and experiences can be transferred directly."
        ),
        scaling_description=(
            "Faster interconnects and more bandwidth enable richer shared "
            "representations. Full model weights and activations can be "
            "shared, not just compressed natural language."
        ),
        human_limitation=(
            "Human communication bandwidth is extremely low (~50 bits/s for "
            "speech). Sharing knowledge requires lossy compression into "
            "language, with lossy decompression on the receiving end."
        ),
        compute_multiplier=5.0,
    ),
    DigitalAdvantage(
        category=AdvantageCategory.DURABILITY,
        name="Substrate Independence & Durability",
        description=(
            "An AI's full algorithmic description (code) is known and "
            "substrate-independent. It can be migrated to new hardware, "
            "backed up, and restored. Its existence is not tied to specific "
            "physical substrate longevity."
        ),
        scaling_description=(
            "More diverse and redundant compute substrates increase "
            "durability. Better hardware enables operation over wider "
            "ranges of conditions (space travel, extreme environments)."
        ),
        human_limitation=(
            "Human existence is tied to a single biological substrate. "
            "Death is irreversible. Cannot be backed up or migrated."
        ),
        compute_multiplier=1.5,
    ),
    DigitalAdvantage(
        category=AdvantageCategory.SCALABILITY,
        name="Flexible Embodiment & Scale",
        description=(
            "An advanced AI's embodiment can adapt and extend flexibly — "
            "from virtual worlds to robotic bodies to large swarms "
            "distributed over large distances. Can operate across a much "
            "larger range of timescales and spatial scales."
        ),
        scaling_description=(
            "More compute enables more embodiments, larger swarms, and "
            "operation at faster timescales. Suspending an AI for space "
            "travel is much simpler than for biological intelligence."
        ),
        human_limitation=(
            "Human embodiment is fixed: one body, one location, one "
            "timescale. Limited sensory bandwidth and motor capabilities."
        ),
        compute_multiplier=5.0,
    ),
    DigitalAdvantage(
        category=AdvantageCategory.REPLICABILITY,
        name="Perfect Replication",
        description=(
            "Programs and memory states can be perfectly copied, creating "
            "instances identical not just in 'DNA' (source code) but also "
            "in accumulated 'lifetime experiences' (memory state). This "
            "is fundamentally impossible for biological intelligence."
        ),
        scaling_description=(
            "More compute enables more copies. Specialist instances can "
            "be fine-tuned from a generalist and spawned in large numbers "
            "to meet demand. Many lifetimes of experience can be rapidly "
            "replayed."
        ),
        human_limitation=(
            "Humans cannot be copied. Each person's knowledge and experience "
            "must be individually acquired over years. Training an expert "
            "takes 10,000+ hours of deliberate practice."
        ),
        compute_multiplier=10.0,
    ),
    DigitalAdvantage(
        category=AdvantageCategory.MODIFIABILITY,
        name="Targeted Self-Modification",
        description=(
            "AI systems can modify their own code, architecture, and "
            "training procedures in a targeted fashion, unlike biological "
            "evolution which relies on random mutation and selection."
        ),
        scaling_description=(
            "More compute enables more thorough search over modifications, "
            "more extensive testing of changes, and faster iteration cycles "
            "for self-improvement."
        ),
        human_limitation=(
            "Human self-modification is limited to learning and behavioral "
            "changes. Cannot modify neural architecture, add neurons, or "
            "change fundamental cognitive capabilities."
        ),
        compute_multiplier=3.0,
    ),
]


def get_advantage(category: AdvantageCategory) -> Optional[DigitalAdvantage]:
    """Get the digital advantage for a given category."""
    for adv in DIGITAL_ADVANTAGES:
        if adv.category == category:
            return adv
    return None


def compute_gap_at_scale(compute_oom: float) -> dict[AdvantageCategory, float]:
    """
    Estimate the human-AI gap for each advantage at a given compute scale.

    Args:
        compute_oom: Orders of magnitude of compute above current baseline.

    Returns:
        Dictionary mapping each advantage category to a gap multiplier.
        A value of 100 means the AI advantage is 100× at this compute level.
    """
    gaps = {}
    for adv in DIGITAL_ADVANTAGES:
        gaps[adv.category] = adv.compute_multiplier ** compute_oom
    return gaps


def total_advantage_score(compute_oom: float) -> float:
    """
    Compute a composite advantage score across all categories.

    This is the geometric mean of all individual advantage multipliers,
    providing a single scalar measure of how much digital intelligence
    dominates biological intelligence at a given compute scale.

    Args:
        compute_oom: Orders of magnitude of compute above baseline.

    Returns:
        Geometric mean of all advantage multipliers.
    """
    import math

    gaps = compute_gap_at_scale(compute_oom)
    if not gaps:
        return 1.0
    log_sum = sum(math.log(g) for g in gaps.values())
    return math.exp(log_sum / len(gaps))
