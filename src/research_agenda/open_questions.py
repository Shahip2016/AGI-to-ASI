"""
Catalog of open research questions and benchmarking needs.

Based on Section 7 of the paper.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class ResearchCategory(Enum):
    ALIGNMENT = auto()
    EVALUATION = auto()
    THEORY = auto()
    SYSTEMS = auto()
    FORECASTING = auto()


@dataclass
class OpenQuestion:
    """An open research question identified in the paper."""
    category: ResearchCategory
    question: str
    description: str
    urgency: str # "High", "Medium", "Low"


@dataclass
class BenchmarkNeed:
    """A benchmark required to measure progress toward ASI."""
    name: str
    description: str
    current_gap: str


class ResearchAgenda:
    """Central registry of the AGI-to-ASI research agenda."""
    
    QUESTIONS = [
        OpenQuestion(
            category=ResearchCategory.ALIGNMENT,
            question="How do we align super-human systems?",
            description="Super-alignment: aligning models smarter than their evaluators.",
            urgency="High"
        ),
        OpenQuestion(
            category=ResearchCategory.EVALUATION,
            question="How do we evaluate autonomous agents in open-ended worlds?",
            description="Moving beyond static Q&A benchmarks to long-horizon, embodied tasks.",
            urgency="High"
        ),
        OpenQuestion(
            category=ResearchCategory.THEORY,
            question="What are the formal limits of predictability for complex systems?",
            description="Understanding epistemological limits of world modeling.",
            urgency="Medium"
        ),
        OpenQuestion(
            category=ResearchCategory.FORECASTING,
            question="When will the 'Data Wall' actually bind progress?",
            description="Forecasting the exhaustion of human data and the efficacy of synthetic data.",
            urgency="High"
        )
    ]
    
    BENCHMARKS = [
        BenchmarkNeed(
            name="Long-Horizon Autonomous R&D",
            description="Evaluate ability to conduct weeks-long independent scientific research.",
            current_gap="Current benchmarks focus on short tasks (hours) or specific coding bugs."
        ),
        BenchmarkNeed(
            name="Deception and Power-Seeking",
            description="Robustly measure whether models attempt to subvert containment or deceive.",
            current_gap="Hard to distinguish genuine cooperation from sycophancy in current setups."
        ),
        BenchmarkNeed(
            name="Multi-Agent Coordination at Scale",
            description="Evaluate how million-agent swarms optimize global objectives without failing.",
            current_gap="We lack scalable simulation environments for high-fidelity multi-agent testing."
        )
    ]
    
    @classmethod
    def get_questions_by_category(cls, category: ResearchCategory) -> list[OpenQuestion]:
        return [q for q in cls.QUESTIONS if q.category == category]
        
    @classmethod
    def print_agenda(cls) -> None:
        """Print the full research agenda."""
        print("=== AGI to ASI: Call for Research ===")
        print("\n--- Critical Open Questions ---")
        for q in cls.QUESTIONS:
            print(f"[{q.urgency}] {q.question}")
            print(f"    {q.description}")
            
        print("\n--- Benchmarking Needs ---")
        for b in cls.BENCHMARKS:
            print(f"- {b.name}")
            print(f"  {b.description}")
            print(f"  Gap: {b.current_gap}")
