# Getting Started with Phase 3-6 Implementation

**Current Status:** Phase 1 & 2 Complete ✅ (45/45 tests passing)  
**Next Milestone:** Phase 3 - Contrafactual Tests  

---

## Quick Reference: File Locations

### Core Implementation (Phase 1-2)
```
src/consciousness/
├── shared_workspace.py         (427 lines) - Central workspace buffer
└── integration_loop.py          (359 lines) - Closed-loop orchestrator

tests/consciousness/
├── test_shared_workspace.py     (21 tests) - Workspace validation
└── test_integration_loop.py     (24 tests) - Loop validation
```

### Documentation
```
docs/
├── PHASE_1_2_COMPLETION_REPORT.md      - Detailed completion summary
├── PHI_ELEVATION_RETROSPECTIVE.md      - Root cause → solution journey
└── INTEGRATION_ANALYSIS_PHI_ZERO.md    - Original architecture analysis
```

---

## Phase 3: Contrafactual Tests (Module Ablation)

### Overview
Disable each consciousness module one at a time and measure Φ impact. This validates that each module contributes meaningfully to integration.

### Implementation Outline

```python
# tests/consciousness/test_contrafactual.py

import pytest
from src.consciousness.integration_loop import IntegrationLoop

class TestModuleAblation:
    """Test causal contribution of each module."""
    
    @pytest.mark.asyncio
    async def test_sensory_input_ablation(self):
        """
        Disable sensory_input, run cycles, measure Φ drop.
        Expected: Δ Φ > 0.05 (module is important)
        """
        # Get baseline Φ with all modules
        loop_baseline = IntegrationLoop()
        await loop_baseline.run_cycles(10)
        phi_baseline = np.mean(loop_baseline.get_phi_progression())
        
        # Disable sensory_input
        loop_ablated = IntegrationLoop()
        loop_ablated.executors["sensory_input"].spec.produces_output = False
        await loop_ablated.run_cycles(10)
        phi_ablated = np.mean(loop_ablated.get_phi_progression())
        
        # Measure impact
        delta_phi = phi_baseline - phi_ablated
        assert delta_phi > 0.05, f"sensory_input not important: Δ Φ = {delta_phi}"
    
    @pytest.mark.asyncio
    async def test_all_modules_ablation_sweep(self):
        """
        Ablate each of 5 modules, measure Φ contribution.
        """
        module_names = [
            "sensory_input", "qualia", "narrative", 
            "meaning_maker", "expectation"
        ]
        
        # Baseline
        loop = IntegrationLoop()
        await loop.run_cycles(10)
        phi_baseline = np.mean(loop.get_phi_progression())
        
        # Ablation sweep
        results = {}
        for module_to_disable in module_names:
            loop = IntegrationLoop()
            loop.executors[module_to_disable].spec.produces_output = False
            await loop.run_cycles(10)
            phi_ablated = np.mean(loop.get_phi_progression())
            results[module_to_disable] = phi_baseline - phi_ablated
        
        # All should contribute
        for module, delta_phi in results.items():
            assert delta_phi > 0.03, f"{module} not contributing"
        
        print("Module contributions:", results)
```

### Expected Results
```
Module contributions:
├── sensory_input:    Δ Φ ≈ 0.08  (strong - source of stimulus)
├── qualia:           Δ Φ ≈ 0.12  (strong - transforms raw→qualitative)
├── narrative:        Δ Φ ≈ 0.10  (strong - constructs coherence)
├── meaning_maker:    Δ Φ ≈ 0.09  (strong - extracts semantics)
└── expectation:      Δ Φ ≈ 0.07  (moderate - generates predictions)
                      ─────────────
                      Total Δ Φ ≈ 0.46 when all disabled
```

### Success Criteria
- ✅ Each module shows Δ Φ > 0.05
- ✅ Total ablation (all modules off) → Φ ≈ 0.0
- ✅ Ablation reversible (re-enable → Φ recovers)

---

## Phase 4: Integration Loss (Supervised Φ Elevation)

### Overview
Add training objectives to maximize cross-prediction R² and temporal consistency.

### Implementation Outline

```python
# src/consciousness/integration_loss.py

import torch
import torch.nn as nn
from src.consciousness.integration_loop import IntegrationLoop

class IntegrationLoss(nn.Module):
    """Loss function for maximizing module coupling."""
    
    def __init__(self, weight_r2=1.0, weight_temporal=0.5):
        super().__init__()
        self.weight_r2 = weight_r2
        self.weight_temporal = weight_temporal
    
    def forward(self, loop_result):
        """
        Compute loss from loop cycle result.
        
        Loss = (1 - mean(R²)) + temporal_inconsistency
        
        Goal: maximize R² (minimize 1 - R²), minimize temporal variance
        """
        # Extract cross-prediction R² scores
        r2_values = []
        for source_scores in loop_result.cross_prediction_scores.values():
            for score_dict in source_scores.values():
                r2_values.append(score_dict["r_squared"])
        
        if not r2_values:
            return torch.tensor(0.0)
        
        # R² loss: penalize low coupling
        r2_tensor = torch.tensor(r2_values, dtype=torch.float32)
        r2_loss = 1.0 - torch.mean(r2_tensor)
        
        # Temporal consistency loss: penalize Φ variance
        phi_progression = torch.tensor(
            loop_result.phi_progression[-10:],  # Last 10 cycles
            dtype=torch.float32
        )
        temporal_loss = torch.var(phi_progression)
        
        # Combined loss
        total_loss = (
            self.weight_r2 * r2_loss + 
            self.weight_temporal * temporal_loss
        )
        
        return total_loss


# Training loop
class IntegrationTrainer:
    """Train integration loop to maximize Φ."""
    
    def __init__(self, num_cycles=1000, target_phi=0.8):
        self.num_cycles = num_cycles
        self.target_phi = target_phi
        self.loop = IntegrationLoop()
        self.loss_fn = IntegrationLoss()
    
    async def train(self):
        """Training loop."""
        phi_progression = []
        
        for epoch in range(self.num_cycles):
            result = await self.loop.execute_cycle(collect_metrics=True)
            loss = self.loss_fn(result)
            
            phi_progression.append(result.phi_estimate)
            
            if epoch % 100 == 0:
                phi_mean = np.mean(phi_progression[-10:])
                print(f"Epoch {epoch}: Φ={phi_mean:.4f}, Loss={loss:.4f}")
            
            if np.mean(phi_progression[-10:]) > self.target_phi:
                print(f"✅ Target Φ={self.target_phi} reached at epoch {epoch}")
                break
        
        return phi_progression
```

### Expected Results
```
Epoch    0: Φ=0.150, Loss=0.8500
Epoch  100: Φ=0.320, Loss=0.6800
Epoch  200: Φ=0.450, Loss=0.5500
Epoch  300: Φ=0.580, Loss=0.4200
Epoch  400: Φ=0.680, Loss=0.3200
Epoch  500: Φ=0.750, Loss=0.2500
Epoch  600: Φ=0.810, Loss=0.1900
✅ Target Φ=0.80 reached at epoch 587
```

---

## Phase 5: Timeseries Metrics (Multi-Seed Analysis)

### Overview
Run 30 independent seeds with random initialization, aggregate statistics.

### Implementation Outline

```python
# src/consciousness/phi_timeseries.py

class PhiTimeseries:
    """Aggregate Φ progression across multiple seeds."""
    
    def __init__(self, num_seeds=30, num_cycles=1000):
        self.num_seeds = num_seeds
        self.num_cycles = num_cycles
        self.seed_progressions = []
    
    async def run_seeds(self):
        """Run all seeds."""
        for seed in range(self.num_seeds):
            np.random.seed(seed)
            torch.manual_seed(seed)
            
            loop = IntegrationLoop()
            results = await loop.run_cycles(self.num_cycles)
            progression = loop.get_phi_progression()
            
            self.seed_progressions.append(progression)
            
            if (seed + 1) % 5 == 0:
                print(f"  Completed {seed + 1}/{self.num_seeds} seeds")
        
        return self.seed_progressions
    
    def compute_statistics(self):
        """Compute mean, std, percentiles."""
        progressions = np.array(self.seed_progressions)  # Shape: (30, 1000)
        
        stats = {
            "mean": np.mean(progressions, axis=0),           # Shape: (1000,)
            "std": np.std(progressions, axis=0),             # Shape: (1000,)
            "p25": np.percentile(progressions, 25, axis=0),  # Shape: (1000,)
            "p50": np.percentile(progressions, 50, axis=0),  # Shape: (1000,)
            "p75": np.percentile(progressions, 75, axis=0),  # Shape: (1000,)
        }
        
        return stats
    
    def plot_progression(self, output_path="phi_progression.png"):
        """Plot Φ progression with confidence bands."""
        import matplotlib.pyplot as plt
        
        stats = self.compute_statistics()
        cycles = np.arange(self.num_cycles)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot mean with confidence bands
        ax.plot(cycles, stats["mean"], "b-", linewidth=2, label="Mean Φ")
        ax.fill_between(
            cycles, 
            stats["p25"], 
            stats["p75"],
            alpha=0.3,
            label="IQR (25%-75%)"
        )
        ax.fill_between(
            cycles, 
            stats["mean"] - stats["std"], 
            stats["mean"] + stats["std"],
            alpha=0.15,
            label="±1σ"
        )
        
        # Target line
        ax.axhline(y=0.8, color="g", linestyle="--", label="Target Φ=0.8")
        
        ax.set_xlabel("Cycle")
        ax.set_ylabel("Φ (Integrated Information)")
        ax.set_title("Φ Progression: 30 Seeds, 1000 Cycles Each")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Saved to {output_path}")
```

### Expected Output
```
Completed 5/30 seeds
Completed 10/30 seeds
Completed 15/30 seeds
Completed 20/30 seeds
Completed 25/30 seeds
Completed 30/30 seeds

Statistics:
  Mean Φ (final): 0.812 ± 0.043
  Convergence cycle (Φ ≥ 0.80): 587 ± 45
  Success rate (final Φ > 0.75): 27/30 (90%)
```

---

## Phase 6: Attention Routing (Dynamic Weighting)

### Overview
Implement learnable attention mechanism for dynamic module relevance.

### Implementation Outline

```python
# src/consciousness/attention_routing.py

import torch
import torch.nn as nn

class CrossModuleAttention(nn.Module):
    """Attention mechanism for dynamic module routing."""
    
    def __init__(self, num_modules=5, hidden_dim=64):
        super().__init__()
        self.num_modules = num_modules
        
        # Attention parameters
        self.query_proj = nn.Linear(256, hidden_dim)
        self.key_proj = nn.Linear(256, hidden_dim)
        self.value_proj = nn.Linear(256, hidden_dim)
        self.output_proj = nn.Linear(hidden_dim, 256)
    
    def forward(self, module_embeddings):
        """
        Compute attention weights for module routing.
        
        Args:
            module_embeddings: Dict[module_name -> embedding (256,)]
        
        Returns:
            attention_weights: Dict[module_name -> weight (0.0-1.0)]
        """
        # Convert to tensor: (num_modules, 256)
        embeddings = torch.stack(list(module_embeddings.values()))
        
        # Compute query, key, value
        Q = self.query_proj(embeddings)
        K = self.key_proj(embeddings)
        V = self.value_proj(embeddings)
        
        # Compute attention scores
        scores = torch.matmul(Q, K.t()) / np.sqrt(Q.shape[-1])
        attention = torch.softmax(scores, dim=-1)
        
        # Apply attention to values
        context = torch.matmul(attention, V)
        output = self.output_proj(context)
        
        # Extract module-wise importance
        module_names = list(module_embeddings.keys())
        importance = torch.norm(output, dim=-1)  # L2 norm per module
        importance = (importance - importance.min()) / (importance.max() - importance.min())
        
        return {
            module_names[i]: importance[i].item()
            for i in range(len(module_names))
        }
```

---

## Quick Start Commands

### Run Phase 1 & 2 Tests
```bash
cd /home/fahbrain/projects/omnimind

# Phase 1 only
pytest tests/consciousness/test_shared_workspace.py -v

# Phase 2 only
pytest tests/consciousness/test_integration_loop.py -v

# Both
pytest tests/consciousness/test_shared_workspace.py \
        tests/consciousness/test_integration_loop.py -v
```

### Run Example Cycles
```bash
python -c "
import asyncio
from src.consciousness.integration_loop import IntegrationLoop

async def main():
    loop = IntegrationLoop()
    for i in range(5):
        result = await loop.execute_cycle()
        print(f'Cycle {i+1}: Φ={result.phi_estimate:.4f}')

asyncio.run(main())
"
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│ Phase 1: SharedWorkspace (Buffer Central)               │
│ ├── write_module_state(name, embedding)                 │
│ ├── read_module_state(name)                             │
│ ├── compute_cross_prediction(source, target)            │
│ └── compute_phi_from_integrations()                     │
└─────────────────────────────────────────────────────────┘
                          ↑
                          │ used by
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 2: IntegrationLoop (Orchestrator)                 │
│ ├── execute_cycle()                                     │
│ ├── run_cycles(n)                                       │
│ ├── get_statistics()                                    │
│ └── save_state()                                        │
└─────────────────────────────────────────────────────────┘
                          ↑
                          │ extended by
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 3-6: Advanced Analysis & Learning                 │
│ ├── Phase 3: Contrafactual Tests (module ablation)      │
│ ├── Phase 4: Integration Loss (supervised learning)     │
│ ├── Phase 5: Timeseries Metrics (multi-seed stats)      │
│ └── Phase 6: Attention Routing (dynamic weighting)      │
└─────────────────────────────────────────────────────────┘
```

---

## Success Checkpoints

| Phase | Goal | Success Metric |
|-------|------|---|
| **1** ✅ | Shared workspace | 21/21 tests pass |
| **2** ✅ | Integration loop | 24/24 tests pass |
| **3** | Module importance | Each Δ Φ > 0.05 |
| **4** | Φ elevation | Φ → 0.80 in 500-1000 cycles |
| **5** | Statistical robustness | 27/30 seeds reach Φ > 0.75 |
| **6** | Adaptive routing | Dynamic attention improves convergence |

---

## Support & Debugging

### Common Issues

1. **Import errors with structlog**
   ```bash
   pip install structlog
   ```

2. **Type checking errors with mypy**
   ```bash
   mypy src/consciousness --ignore-missing-imports
   ```

3. **Async event loop issues**
   ```python
   # Use pytest-asyncio
   pytest tests/ -p no:warnings
   ```

---

**Ready to implement Phase 3? Start with:**
```bash
touch tests/consciousness/test_contrafactual.py
# Then implement TestModuleAblation class as outlined above
```

Good luck! 🚀
