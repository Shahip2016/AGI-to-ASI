"""
Flask REST API server for the AGI-to-ASI web UI.

Endpoints:
  GET /api/scenarios   — run all scenarios with optional query params
  GET /api/pathways    — list available pathways with descriptions
  GET /api/research    — return the research agenda as JSON
"""

from __future__ import annotations

import sys
import os

# Ensure the project root is on the path so `src.*` imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.compute.growth_model import ComputeGrowthModel, GrowthFactors
from src.compute.scaling_laws import PowerLawScaling, CapabilityExtrapolator
from src.frictions.models import CompositeFrictionModel, STANDARD_FRICTIONS
from src.pathways.scaling import ScalingPathway, DataWallConstraints
from src.pathways.recursive_improvement import (
    RecursiveImprovementPathway,
    RSIMechanism,
    RSIType,
)
from src.pathways.multi_agent import MultiAgentPathway
from src.pathways.paradigm_shifts import ParadigmShiftPathway
from src.research_agenda.open_questions import ResearchAgenda

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_scenario_smooth(years: float, factors: GrowthFactors, dw_year: float,
                            synthetic_eff: float) -> dict:
    """Smooth scaling with user-supplied parameters."""
    growth = ComputeGrowthModel(factors=factors)
    scaling = PowerLawScaling(alpha=0.5, c_c=100.0, l_inf=0.0)
    caps = CapabilityExtrapolator(scaling)
    caps.add_milestone("Competent AGI", 2.0)
    caps.add_milestone("Expert AGI", 1.0)
    caps.add_milestone("ASI", 0.5)
    caps.add_milestone("UAI-Approximation", 0.1)

    dw = DataWallConstraints(exhaustion_year=dw_year,
                              synthetic_data_efficiency=synthetic_eff)
    pathway = ScalingPathway(growth, caps, dw)
    return _result_to_dict(pathway.simulate(years=years))


def _build_scenario_hard(years: float, factors: GrowthFactors, dw_year: float,
                          synthetic_eff: float) -> dict:
    """Hard bottleneck scenario."""
    growth = ComputeGrowthModel(factors=factors)
    scaling = PowerLawScaling(alpha=0.5, c_c=100.0, l_inf=0.0)
    caps = CapabilityExtrapolator(scaling)
    caps.add_milestone("Competent AGI", 2.0)
    caps.add_milestone("Expert AGI", 1.0)
    caps.add_milestone("ASI", 0.5)
    caps.add_milestone("UAI-Approximation", 0.1)

    dw = DataWallConstraints(exhaustion_year=dw_year,
                              synthetic_data_efficiency=synthetic_eff)
    pathway = ScalingPathway(growth, caps, dw)
    res = pathway.simulate(years=years)
    res.pathway_name = "Scaling with Hard Frictions"

    frictions = CompositeFrictionModel(STANDARD_FRICTIONS)
    for i, t in enumerate(res.time_series["year"]):
        fm = frictions.get_effective_growth_multiplier(t)
        res.time_series["effective_compute"][i] *= fm

    final = res.time_series["effective_compute"][-1]
    res.final_compute_multiplier = final / res.time_series["effective_compute"][0]
    res.capabilities_unlocked = caps.capabilities_at_compute(final)
    res.bottleneck_hit = True
    res.bottleneck_name = "Multiple (Data, Power, Eval)"
    res.bottleneck_year = dw_year
    return _result_to_dict(res)


def _result_to_dict(res) -> dict:
    """Serialize a PathwayResult to a plain dict."""
    ts = res.time_series or {}
    return {
        "pathway_name": res.pathway_name,
        "final_compute_multiplier": res.final_compute_multiplier,
        "capabilities_unlocked": res.capabilities_unlocked,
        "bottleneck_hit": res.bottleneck_hit,
        "bottleneck_name": res.bottleneck_name,
        "bottleneck_year": res.bottleneck_year,
        "time_series": {
            "year": ts.get("year", []),
            "effective_compute": ts.get("effective_compute", []),
            "raw_compute": ts.get("raw_compute", []),
        },
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/scenarios")
def get_scenarios():
    """Run scenario simulations with optional query parameters."""
    years = float(request.args.get("years", 10))
    hw = float(request.args.get("hardware_improvements", 1.5))
    inv = float(request.args.get("investment_growth", 2.5))
    algo = float(request.args.get("algorithmic_efficiency", 3.0))
    dw_year = float(request.args.get("data_wall_year", 4.0))
    syn_eff = float(request.args.get("synthetic_data_efficiency", 0.5))

    factors = GrowthFactors(
        hardware_improvements=hw,
        investment_growth=inv,
        algorithmic_efficiency=algo,
    )

    return jsonify({
        "smooth_scaling": _build_scenario_smooth(years, factors, dw_year, syn_eff),
        "hard_bottlenecks": _build_scenario_hard(years, factors, dw_year, syn_eff),
        "params": {
            "years": years,
            "hardware_improvements": hw,
            "investment_growth": inv,
            "algorithmic_efficiency": algo,
            "data_wall_year": dw_year,
            "synthetic_data_efficiency": syn_eff,
            "total_growth_per_year": factors.total_effective_growth,
        }
    })


@app.get("/api/pathways")
def get_pathways():
    """Return static metadata about each pathway."""
    return jsonify([
        {
            "id": "scaling",
            "name": "Quantitative Scaling",
            "section": "Section 5.1",
            "description": (
                "Extrapolating current scaling laws. Progress is driven by massive "
                "scaling of effective compute and data (including synthetic) without "
                "fundamental paradigm shifts."
            ),
            "key_risk": "Data Wall — exhaustion of high-quality human data.",
        },
        {
            "id": "paradigm",
            "name": "Algorithmic Paradigm Shifts",
            "section": "Section 5.2",
            "description": (
                "Discontinuous jumps caused by fundamentally new architectures or "
                "learning algorithms (e.g., post-Transformer breakthroughs)."
            ),
            "key_risk": "Unpredictable timing; could stall or leap unexpectedly.",
        },
        {
            "id": "rsi",
            "name": "Recursive Self-Improvement",
            "section": "Section 5.3",
            "description": (
                "AI systems automate and accelerate AI R&D, creating a positive "
                "feedback loop that can lead to explosive, super-exponential growth."
            ),
            "key_risk": "Intelligence explosion / computational singularity if unchecked.",
        },
        {
            "id": "multi_agent",
            "name": "Multi-Agent Coordination",
            "section": "Section 5.4",
            "description": (
                "Large swarms of specialized AI agents acting as a collective "
                "superintelligence through division of labor and emergent coordination."
            ),
            "key_risk": "Coordination overhead; communication bandwidth limits.",
        },
    ])


@app.get("/api/research")
def get_research():
    """Return the research agenda (questions + benchmarks) as JSON."""
    questions = [
        {
            "category": q.category.name,
            "question": q.question,
            "description": q.description,
            "urgency": q.urgency,
        }
        for q in ResearchAgenda.QUESTIONS
    ]
    benchmarks = [
        {
            "name": b.name,
            "description": b.description,
            "current_gap": b.current_gap,
        }
        for b in ResearchAgenda.BENCHMARKS
    ]
    return jsonify({"questions": questions, "benchmarks": benchmarks})


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("AGI→ASI UI server running at http://localhost:5000")
    print("Open ui/index.html in your browser (or serve it via the same server).")
    app.run(debug=True, port=5000)
