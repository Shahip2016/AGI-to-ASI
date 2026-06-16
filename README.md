# From AGI to ASI

**A Python framework implementing the concepts from ["From AGI to ASI"](https://arxiv.org/abs/2606.12683) (Genewein et al., 2025)**

> *"We can only see a short distance ahead, but we can see plenty there that needs to be done."*
> — Alan Turing, Computing Machinery and Intelligence (1950)

## Overview

This project provides a computational framework for exploring the transition from Artificial General Intelligence (AGI) to Artificial Superintelligence (ASI), as analyzed in the paper by Tim Genewein et al. from Google DeepMind. The framework includes:

- **Core definitions** of AGI, ASI, and Universal AI (UAI/AIXI) along the intelligence continuum
- **Compute growth models** capturing the ~10× per year effective compute growth
- **Four pathway simulators** for AGI→ASI transitions:
  1. Scaling compute, models, and data
  2. Algorithmic paradigm shifts
  3. Recursive self-improvement
  4. Multi-agent coordination & collective intelligence
- **Friction & bottleneck models** that can be composed with pathways
- **Forecasting tools** for scenario analysis with uncertainty quantification
- **Visualization dashboard** for interactive exploration
- **Research agenda tracker** cataloging open questions from the paper

## Project Structure

```
src/
├── core/               # Core definitions (AGI/ASI/UAI, advantages, limits)
├── compute/            # Compute growth models and scaling laws
├── universal_ai/       # AIXI framework, Solomonoff prior, Legg-Hutter score
├── pathways/           # Four AGI→ASI pathways
├── agents/             # Multi-agent collective simulation
├── frictions/          # Bottleneck and friction models
├── forecasting/        # Scenario analysis and uncertainty modeling
├── visualization/      # Plotting and dashboard
├── research_agenda/    # Open questions and benchmarking
├── cli.py              # Command-line interface
└── simulator.py        # Integrated simulator
tests/                  # Unit tests
examples/               # Usage examples
docs/                   # Documentation and paper mapping
```

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from src.simulator import Simulator
from src.forecasting.scenarios import ScenarioGenerator

# Run a default AGI→ASI simulation
sim = Simulator()
results = sim.run(years=15)

# Generate scenario comparison
gen = ScenarioGenerator()
scenarios = gen.generate_all()
```

## Paper Reference

```bibtex
@article{genewein2025agi,
  title={From AGI to ASI},
  author={Genewein, Tim and others},
  journal={arXiv preprint arXiv:2606.12683},
  year={2025}
}
```

## License

MIT License — see [LICENSE](LICENSE) for details.
