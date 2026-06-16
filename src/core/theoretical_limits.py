"""
Fundamental theoretical limits of ASI.

Implements Table 2 from the paper (Section 3): even exceeding human-level
intelligence by a large margin does NOT imply omniscience or omnipotence.
ASI is bounded by fundamental physical and complexity-theoretic limitations.

These limits can be formally characterized via the AIXI framework
(Hutter et al., 2024) and fundamental results in computability theory,
complexity theory, and physics.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class LimitType(Enum):
    """Categories of fundamental limits on superintelligence."""

    COMPUTABILITY = auto()      # What is computable at all
    COMPLEXITY = auto()         # Computational complexity bounds
    INFORMATION_THEORETIC = auto()  # Information-theoretic limits
    PHYSICAL = auto()           # Physical/thermodynamic limits
    EPISTEMOLOGICAL = auto()    # Limits on knowledge and prediction


@dataclass(frozen=True)
class TheoreticalLimit:
    """
    A fundamental theoretical limit on what any intelligence can achieve.

    These limits apply to ALL intelligences — biological and artificial —
    and cannot be overcome by any amount of compute or algorithmic improvement.

    Attributes:
        limit_type: Category of the limit.
        name: Short descriptive name.
        description: Detailed description of the limit.
        formal_basis: The formal result or theorem underlying this limit.
        implication_for_asi: What this means for ASI capabilities.
        can_be_mitigated: Whether the limit can be partially mitigated.
        mitigation: How the limit might be partially mitigated, if at all.
    """

    limit_type: LimitType
    name: str
    description: str
    formal_basis: str
    implication_for_asi: str
    can_be_mitigated: bool = False
    mitigation: str = ""


# Table 2 from the paper: Fundamental limits that apply to any intelligence

THEORETICAL_LIMITS: list[TheoreticalLimit] = [
    TheoreticalLimit(
        limit_type=LimitType.COMPUTABILITY,
        name="Halting Problem / Incomputability",
        description=(
            "There exist well-defined mathematical problems that no algorithm "
            "can solve in general. The most famous is the Halting Problem: "
            "no program can determine whether an arbitrary program halts."
        ),
        formal_basis=(
            "Turing (1936): The Halting Problem is undecidable. Rice's theorem "
            "generalizes this to all non-trivial semantic properties of programs."
        ),
        implication_for_asi=(
            "ASI cannot predict the behavior of arbitrary programs, verify "
            "arbitrary mathematical conjectures, or determine whether its own "
            "modifications will improve or degrade performance in general."
        ),
        can_be_mitigated=True,
        mitigation=(
            "Practical mitigation via approximation, probabilistic methods, "
            "time-bounded computation, and restricting to decidable subsets."
        ),
    ),
    TheoreticalLimit(
        limit_type=LimitType.COMPUTABILITY,
        name="Incomputability of AIXI",
        description=(
            "AIXI — the theoretically optimal universal agent — is itself "
            "incomputable. It cannot be exactly implemented on any physical "
            "computer. Any practical AI is necessarily a bounded approximation."
        ),
        formal_basis=(
            "Hutter (2005): AIXI requires computing the Solomonoff prior, "
            "which involves summing over all programs — an incomputable "
            "operation."
        ),
        implication_for_asi=(
            "No physical ASI can be perfectly optimal. All ASIs are bounded "
            "approximations of AIXI, trading off optimality for computability. "
            "However, approximations can improve with more compute."
        ),
        can_be_mitigated=True,
        mitigation=(
            "Computable approximations like AIXItl (time-limited AIXI), "
            "speed priors (Schmidhuber 2002), and practical approaches like "
            "large pretrained models that approximate universal compression."
        ),
    ),
    TheoreticalLimit(
        limit_type=LimitType.COMPLEXITY,
        name="Computational Intractability (NP-hardness)",
        description=(
            "Many important optimization and decision problems are NP-hard, "
            "meaning no known polynomial-time algorithm exists. Even with "
            "vast compute, exact solutions to large instances are infeasible."
        ),
        formal_basis=(
            "Cook-Levin theorem (1971): SAT is NP-complete. Unless P=NP "
            "(widely believed false), no polynomial-time algorithm exists "
            "for NP-hard problems."
        ),
        implication_for_asi=(
            "ASI cannot optimally solve general combinatorial optimization, "
            "planning in complex domains, or protein design at arbitrary "
            "scale. Must rely on heuristics and approximations."
        ),
        can_be_mitigated=True,
        mitigation=(
            "Better heuristics, approximation algorithms with provable bounds, "
            "quantum computing for specific problem classes, and exploiting "
            "structure in real-world problem instances."
        ),
    ),
    TheoreticalLimit(
        limit_type=LimitType.INFORMATION_THEORETIC,
        name="Data Efficiency / Sample Complexity",
        description=(
            "Learning requires data. The Solomonoff prior provides the "
            "theoretical maximum data efficiency — no learner can reliably "
            "learn with fewer samples than AIXI across all environments."
        ),
        formal_basis=(
            "Solomonoff (1964): Universal induction has optimal convergence "
            "rates. PAC-learning (Valiant 1984) provides sample complexity "
            "lower bounds for specific hypothesis classes."
        ),
        implication_for_asi=(
            "Even ASI cannot learn from zero data or predict complex systems "
            "without sufficient observations. Novel domains require "
            "exploration and data collection, which takes real time."
        ),
        can_be_mitigated=True,
        mitigation=(
            "Transfer learning, simulation-based training, and meta-learning "
            "can improve data efficiency but cannot eliminate the fundamental "
            "need for some data from the target domain."
        ),
    ),
    TheoreticalLimit(
        limit_type=LimitType.PHYSICAL,
        name="Thermodynamic / Energy Limits",
        description=(
            "Computation requires energy. Landauer's principle sets a minimum "
            "energy cost per bit erased. The speed of light limits communication "
            "and coordination across distances."
        ),
        formal_basis=(
            "Landauer (1961): Minimum energy to erase one bit = kT·ln(2). "
            "Bremermann's limit: maximum computation rate per unit mass. "
            "Bekenstein bound: maximum information in finite region."
        ),
        implication_for_asi=(
            "ASI's compute is ultimately limited by available energy, "
            "heat dissipation, and the speed of light. Cannot grow compute "
            "arbitrarily without proportional energy and cooling. Distributed "
            "systems face latency limits."
        ),
        can_be_mitigated=True,
        mitigation=(
            "More energy-efficient hardware (approaching Landauer limit), "
            "reversible computing, neuromorphic/analog approaches, and "
            "better thermal management."
        ),
    ),
    TheoreticalLimit(
        limit_type=LimitType.PHYSICAL,
        name="Irreducible Physical Uncertainty",
        description=(
            "Quantum mechanics introduces fundamental randomness. Chaotic "
            "systems exhibit sensitive dependence on initial conditions, "
            "making long-term prediction impossible beyond certain horizons."
        ),
        formal_basis=(
            "Heisenberg uncertainty principle. Lyapunov exponents for "
            "chaotic systems. Thermodynamic limits on measurement precision."
        ),
        implication_for_asi=(
            "ASI cannot perfectly predict weather beyond ~2 weeks, earthquake "
            "timing, individual quantum events, or the detailed long-term "
            "evolution of complex systems. Probabilistic reasoning is the "
            "best that can be done."
        ),
        can_be_mitigated=False,
        mitigation="",
    ),
    TheoreticalLimit(
        limit_type=LimitType.EPISTEMOLOGICAL,
        name="Gödel's Incompleteness",
        description=(
            "Any sufficiently powerful formal system contains true statements "
            "that cannot be proven within the system. This applies to ASI's "
            "reasoning about its own properties."
        ),
        formal_basis=(
            "Gödel (1931): First and second incompleteness theorems. "
            "No consistent formal system powerful enough to express "
            "arithmetic can prove its own consistency."
        ),
        implication_for_asi=(
            "ASI cannot prove all mathematical truths, verify its own "
            "consistency, or guarantee the correctness of its reasoning "
            "in general. Self-referential reasoning has inherent limits."
        ),
        can_be_mitigated=True,
        mitigation=(
            "Using multiple formal systems, probabilistic reasoning, "
            "and empirical verification as complements to formal proof."
        ),
    ),
    TheoreticalLimit(
        limit_type=LimitType.EPISTEMOLOGICAL,
        name="Embedded Agency Problem",
        description=(
            "AIXI is formulated as an agent outside its environment. Real "
            "AI systems are embedded in the world, meaning they are part of "
            "the environment they model. This creates fundamental issues "
            "with self-reference and self-modeling."
        ),
        formal_basis=(
            "Discussed in Hutter et al. (2024). Recently addressed in "
            "Meulemans et al. (2025) with an embedded, multi-agent extension."
        ),
        implication_for_asi=(
            "ASI must reason about environments that contain itself, "
            "other intelligent agents, and its own effects on the world. "
            "This creates paradoxes and computational challenges."
        ),
        can_be_mitigated=True,
        mitigation=(
            "Embedded AIXI extensions (Meulemans et al. 2025), "
            "reflective oracles (Fallenstein et al. 2015), and "
            "logical induction (Garrabrant et al. 2016)."
        ),
    ),
]


def get_limits_by_type(limit_type: LimitType) -> list[TheoreticalLimit]:
    """Get all theoretical limits of a specific type."""
    return [lim for lim in THEORETICAL_LIMITS if lim.limit_type == limit_type]


def get_mitigable_limits() -> list[TheoreticalLimit]:
    """Get all limits that can be at least partially mitigated."""
    return [lim for lim in THEORETICAL_LIMITS if lim.can_be_mitigated]


def get_hard_limits() -> list[TheoreticalLimit]:
    """Get limits that cannot be mitigated — fundamental barriers."""
    return [lim for lim in THEORETICAL_LIMITS if not lim.can_be_mitigated]
