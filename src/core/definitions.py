"""
Core definitions for the intelligence continuum from AGI to ASI to UAI.

Implements the characterizations from Section 3 of the paper:
- AGI: median human-level artificial general intelligence
- ASI: artificial general superintelligence exceeding large human-expert collectives
- UAI: Universal AI / AIXI — the theoretical limit of superintelligence

The Legg-Hutter score provides formal grounding for a continuum of intelligence,
where simpler tasks (lower Kolmogorov complexity) receive more weight.

Reference: Legg & Hutter (2007a), "Universal Intelligence: A Definition of
Machine Intelligence", Minds and Machines.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class IntelligenceLevel(Enum):
    """
    Discrete levels on the intelligence continuum.

    While the Legg-Hutter score is continuous, these levels provide
    qualitative anchors for discussion (Section 3 of the paper).
    """

    NARROW_AI = auto()       # Superhuman in specific domains (e.g., AlphaGo)
    COMPETENT_AGI = auto()   # Median human-level on most cognitive tasks
    EXPERT_AGI = auto()      # Expert human-level across domains
    ASI = auto()             # Exceeds large human-expert collectives
    UAI = auto()             # Theoretical limit (AIXI)

    @classmethod
    def get_all_levels(cls) -> list["IntelligenceLevel"]:
        """Return all intelligence levels in order."""
        return list(cls)

    @property
    def level_name(self) -> str:
        """Return a human-readable name of the level."""
        return self.name.replace("_", " ").title()


class AdvantageCategory(Enum):
    """Categories of advantages that digital intelligence has over biological."""

    SPEED = auto()           # Faster processing, clock speed scaling
    PARALLELISM = auto()     # Multiple instances, parallel execution
    MEMORY = auto()          # Perfect recall, shared memory states
    COMMUNICATION = auto()   # High-bandwidth inter-agent communication
    DURABILITY = auto()      # Substrate independence, backup/restore
    SCALABILITY = auto()     # Flexible embodiment, spatial/temporal scales
    REPLICABILITY = auto()   # Perfect copying of code AND memory state
    MODIFIABILITY = auto()   # Targeted self-modification of "DNA"


@dataclass(frozen=True)
class LeggHutterScore:
    """
    Represents a (conceptual) Legg-Hutter intelligence score.

    The Legg-Hutter score formalizes intelligence as the average performance
    of an agent across all computable tasks, where simpler tasks receive
    exponentially more weight (via the Solomonoff/Universal Prior).

    AIXI achieves the maximum possible score by definition.
    The score is incomputable but can be approximated from below.

    Attributes:
        value: Normalized score in [0, 1] where 1.0 = AIXI (theoretical max).
        level: Qualitative intelligence level.
        description: Human-readable description of capabilities.
        compute_flops: Approximate compute budget (FLOP/s) for this level.
    """

    value: float
    level: IntelligenceLevel
    description: str
    compute_flops: Optional[float] = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"Score must be in [0, 1], got {self.value}")

    def dominates(self, other: LeggHutterScore) -> bool:
        """Check if this score dominates another (higher intelligence)."""
        return self.value > other.value

    def gap_to(self, other: LeggHutterScore) -> float:
        """Compute the intelligence gap between two scores."""
        return abs(self.value - other.value)

    @property
    def is_superhuman(self) -> bool:
        """Check if this intelligence level is considered superhuman."""
        return self.level in [IntelligenceLevel.EXPERT_AGI, IntelligenceLevel.ASI, IntelligenceLevel.UAI]

    def to_dict(self) -> dict:
        """Convert the score to a dictionary representation."""
        return {
            "value": self.value,
            "level": self.level.name,
            "description": self.description,
            "compute_flops": self.compute_flops,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LeggHutterScore":
        """Create a score from a dictionary representation."""
        return cls(
            value=data["value"],
            level=IntelligenceLevel[data["level"]],
            description=data["description"],
            compute_flops=data.get("compute_flops"),
        )

    @property
    def gap_to_uai(self) -> float:
        """Compute the intelligence gap to the theoretical limit (UAI)."""
        return 1.0 - self.value


# Reference intelligence scores for key levels on the continuum
# These are illustrative — the actual Legg-Hutter score is incomputable

REFERENCE_SCORES = {
    IntelligenceLevel.NARROW_AI: LeggHutterScore(
        value=0.15,
        level=IntelligenceLevel.NARROW_AI,
        description=(
            "Superhuman in specific narrow domains (e.g., chess, Go, protein "
            "folding) but not general. Systems like AlphaFold and AlphaGo."
        ),
        compute_flops=1e15,  # ~petaFLOP/s
    ),
    IntelligenceLevel.COMPETENT_AGI: LeggHutterScore(
        value=0.35,
        level=IntelligenceLevel.COMPETENT_AGI,
        description=(
            "Roughly median human-level on most cognitive tasks. The first AGI "
            "will already be superhuman on many tasks due to advantages of "
            "digital intelligence. 'Competent AGI' per Morris et al. (2024)."
        ),
        compute_flops=1e18,  # ~exaFLOP/s
    ),
    IntelligenceLevel.EXPERT_AGI: LeggHutterScore(
        value=0.50,
        level=IntelligenceLevel.EXPERT_AGI,
        description=(
            "Expert human-level across a broad range of domains. Outperforms "
            "individual human experts but not necessarily large coordinated "
            "groups of experts."
        ),
        compute_flops=1e20,
    ),
    IntelligenceLevel.ASI: LeggHutterScore(
        value=0.75,
        level=IntelligenceLevel.ASI,
        description=(
            "Exceeds the performance of large human-expert collectives "
            "(tens of thousands of well-coordinated experts working for ~10 "
            "years with 2010-era technology) on virtually all tasks and "
            "domains of human activity."
        ),
        compute_flops=1e24,
    ),
    IntelligenceLevel.UAI: LeggHutterScore(
        value=1.0,
        level=IntelligenceLevel.UAI,
        description=(
            "Universal AI / AIXI — the theoretical limit of superintelligence. "
            "Maximizes the Legg-Hutter score by definition. Incomputable but "
            "can be approximated from below with more compute."
        ),
        compute_flops=float("inf"),
    ),
}


@dataclass
class IntelligenceContinuum:
    """
    Models the continuum of intelligence from narrow AI to UAI.

    The key insight from the paper is that intelligence is a continuous
    score, not a binary threshold. The transition from AGI to ASI is
    a traversal along this continuum.

    Remark III from the paper: While the Legg-Hutter measure is smooth
    w.r.t. increasing compute (given ideal algorithms), capability profiles
    of concrete systems may be "jagged" w.r.t. human-level intelligence.
    """

    scores: dict[IntelligenceLevel, LeggHutterScore] = field(
        default_factory=lambda: dict(REFERENCE_SCORES)
    )

    def score_for_compute(self, flops: float) -> float:
        """
        Estimate intelligence score given a compute budget.

        This is a rough log-linear interpolation — the actual relationship
        between compute and intelligence is an open research question
        (Section 2 of the paper).

        Args:
            flops: Available compute in FLOP/s.

        Returns:
            Estimated normalized Legg-Hutter score in [0, 1).
        """
        if flops <= 0:
            return 0.0

        # Log-linear interpolation between reference points
        # This is illustrative — real scaling laws are more complex
        log_flops = math.log10(flops)

        # Reference points: (log10_flops, score)
        points = sorted(
            [
                (math.log10(s.compute_flops), s.value)
                for s in self.scores.values()
                if s.compute_flops is not None and s.compute_flops < float("inf")
            ]
        )

        if log_flops <= points[0][0]:
            return points[0][1] * (log_flops / points[0][0])
        if log_flops >= points[-1][0]:
            # Asymptotic approach to 1.0 (UAI limit)
            excess = log_flops - points[-1][0]
            return points[-1][1] + (1.0 - points[-1][1]) * (1 - math.exp(-excess / 10))

        # Linear interpolation between reference points
        for i in range(len(points) - 1):
            x0, y0 = points[i]
            x1, y1 = points[i + 1]
            if x0 <= log_flops <= x1:
                t = (log_flops - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)

        return 0.0

    def level_for_compute(self, flops: float) -> IntelligenceLevel:
        """Determine the intelligence level for a given compute budget."""
        score = self.score_for_compute(flops)

        if score < 0.25:
            return IntelligenceLevel.NARROW_AI
        elif score < 0.42:
            return IntelligenceLevel.COMPETENT_AGI
        elif score < 0.62:
            return IntelligenceLevel.EXPERT_AGI
        elif score < 0.90:
            return IntelligenceLevel.ASI
        else:
            return IntelligenceLevel.UAI

    def compute_for_level(self, level: IntelligenceLevel) -> Optional[float]:
        """Get the reference compute budget for a given intelligence level."""
        score = self.scores.get(level)
        return score.compute_flops if score else None
